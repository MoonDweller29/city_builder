from .Utils import Vec, lerp


def test_add():
    assert Vec((383, 122)) + Vec((10, 2))  == (393, 124)
    assert Vec((100, 100)) + Vec((-10, 0)) == (90, 100)
    assert Vec((-20, 0))   + Vec((-10, 0)) == (-30, 0)


def test_sub():
    assert Vec((383, 122)) - Vec((10, 2))  == (373, 120)
    assert Vec((100, 100)) - Vec((-10, 0)) == (110, 100)
    assert Vec((-20, 0))   - Vec((-10, 0)) == (-10, 0)


def test_mul():
    assert Vec((383, 122)) * Vec((10, 2))  == (3830, 244)
    assert Vec((100, 100)) * Vec((-10, 0)) == (-1000, 0)
    assert Vec((-20, 0))   * Vec((-10, 0)) == (200, 0)


def test_div():
    assert Vec((383, 122)) / Vec(( 10, 2)) == (38.3, 61)
    assert Vec((100, 100)) / Vec((-10, 1)) == (-10, 100)
    assert Vec((-20, 0))   / Vec((-10, 1)) == (2, 0)


def test_lerp():
    assert lerp(-2.3, 100, 123) == 100
    assert lerp(3.51, -12, -2)  == -2
    assert lerp(0.5, 120, 140)  == 130
