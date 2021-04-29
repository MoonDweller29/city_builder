import pytest
from .Utils import add, sub, mul, div, lerp

def test_add():
    assert add((383, 122), (10, 2))  == (393, 124)
    assert add((100, 100), (-10, 0)) == (90, 100)
    assert add((-20, 0), (-10, 0))   == (-30, 0)

def test_sub():
    assert sub((383, 122), (10, 2))  == (373, 120)
    assert sub((100, 100), (-10, 0)) == (110, 100)
    assert sub((-20, 0), (-10, 0))   == (-10, 0)

def test_mul():
    assert mul((383, 122), (10, 2))  == (3830, 244)
    assert mul((100, 100), (-10, 0)) == (-1000, 0)
    assert mul((-20, 0), (-10, 0))   == (200, 0)

def test_div():
    assert div((383, 122), ( 10, 2)) == (38.3, 61)
    assert div((100, 100), (-10, 1)) == (-10, 100)
    assert div((-20, 0)  , (-10, 1)) == (2, 0)

def test_lerp():
    assert lerp(-2.3, 100, 123) == 100
    assert lerp(3.51, -12, -2) == -2
    assert lerp(0.5, 120, 140) == 130