import ctypes
import win32gui
import win32ui

import cv2
import mss
import numpy as np
from PIL import ImageWin, Image


def get_window(name):
    enum_windows = ctypes.windll.user32.EnumWindows
    enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    get_window_text = ctypes.windll.user32.GetWindowTextW
    get_window_text_length = ctypes.windll.user32.GetWindowTextLengthW
    print_window = ctypes.windll.user32.PrintWindow

    mesen_handlers = []

    def foreach_window(hwnd, l_param):
        length = get_window_text_length(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        get_window_text(hwnd, buff, length + 1)
        if name in buff.value:
            mesen_handlers.append(hwnd)

    enum_windows(enum_windows_proc(foreach_window), 0)

    image = ImageWin.Dib('RGB', (1920, 1080))
    print(image.expose(mesen_handlers[0]))
    # print(print_window(mesen_handlers[0], int(image)))

    # image.expose(mesen_handlers[0])
    # dc =  ImageWin.HDC()
    # print(hdc.)

    # CDC.GetHandleAttrib()

    #
    # get_window_rect = ctypes.windll.user32.GetWindowRect
    # print_window()

    # EnumWindows = ctypes.windll.user32.EnumWindows
    # EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    # GetWindowText = ctypes.windll.user32.GetWindowTextW
    # GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    # IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    # titles = []

    # def foreach_window(hwnd, lParam):
    #    if IsWindowVisible(hwnd):
    #        length = GetWindowTextLength(hwnd)
    #        buff = ctypes.create_unicode_buffer(length + 1)
    #        GetWindowText(hwnd, buff, length + 1)
    #        titles.append(buff.value)
    #    return True

    # EnumWindows(EnumWindowsProc(foreach_window), 0)
    # for title in titles:
    #    if "Mesen" in title:
    #        print(title)


def main():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        while True:
            image = sct.grab(monitor)
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            cv2.imshow('screen', gray)
            cv2.waitKey(1)


def another_try():
    hwnd = win32gui.FindWindow(None, 'Mesen - Tetris')
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    cv2.imshow('screen', gray)
    cv2.waitKey(1)


if __name__ == '__main__':
    # main()
    # get_window("Mesen")
    while True:
        another_try()
