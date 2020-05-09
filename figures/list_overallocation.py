from itertools import islice

import pylab as py


# coding: utf-8
def overalloc_dict():
    o = list_overalloc()
    i = 1
    s, e, _ = next(o)
    while True:
        if i > e:
            s, e, _ = next(o)
        yield e - i
        i += 1


def list_overalloc():
    s = 1
    while True:
        e = alloc = s + overalloc(s)
        yield s, e, alloc
        s = e + 1


overalloc = lambda N: (N >> 3) + (3 if N < 9 else 6)

py.scatter(list(range(1, 10000)), list(islice(overalloc_dict(), 10000 - 1)))
py.ylim(0, 10000 - 1)
py.xlim(0, 10000 - 1)
py.ylim(0, 2000)
py.ylim(0, 1500)
py.ylim(0, 1400)
py.ylim(0, 1300)
py.xlabel("Size of the list")
py.ylabel("Number of elements overallocated")
py.title("Overallocation in lists")
py.savefig("../list_overallocation.png")
