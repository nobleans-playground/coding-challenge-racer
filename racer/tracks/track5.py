# Path: coding-challenge-racer/extract_svg_path
import os.path

import pygame

name = 'Rectangle'
background = pygame.image.load(os.path.dirname(__file__) + '/stars.webp')
scale = 1
track_width = 30

(w, h) = background.get_size()

lines = [
    (200, 880),
    (w - 200, 880),
    (w - 200, 680),
    (200, 680),
]
