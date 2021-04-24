import operator

# Vector operations on tuples

def add(a, b):
    return tuple(map(operator.add, a, b))

def sub(a, b):
    return tuple(map(operator.sub, a, b))

def mul(a, b):
    return tuple(map(operator.mul, a, b))

def truediv(a, b):
    return tuple(map(operator.truediv, a, b))

