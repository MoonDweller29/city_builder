"""Module contains functions of vector operations on tuples and other useful ones."""

import math
import operator


class Vec(tuple):
    def __add__(self, other):
        return Vec(map(operator.add, self, other))

    def __sub__(self, other):
        return Vec(map(operator.sub, self, other))

    def __mul__(self, other):
        return Vec(map(operator.mul, self, other))

    def __truediv__(self, other):
        return Vec(map(operator.truediv, self, other))

    def __div__(self, other):
        return Vec(map(operator.div, self, other))


def floor(x: Vec) -> Vec:
    """Calculate element-wise math.floor from tuple x.

    :param x: tuple of floats or objects with overloaded __floor__() method
    :return: tuple of floored elements of x
    """
    return Vec(tuple(map(math.floor, x)))


def to_int(a: Vec) -> Vec:
    """Cast tuple of 2 floats to tuple of 2 ints.

    :param a: tuple of 2 float elements
    :return: tuple of 2 int elements
    """
    return Vec((int(a[0]), int(a[1])))


def lerp(t: float, a: float, b: float) -> float:
    """Perform linear interpolation between floats a and b with coefficient t.

    :param t: float in range [0,1], t==0 => a, t==1 => b
    :param a: first value for linear interpolation
    :param b: second value for linear interpolation
    :return: interpolated value between a and b
    """
    if (t > 1):
        return b

    if (t < 0):
        return a

    return a + (b - a) * t


def ease_out_elastic(t: float) -> float:
    """Calculate Out Elastic easing from time t.

    :param t: time in range [0, 1]
    :return: calculated easing value
    """
    c4 = (2 * math.pi) / 3

    if t < 0:
        return 0

    if t > 1:
        return 1

    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1
