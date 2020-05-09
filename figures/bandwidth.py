import csv
from collections import defaultdict

import numpy as np
import pylab as py


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            "{}".format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )


if __name__ == "__main__":
    data = list(csv.DictReader(open("bandwidth.csv")))

    N = len(data)
    ind = np.arange(N)
    width = 0.35

    ax = py.gca()
    bar = ax.bar(ind, [float(d["Speed (Gbit/s)"]) for d in data], width, color="r")
    autolabel(bar)
    py.ylim(ymin=0)
    ax.set_ylabel("Speed (Gbit/s)")
    ax.set_xticks(ind + width)
    ax.set_xticklabels(
        [x["Name"].replace(" ", "\n") for x in data], rotation=45, ha="right"
    )

    py.title("Bandwidth for Common Interfaces")

    py.savefig("../bandwidth.png")
