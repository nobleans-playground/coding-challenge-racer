import math
from math import cos, sin

from pygame.math import Vector2


class Rotation:
    """2x2 rotation matrix"""

    def __init__(self, angle):
        self.rows = ((cos(angle), -sin(angle)), (sin(angle), cos(angle)))

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.rows[item[0]][item[1]]
        # elif isinstance(item, int):
        #     return self.rows[item]
        else:
            raise IndexError('Invalid index type')

    @property
    def angle(self):
        return math.atan2(self.rows[1][0], self.rows[0][0])

    def __mul__(self, other: Vector2):
        x = self.rows[0] * other
        y = self.rows[1] * other
        return Vector2(x, y)

    def __repr__(self):
        return f"Matrix2x2({self.rows})"


class Transform:
    """Rigid 2d transforms with only translation and rotation"""

    def __init__(self, M: Rotation, p: Vector2):
        self.M = M
        self.p = p
