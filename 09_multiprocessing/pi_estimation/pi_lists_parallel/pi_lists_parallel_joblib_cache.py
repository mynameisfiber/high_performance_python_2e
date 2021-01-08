import random
import os
import time
import argparse
from joblib import Parallel, delayed
from joblib import Memory
from pi_lists_parallel import estimate_nbr_points_in_quarter_circle as estimate_nbr_points_in_quarter_circle_orig

memory = Memory("./joblib_cache", verbose=0)

@memory.cache
def estimate_nbr_points_in_quarter_circle_with_idx(nbr_estimates, idx):
    print(f"Executing estimate_nbr_points_in_quarter_circle with {nbr_estimates} on sample {idx} on pid {os.getpid()}")
    nbr_trials_in_quarter_unit_circle = 0
    for step in range(int(nbr_estimates)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_quarter_unit_circle += is_in_unit_circle

    return nbr_trials_in_quarter_unit_circle


estimate_nbr_points_in_quarter_circle = memory.cache(estimate_nbr_points_in_quarter_circle_orig)

if __name__ == "__main__":
    nbr_samples_in_total = int(1e8)
    nbr_parallel_blocks = 8

    nbr_samples_per_worker = int(nbr_samples_in_total / nbr_parallel_blocks)
    print("Making {:,} samples per {} worker".format(nbr_samples_per_worker, nbr_parallel_blocks))
    t1 = time.time()
    # beware if you don't have a sample_idx, you cache the same result!
    nbr_in_quarter_unit_circles = Parallel(n_jobs=nbr_parallel_blocks)(delayed(estimate_nbr_points_in_quarter_circle_with_idx)(nbr_samples_per_worker, idx) for idx in range(nbr_parallel_blocks))
    #nbr_in_quarter_unit_circles = Parallel(n_jobs=nbr_parallel_blocks)(delayed(estimate_nbr_points_in_quarter_circle)(nbr_samples_per_worker) for idx in range(nbr_parallel_blocks))
    pi_estimate = sum(nbr_in_quarter_unit_circles) * 4 / float(nbr_samples_in_total)
    print("Estimated pi", pi_estimate)
    print("Delta:", time.time() - t1)

