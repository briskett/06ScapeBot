import cv2 as cv
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

# Init WindowCapture class
wincap = WindowCapture('Vidyascape 8.2.5')
# Init vision class
cow = Vision(None)
# Load trained model
cascade = cv.CascadeClassifier('cascade/cascade.xml')
loop_time = time()

while (True):

    # Screenshot, apply filter
    screenshot = wincap.get_screenshot()

    # Detect objects
    rectangles = cascade.detectMultiScale(screenshot)

    # Draw detection results onto original image
    detection_image = cow.draw_rectangles(screenshot, rectangles)

    # Display processed image
    cv.imshow('results', detection_image)

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

