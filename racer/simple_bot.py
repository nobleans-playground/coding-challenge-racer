from typing import Tuple

from pygame import Vector2

from .bot import Bot
from .linear_math import Transform


class SimpleBot(Bot):
    @property
    def name(self):
        return "SimpleBot"

    @property
    def contributor(self):
        return "Nobleo"

    def compute_commands(self, next_waypoint: int, position: Transform, velocity: Vector2) -> Tuple:
        target = self.track.lines[next_waypoint]
        # calculate the target in the frame of the robot
        target = position.inverse() * target
        # calculate the angle to the target
        angle = target.as_polar()[1]

        # calculate the throttle and steering
        if abs(angle) < 0.1:
            return 1, 0
        if angle > 0:
            return 0.1, 1
        else:
            return 0.1, -1
