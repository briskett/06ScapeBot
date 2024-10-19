import cv2 as cv
from windowcapture import WindowCapture
from vision import Vision
from time import time

# Init WindowCapture class
wincap = WindowCapture('Vidyascape 8.2.5')
# Init vision class
vision = Vision()
# Init trackbar window
vision.init_control_gui()
# for fps
loop_time = time()


while True:

    # Screenshot, apply filter
    screenshot = wincap.get_screenshot()
    processed_image = vision.apply_hsv_filter(screenshot)  # I can apply any hsv filter as a second parameter.

    # Display processed image
    cv.imshow('Filter Test', processed_image)

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

