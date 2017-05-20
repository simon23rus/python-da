from copy import copy
from functools import wraps
import sys


class TopGenerator(object):

    def __init__(self, gen, argv, kwargv):
        self.gen = gen
        self.argv, self.kwargv = copy(argv), copy(kwargv)
        self.local_copy = iter(self)

    def __iter__(self):
        return self.gen(*self.argv, **self.kwargv)

    def __next__(self):
        return next(self.local_copy)


def inexhaustible(generator):
    @wraps(generator)
    def gen(*argv, **kwargv):
        return TopGenerator(generator, argv, kwargv)
    return gen


exec(sys.stdin.read())
