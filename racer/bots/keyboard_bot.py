from typing import Tuple

from pygame import Vector2, key, K_LEFT, K_RIGHT, K_UP, K_DOWN, Color

from ..bot import Bot
from ..linear_math import Transform


class KeyboardBot(Bot):
    @property
    def name(self):
        return "Player 1"

    @property
    def contributor(self):
        return "Nobleo"

    @property
    def color(self) -> Color:
        return Color('#3e59f8')

    def compute_commands(self, next_waypoint: int, position: Transform, velocity: Vector2) -> Tuple:
        keys = key.get_pressed()
        throttle = 0
        steering_command = 0
        if keys[K_LEFT]:
            steering_command = -1
        if keys[K_RIGHT]:
            steering_command = 1
        if keys[K_UP]:
            throttle = 1
        if keys[K_DOWN]:
            throttle = -1

        return throttle, steering_command
