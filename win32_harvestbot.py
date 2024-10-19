from time import time, sleep
from bots.woodcutter_bot import liveCapture
from windowcapture import WindowCapture
from vision import Vision
import random
from bots.woodcutter_bot.logtype import LogType
from pywinauto import mouse, keyboard
import win32gui

class HarvestBot:

    def __init__(self, wincap: WindowCapture, vision: Vision, log: LogType):
        self.is_bot_running = False
        self.loop_time = time()
        self.wincap = wincap
        self.trunks = vision  # The object to be detected.
        self.tooltip_vision = log.get_tooltip_vision()
        self.log = log
        self.hwnd = self.wincap.hwnd
        self.window_rect = win32gui.GetWindowRect(self.hwnd)  # Get window rect at initialization

        print('Bot starting in 5!')
        for x in range(0, 5):
            print(5 - x)
            sleep(1)

    def click_target(self, rectangles, screenshot):
        self.drop_inv(self.log)
        found = False
        if len(rectangles) > 0:
            print('Target found')
            targets = self.trunks.get_click_points(rectangles)
            for target in targets:
                screen_pos = self.wincap.get_screen_position(target)
                self.move_mouse(screen_pos[0], screen_pos[1])
                sleep(.8)  # Sleep to ensure movement time

                # Confirm tree after moving mouse to supposed tree
                confirmation = self.confirm()
                if confirmation:
                    self.click_mouse(screen_pos[0], screen_pos[1])
                    sleep(random.randint(14, 20))  # Sleep to simulate harvesting time
                    found = True
                    break  # Exit loop if target confirmed

        if not found:
            self.search()

        self.is_bot_running = False

    def search(self):
        print('Searching..')
        self.press_key('{RIGHT}')
        self.press_key('{DOWN}')
        sleep(.5)
        self.release_key('{RIGHT}')
        self.release_key('{DOWN}')
        sleep(.5)  # Sleep to ensure rotation time

    def confirm(self):
        tooltip_rectangles = liveCapture.get_tooltip_rectangles()
        if tooltip_rectangles.size != 0:
            print("Object confirmed")
            return True
        else:
            print("Object NOT confirmed")
            return False

    def drop_inv(self, log: LogType):
        log_rectangles = liveCapture.get_log_rectangles()
        print(log_rectangles.size)
        if log_rectangles.size > 25:
            targets = log.get_log_vision().get_click_points(log_rectangles)
            for target in targets:
                screen_pos = self.wincap.get_screen_position(target)
                self.move_mouse(screen_pos[0], screen_pos[1])
                sleep(.3)  # Sleep to ensure movement time
                self.right_click_mouse(screen_pos[0], screen_pos[1])
                self.move_mouse(screen_pos[0], screen_pos[1] + 40)
                self.click_mouse(screen_pos[0], screen_pos[1])

    def move_mouse(self, x, y):
        screen_x = self.window_rect[0] + x
        screen_y = self.window_rect[1] + y
        mouse.move(coords=(screen_x, screen_y))

    def click_mouse(self, x, y):
        screen_x = self.window_rect[0] + x
        screen_y = self.window_rect[1] + y
        mouse.click(button='left', coords=(screen_x, screen_y))

    def right_click_mouse(self, x, y):
        screen_x = self.window_rect[0] + x
        screen_y = self.window_rect[1] + y
        mouse.click(button='right', coords=(screen_x, screen_y))

    def press_key(self, key):
        keyboard.send_keys(key)

    def release_key(self, key):
        # Pywinauto handles key release automatically
        pass


