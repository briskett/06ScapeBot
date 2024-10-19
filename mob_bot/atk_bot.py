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
        """
        Initializes the AttackBot class with essential components for interacting with the game.

        :param wincap: A WindowCapture object that facilitates capturing the game screen.
        :param cascade: A Haar cascade or similar object detection model used to detect mobs.
        :param mob: A MobType object representing the specific mob the bot is designed to target.
        """
        self.is_bot_running = False  # Flag to track if the bot is currently running.
        self.loop_time = time()  # Tracks the time for each loop iteration.
        self.wincap = wincap  # Used to capture screenshots from the game window.
        self.tooltip_vision = mob.get_tooltip_vision()  # Vision system to detect tooltips related to mobs.
        self.cascade = cascade  # The classifier used for object detection.
        self.player = Player('player')  # Represents the player, including their health and status.
        self.food = FoodType('shark')  # Food type for healing, with 'shark' being the type of food.
        self.vision = Vision()  # Vision object used for detecting different in-game elements.
        self.mob = mob  # The target mob object that the bot will be interacting with.

        # Initial countdown before the bot starts, giving the user time to set things up.
        print('Bot starting in 5!')
        for x in range(0, 5):
            print(x)
            sleep(1)

    def click_target(self, mob_rectangles, screenshot):
        """
        Clicks on a detected mob, initiates combat, and handles healing while engaging the target.

        :param mob_rectangles: Rectangles detected from the screen where mobs are located.
        :param screenshot: Current screenshot of the game window.
        """
        # First, heal the player before engaging in combat.
        self.heal(screenshot)

        found = False  # Flag to track if a valid target is found.

        # If any mobs were detected from the screen.
        if len(mob_rectangles) > 0:
            print('target found')
            # Get the click points for all detected mobs.
            targets = self.tooltip_vision.get_click_points(mob_rectangles)

            # Loop through the detected targets.
            for target in targets:
                # Get the screen position for the current target.
                screen_pos = self.wincap.get_screen_position(target)
                pyautogui.moveTo(screen_pos[0], screen_pos[1])  # Move the mouse to the target's location.
                sleep(.2)  # Short delay to simulate human-like mouse movement.

                # Confirm if the object under the mouse is actually the target mob.
                confirmation = self.confirm()
                if confirmation:
                    found = True  # Mark the target as found and confirmed.
                    pyautogui.click()  # Click to initiate interaction with the mob.

                    # After engaging the mob, wait to ensure the mob is in combat.
                    sleep(3)  # Pause to wait for the mob's "death" tooltip to appear.

                    # Check if the mob has died.
                    dead = self.mob_death(mobcapture.get_death_rectangles())

                    # Continue healing while the mob is alive.
                    while not dead:  # If the mob isn't dead yet.
                        self.heal(screenshot)  # Heal the player periodically during combat.
                        dead = self.mob_death(mobcapture.get_death_rectangles())  # Check again if the mob has died.

                    break  # Exit the loop after the target is confirmed and fought.

        if not found:
            self.search()  # If no valid target is found, initiate a search by rotating the camera.

        self.is_bot_running = False  # Stop the bot after the target interaction is completed.

    def search(self):
        """
        Rotates the in-game camera to search for targets when no mob is detected.
        """
        print('Searching..')
        # Rotate the camera by holding down the movement keys.
        pyautogui.keyDown('right')
        pyautogui.keyDown('down')
        sleep(.5)  # Small delay to allow for proper camera rotation.
        pyautogui.keyUp('right')
        pyautogui.keyUp('down')
        sleep(.5)  # Another pause after releasing the keys.

    def confirm(self):
        """
        Confirms if the target under the cursor is a valid mob by checking for tooltip rectangles.

        :return: Boolean indicating whether the mob was confirmed.
        """
        tooltip_rectangles = mobcapture.get_tooltip_rectangles()  # Get the detected tooltip rectangles.
        if tooltip_rectangles.size != 0:
            print("Mob confirmed")  # Log if a mob was confirmed.
        else:
            print("Mob NOT confirmed")  # Log if no mob was confirmed.

        return len(tooltip_rectangles) > 0  # Return True if any tooltip rectangles were found.

    def heal(self, screenshot):
        """
        Checks the player's health and performs a healing action if health is below a certain threshold.

        :param screenshot: Current screenshot of the game window.
        """
        # Capture the health bar area from the screenshot.
        health_screenshot = self.process_screenshot(screenshot)

        # Double the image size to better analyze the health pixels.
        health_screenshot = cv.resize(health_screenshot, None, fx=8, fy=8, interpolation=cv.INTER_NEAREST)

        # Check if health is low based on the color of a specific pixel in the health bar.
        health_low = self.get_health_percentage(health_screenshot)

        # If health is low, perform a healing action (consume food).
        if health_low:
            self.perform_heal_action(screenshot)

    def process_screenshot(self, screenshot):
        """
        Captures the relevant area of the screen that contains the player's health bar.

        :param screenshot: The screenshot from which to extract the health area.
        :return: Cropped image containing the health bar.
        """
        # Capture the area of the screen where the health bar is located using a health bar template.
        health_area = self.vision.capture_health_area(screenshot, self.player.get_health_bar_template())
        return health_area

    def get_health_percentage(self, health_screenshot):
        """
        Determines whether the player's health is low based on pixel analysis of the health bar.

        :param health_screenshot: Screenshot of the health bar.
        :return: Boolean indicating if the player's health is low.
        """
        # Save the health area image for further analysis.
        cv.imwrite('mobs/human/health_area.png', health_screenshot)

        # Analyze the color of a specific pixel in the health bar to determine health status.
        pixel_color = health_screenshot[105][228]  # Pixel coordinates for health analysis (y, x).

        # If the pixel matches the expected low-health color, return True.
        if (pixel_color == [19, 19, 19]).all():
            return True
        else:
            return False

    def perform_heal_action(self, screenshot):
        """
        Performs a healing action by detecting and consuming food from the inventory.

        :param screenshot: Current screenshot of the game window.
        """
        # Detect food items in the player's inventory.
        food_vision = self.food.get_food_vision()
        food_rectangles = food_vision.find(screenshot)

        # Get click points for the detected food items.
        targets = food_vision.get_click_points(food_rectangles)

        # Loop through detected food items and click on the first one found.
        for target in targets:
            screen_pos = self.wincap.get_screen_position(target)  # Get the screen position of the food.
            pyautogui.moveTo(screen_pos[0], screen_pos[1])  # Move the mouse to the food item.
            sleep(.1)  # Short delay to simulate human-like movement.
            pyautogui.click()  # Click to consume the food item.
            break  # Exit after clicking on the first food item.

    def mob_death(self, death_rectangle):
        """
        Checks if the mob has died based on the appearance of the "death" tooltip.

        :param death_rectangle: Detected rectangles that signify the mob's death.
        :return: Boolean indicating if the mob has died.
        """
        # If no death rectangles are found, the mob is considered dead.
        if len(death_rectangle) < 1:
            print("Mob dead")
            return True
        else:
            return False  # If death rectangles are still present, the mob is not dead yet.
