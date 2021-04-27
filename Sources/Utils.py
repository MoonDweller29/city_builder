import operator
import math

# Vector operations on tuples

def add(a, b):
    return tuple(map(operator.add, a, b))

def sub(a, b):
    return tuple(map(operator.sub, a, b))

def mul(a, b):
    return tuple(map(operator.mul, a, b))

def div(a, b):
    return tuple(map(operator.truediv, a, b))

def floor(a, b):
    return tuple(map(floor, a, b))

def toInt(a):
    return (int(a[0]), int(a[1]))

def Lerp(t, a, b):
    return a + (b - a) * t

def ease_out_elastic(x):
    c4 = (2 * math.pi) / 3

    if x < 0:
        return 0

    if x > 1:
        return 1

    return pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1