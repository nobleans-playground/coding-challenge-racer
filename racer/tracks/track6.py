# Path: coding-challenge-racer/extract_svg_path
import os.path
from math import sin, cos

import numpy as np
import pygame

name = 'Circle'
background = pygame.image.load(os.path.dirname(__file__) + '/stars.webp')
scale = 1
track_width = 30

r = (1080 - 200) / 2
cx = r + 300
cy = 1080 - r - 100

lines = [(cx + r * cos(t), cy + r * sin(t)) for t in np.linspace(0, 2 * np.pi, 40)[:-1]]
