from hsvfilter import HsvFilter
from vision import Vision
import os


class FoodType:
    # Define constants for what's needed
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    THRESHOLDS = {
        'shark': 0.90,
        'shrimp': 0.90
    }
    IMAGE_PATHS = {
        'shark': {
            'food_icon': os.path.join(BASE_DIR, 'food', 'shark', 'shark_icon.jpg'),
            'tooltip': os.path.join(BASE_DIR, 'food', 'shark', 'shark_tooltip.jpg'),
        },
        'shrimp': {
            'food_icon': '',
            'tooltip': '',
        },
        'beef': {
            'food_icon': os.path.join(BASE_DIR, 'food', 'beef', 'beef_icon.jpg'),
            'tooltip': os.path.join(BASE_DIR, 'food', 'beef', 'beef_tooltip.jpg'),
        }
    }

    def __init__(self, type: str):
        if type not in self.IMAGE_PATHS:
            raise ValueError(f"Unsupported food type: {type}")

        self.food_vision = Vision(self.IMAGE_PATHS[type]['food_icon'])
        self.tooltip_vision = Vision(self.IMAGE_PATHS[type]['tooltip'])


    def get_food_vision(self):
        return self.food_vision

    def get_tooltip_vision(self):
        return self.tooltip_vision

