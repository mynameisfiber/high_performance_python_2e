import ctypes
import pickle
import time
from contextlib import contextmanager
from pprint import pprint

from tqdm import tqdm

from countmemaybe import HyperLogLog, KMinValues
from ll import LL
from llregister import LLRegister
from morriscounter import MorrisCounter
from scalingbloomfilter import ScalingBloomFilter
from superll import SuperLL

methods = [
    {"name": "LogLog", "obj": LL(16)},
    {"name": "SuperLogLog", "obj": SuperLL(16)},
    {"name": "Morris Counter", "obj": MorrisCounter()},
    {"name": "Log Log Register", "obj": LLRegister()},
    {"name": "HyperLogLog", "obj": HyperLogLog(b=16)},
    {"name": "KMinValues", "obj": KMinValues(k=1 << 16)},
    {"name": "ScalingBloom", "obj": ScalingBloomFilter(1048576)},
]


@contextmanager
def TimerBlock(name):
    start = time.time()
    t = ctypes.c_double()
    try:
        yield t
    finally:
        t.value = time.time() - start
        print(f"[{name}] took {t.value} seconds")


def wikireader(filename, buffering=1 << 10):
    total = 1148708949
    with open(filename, "r", buffering=buffering) as fd:
        for line in tqdm(fd, desc="Reading Wiki Data", total=total):
            yield line.strip()


if __name__ == "__main__":
    filename = "/data/datasets/internet/wikipedia/enwiki-20140404-pages-articles.tokens"
    print("baseline reading measurement")
    with TimerBlock("Iterate File") as baseline:
        tmp = 0
        for line in wikireader(filename):
            tmp += len(line)

    for method in methods:
        print((method["name"]))
        obj = method["obj"]
        with TimerBlock("Iterate File") as bench:
            for line in wikireader(filename):
                obj.add(line)
        method["time"] = bench.value - baseline.value
        method["estimate"] = obj.__len__()

    pprint(methods)
    pickle.dump(methods, open("_benchmark.pkl", "wb+"))
