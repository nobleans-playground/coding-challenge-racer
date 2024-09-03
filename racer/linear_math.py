from __future__ import annotations

import math
from math import cos, sin
from typing import Union

from pygame.math import Vector2


class Rotation:
    """2x2 rotation matrix"""

    __slots__ = ('rows',)

    def __init__(self, xx, xy, yx, yy):
        self.rows = (Vector2(xx, xy), Vector2(yx, yy))

    @classmethod
    def fromangle(self, angle):
        return Rotation(cos(angle), -sin(angle), sin(angle), cos(angle))

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.rows[item[0]][item[1]]
        # elif isinstance(item, int):
        #     return self.rows[item]
        else:
            raise IndexError('Invalid index type')

    @property
    def cols(self):
        return (Vector2(self.rows[0].x, self.rows[1].x), Vector2(self.rows[0].y, self.rows[1].y))

    @property
    def angle(self):
        return math.atan2(self.rows[1][0], self.rows[0][0])

    def transpose(self):
        return Rotation(self.rows[0].x, self.rows[1].x, self.rows[0].y, self.rows[1].y)

    def __mul__(self, other: Union[Rotation, Vector2]):
        if isinstance(other, Rotation):
            xx = self.rows[0].dot(Vector2(other.rows[0].x, other.rows[1].x))
            xy = self.rows[0].dot(Vector2(other.rows[0].y, other.rows[1].y))
            yx = self.rows[1].dot(Vector2(other.rows[0].x, other.rows[1].x))
            yy = self.rows[1].dot(Vector2(other.rows[0].y, other.rows[1].y))
            return Rotation(xx, xy, yx, yy)
        elif isinstance(other, Vector2):
            x = self.rows[0] * other
            y = self.rows[1] * other
            return Vector2(x, y)
        else:
            raise TypeError(f'other should be {self.__mul__.__annotations__["other"]} not {type(other)}')

    def __repr__(self):
        return f"Matrix2x2({self.rows[0].x}, {self.rows[0].y}, {self.rows[1].x}, {self.rows[1].y})"


class Transform:
    """Rigid 2d transforms with only translation and rotation"""

    __slots__ = ('M', 'p')

    def __init__(self, M: Rotation = None, p: Vector2 = None):
        self.M = M if M is not None else Rotation.fromangle(0)
        self.p = p if p is not None else Vector2()

    def inverse(self):
        M = self.M.transpose()
        return Transform(M, M * -self.p)

    def __mul__(self, other: Union[Transform, Vector2]):
        if isinstance(other, Transform):
            return Transform(self.M * other.M, self * other.p)
        elif isinstance(other, Vector2):
            return self.M * other + self.p
        else:
            raise TypeError(f'other should be {self.__mul__.__annotations__["other"]} not {type(other)}')

    def __repr__(self):
        return f"Transform(M={self.M}, p={self.p})"
