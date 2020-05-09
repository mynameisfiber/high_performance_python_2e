#!/usr/bin/env python3

import time
from functools import partial

import numpy as np
import torch
from torch import roll, zeros  # <1>

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # <2>

GRID_SHAPE = (2048, 2048)


def timer(fxn, max_time=5):
    N = 0
    total_time = 0
    fxn()  # prime the pump
    while total_time < max_time:
        start = time.perf_counter()
        fxn()
        total_time += time.perf_counter() - start
        N += 1
    return total_time / N


def laplacian(grid):
    return (
        roll(grid, +1, 0)
        + roll(grid, -1, 0)
        + roll(grid, +1, 1)
        + roll(grid, -1, 1)
        - 4 * grid
    )


def evolve(grid, dt, D=1):
    return grid + dt * D * laplacian(grid)


def run_experiment(num_iterations, grid_shape=GRID_SHAPE, device=DEVICE):
    grid = zeros(grid_shape, device=device)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return grid


def debug_cpu_onboard(num_iterations, grid_shape=GRID_SHAPE, device=DEVICE):
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    grid = grid.to(device)  # <3>
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
        torch.cuda.synchronize()
    return grid


def debug_cpu_copy(num_iterations, grid_shape=GRID_SHAPE, device=DEVICE):
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    grid = grid.to(device)  # <3>
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
        grid.cpu()
    return grid


if __name__ == "__main__":
    n_iter = 100
    grid_shape = (4096, 4096)

    t_vanilla = timer(partial(run_experiment, n_iter, grid_shape=grid_shape))
    print(f"Runtime vanilla: {t_vanilla:0.4f}s")

    # t_copy = timer(partial(debug_cpu_copy, n_iter, grid_shape=grid_shape))
    # print(f"Runtime with copy: {t_copy:0.4f}s")

    # t_inplace = timer(partial(debug_cpu_onboard, n_iter, grid_shape=grid_shape))
    # print(f"Runtime without copy: {t_inplace:0.4f}s")

    # print(f"Copy is {t_copy / t_vanilla:0.2f}x slower than vanilla")
    # print(f"Inplace is {t_copy / t_inplace:0.2f}x faster than copy")
