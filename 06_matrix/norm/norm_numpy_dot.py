import time

import numpy


def norm_square_numpy_dot(vector):
    return numpy.dot(vector, vector)


def run_experiment(size, num_iter=3):
    vector = numpy.arange(size)
    times = []
    for i in range(num_iter):
        start = time.time()
        norm_square_numpy_dot(vector)
        times.append(time.time() - start)
    return min(times)


if __name__ == "__main__":
    print(run_experiment(1000000, 10))
