import random
import os
import time
import argparse
from joblib import Parallel, delayed
from pi_lists_parallel import estimate_nbr_points_in_quarter_circle


if __name__ == "__main__":
    nbr_samples_in_total = int(1e8)
    nbr_parallel_blocks = 8

    nbr_samples_per_worker = int(nbr_samples_in_total / nbr_parallel_blocks)
    print("Making {:,} samples per {} worker".format(nbr_samples_per_worker, nbr_parallel_blocks))
    t1 = time.time()
    nbr_in_quarter_unit_circles = Parallel(n_jobs=nbr_parallel_blocks, verbose=1)(delayed(estimate_nbr_points_in_quarter_circle)(nbr_samples_per_worker) for sample_idx in range(nbr_parallel_blocks))
    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    print("Estimated pi", pi_estimate)
    print("Delta:", time.time() - t1)

