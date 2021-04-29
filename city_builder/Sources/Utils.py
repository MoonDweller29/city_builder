import math
import operator
from typing import Tuple


# Vector operations on tuples

def add(a: Tuple, b: Tuple) -> Tuple:
    """Calculate element-wise sum of tuples of equal size.

    :param a: tuple of size N which contains objects with overloaded operator.__add__
    :param b: tuple of size N which contains objects with overloaded operator.__add__
    :return: tuple of size N with element-wise sum of tuples a and b
    """
    return tuple(map(operator.add, a, b))


def sub(a: Tuple, b: Tuple) -> Tuple:
    """Calculate element-wise subtraction of tuple b from tuple a.

    :param a: tuple of size N which contains objects with overloaded operator.__sub__
    :param b: tuple of size N which contains objects with overloaded operator.__sub__
    :return: tuple of size N with element-wise subtraction of tuple b from tuple a
    """
    return tuple(map(operator.sub, a, b))


def mul(a: Tuple, b: Tuple) -> Tuple:
    """Calculate element-wise multiplication of tuples of equal size.

    :param a: tuple of size N which contains objects with overloaded operator.__mul__
    :param b: tuple of size N which contains objects with overloaded operator.__mul__
    :return: tuple of size N with element-wise multiplication of tuples a and b
    """
    return tuple(map(operator.mul, a, b))


def div(a: Tuple, b: Tuple) -> Tuple:
    """Calculate element-wise division of tuple a by tuple b.

    :param a: tuple of size N which contains objects with overloaded operator.__div__
    :param b: tuple of size N which contains objects with overloaded operator.__div__
    :return: tuple of size N with element-wise division of tuple a by tuple b
    """
    return tuple(map(operator.truediv, a, b))


def floor(x: Tuple) -> Tuple:
    """Calculate element-wise math.floor from tuple x.

    :param x: tuple of floats or objects with overloaded __floor__() method
    :return: tuple of floored elements of x
    """
    return tuple(map(math.floor, x))


def to_int(a: Tuple[float, float]) -> Tuple[int, int]:
    """Cast tuple of 2 floats to tuple of 2 ints.

    :param a: tuple of 2 float elements
    :return: tuple of 2 int elements
    """
    return (int(a[0]), int(a[1]))


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
