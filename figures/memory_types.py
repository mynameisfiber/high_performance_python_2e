"""
Data resources:
    - Main Resources:
        - http://www.tomshardware.com/charts/hdd-charts-2013/
        - http://www.tomshardware.com/charts/ssd-charts-2013/benchmarks,129.html
        - http://en.wikipedia.org/wiki/List_of_device_bit_rates
    
    - Also important
        - http://en.wikipedia.org/wiki/Intel_QuickPath_Interconnect
        - http://en.wikipedia.org/wiki/DDR3_SDRAM
        - http://en.wikipedia.org/wiki/Hard_disk_drive
        - http://www.storagereview.com/samsung_ssd_840_review_tlc
        - http://en.wikipedia.org/wiki/Solid-state_drive
"""

import csv
from collections import defaultdict

import numpy as np
import pylab as py


def plot_field(names, type, data):
    N = len(names)
    ind = np.arange(N)
    width = 0.35

    ax = py.gca()
    bar = ax.bar(ind, data["avg"], width, color="r", yerr=data["extend"])
    ax.set_ylabel("%s (%s)" % (type, data["unit"]))
    ax.set_xticks(ind + width)
    ax.set_xticklabels([x.replace(" ", "\n") for x in names], rotation=45, ha="right")
    ax.set_yscale("log")
    return bar


if __name__ == "__main__":
    data = list(csv.DictReader(open("memory_types_data.csv")))

    names = [line["type"] for line in data]
    values = defaultdict(dict)
    for field in data[0].keys():
        if field == "type":
            continue
        f, unit = field.strip().split(" ")
        t, name = f.strip().split("_", 1)
        values[name]["unit"] = unit.strip("()")
        values[name][t] = np.asarray([float(line[field]) for line in data])

    for field in values.keys():
        values[field]["avg"] = (values[field]["min"] + values[field]["max"]) / 2.0
        values[field]["extend"] = values[field]["max"] - values[field]["avg"]

    for i, f in enumerate(values.keys()):
        py.subplot(2, 2, i + 1)
        plot_field(names, f, values[f])

    py.suptitle("Characteristics of various memory units")
    py.savefig("../memory_types.png")
