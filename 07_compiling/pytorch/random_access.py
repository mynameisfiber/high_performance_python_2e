import time
from functools import partial

import torch


def timer(fxn, max_time=5):
    N = 0
    total_time = 0
    fxn()
    while total_time < max_time:
        start = time.perf_counter()
        fxn()
        total_time += time.perf_counter() - start
        N += 1
    return total_time / N


def task(A, target):
    result = 0
    i = 0
    N = 0
    while result < target:
        r = A[i]
        result += r
        i = A[i]
        N += 1
    return N


if __name__ == "__main__":
    N = 1000
    print(f"Testing with array of length {N}")

    A_py = (torch.rand(N) * N).type(torch.int).to("cuda:0")
    A_np = A_py.cpu().numpy()

    t_py = timer(partial(task, A_py, 500))
    t_np = timer(partial(task, A_np, 500))
    print(f"PyTorch took: {t_py:0.3e}s")
    print(f"Numpy took:   {t_np:0.3e}s")
    print(f"Numpy is {100 - t_np/t_py*100:0.2f}% faster")
