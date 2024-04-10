from math import pi

import pytest

from .linear_math import Rotation
from .linear_math import Vector2


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
    m = Rotation(pi / 2)
    a = Vector2(1, 2)
    b = m * a
    assert b[0] == pytest.approx(-2)
    assert b[1] == pytest.approx(1)
