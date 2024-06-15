import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:
    # Monitor width and height
    offset_x = 0
    offset_y = 0
    cropped_x = 0
    cropped_y = 0
    w = 0
    h = 0
    hwnd = None

    # Constructor, pass self to pass class 'members', and the values within the members are called 'states'.
    def __init__(self, window_name = None):
        # if no window name is given, capture desktop
        if window_name == None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window {} not found'.format(window_name))

        # Get window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # Remove window border and title bar
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # Set cropped coords offset to translate screenshots to real screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        # Get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # optimizing and completing conversion
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Get rid of the alpha channel, literally no idea what this means.
        # It will cause issues with match template if we don't. Sad, causes frame drops.
        img = img[..., :3]

        # This too prevents more errors. No idea why.
        img = np.ascontiguousarray(img)

        # convert and return color
        return img

    # Translates a pixel coord on screenshot img to a pixel coord on screen.
    # pos = x,y
    # WARNING: don't move the window being captured after execution, this will return incorrect coords.
    # This is not constantly updated, it's called only once, which is in the constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows(winEnumHandler, None)
