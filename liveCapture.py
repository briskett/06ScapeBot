import cv2 as cv
from windowcapture import WindowCapture
from vision import Vision
from threading import Thread
from time import time
from logtype import LogType
from harvestbot import HarvestBot

# Init WindowCapture class
wincap = WindowCapture('Vidyascape 8.2.5')

# track bot status
is_bot_running = False
loop_time = time()
# Init oak vision
log_type = LogType('oak')
# Tree HSV Filter
hsv_filter = log_type.get_hsv_filter()
# Init vision class to find processed trunk of tree
trunk = log_type.get_processed_trunk()
# Init harvestBot
bot = HarvestBot(wincap, trunk, log_type)


def click_target():
    bot.click_target(trunk_rectangles, screenshot)


def get_tooltip_rectangles():
    return tooltip_rectangles

def get_log_rectangles():
    return log_rectangles


while True:

    # Screenshot, apply filter
    screenshot = wincap.get_screenshot()
    processed_image = trunk.apply_hsv_filter(screenshot, hsv_filter)  # New Haystack to search through

    # Detect objects
    trunk_rectangles = trunk.find(processed_image, log_type.trunk_threshold)  # Apply new Haystack for processed object to be found.
    tooltip_rectangles = log_type.tooltip_vision.find(screenshot, 0.9, 1)  # Modify threshold for tooltip if needed.
    log_rectangles = log_type.log_vision.find(screenshot, .90, 28)  # Modify threshold for log if needed.

    # Draw detection results onto original image.
    output_image = trunk.draw_rectangles(screenshot, trunk_rectangles)  # Draw rectangles around trunks.
    output_image = log_type.tooltip_vision.draw_rectangles(screenshot, tooltip_rectangles)  # Draws a rectangle around the tooltip.
    output_image = log_type.log_vision.draw_rectangles(screenshot, log_rectangles)  # Draw rectangles around logs

    # Display processed image
    cv.imshow('Matches', output_image)
    cv.imshow("hsv", processed_image)

    if not bot.is_bot_running:
        bot.is_bot_running = True
        t = Thread(target=click_target)
        t.start()

    # Comparing current time, to last bookmark of time in while loop.
    print('FPS {}'.format(1 / (time() - loop_time)))
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
