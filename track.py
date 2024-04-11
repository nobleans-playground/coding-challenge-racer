from pygame.math import Vector2


class Track:
    def __init__(self, module):
        self.name = module.name
        self.background = module.background
        self.resolution = module.resolution
        self.lines = [Vector2(l) for l in module.lines]

    @property
    def size(self):
        """Track size (x, y) in meters"""
        return Vector2(self.background.get_size()) * self.resolution

    def __repr__(self):
        return f"Track({self.name!r}, {self.resolution!r}, {self.background!r})"
