import pygame
from pygame import Color
from pygame.surface import Surface


class Car:
    def __init__(self, name: str, image: Surface, scale: float, color: Color):
        self.name = name
        self.image: Surface = image.copy()
        self.scale = scale

        color_image = pygame.Surface(self.image.get_size())
        color_image.fill(color)
        self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_MULT)

    @staticmethod
    def from_module(module, color: Color):
        return Car(module.name, module.image, module.scale, color)

    def __repr__(self):
        return 'f"Car({self.name!r}, {self.image!r}, {self.scale!r})'
