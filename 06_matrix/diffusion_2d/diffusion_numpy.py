#!/usr/bin/env python3

import timeit

from numpy import roll, zeros

try:
    profile
except NameError:
    profile = lambda x: x

grid_shape = (2048, 2048)


def laplacian(grid):
    return (
        roll(grid, +1, 0)
        + roll(grid, -1, 0)
        + roll(grid, +1, 1)
        + roll(grid, -1, 1)
        - 4 * grid
    )


@profile
def evolve(grid, dt, D=1):
    return grid + dt * D * laplacian(grid)


def run_experiment(num_iterations):
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return grid


if __name__ == "__main__":
    n_iter = 100
    N, runtime = timeit.Timer(
        f"run_experiment({n_iter})", globals=globals()
    ).autorange()
    print(f"Runtime with grid {grid_shape}: {runtime / N:0.4f}s")
