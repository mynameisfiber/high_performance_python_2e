import timeit


def linear_search(needle, array):
    for i, item in enumerate(array):
        if item == needle:
            return i
    return -1


if __name__ == "__main__":
    setup = "from __main__ import (linear_search, haystack, needle)"
    iterations = 1000

    for haystack_size in (10000, 100000, 1000000):
        haystack = range(haystack_size)
        for needle in (1, 6000, 9000, 1000000):
            index = linear_search(needle, haystack)
            t = timeit.timeit(
                stmt="linear_search(needle, haystack)", setup=setup, number=iterations
            )
            print(
                f"Value {needle: <8} found in haystack of "
                f"size {len(haystack): <8} at index "
                f"{index: <8} in {t/iterations:.5e} seconds"
            )
