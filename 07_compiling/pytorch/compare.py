import time
from functools import partial

from tqdm import tqdm

import diffusion_numpy
import diffusion_pytorch
import numpy as np
import pylab as py


def get_timings(fxn):
    start = time.perf_counter()
    fxn()
    return time.perf_counter() - start


if __name__ == "__main__":
    grid_sizes = (256, 512, 1024, 2048, 4096)
    n_iter = 1000

    diffusion_pytorch.run_experiment(1, (24, 24), "cuda:0")
    results_pytorch_gpu = []
    for g in tqdm(grid_sizes, desc="pytorch gpu"):
        r = get_timings(
            partial(diffusion_pytorch.run_experiment, n_iter, (g, g), "cuda:0")
        )
        results_pytorch_gpu.append(r)
    results_pytorch_gpu = np.asarray(results_pytorch_gpu)

    results_numpy = []
    for g in tqdm(grid_sizes, desc="numpy"):
        r = get_timings(partial(diffusion_numpy.run_experiment, n_iter, (g, g)))
        results_numpy.append(r)
    results_numpy = np.asarray(results_numpy)

    # diffusion_pytorch.run_experiment(1, (24, 24), 'cpu')
    # results_pytorch_cpu = []
    # for g in tqdm(grid_sizes, desc="pytorch cpu"):
    # r = get_timings(partial(diffusion_pytorch.run_experiment, n_iter, (g, g), 'cpu'))
    # results_pytorch_cpu.append(r)
    # results_pytorch_cpu = np.asarray(results_pytorch_cpu)

    print(grid_sizes)
    print(results_numpy / results_pytorch_gpu)
    print()

    fig = py.figure()
    py.plot(grid_sizes, results_numpy, "-v", label="Numpy")
    py.plot(grid_sizes, results_pytorch_gpu, "-o", label="PyTorch GPU")
    # py.plot(grid_sizes, results_pytorch_cpu, '-x', label="PyTorch CPU")
    py.legend()
    py.title("Runtime for various grid sizes")
    py.xlabel("Grid size")
    py.ylabel("Runtime (seconds)")
    py.yscale("log")
    py.savefig("../../../images/comparison_pytorch_vs_numpy.png")
    py.close(fig)
