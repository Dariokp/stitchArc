"""
A file containing implementations for the transformed python functions.
"""

def curry(func):
    def curried(*args):
        # print(f'{args}')
        if len(args) == func.__code__.co_argcount:
            return func(*args)
        else:
            return lambda x: curried(*(args + (x,)))
    return curried

@curry
def __bitOr__(a, b):
    """Implements bitwise OR operation"""
    return a | b

@curry
def __bitAnd__(a, b):
    """Implements bitwise AND operation"""
    return a & b

@curry
def __bitXor__(a, b):
    """Implements bitwise XOR operation"""
    return a ^ b

@curry
def __lshift__(a, b):
    """Implements left shift operation"""
    return a << b

@curry
def __rshift__(a, b):
    """Implements right shift operation"""
    return a >> b

@curry
def __bitNot__(a):
    """Implements bitwise NOT operation"""
    return ~a