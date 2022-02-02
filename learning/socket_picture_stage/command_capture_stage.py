"""
    Add GPIO and set_camera_gain func to RawImageCapture.py.
    Put this file and "set_picamera_gain.py" in directory "/home/pi/Desktop/Python/"

    Command
        S : take a picture and save as a file named with date.
        C : start waiting for socket communication from client.
            (server's ip address and portnum should be set correctly.)
"""
import serial
import time
COM = "/dev/ttyUSB0"
bitrate=9600
step="100"

import os
import gc
import time
from linearstage import AutoStage
import socket
import shutil
import picamera
import picamera.array
import numpy as np
from PIL import Image
from datetime import datetime
import RPi.GPIO as GPIO
from set_picamera_gain import set_analog_gain, set_digital_gain

#  Variables setting
image_directory = "/home/pi/Desktop/"
save_directory = image_directory + datetime.now().strftime("%Y%m%d/")
shutter_speed = 100000
iso = 100  # 100 recommended
ag = 1  # 1 recommended
dg = 1  # 1 recommended
pinnum = 27  # Pin number in BCM for flashing signal

#  for socket communication
portnum = 1025
# ip_wired = "169.254.65.128"  # piBeam
#ip_wired = "169.254.61.118"  # piBeam2
ip_wired = "192.168.0.201"

stageport = "/dev/ttyUSB0"

#  taking Image using PiBayerArray
def takeImage(cropRect=[0, 800, 400, 400], demosaic=False):
    gc.collect()
    global count, stream, cam
    count += 1
    print("count:", count)
    if count % 20 == 0:
        cam = initializePiCamera()
    if count % 10 == 0:
        stream = picamera.array.PiBayerArray(cam)
    GPIO.output(pinnum, 1)
    cam.capture(stream, 'jpeg', bayer=True, quality=1, thumbnail=None)
    GPIO.output(pinnum, 0)
    output = (stream.array).astype(np.uint16) if not demosaic else (
        stream.demosaic()).astype(np.uint16)
    # output = output[1::2, 1::2, 0]  # R layer
    # sum(output[1::2, 0::2,1], output[0::2, 1::2,1]) / 2 # G layer
    output = output[1::2, 0::2, 1]  # G layer
    # output = output[0::2, 0::2, 2]  # B layer
    return output


def initializeImageDir():
    shutil.rmtree(image_directory)
    os.makedirs(save_directory, exist_ok=True)


def initializePiCamera():
    global cam, shutter_speed, iso, count, pinnum
    if count == 0:
        cam = picamera.PiCamera()
    else:
        cam.close()
        cam = picamera.PiCamera()
    # GPIO.output(pinnum, 1)
    cam.iso = iso
    cam.framerate_range = (0.10, 30)
    cam.shutter_speed = shutter_speed
    set_analog_gain(cam, ag)
    set_digital_gain(cam, dg)
    cam.awb_mode = "off"
    cam.exposure_mode = "off"
    time.sleep(2)
    # GPIO.output(pinnum, 0)
    # cam.flash_mode = 'on'
    print("analog gain:", cam.analog_gain, "digital gain:", cam.digital_gain, "shutter speed:", cam.exposure_speed, "ISO:", cam.iso)
    return cam


def getCenterOfMass(map):  # legacy code
    norm = np.mean(map)
    xvalue = np.arange(0, map.shape[0])
    yvalue = np.arange(0, map.shape[1])
    return np.mean(np.mean(map, axis=1) * xvalue) / norm, np.mean(np.mean(map, axis=0) * yvalue) / norm


def getPeakPos(map):  # legacy code
    return np.argmax(np.ndarray.argmax(map, 1)), np.argmax(np.ndarray.argmax(map, 0))


def normalizeMap(map):  # legacy code
    max = np.max(map)
    min = np.min(map)
    norm_map = (map - min) / (max - min)
    # print(norm_map)
    return norm_map * 255


def getFWHM(data):  # legacy code
    maxValue = np.max(data)
    minValue = np.min(data)
    data = (data - minValue) / (maxValue - minValue)
    stateFlag = False
    pos0 = 0
    pos1 = 0
    for i, value in enumerate(data):
        if value > 0.5:
            if not stateFlag:
                pos0 = i
            stateFlag = True
            pos1 = i
    return pos1 - pos0

