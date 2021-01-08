"""Estimate Pi using 1 large array"""
import time
import numpy as np
import pi_lists_parallel

nbr_samples_in_total = int(1e8)

t1 = time.time()
nbr_in_circle = pi_lists_parallel.estimate_nbr_points_in_quarter_circle(nbr_samples_in_total)
print("Took {0:2f}s".format(time.time() - t1))
pi_estimate = float(nbr_in_circle) / nbr_samples_in_total * 4
print("Estimated pi", pi_estimate)
print("Pi", np.pi)

