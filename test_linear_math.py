from math import pi

import pytest

from linear_math import Vector2, Rotation


def test_vector_add():
    a = Vector2(1, 2)
    b = Vector2(3, 4)
    c = a + b
    assert c.x == 4
    assert c.y == 6
    assert c == Vector2(4, 6)
    assert c != Vector2(9, 9)


def test_matrix2x2_angle():
    m = Rotation.fromangle(0)
    assert m[0, 0] == 1
    assert m[0, 1] == 0
    assert m[1, 0] == 0
    assert m[1, 1] == 1
    assert m.angle == 0

    m = Rotation.fromangle(1)
    assert m.angle == 1


def test_matrix2x2_rotate():
    m = Rotation.fromangle(0)
    a = Vector2(1, 2)
    b = m * a
    assert b == Vector2(1, 2)


def test_matrix2x2_rotate_90():
    m = Rotation.fromangle(pi / 2)
    a = Vector2(1, 2)
    b = m * a
    assert b[0] == pytest.approx(-2)
    assert b[1] == pytest.approx(1)


def test_matrix2x2_transpose():
    m = Rotation(0, -1, 1, 0)
    mt = m.transpose()
    assert mt[0, 0] == 0
    assert mt[0, 1] == 1
    assert mt[1, 0] == -1
    assert mt[1, 1] == 0

def test_transform_mul():
    m = Rotation.fromangle(0)
    t = Vector2(1, 2)
    tr = m * t
    assert tr == Vector2(1, 2)