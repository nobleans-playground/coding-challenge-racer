from copy import deepcopy
from math import radians

from pygame.math import Vector2

from .car import Car
from .linear_math import Transform, Rotation
from .track import Track


class CarPhysics:
    __slots__ = ('position', 'velocity')

    def __init__(self, position: Transform, velocity: Vector2):
        self.position = position
        self.velocity = velocity

    def update(self, dt: float, throttle: float, steering_command: float):
        # constants
        max_throttle = 100
        max_steering_speed = 3
        slipping_acceleration = 200
        slipping_ratio = 0.6

        acceleration = self.position.M * Vector2(throttle * max_throttle, 0)

        sideways_velocity = (self.velocity * self.position.M.cols[1]) * self.position.M.cols[1]
        if sideways_velocity.length_squared() > 0.001:
            # slow down the car in sideways direction
            acceleration -= sideways_velocity.normalize() * slipping_acceleration

        # rotate velocity partially
        self.velocity = Rotation.fromangle(
            steering_command * max_steering_speed * dt * (1 - slipping_ratio)) * self.velocity

        # integrate acceleration
        delta_velocity = acceleration * dt
        self.velocity += delta_velocity

        # integrate velocity
        self.position.p += self.velocity * dt
        self.position.M *= Rotation.fromangle(steering_command * max_steering_speed * dt)


class CarInfo:
    def __init__(self, car_type: Car, track: Track):
        # angle of the first section
        starting_vector = track.lines[1] - track.lines[0]
        starting_vector.normalize_ip()
        starting_rotation = Rotation(starting_vector[0], -starting_vector[1], starting_vector[1], starting_vector[0])

        self.car_type = car_type
        self.track = track
        self.car_physics = CarPhysics(Transform(starting_rotation, deepcopy(track.lines[0])),
                                      Vector2())
        self.round = 0
        self.next_waypoint = 0
        self.cpu = 0
        self.last_exception = None
        self.waypoint_timing = []

    @property
    def position(self) -> Transform:
        return self.car_physics.position

    @property
    def velocity(self) -> Vector2:
        return self.car_physics.velocity

    def reset(self):
        # angle of the first section
        starting_angle = (self.track.lines[1] - self.track.lines[0]).as_polar()[1]

        self.car_physics = CarPhysics(
            Transform(Rotation.fromangle(radians(starting_angle)), deepcopy(self.track.lines[0])),
            Vector2())
        self.round = 0
        self.next_waypoint = 0
        self.cpu = 0
        self.last_exception = None
        self.waypoint_timing = []

    def update(self, time: float, dt: float, throttle: float, steering_command: float):
        self.car_physics.update(dt, throttle, steering_command)

        # Update next waypoint
        if (self.track.lines[self.next_waypoint] - self.position.p).length() < self.track.track_width:
            self.next_waypoint = self.next_waypoint + 1
            if self.next_waypoint >= len(self.track.lines):
                self.next_waypoint = 0
                self.round += 1

            # Save the time it took to reach the waypoint
            self.waypoint_timing.append(time)
