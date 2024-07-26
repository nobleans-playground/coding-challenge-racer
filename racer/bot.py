from abc import ABC, abstractmethod
from typing import Tuple

from pygame import Vector2

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

    @abstractmethod
    def compute_commands(self, next_waypoint: int, position: Transform, velocity: Vector2) -> Tuple:
        """
        Returns: Throttle % [-1, 1], Steering % [-1, 1]
        """
        pass
