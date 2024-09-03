from pygame import Color

from ..car import Car
from ..cars import car1


def test_car1():
    car = Car.from_module(car1, Color('red'))
    assert isinstance(car.name, str)
