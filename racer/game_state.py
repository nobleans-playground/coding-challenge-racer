from copy import deepcopy
from time import time
from traceback import print_exception
from typing import Dict

from .bots import all_bots
from .car_info import CarInfo
from .cars import car1
from .track import Track
from .tracks import track1


class GameState:
    def __init__(self):
        self.track = Track(track1)
        self.bots = {}  # type: Dict[Bot, CarInfo]
        for Bot in all_bots:
            self.bots[Bot(deepcopy(self.track))] = CarInfo(car1, self.track)

    def update(self, dt: float):
        for bot, car_info in self.bots.items():
            result, cpu = self.get_bot_commands(bot, car_info)

            car_info.cpu += cpu

            if isinstance(result, Exception):
                if type(car_info.last_exception) != type(result):
                    print(f'{bot.name} did not return an instance of Move, it returned an exception:')
                    print_exception(type(result), result, result.__traceback__)
                car_info.last_exception = result
                throttle, steering_command = 0, 0
            elif type(result) is not tuple:
                print(f'Bot {bot.name} returned {type(result)} instead of a Tuple')
                throttle, steering_command = 0, 0
            else:
                throttle, steering_command = result
            car_info.update(dt, throttle, steering_command)

    def get_bot_commands(self, bot, car_info):
        start = time()
        try:
            result = bot.compute_commands(car_info.next_waypoint, deepcopy(car_info.position),
                                          deepcopy(car_info.velocity))
        except Exception as e:
            result = e

        cpu = time() - start
        return result, cpu
