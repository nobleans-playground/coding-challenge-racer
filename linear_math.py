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


class Matrix2x2:
    """2x2 rotation matrix"""

    def __init__(self, angle):
        self.rows = ((cos(angle), -sin(angle)), (sin(angle), cos(angle)))

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

    def __init__(self, basis: Matrix2x2, origin: Vector):
        self.basis = basis
        self.origin = origin


def test_vector_add():
    a = Vector(1, 2)
    b = Vector(3, 4)
    c = a + b
    assert c == Vector(4, 6)
    assert c != Vector(9, 9)


def test_matrix2x2_angle():
    m = Matrix2x2(0)
    assert m.angle == 0
    m = Matrix2x2(1)
    assert m.angle == 1


def test_matrix2x2_rotate():
    m = Matrix2x2(0)
    a = Vector(1, 2)
    b = m * a
    assert b == Vector(1, 2)


def test_matrix2x2_rotate_90():
    m = Matrix2x2(math.pi / 2)
    a = Vector(1, 2)
    b = m * a
    assert b[0] == pytest.approx(-2)
    assert b[1] == pytest.approx(1)
