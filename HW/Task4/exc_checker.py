import sys


class AssertRaises(object):
    def __init__(self, exception_type):
        self.exception_type = exception_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError
            return
        elif issubclass(exc_type, self.exception_type):
            return True
        raise AssertionError


exec(sys.stdin.read())
