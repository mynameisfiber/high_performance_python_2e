#!/usr/bin/env python3

import time

import numpy as np

try:
    profile
except NameError:
    profile = lambda x: x

grid_shape = (640, 640)


def laplacian(grid, out):
    np.copyto(out, grid)
    out *= -4
    out += np.roll(grid, +1, 0)
    out += np.roll(grid, -1, 0)
    out += np.roll(grid, +1, 1)
    out += np.roll(grid, -1, 1)


@profile
def evolve(grid, dt, out, D=1):
    laplacian(grid, out)
    out *= D * dt
    out += grid


def run_experiment(num_iterations):
    scratch = np.zeros(grid_shape)
    grid = np.zeros(grid_shape)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid
    return time.time() - start


if __name__ == "__main__":
    run_experiment(500)
