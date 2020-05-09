#!/usr/bin/env python2.7

import os
import sys
from itertools import cycle

import matplotlib
import norm_array
import norm_numpy
import norm_numpy_dot
import norm_python
import norm_python_comprehension
import numpy as np
import pylab as py

sys.path.append(os.path.abspath("../../examples/matrix/norm/"))




methods = {k: v for k, v in globals().items() if k.startswith("norm")}

markers = cycle("h*o>Dxsp8")
linestyles = cycle(["-", ":", "--", "-."])

if __name__ == "__main__":
    timings = {k: [] for k in methods}
    for exponent in range(12, 35):
        N = int(1.5 ** exponent)
        print("exponent:", exponent)
        print("N:", N)
        for name, method in methods.items():
            t = method.run_experiment(N, num_iter=5) * 1000.0
            timings[name].append((N, t))
            print("%s: %f" % (name, t))

    for name, data in timings.items():
        d = np.asarray(data)
        py.plot(
            d[:, 0],
            d[:, 1],
            label=name,
            marker=next(markers),
            linestyle=next(linestyles),
            linewidth=4,
        )

    py.title("Runtime for various norm squared routines")
    py.xlabel("Vector length")
    py.ylabel("Runtime (miliseconds) -- less is better")
    py.yscale("log")
    py.xscale("log")
    ax = py.gca()
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%d"))

    ax.xaxis.grid(True, which="minor", alpha=0.4)
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.grid(True, which="minor", alpha=0.4)
    py.legend(loc="upper left", handlelength=5)

    py.tight_layout()
    py.savefig("../norm_squared.png")
