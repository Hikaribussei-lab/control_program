# -*- coding: utf-8 -*-
"""

@author: B. Platzer, N. Fiaschi

This work is licensed under the GNU Affero General Public License v3.0

Copyright (c) 2021, GroeblacherLab
All rights reserved.


___________________________________________________________________________________________________


This driver controls the mechonics stage MX35 via the USB controller CU30.

___________________________________________________________________________________________________

HOW TO USE THE CODE:

    1. Connect the controller CU30 via USB to the computer
    2. Get the absolute path of CU30_Wrapper_DLL_x64_C++/bin/CU30Wrap.dll


----------- example of usage, open connection and move in x and y direction: ----------

    mechonics = Mechonics()
    mechonics.open_connection()
    mechonics.sweep(Timeout = 100)
    time.sleep(2)
    mechonics.sweep(Axis=2)
    time.sleep(2)
    mechonics.close_connection()
    
---------------------------------------------------------------------------------------

TDB:
    - get_EEprom_info, does not return the info
    - get the connection result (success or not) from open_connection
    
tested with Spyder 4, Python 3.7, Windows 10 and ctypes 0.2.0
"""

import sys
import ctypes 
import time
import pyvisa as visa
import subprocess
import numpy as np
import statistics
sys.path.append('../ThorCam/examples')
import tifffile_tiff_writing # as tc

