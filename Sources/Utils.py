import operator

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

def int(a, b):
    return tuple(map(int, a, b))
