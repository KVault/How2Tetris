import ctypes
import win32gui
import win32ui

import cv2
import numpy as np
from PIL import Image


class ScreenCapture:
    """Holds the screen capture method and a function to return a Bitmap with the
    latest screen information. Bear in mind the returned image might not be OpenCV compatible"""

    def __init__(self, window_name="Mesen - Tetris"):
        """Initializes the Screen capture object. This needs the exact window title
            that the program is going to use (i.e. 'Mesen - Tetris')"""
        self.window_name = window_name
        self.window_handle = win32gui.FindWindow(None, self.window_name)
        hwnd_dc = win32gui.GetWindowDC(self.window_handle)
        self.mfcdc = win32ui.CreateDCFromHandle(hwnd_dc)
        self.dc = self.mfcdc.CreateCompatibleDC()

    def frame(self):
        # First get the rect enclosing the window
        left, top, right, bot = win32gui.GetWindowRect(self.window_handle)
        width = right - left
        height = bot - top

        # Now create the bitmap to hold the image
        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(self.mfcdc, width*3, height*3)

        # Print the window
        self.dc.SelectObject(save_bit_map)
        ctypes.windll.user32.PrintWindow(self.window_handle, self.dc.GetSafeHdc(), 0)

        bmpinfo = save_bit_map.GetInfo()
        bmpstr = save_bit_map.GetBitmapBits(True)

        win32gui.DeleteObject(save_bit_map.GetHandle())
        return Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

    def frame_rgb(self):
        """Returns the current frame in OpenCV RGB mode"""
        bitmap = self.frame()
        rgb = cv2.cvtColor(np.array(bitmap), cv2.COLOR_RGB2BGR)
        return rgb

    def frame_gray(self):
        """Returns the current frame in OpenCV Gray mode"""
        bitmap = self.frame()
        gray = cv2.cvtColor(np.array(bitmap), cv2.COLOR_RGB2GRAY)
        return gray