class Mechonics:
    
    def __init__(self, path = "C:\\Users\\Takuma Iwata\\control_program\\Polarization_microscope\\Mechonics\\CU17Wrap_x64.dll", USBInstance=0, USBVersion=1, DevID=2, EEID=0):
        """Initialisation. Loads the CU30Wrap.dll file containing the methods to control the device.
        
        -CU30WrapperInit()
        The function performs initialization of the wrapper dll. It is either called automatically during the loading of the DLL into
        the memory or manually.
        """
        self.path = path
        self.CU80 = ctypes.windll.LoadLibrary(path)
        self.USBInstance = USBInstance
        self.USBVersion = USBVersion
        self.DevID = DevID
        self.EEID = EEID
    
        self.initialisation()
        
    def __enter__(self):
        """Method to allow the use of the with-as statement
        """
        return self
    
    def __exit__(self, type, value, traceback):
        """Method to allow the use of the with-as statement
        """
        self.close_connection()
        
    def initialisation(self):
        """
        """
        #self.CU80.CU80WrapperInit()
        #self.open_connection()
        
    def open_connection(self):
        """Opens the connection to the device, using the CU30WOpen() function saved in the .dll file. This function takes four pointers to DWORD-type objects as input.
        info from pdf:
        The function opens a connection to the hardware through the selected USB port. All the settings for the connection
        are collected in DeviceRec structure.
        """
        
        # initialise of which type the arguments and output of the function will be
        self.CU80.CU80WOpen.argtypes = [ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong)]
        self.CU80.CU80WOpen.restype = ctypes.c_char  # not sure about this one
    
        # call the function with 4 input arguments (ctypes.pointer creates a pointer to an object, c_ulong makes a DWORD)
        self.CU80.CU80WOpen(
            ctypes.pointer(ctypes.c_ulong(self.USBInstance)),
            ctypes.pointer(ctypes.c_ulong(self.USBVersion)), 
            ctypes.pointer(ctypes.c_ulong(self.DevID)), 
            ctypes.pointer(ctypes.c_ulong(self.EEID)) )
        
        print('Connected to the Mechonics stage')

        
    def move(self, Axis, Velocity, Voltage):
        """Move the stage. Info from documentation pdf:
        The function performs continuous movement along one of the axes. The movement could be stopped using
        CU30WStop() or adjusting the Timeout parameter. All the settings for the connection are collected in DeviceRec
        structure members, initialized during CU30WOpen() call.
        USBInstance, USBVersion, DevID, EEID – represent the corresponding fields of a DeviceRec structure,
        which contains the settings of the opened connection.
        Vel – Velocity of the movement; Vel = [-1000...-1, 1…+1000] , Vel = 0 => Vel = 1;
        Axis – Determines the axis of the movement (1 = X-Axis, 2 = Y-Axis, 3 = Z-Axis)
        Timeout – Determines the movement duration. Timeout = [2..255]
        If Timeout < 0, - the duration of the movement will be: Duration = 2 * 0.016 sec.
        If Timeout = 0, - the timeout will be disabled.
        If Timeout = 1, - the duration of the movement will be: Duration = 2 * 0.016 sec.
        If Timeout = [2…254], - the duration of the movement will be: Duration = Timeout * 0.016 sec.
        If Timeout > 254, - the timeout will be disabled.
        """
        
        # initialise types of input parameters (DWORD for usb info, int for movement commands)
        self.CU80.CU80WPiezoMove.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.CU80.CU80WPiezoMove.restype = None  # this function creates no output
        
        # call function
        self.CU80.CU80WPiezoMove(
            ctypes.c_ulong(self.USBInstance),
            ctypes.c_ulong(self.USBVersion),
            ctypes.c_ulong(self.DevID),
            ctypes.c_ulong(self.EEID),
            ctypes.c_int(Axis),
            ctypes.c_int(Velocity),
            ctypes.c_int(Voltage))
        #time.sleep(2)
        #print("move")
                
    def close_connection(self):
        """info from pdf:
        The function closes a connection to the hardware through the selected USB port, opened with previous call of
        CU30Open() function. All the settings for the connection are collected in DeviceRec structure members, initialized
        during CU30WOpen() call.
        
        -CU30WrapperDispose()
        The function releases all the memory and resources, allocated during work of the wrapper dll. It is called automatically
        when the dll is being removed from memory or it can be accessed manually.
        """
        
        # initialise types of input parameters (DWORD for usb info)
        self.CU80.CU80WClose.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
        self.CU80.CU80WClose.restype = None  # this function creates no output
        
        # call function
        self.CU80.CU80WClose(
            ctypes.c_ulong(self.USBInstance),
            ctypes.c_ulong(self.USBVersion),
            ctypes.c_ulong(self.DevID),
            ctypes.c_ulong(self.EEID) )
        
        print("connection is closed")
        
    def stop_moving(self):
        """info from pdf:
        The function instantly terminates any movement of the selected hardware. All the settings for the connection are
        collected in DeviceRec structure members, initialized during CU30WOpen() call.
        """
        
        # initialise types of input parameters (DWORD for usb info)
        self.CU80.CU80WPiezoStop.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
        self.CU80.CU80WPiezoStop.restype = None  # this function creates no output
        
        # call function
        self.CU80.CU80WPiezoStop(
            ctypes.c_ulong(self.USBInstance),
            ctypes.c_ulong(self.USBVersion),
            ctypes.c_ulong(self.DevID),
            ctypes.c_ulong(self.EEID) )
        
        #print("stop")
        
    def dcdc_on(self):
        """info from pdf:
        The function switches DCDC-converter on for the selected hardware. All the settings for the connection are collected
        in DeviceRec structure members, initialized during CU30WOpen() call.
        """
        
        # initialise types of input parameters (DWORD for usb info)
        self.CU80.CU80WDCDCon.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
        self.CU80.CU80WDCDCon.restype = None  # this function creates no output
        
        # call function
        self.CU80.CU80WDCDCon(
            ctypes.c_ulong(self.USBInstance),
            ctypes.c_ulong(self.USBVersion),
            ctypes.c_ulong(self.DevID),
            ctypes.c_ulong(self.EEID) )
        
    def dcdc_off(self):
        """info from pdf:
        The function switches DCDC-converter on for the selected hardware. All the settings for the connection are collected
        in DeviceRec structure members, initialized during CU30WOpen() call.
        """
        
        # initialise types of input parameters (DWORD for usb info)
        self.CU80.CU80WDCDCoff.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
        self.CU80.CU80WDCDCoff.restype = None  # this function creates no output
        
        # call function
        self.CU80.CU80WDCDCoff(
            ctypes.c_ulong(self.USBInstance),
            ctypes.c_ulong(self.USBVersion),
            ctypes.c_ulong(self.DevID),
            ctypes.c_ulong(self.EEID) )
        
    def get_EEprom_info(self): #still to be implemented
        """info from pdf:
        The function collects information about EEPROM and returns it in the output parameters. All the settings for the
        connection are collected in DeviceRec structuremembers, initialized during CU30WOpen() call.
        Parameters:
        USBInstance, USBVersion, DevID, EEID – represent the corresponding fields of a DeviceRec structure,
        which contains the settings of the opened connection.
        pUSBVendorID - pointer to a DWORD variable, where the vendor ID will be returned.
        pUSBProductID - pointer to a DWORD variable, where the product ID will be returned.
        pUSBDeviceID - pointer to a DWORD variable, where the USB device ID will be returned.
        pDeviceID - pointer to a DWORD variable, where the device ID will be returned.
        pEEPromID - pointer to a DWORD variable, where the EEPROM id will be returned.
        pVersion - pointer to a DWORD variable, where the version will be returned.
        pSerialNumber - pointer to a DWORD variable, where the serial number will be returned.
        pCustomerID - pointer to a DWORD variable, where the customer ID will be returned.
        pCompany - pointer to a string variable, where the company name will be returned. The size of the
        buffer must be at least 32 characters.
        pDate - pointer to a string variable, where the date will be returned. The size of the buffer must be
        at least 32 characters.
        pProductStr - pointer to a string variable, where the product name will be returned. The size of the
        buffer must be at least 32 characters.
        pCustomer - pointer to a string variable, where the customer name will be returned. The size of the
        buffer must be at least 32 characters.
        pCustomerStr - pointer to a string variable, where the customer string will be returned. The size of the
        buffer must be at least 32 characters.
        """
        
        self.CU80.CU80WGetEEPROMInfo.argtypes = [
            ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, 
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_wchar),
            ctypes.POINTER(ctypes.c_wchar),
            ctypes.POINTER(ctypes.c_wchar),
            ctypes.POINTER(ctypes.c_wchar),
            ctypes.POINTER(ctypes.c_wchar)] 
        
        class Output(ctypes.Structure):
            _fields_ = [
            ("pUSBVendorID", ctypes.POINTER(ctypes.c_ulong)),
            ("pUSBProductID", ctypes.POINTER(ctypes.c_ulong)),
            ("pUSBDeviceID", ctypes.POINTER(ctypes.c_ulong)),
            ("pDeviceID", ctypes.POINTER(ctypes.c_ulong)),
            ("pEEPromID", ctypes.POINTER(ctypes.c_ulong)),
            ("pVersion", ctypes.POINTER(ctypes.c_ulong)),
            ("pSerialNumber", ctypes.POINTER(ctypes.c_ulong)),
            ("pCustomerID", ctypes.POINTER(ctypes.c_ulong)),
            ("pCompany", ctypes.POINTER(ctypes.c_wchar)),
            ("pDate", ctypes.POINTER(ctypes.c_wchar)),
            ("pProductStr", ctypes.POINTER(ctypes.c_wchar)),
            ("pCustomer", ctypes.POINTER(ctypes.c_wchar)),
            ("pCustomerStr", ctypes.POINTER(ctypes.c_wchar))]
        
        self.CU80.CU80WGetEEPROMInfo.restype = None
        
        # initialize saving spots for function output:
        pUSBVendorID = ctypes.c_ulong()
        pUSBProductID = ctypes.c_ulong()
        pUSBDeviceID = ctypes.c_ulong()
        pDeviceID = ctypes.c_ulong()
        pEEPromID = ctypes.c_ulong()
        pVersion = ctypes.c_ulong()
        pSerialNumber = ctypes.c_ulong()
        pCustomerID = ctypes.c_ulong()
        pCompany = ctypes.c_wchar()
        pDate = ctypes.c_wchar()
        pProductStr = ctypes.c_wchar()
        pCustomer = ctypes.c_wchar()
        pCustomerStr = ctypes.c_wchar()
        
        print("bla")
        print(pUSBVendorID.value)
        print(pUSBProductID.value)
        print(pUSBDeviceID.value)
        print(pDeviceID.value)
        print(pEEPromID.value)
        print(pVersion.value)
        print(pSerialNumber.value)
        print(pCustomerID.value)
        print(pCompany.value)
        print(pDate.value)
        print(pProductStr.value)
        print(pCustomer.value)
        print(pCustomerStr.value)
        
        self.CU80.CU80WGetEEPROMInfo(
            ctypes.c_ulong(self.USBInstance),
            ctypes.c_ulong(self.USBVersion),
            ctypes.c_ulong(self.DevID),
            ctypes.c_ulong(self.EEID),
            ctypes.byref(pUSBVendorID),
            ctypes.byref(pUSBProductID),
            ctypes.byref(pUSBDeviceID),
            ctypes.byref(pDeviceID),
            ctypes.byref(pEEPromID),
            ctypes.byref(pVersion),
            ctypes.byref(pSerialNumber),
            ctypes.byref(pCustomerID),
            ctypes.byref(pCompany),
            ctypes.byref(pDate),
            ctypes.byref(pProductStr),
            ctypes.byref(pCustomer),
            ctypes.byref(pCustomerStr) )
        
        print("blub")
        print(pUSBVendorID.value)
        print(pUSBProductID.value)
        print(pUSBDeviceID.value)
        print(pDeviceID.value)
        print(pEEPromID.value)
        print(pVersion.value)
        print(pSerialNumber.value)
        print(pCustomerID.value)
        print(pCompany.value)
        print(pDate.value)
        print(pProductStr.value)
        print(pCustomer.value)
        print(pCustomerStr.value)
        


