from ..car_info import CarPhysics, CarInfo
from ..constants import framerate
from ..linear_math import Transform, Vector2
from ..track import Track
from ..tracks import track1


def test_car_physics_update(benchmark):
    car = CarPhysics(Transform(), Vector2())
    benchmark(car.update, 1 / framerate, 1.0, 1.0)


def test_car_info_init(benchmark):
    benchmark(CarInfo, None, Track(track1))
