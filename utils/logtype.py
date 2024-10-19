from utils.hsvfilter import HsvFilter
from vision import Vision


class LogType:
    # Define constants for HSV filters and thresholds
    HSV_FILTERS = {
        'oak': HsvFilter(14, 155, 98, 20, 177, 255, 0, 0, 85, 0),
        'willow': HsvFilter(23, 149, 227, 41, 181, 255, 22, 0, 255, 0)
    }
    THRESHOLDS = {
        'oak': 0.50,
        'willow': 0.40
    }
    IMAGE_PATHS = {
        'oak': {
            'log': 'images/oak/oakLog.jpg',
            'tooltip': 'images/oak/oak_tooltip.jpg',
            'trunk': 'images/oak/newOakTrunk.jpg'
        },
        'willow': {
            'log': 'images/willow/willow_log.jpg',
            'tooltip': 'images/willow/willow_tooltip.jpg',
            'trunk': 'images/willow/willow_trunk.jpg'
        },
        'maple': {
            'log': 'images/maple/maple_log.jpg',
            'tooltip': 'images/maple/maple_tooltip.jpg',
            'trunk': 'images/maple/maple_trunk.jpg'
        },
        'yew': {
            'log': 'images/yew/yew_log.jpg',
            'tooltip': 'images/yew/yew_tooltip.jpg',
            'trunk': 'images/yew/yew_trunk.jpg'
        }
    }

    def __init__(self, type: str):
        if type not in self.HSV_FILTERS:
            raise ValueError(f"Unsupported log type: {type}")

        self.log_vision = Vision(self.IMAGE_PATHS[type]['log'])
        self.tooltip_vision = Vision(self.IMAGE_PATHS[type]['tooltip'])
        self.processed_trunk = Vision(self.IMAGE_PATHS[type]['trunk'])
        self.hsv_filter = self.HSV_FILTERS[type]
        self.trunk_threshold = self.THRESHOLDS[type]

    def get_log_vision(self):
        return self.log_vision

    def get_hsv_filter(self):
        return self.hsv_filter

    def get_tooltip_vision(self):
        return self.tooltip_vision

    def get_processed_trunk(self):
        return self.processed_trunk