def getFWHM2(data, posmax):  # legacy code
    maxValue = np.max(data)
    minValue = np.min(data)
    data = (data - minValue) / (maxValue - minValue)
    stateFlag = False
    pos0 = 0
    pos1 = 0
    for i, value in enumerate(data[posmax[0]]):
        if value > 0.5:
            if not stateFlag:
                pos0 = i
            stateFlag = True
            pos1 = i
    xFWHM = pos1 - pos0
    
    for i, value in enumerate(data[:,posmax[1]]):
        if value > 0.5:
            if not stateFlag:
                pos0 = i
            stateFlag = True
            pos1 = i
    yFWHM = pos1 - pos0
    
    return np.max([xFWHM,yFWHM])
    
    

def analyzeImage(image):  # legacy code
    imageArray = np.asarray(image).astype(np.float32)

    centerPos = getCenterOfMass(imageArray)

    print("Center of mass:{}".format(centerPos))
    fwhm_x = getFWHM(imageArray[:, int(centerPos[1])])
    fwhm_y = getFWHM(imageArray[int(centerPos[0]), :])
    # array_median = scipy.signal.medfilt(imageArray, kernel_size = 3)
    np.savetxt('output.txt', imageArray[int(centerPos[0]), :])
    print("FWHM: x:{}, y:{}".format(fwhm_x, fwhm_y))
    numPixelMoreThan128 = np.sum(np.where(imageArray > 128, 1, 0))
    return [fwhm_x, fwhm_y, numPixelMoreThan128]  # np.max(array_median)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinnum, GPIO.OUT)
    GPIO.output(pinnum, 0)
    current_directory = os.getcwd()
    initializeImageDir()
    count = 0
    cam = initializePiCamera()
    stream = picamera.array.PiBayerArray(cam)
    print("Ready")
    while True:
        command = input("Command:")
        if command[0] == 'I':
            ser = serial.Serial(COM, bitrate, timeout=0.1)
            ser.write("H:W\r\n".encode())
        
        if command == 'S':
            array = takeImage()
            filename = datetime.now().strftime("Img_%Y%m%d_%H%M%S.png")
            img = Image.fromarray((array / 4).astype(np.uint8))
            img.save(filename)
            print(filename)
        
        if command == 'W':
            stage = AutoStage(stageport)
            stage.stop()
            print("stage.um += 1000")
            stage.um += 1000
            print(f">>> {stage.um}\n")
        if command == 'C':
            os.makedirs(save_directory, exist_ok=True)
            os.chdir(save_directory)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((ip_wired, portnum))
                s.listen(10)
                quitFlag = False
                filename = None
                print("Waiting for connection... ")
                while not quitFlag:
                    connection, address = s.accept()
                    with connection:
                        while not quitFlag:
                            data = connection.recv(1024)
                            if not data:
                                break
                            command = data.decode()
                            print("Command from the client:{}".format(command))
                            if command == "move_stage":
                                stage = AutoStage(stageport)
                                stage.stop()
                                stage.um += 100
                                print(f"moved >>> {stage.um}\n")
                                connection.sendall(f"moved >>> {stage.um}".encode())
                            if command == "measure":
                                array = takeImage()
                                filename = datetime.now().strftime("Img_%Y%m%d_%H%M%S.png")
                                img = Image.fromarray((array / 4).astype(np.uint8))
                                img.save(filename)
                                filename = datetime.now().strftime("Img_%Y%m%d_%H%M%S.npy")
                                np.save(filename, array)
                                posmax = np.unravel_index(np.argmax(array), array.shape)
                                #print(posmax)
                                #xyFWHM = getFWHM2(array, posmax)
                                #print(xyFWHM)
                                print(filename)
                                connection.sendall(filename.encode())
                            elif command == "send":
                                if filename is None:
                                    connection.sendall(b'NG')
                                    break
                                connection.sendall(b'OK')
                                print("OK. Sending a file...")
                                with open(filename, "rb") as f:
                                    line = f.read(1024)
                                    while line:
                                        connection.sendall(line)
                                        line = f.read(1024)
                                print("Done")
                                break
                            elif command[0:3] == "iso":
                                cam.iso = int(command[3:])
                                connection.sendall(b'OK')
                                break
                            elif command[0:2] == "ss":
                                cam.shutter_speed = int(command[2:])
                                connection.sendall(b'OK')
                            elif command == "quit":
                                connection.sendall(b'Bye!')
                                quitFlag = True
                                break
                            elif command == "info":
                                print(cam.analog_gain, cam.digital_gain, cam.exposure_speed, cam.iso)
                                connection.sendall(b'OK')
                            else:
                                connection.sendall(b'NG')
        if command == 'Q':
            break
        else:
            pass
    os.chdir(current_directory)
    GPIO.cleanup()
