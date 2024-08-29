from copy import deepcopy
from math import radians

from pygame.math import Vector2

from .car import Car
from .linear_math import Transform, Rotation
from .track import Track


class CarInfo:
    def __init__(self, car_type: Car, track: Track):
        # angle of the first section
        starting_angle = (track.lines[1] - track.lines[0]).as_polar()[1]

        self.car_type = car_type
        self.position = Transform(Rotation.fromangle(radians(starting_angle)), deepcopy(track.lines[0]))
        self.velocity = Vector2()
        self.round = 0
        self.next_waypoint = 0
        self.track = track
        self.cpu = 0
        self.last_exception = None

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

        # Update next waypoint
        if (self.track.lines[self.next_waypoint] - self.position.p).length() < self.track.track_width:
            self.next_waypoint = self.next_waypoint + 1
            if self.next_waypoint >= len(self.track.lines):
                self.next_waypoint = 0
                self.round += 1
