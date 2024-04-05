import math
from math import cos, sin

import pytest


class Vector:
    """A 2d vector"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise IndexError()

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


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

    def __mul__(self, other: Vector):
        x = self.rows[0][0] * other.x + self.rows[0][1] * other.y
        y = self.rows[1][0] * other.x + self.rows[1][1] * other.y
        return Vector(x, y)

    def __repr__(self):
        return f"Matrix2x2({self.rows})"


class Transform:
    """Rigid 2d transforms with only translation and rotation"""

    def __init__(self, M: Rotation, p: Vector):
        self.M = M
        self.p = p


def test_vector_add():
    a = Vector(1, 2)
    b = Vector(3, 4)
    c = a + b
    assert c.x == 4
    assert c.y == 6
    assert c == Vector(4, 6)
    assert c != Vector(9, 9)


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
    a = Vector(1, 2)
    b = m * a
    assert b == Vector(1, 2)


def test_matrix2x2_rotate_90():
    m = Rotation(math.pi / 2)
    a = Vector(1, 2)
    b = m * a
    assert b[0] == pytest.approx(-2)
    assert b[1] == pytest.approx(1)
