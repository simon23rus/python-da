import sys
from functools import wraps


def takes(*args_dec):
    def real_decorator(fun):
        @wraps(fun)
        def wrapper(*args_fun):
            for i in range(min(len(args_dec), len(args_fun))):
                if not isinstance(args_fun[i], args_dec[i]):
                    raise TypeError
            fun(*args_fun)
        return wrapper
    return real_decorator


exec(sys.stdin.read())
