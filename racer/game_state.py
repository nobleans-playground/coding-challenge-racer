from copy import deepcopy
from time import time
from traceback import print_exception
from typing import Dict, List

from .bot import Bot
from .bots import all_bots
from .car import Car
from .car_info import CarInfo
from .cars import car1
from .constants import rounds
from .track import Track


def clamp(v: float, lo: float, hi: float):
    return max(lo, min(v, hi))


class GameState:
    def __init__(self, track: Track):
        self.track = track
        self.frames = 0  # type: int # Number of frames since the start of the game
        self.initialize_bots()

    def initialize_bots(self):
        # Deconstructs all cars and recreate them so any internal logic is correctly reset
        self.bots = {}  # type: Dict[Bot, CarInfo]
        for Bot in all_bots:
            bot = Bot(deepcopy(self.track))
            self.bots[bot] = CarInfo(Car.from_module(car1, bot.color), self.track)

    def reset(self):
        self.frames = 0
        self.initialize_bots()

    def update(self, dt: float):
        self.frames += 1
        for bot, car_info in self.bots.items():
            if car_info.round >= rounds:
                continue

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
                # Clamp inputs
                throttle = clamp(throttle, -1, 1)
                steering_command = clamp(steering_command, -1, 1)
            car_info.update(self.frames * dt, dt, throttle, steering_command)

    def get_bot_commands(self, bot, car_info):
        start = time()
        try:
            result = bot.compute_commands(car_info.next_waypoint, deepcopy(car_info.position),
                                          deepcopy(car_info.velocity))
        except Exception as e:
            result = e

        cpu = time() - start
        return result, cpu

    def ranked(self) -> List[Bot]:
        # Search for the car_info with the longest waypoint_timing
        bots = list(self.bots.keys())

        def bot_distance(bot):
            info = self.bots[bot]
            return info.round, info.next_waypoint, -info.waypoint_timing[-1] if info.waypoint_timing else 0

        bots.sort(key=bot_distance, reverse=True)
        return bots
