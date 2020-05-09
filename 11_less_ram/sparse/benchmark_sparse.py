import timeit

import numpy as np
import pylab as py
from scipy import sparse


def benchmark(size=2048):
    densities = np.asarray([0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.2])
    results = {"sparse": [], "dense": []}
    for density in densities:
        m_sparse = sparse.random(size, size, density).tocsr()
        m_dense = m_sparse.todense()
        N_sparse, total_time_sparse = timeit.Timer(
            "m_sparse * m_sparse", globals=locals()
        ).autorange()
        N_dense, total_time_dense = timeit.Timer(
            "m_dense * m_dense", globals=locals()
        ).autorange()
        time_sparse = total_time_sparse / N_sparse
        time_dense = total_time_dense / N_dense
        results["sparse"].append(time_sparse)
        results["dense"].append(time_dense)
        print(time_sparse, time_dense)

    fig = py.figure()
    py.plot(
        densities * 100, results["sparse"], "--", marker="s", label="CSR Sparse Matrix"
    )
    py.plot(densities * 100, results["dense"], "-", marker="o", label="Numpy Array")
    py.title(f"Runtime for {size}x{size} multiplication with different matrix sparsity")
    py.ylabel("Runtime (seconds)")
    py.xlabel("Density (percent non-zero entries)")
    py.legend()
    ax = py.gca()
    py.tight_layout()
    py.savefig("../../images/sparse_runtime.png")
    py.close(fig)


def matrix_size(size=2028):
    densities = np.linspace(0, 100, 10)
    sparse_size = []
    dense_size = []
    for density in densities:
        m_sparse = sparse.random(size, size, density / 100).tocsr()
        m_dense = m_sparse.todense()

        sparse_size.append(
            (m_sparse.data.nbytes + m_sparse.indices.nbytes + m_sparse.indptr.nbytes)
            / 1e6
        )
        dense_size.append(m_dense.data.nbytes / 1e6)

    fig = py.figure()
    py.plot(densities, sparse_size, "--", marker="s", label="CSR Sparse Matrix")
    py.plot(densities, dense_size, "-", marker="o", label="Numpy Array")
    py.title(f"Memory footprint for {size}x{size} matrices")
    py.ylabel("Size (MB)")
    py.xlabel("Density (percent non-zero entries)")
    py.legend()
    ax = py.gca()
    py.tight_layout()
    py.savefig("../../images/sparse_footprint.png")
    py.close(fig)


if __name__ == "__main__":
    matrix_size()
    benchmark()
