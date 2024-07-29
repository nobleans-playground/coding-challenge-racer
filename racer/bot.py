from abc import ABC, abstractmethod
from hashlib import sha1
from typing import Tuple

from pygame import Vector2, Color

from .linear_math import Transform


class Bot(ABC):
    """
    To implement a Bot, you'll have to inherit from this class and implement all abstract methods
    """

    def __init__(self, track):
        self.track = track

    @property
    @abstractmethod
    def name(self):
        """
        The name you want to give your snake
        """
        pass

    @property
    @abstractmethod
    def contributor(self):
        """
        Your own name
        """
        pass

    @property
    def color(self) -> Color:
        # hash self.name with sha1
        h = sha1(self.name.encode()).hexdigest()
        r = int(h[:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return Color(r, g, b)

    @abstractmethod
    def compute_commands(self, next_waypoint: int, position: Transform, velocity: Vector2) -> Tuple:
        """
        Returns: Throttle % [-1, 1], Steering % [-1, 1]
        """
        pass

    def draw(self, map_scaled, zoom):
        pass
