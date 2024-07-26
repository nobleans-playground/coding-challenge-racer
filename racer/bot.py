from abc import ABC, abstractmethod
from typing import Tuple


class Bot(ABC):
    """
    To implement a Bot, you'll have to inherit from this class and implement all abstract methods
    """

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
    def compute_commands(self) -> Tuple:
        """
        Returns: Throttle % [-1, 1], Steering % [-1, 1]
        """
        pass
