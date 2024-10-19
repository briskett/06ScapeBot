from time import time, sleep
import liveCapture
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
import random
from bots.woodcutter_bot.logtype import LogType

class HarvestBot:

    def __init__(self, wincap: WindowCapture, vision: Vision, log: LogType):
        self.is_bot_running = False
        self.loop_time = time()
        self.wincap = wincap
        self.trunks = vision  # The object to be detected.
        self.tooltip_vision = log.get_tooltip_vision()
        self.log = log

        print('Bot starting in 5!')
        for x in range(0, 5):
            print(x)
            sleep(1)


    def click_target(self, rectangles, screenshot):
        self.drop_inv(self.log)
        found = False
        if len(rectangles) > 0:
            print('target found')
            targets = self.trunks.get_click_points(rectangles)
            for target in targets:
                screen_pos = self.wincap.get_screen_position(target)
                pyautogui.moveTo(screen_pos[0], screen_pos[1])
                sleep(.8)  # Sleep to ensure movement time

                # Confirm tree after moving mouse to supposed tree
                confirmation = self.confirm()
                if confirmation:
                    pyautogui.click()
                    sleep(random.randint(14, 20))  # Sleep to simulate mining time
                    found = True
                    break  # Exit loop if target confirmed

        if not found:
            self.search()

        self.is_bot_running = False

    def search(self):
        print('Searching..')
        pyautogui.keyDown('right')
        pyautogui.keyDown('down')
        sleep(.5)
        pyautogui.keyUp('right')
        pyautogui.keyDown('down')
        sleep(.5)  # Sleep to ensure rotation time

    def confirm(self):
        tooltip_rectangles = liveCapture.get_tooltip_rectangles()
        if tooltip_rectangles.size != 0:
            print("Object confirmed")
        else:
            print("Object NOT confirmed")

        return len(tooltip_rectangles) > 0

    def drop_inv(self, log: LogType):
        log_rectangles = liveCapture.get_log_rectangles()
        print(log_rectangles.size)
        if log_rectangles.size > 25:
            targets = log.get_log_vision().get_click_points(log_rectangles)
            for target in targets:
                screen_pos = self.wincap.get_screen_position(target)
                pyautogui.moveTo(screen_pos[0], screen_pos[1])
                sleep(.3)  # Sleep to ensure movement time
                pyautogui.rightClick()
                pyautogui.moveTo(screen_pos[0], screen_pos[1] + 40)
                pyautogui.click()

    #def pickpocket(self, mob):