from time import time, sleep
import cv2 as cv
from mob_bot import mobcapture, player
from vision import Vision
from windowcapture import WindowCapture
import pyautogui
import random
from mobtype import MobType
from player import Player
from foodtype import FoodType


class AttackBot:

    def __init__(self, wincap: WindowCapture, cascade, mob: MobType):
        self.is_bot_running = False
        self.loop_time = time()
        self.wincap = wincap
        self.tooltip_vision = mob.get_tooltip_vision()
        self.cascade = cascade
        self.player = Player('player')
        self.food = FoodType('shark')
        self.vision = Vision()
        self.mob = mob

        print('Bot starting in 5!')
        for x in range(0, 5):
            print(x)
            sleep(1)

    def click_target(self, mob_rectangles, screenshot):
        self.heal(screenshot)
        found = False
        if len(mob_rectangles) > 0:
            print('target found')
            targets = self.tooltip_vision.get_click_points(mob_rectangles)
            for target in targets:
                screen_pos = self.wincap.get_screen_position(target)
                pyautogui.moveTo(screen_pos[0], screen_pos[1])
                sleep(.2)  # Sleep to ensure movement time

                # Confirm mob after moving mouse to supposed mob
                confirmation = self.confirm()
                if confirmation:
                    found = True
                    pyautogui.click()

                    # Maintain healing process while mob still alive
                    sleep(3)  # To ensure that death tooltip appears
                    dead = self.mob_death(mobcapture.get_death_rectangles())
                    while not dead:  # While the mob ain't dead
                        self.heal(screenshot)
                        dead = self.mob_death(mobcapture.get_death_rectangles())

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
        pyautogui.keyUp('down')
        sleep(.5)  # Sleep to ensure rotation time

    def confirm(self):
        tooltip_rectangles = mobcapture.get_tooltip_rectangles()
        if tooltip_rectangles.size != 0:
            print("Mob confirmed")
        else:
            print("Mob NOT confirmed")

        return len(tooltip_rectangles) > 0

    def heal(self, screenshot):
        # Capture the health bar or health text area
        health_screenshot = self.process_screenshot(screenshot)

        # Double img size
        health_screenshot = cv.resize(health_screenshot, None, fx=8, fy=8, interpolation=cv.INTER_NEAREST)

        # Process the image to determine health status
        health_low = self.get_health_percentage(health_screenshot)

        if health_low:  # Set your threshold for healing
            self.perform_heal_action(screenshot)

    def process_screenshot(self, screenshot):
        health_area = self.vision.capture_health_area(screenshot, self.player.get_health_bar_template())
        return health_area

    def get_health_percentage(self, health_screenshot):
        # Save the health area for further analysis
        cv.imwrite('mobs/human/health_area.png', health_screenshot)
        pixel_color = health_screenshot[105][228]  # y, x of pixel in health sphere

        if (pixel_color == [19, 19, 19]).all():
            return True
        else:
            return False

    def perform_heal_action(self, screenshot):
        # Find food
        food_vision = self.food.get_food_vision()
        food_rectangles = food_vision.find(screenshot)
        targets = food_vision.get_click_points(food_rectangles)
        for target in targets:
            screen_pos = self.wincap.get_screen_position(target)
            pyautogui.moveTo(screen_pos[0], screen_pos[1])
            sleep(.1)  # Sleep to ensure movement time
            pyautogui.click()
            break

    def food_confirm(self):
        food_tooltip_vision = self.food.get_tooltip_vision()
        food_rectangles = food_tooltip_vision.find(food_tooltip_vision)
        if food_rectangles.size != 0:
            print("Object confirmed")
        else:
            print("Object NOT confirmed")

        return len(food_rectangles) > 0

    def mob_death(self, death_rectangle):

        if len(death_rectangle) < 1:
            print("Mob dead")
            return True
        else:
            return False
