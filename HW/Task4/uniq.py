import sys


def unique(iterable):
    iterator = iter(iterable)
    cur_elem = None
    next_elem = None
    try:
        cur_elem = next(iterator)
        next_elem = next(iterator)
    except (StopIteration, ValueError):
        if cur_elem is not None:
            yield cur_elem
        return
    while True:
        try:
            while cur_elem == next_elem:
                cur_elem = next_elem
                next_elem = next(iterator)
            yield cur_elem
            cur_elem = next_elem

        except (StopIteration, ValueError):
            yield next_elem
            break


exec(sys.stdin.read())
