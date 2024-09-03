from copy import deepcopy

from ..car import Car
from ..cars import car1


def test_car1():
    car = Car(car1)
    deepcopy(car)