def count():
    inst = visa.ResourceManager().open_resource('TCPIP::192.168.0.208::INSTR')
    reply = inst.query(':MEASure:ITEM? VMID,CHANnel1')
    return reply

def rigol():
    v = []
    for i in range(5):
        c = count()
        v.append(float(c))
        time.sleep(0.1)
    av = np.mean(v)
    return av
   
if __name__ == '__main__':   
    #example of usage, open connection and move in x and y direction:
    mechonics = Mechonics()
    mechonics.open_connection()
    mechonics.dcdc_on()
    data = []
    piezo = []
    r = []
    #for k in range(10):
    for i in range(5):
            #x move posi
        #for i in range(1):
            vel=1; vol=1
            mechonics.move(1, vel, vol)
            time.sleep(0.05)
            mechonics.stop_moving()

            #piezo.append(j)
            #record
            #time.sleep(0.5)
            ##ct = rigol()
            #r.append(ct)
            #print(k, j, ct)
        #back original position
        #for i in range(1*50):
        #        mechonics.move(1, -vel, vol)
        #        time.sleep(0.05)
        #        mechonics.stop_moving()
    #data.append(piezo)
    #data.append(r)
    #x = np.array(data)
    #mechonics.dcdc_off()
    #time.sleep(0.5)
    #mechonics.close_connection()
    #np.savetxt('data2.txt', x.T, delimiter=",")


