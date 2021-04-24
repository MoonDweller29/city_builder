import operator

# Vector operations on tuples

def add(a, b):
    return tuple(map(operator.add, a, b))

def sub(a, b):
    return tuple(map(operator.sub, a, b))
