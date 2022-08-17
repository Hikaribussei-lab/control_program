import pyautogui
import time
import win32gui
import win32con
import win32api

def getpos():   
    print (pyautogui.position())

def measure(x1, y1, x2, y2, a, b):
    pyautogui.hotkey("ctrl", "U")
    pyautogui.click(x1, y1)
    pyautogui.click(x2, y2)
    pyautogui.click(a, b)

def foreground():
    hwnd = win32gui.FindWindow(None, "SES")
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    pyautogui.moveTo(left+60, top + 10)
    pyautogui.click()

    
#pyautogui.click(1150, 710)
#ses = win32gui.FindWindow(None, "SES")
#time.sleep(1)
#win32gui.SetForegroundWindow(ses)
#time.sleep(1)
#pyautogui.hotkey("ctrl", "u")
#time.sleep(1)
pyautogui.click(1150, 600, clicks=5, interval=1)
time.sleep(2)
#foreground()
pyautogui.hotkey("ctrl", "u")
