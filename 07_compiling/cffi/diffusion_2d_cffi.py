#!/usr/bin/env python2.7

import time

from cffi import FFI, verifier

import numpy as np

grid_shape = (512, 512)

ffi = FFI()
ffi.cdef("void evolve(double **in, double **out, double D, double dt);")  # <1>
lib = ffi.dlopen("../diffusion.so")


def evolve(grid, dt, out, D=1.0):
    pointer_grid = ffi.cast("double**", grid.ctypes.data)  # <2>
    pointer_out = ffi.cast("double**", out.ctypes.data)
    lib.evolve(pointer_grid, pointer_out, D, dt)


def run_experiment(num_iterations):
    scratch = np.zeros(grid_shape, dtype=np.double)
    grid = np.zeros(grid_shape, dtype=np.double)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid
    return time.time() - start


if __name__ == "__main__":
    t = run_experiment(500)
    print(t)

    verifier.cleanup_tmpdir()
