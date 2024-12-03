# Path: coding-challenge-racer/extract_svg_path
import os.path

import pygame

name = 'Square'
background = pygame.image.load(os.path.dirname(__file__) + '/stars.webp')
scale = 1
track_width = 30
lines = [
    (200, 880),
    (880, 880),
    (880, 200),
    (200, 200),
]
