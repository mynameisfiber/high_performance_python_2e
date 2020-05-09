import time
from array import array


def norm_square_array(vector):
    norm = 0
    for v in vector:
        norm += v * v
    return norm


def run_experiment(size, num_iter=3):
    vector = array("l", list(range(size)))
    times = []
    for i in range(num_iter):
        start = time.time()
        norm_square_array(vector)
        times.append(time.time() - start)
    return min(times)


if __name__ == "__main__":
    print(run_experiment(1000000, 10))
