import timeit


def search_fast(haystack, needle):
    for item in haystack:
        if item == needle:
            return True
    return False


def search_slow(haystack, needle):
    return_value = False
    for item in haystack:
        if item == needle:
            return_value = True
    return return_value


def search_unknown1(haystack, needle):
    return any((item == needle for item in haystack))


def search_unknown2(haystack, needle):
    return any([item == needle for item in haystack])


if __name__ == "__main__":
    iterations = 10000
    haystack = list(range(1000))
    setup = "from __main__ import (haystack, needle, search_fast, search_slow)"

    needle = 5
    print(
        f"Testing search speed with {len(haystack)} items and needle close to the head of the list"
    )

    t = timeit.timeit(
        stmt="search_fast(haystack, needle)", setup=setup, number=iterations
    )
    print(f"search_fast time: {t/iterations:.5e}")

    t = timeit.timeit(
        stmt="search_slow(haystack, needle)", setup=setup, number=iterations
    )
    print(f"search_slow time: {t/iterations:.5e}")

    needle = len(haystack) - 10
    print(
        f"Testing search speed with {len(haystack)} items and needle close to the tail of the list"
    )

    t = timeit.timeit(
        stmt="search_fast(haystack, needle)", setup=setup, number=iterations
    )
    print(f"search_fast time: {t/iterations:.5e}")

    t = timeit.timeit(
        stmt="search_slow(haystack, needle)", setup=setup, number=iterations
    )
    print(f"search_slow time: {t/iterations:.5e}")
