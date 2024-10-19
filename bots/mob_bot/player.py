from vision import Vision
import os


class Player:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Define constants for HSV filters and thresholds
    IMAGE_PATHS = {
        'player': {
            'health': os.path.join(BASE_DIR, 'mobs', 'human', 'health_bar_template.jpg'),

        }

    }

    def __init__(self, type: str):
        if type not in self.IMAGE_PATHS:
            raise ValueError(f"Unsupported mob type: {type}")

        self.health_bar_template = self.IMAGE_PATHS[type]['health']
        self.health_vision = Vision(self.health_bar_template)

    def get_health_bar_template(self) -> str:
        return self.health_bar_template


    def get_health_vision(self):
        return self.health_vision
