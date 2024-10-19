from vision import Vision
import os


class MobType:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Define constants for HSV filters and thresholds
    MOB_PATHS = {
        'cow': {
            'cascade': os.path.join(BASE_DIR, 'mobs', 'cow', 'cow.xml'),
            'tooltip': os.path.join(BASE_DIR, 'mobs', 'cow', 'cow_tooltip.jpg'),
            'death_tooltip': os.path.join(BASE_DIR, 'mobs', 'cow', 'cow_death_tooltip.jpg'),
        },
        'chicken': {
            'cascade': os.path.join(BASE_DIR, 'mobs', 'chicken', 'chicken.xml'),
            'tooltip': os.path.join(BASE_DIR, 'mobs', 'chicken', 'chicken_tooltip.jpg'),
            'death_tooltip': os.path.join(BASE_DIR, 'mobs', 'chicken', 'chicken_death2.jpg'),
        }
    }

    def __init__(self, type: str):
        if type not in self.MOB_PATHS:
            raise ValueError(f"Unsupported mob type: {type}")

        self.cascade_path = self.MOB_PATHS[type]['cascade']
        self.tooltip_vision = Vision(self.MOB_PATHS[type]['tooltip'])
        self.death_vision = Vision(self.MOB_PATHS[type]['death_tooltip'])

    def get_cascade_path(self):
        return self.cascade_path

    def get_tooltip_vision(self):
        return self.tooltip_vision

    def get_death_tooltip(self):
        return self.death_vision
