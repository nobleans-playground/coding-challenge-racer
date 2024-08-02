from copy import deepcopy

import racer.car1 as car1
import racer.track1 as track1

from .bots import all_bots
from .car_info import CarInfo
from .track import Track


class GameState:
    def __init__(self):
        self.track = Track(track1)
        self.bots = {}
        for Bot in all_bots:
            self.bots[Bot(deepcopy(self.track))] = CarInfo(car1, self.track)

    def update(self, dt: float):
        for bot, car_info in self.bots.items():
            result = bot.compute_commands(car_info.next_waypoint, deepcopy(car_info.position),
                                          deepcopy(car_info.velocity))
            if type(result) is tuple:
                throttle, steering_command = result
            else:
                print(f"Bot {bot.name} returned {type(result)} instead of a Tuple")
                throttle, steering_command = 0, 0
            car_info.update(dt, throttle, steering_command)
