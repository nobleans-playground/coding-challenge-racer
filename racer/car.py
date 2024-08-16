from argparse import Namespace
from copy import deepcopy

from pygame.surface import Surface


class Car:
    def __init__(self, module):
        self.name: str = module.name
        self.image: Surface = module.image
        self.scale: float = module.scale

    def __deepcopy__(self, memo):
        return self.__class__(Namespace(name=deepcopy(self.name),
                                        image=self.image.copy(),
                                        scale=deepcopy(self.scale)))

    def __repr__(self):
        return 'f"Car({self.name!r}, {self.image!r}, {self.scale!r})'
