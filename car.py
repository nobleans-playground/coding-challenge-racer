# https://www.autoevolution.com/cars/nissan-skyline-gt-r-r32-1989.html#aeng_nissan-skyline-gt-r-r32-1989-26-tt-280-hp
import os

import pygame.image
from pygame import Vector2

name = 'Nissan Skyline GT-R R32'
image = pygame.image.load(os.path.splitext(__file__)[0] + '.png')
footprint = Vector2(4.544, 1.755)  # m
weight = 1650  # kg
power = 209  # kW
torque = 361  # Nm
acceleration = 5.91  # m/s^2
top_speed = 69.1667  # m/s

# TODO: Add more car parameters
braking = 2.0
cornering = 1.3
stability = 1.1
