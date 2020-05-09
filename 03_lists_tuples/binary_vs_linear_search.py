import timeit

from binary_search import binary_search
from linear_search import linear_search


def time_and_log(function, needle, haystack):
    index = function(needle, haystack)
    t = timeit.timeit(
        stmt=f"{function.__name__}(needle, haystack)", setup=setup, number=iterations
    )
    print(
        f"[{function.__name__}] Value {needle: <8} found in haystack of "
        f"size {len(haystack): <8} at index "
        f"{index: <8} in {t/iterations:.5e} seconds"
    )


if __name__ == "__main__":
    setup = "from __main__ import " "(binary_search, linear_search, haystack, needle)"
    iterations = 1000

    for haystack_size in (10000, 100000, 1000000):
        haystack = range(haystack_size)
        for needle in (1, 6000, 9000, 1000000):
            time_and_log(linear_search, needle, haystack)
            time_and_log(binary_search, needle, haystack)
