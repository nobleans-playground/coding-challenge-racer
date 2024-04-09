import math
from math import cos, sin

import pytest
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
        x = self.rows[0][0] * other.x + self.rows[0][1] * other.y
        y = self.rows[1][0] * other.x + self.rows[1][1] * other.y
        return Vector2(x, y)

    def __repr__(self):
        return f"Matrix2x2({self.rows})"


class Transform:
    """Rigid 2d transforms with only translation and rotation"""

    def __init__(self, M: Rotation, p: Vector2):
        self.M = M
        self.p = p


def test_vector_add():
    a = Vector2(1, 2)
    b = Vector2(3, 4)
    c = a + b
    assert c.x == 4
    assert c.y == 6
    assert c == Vector2(4, 6)
    assert c != Vector2(9, 9)


def test_matrix2x2_angle():
    m = Rotation(0)
    assert m[0, 0] == 1
    assert m[0, 1] == 0
    assert m[1, 0] == 0
    assert m[1, 1] == 1
    assert m.angle == 0

    m = Rotation(1)
    assert m.angle == 1


def test_matrix2x2_rotate():
    m = Rotation(0)
    a = Vector2(1, 2)
    b = m * a
    assert b == Vector2(1, 2)


def test_matrix2x2_rotate_90():
    m = Rotation(math.pi / 2)
    a = Vector2(1, 2)
    b = m * a
    assert b[0] == pytest.approx(-2)
    assert b[1] == pytest.approx(1)
