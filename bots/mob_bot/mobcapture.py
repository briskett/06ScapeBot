import cv2 as cv
from windowcapture import WindowCapture
from threading import Thread
from time import time
from mobtype import MobType
from atk_bot import AttackBot
from vision import Vision
from player import Player

# Init WindowCapture class
wincap = WindowCapture('RuneScape 2006 singleplayer [v3.4] by Mige')
# track bot status
is_bot_running = False
# Init mob type
mob_type = MobType('cow')
# Init vision
vision = Vision()
# Init cascade path
cascade = cv.CascadeClassifier(mob_type.get_cascade_path())
# Init Attack Bot
bot = AttackBot(wincap, cascade, mob_type)

loop_time = time()


def click_target():
    bot.click_target(body_rectangles, screenshot)


def get_tooltip_rectangles():
    return tooltip_rectangles


def get_death_rectangles():
    return death_rectangle


while True:

    # Screenshot, apply filter
    screenshot = wincap.get_screenshot()

    # Detect objects
    body_rectangles = cascade.detectMultiScale(screenshot)
    tooltip_rectangles = mob_type.tooltip_vision.find(screenshot, 0.5, 1)  # Modify threshold for tooltip if needed.
    death_rectangle = mob_type.get_death_tooltip().find(screenshot, 0.9, 1)
    # Draw detection results onto original image.
    output_image = vision.draw_rectangles(screenshot, body_rectangles)  # Draw rectangles around the mob's body.
    output_image = vision.draw_rectangles(screenshot, tooltip_rectangles)  # Draws a rectangle around the tooltip.
    output_image = vision.draw_rectangles(output_image, death_rectangle)  # Draw death tooltip rectangle

    # Display processed image
    cv.imshow('Matches', output_image)

    if not bot.is_bot_running:
        bot.is_bot_running = True
        t = Thread(target=click_target)
        t.start()

    # Comparing current time, to last bookmark of time in while loop.
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press q with the output window FOCUSED to quit
    # waits 1ms every loop to process key presses.
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('images/positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('images/negative/{}.jpg'.format(loop_time), screenshot)

print('Done.')
