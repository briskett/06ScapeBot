from time import time, sleep
from mob_bot import mobcapture
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
import random
from fishtype import FishType


class FishBot:

    def __init__(self, wincap: WindowCapture, vision: Vision, fish: FishType):
        self.is_bot_running = False
        self.loop_time = time()
        self.wincap = wincap
        self.body = vision  # The object to be detected.
        self.tooltip_vision = fish.get_tooltip_vision()

        print('Bot starting in 5!')
        for x in range(0, 5):
            print(x)
            sleep(1)

    def click_target(self, rectangles, screenshot):
        found = False
        if len(rectangles) > 0:
            print('target found')
            targets = self.body.get_click_points(rectangles)
            for target in targets:
                screen_pos = self.wincap.get_screen_position(target)
                pyautogui.moveTo(screen_pos[0], screen_pos[1])
                sleep(.8)  # Sleep to ensure movement time

                # Confirm mob after moving mouse to supposed mob
                confirmation = self.confirm()
                if confirmation:
                    pyautogui.click()
                    sleep(random.randint(14, 20))  # Sleep to simulate attack time
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
        tooltip_rectangles = mobcapture.get_tooltip_rectangles()
        if tooltip_rectangles.size != 0:
            print("Object confirmed")
        else:
            print("Object NOT confirmed")

        return len(tooltip_rectangles) > 0
