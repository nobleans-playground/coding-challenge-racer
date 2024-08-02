from argparse import Namespace
from copy import deepcopy

from pygame.math import Vector2
from pygame.surface import Surface


class Track:
    def __init__(self, module):
        self.name: str = module.name
        self.background: Surface = module.background
        self.track_width: float = module.track_width
        self.lines = [Vector2(line) for line in module.lines]

    def __deepcopy__(self, memo):
        return Track(Namespace(name=deepcopy(self.name),
                               background=self.background.copy(),
                               track_width=deepcopy(self.track_width),
                               lines=deepcopy(self.lines)))

    def __repr__(self):
        return f"Track({self.name!r}, {self.background!r}, {self.track_width!r})"
