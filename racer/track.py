from copy import deepcopy

import pygame
from pygame.math import Vector2
from pygame.surface import Surface


class Track:
    def __init__(self, module=None):
        if module is None:
            return
        size = module.background.get_size()
        self.name: str = module.name
        self.background: Surface = pygame.transform.scale(module.background,
                                                          (size[0] * module.scale, size[1] * module.scale))
        self.track_width: float = module.scale * module.track_width
        self.lines = [Vector2(line) * module.scale for line in module.lines]

    def __deepcopy__(self, memo):
        track = self.__class__()
        track.name = deepcopy(self.name, memo)
        track.background = self.background.copy()
        track.track_width = deepcopy(self.track_width, memo)
        track.lines = deepcopy(self.lines, memo)
        return track

    def __repr__(self):
        return f"Track({self.name!r}, {self.background!r}, {self.track_width!r})"
