from argparse import Namespace
from copy import deepcopy

from pygame.math import Vector2
from pygame.surface import Surface


class Track:
    def __init__(self, module):
        self.name: str = module.name
        self.background: Surface = module.background
        self.track_width: float = module.track_width
        self.lines = [Vector2(l) for l in module.lines]

    def __deepcopy__(self, memo):
        return Track(Namespace(name=deepcopy(self.name),
                               background=self.background.copy(),
                               track_width=deepcopy(self.track_width),
                               lines=deepcopy(self.lines)))

    def __repr__(self):
        return f"Track({self.name!r}, {self.background!r})"

# class Track:
#     def __init__(self, module):
#         self.name = module.name
#         self.background = module.background
#         self.resolution = module.resolution
#         self.width = module.width
#         self.lines = [Vector2(l) for l in module.lines]
#
#     @property
#     def size(self):
#         """Track size (x, y) in meters"""
#         return Vector2(self.background.get_size()) * self.resolution
#
#     def __repr__(self):
#         return f"Track({self.name!r}, {self.resolution!r}, {self.background!r})"
