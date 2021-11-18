import os
import sys
import subprocess
import re
import time
import array
import win32gui
import win32con

def test():
    win_name = win32gui.FindWindow(None, 'Line')
    win32gui.SetForegroundWindow(win_name)

if __name__ == '__main__':
    test()