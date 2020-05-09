#!/usr/bin/env python

import string
from itertools import cycle
from random import sample

import numpy as np
import pylab as py
from hyperloglog import HyperLogLog
from kminvalues import KMinValues
from llregister import LLRegister
from morriscounter import MorrisCounter
# from ll import LL
# from superll import SuperLL
from scalingbloomfilter import ScalingBloomFilter


def generate_keys(num_keys, num_letters):
    for i in range(num_keys):
        yield "".join(sample(string.ascii_lowercase, num_letters))


methods = [
    {"name": "Exact Solution", "init": set},
    {"name": "Morris Counter", "init": MorrisCounter},
    {"name": "Log Log Register", "init": LLRegister},
    # {
    # "name" : "LogLog",
    # "init" : lambda : LL(4),
    # },
    # {
    # "name" : "SuperLogLog",
    # "init" : lambda : SuperLL(4),
    # },
    {"name": "HyperLogLog", "init": lambda: HyperLogLog(4)},
    {"name": "KMinValues", "init": lambda: KMinValues(2 << 4)},
    {"name": "ScalingBloom", "init": lambda: ScalingBloomFilter(2048)},
]


def run_experiment(exp_name, filename, key_generator, data, sample_freq=3000):
    for item in data:
        item["_tmp"] = item["init"]()
        item[exp_name] = []

    for i, key in enumerate(key_generator):
        for item in data:
            item["_tmp"].add(str(key))
            if i % sample_freq == 0:
                item[exp_name].append((i, len(item["_tmp"])))

    print("%s summary:" % exp_name)
    for item in data:
        print("\t%-24s: %d" % (item["name"], len(item["_tmp"])))
        item.pop("_tmp")

    py.figure()
    plot_experiment(exp_name, data, filename)


def plot_experiment(exp_name, data, filename):
    markers = cycle("h*o>Dxsp8")
    py.title(exp_name)
    ymax = []
    for item in data:
        ext_args = {}
        name = item["name"]
        data_ndarray = np.asarray(item[exp_name])
        ymax.append(data_ndarray[-1][1])
        if name == "Exact Solution":
            ext_args = {"linewidth": 6}
        py.plot(
            data_ndarray[:, 0],
            data_ndarray[:, 1],
            label=name,
            marker=next(markers),
            alpha=0.6,
            markersize=8,
            **ext_args
        )
    py.legend(loc="best", fontsize="medium")
    py.xlabel("Number of non-unique items added")
    py.ylabel("Prediction of number of unique items")

    ymax.sort()
    py.ylim(ymax=ymax[-2] * 1.1)
    py.savefig("../../images/prob_ds_%s.png" % filename)

    # actual_data = np.asarray(data[0][exp_name], dtype=np.float)
    # for item in data[1:]:
    # name = item["name"]
    # data_ndarray = np.asarray(item[exp_name], dtype=np.float)
    # py.figure()
    # py.plot(data_ndarray[1:,0], (1 - data_ndarray[:,1]/actual_data[:,1])[1:])

    # py.xlabel("Items added")
    # py.ylabel("Relative Error %")
    # py.title("Relative error of %s for %s" % (name, exp_name))
    # py.savefig("../prod_ds_%s_%s.png" % (filename, name.replace(" ","_")))


if __name__ == "__main__":
    run_experiment("Inserting Unique Items", "unique", range(100000), methods)
    run_experiment(
        "Inserting Items with Duplicates", "dup", generate_keys(60000, 3), methods
    )
