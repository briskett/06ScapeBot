from utils.hsvfilter import HsvFilter
from vision import Vision
import os


class FishType:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Define constants for HSV filters and thresholds
    HSV_FILTERS = {
        'net': HsvFilter(46, 0, 219, 179, 255, 255, 255, 255, 0, 0),
    }
    THRESHOLDS = {
        'net': 0.70,
    }
    IMAGE_PATHS = {
        'net': {
            'spot': os.path.join(BASE_DIR, 'fish_bot', 'fish_spot.jpg'),
            'tooltip': os.path.join(BASE_DIR, 'fish_bot', 'net_tooltip.jpg'),
        }
    }

    def __init__(self, type: str):
        if type not in self.HSV_FILTERS:
            raise ValueError(f"Unsupported mob type: {type}")

        self.spot_vision = Vision(self.IMAGE_PATHS[type]['body'])
        self.tooltip_vision = Vision(self.IMAGE_PATHS[type]['tooltip'])
        self.hsv_filter = self.HSV_FILTERS[type]
        self.spot_threshold = self.THRESHOLDS[type]

    def get_spot_vision(self):
        return self.spot_vision

    def get_hsv_filter(self):
        return self.hsv_filter

    def get_tooltip_vision(self):
        return self.tooltip_vision

    def get_spot_threshold(self):
        return self.spot_threshold
