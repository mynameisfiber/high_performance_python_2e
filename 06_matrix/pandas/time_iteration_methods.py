import time
import pandas as pd
from numpy.testing import assert_almost_equal, assert_array_almost_equal
import numba
from numba import jit
import numpy as np
import matplotlib.pyplot
from utility import ols_lstsq, ols_lstsq_raw

df = pd.read_pickle('generated_ols_data.pickle')
print(f"Loaded {df.shape} rows")

results_ols_lstsq = df.apply(ols_lstsq, axis=1)

t1 = time.time()
t1a = time.time()
results = None
for row_idx in range(df.shape[0]):
    if row_idx % 10000 == 0:
        if row_idx > 0:
            t1b = time.time()
            print(f"At row {row_idx:,} taking {t1b-t1a} for the last block")
            t1a = t1b
    row = df.iloc[row_idx]
    m = ols_lstsq(row)
    if results is None:
        results = pd.Series([m])
    else:
        #results = results.append(pd.Series([m]))  # equivalent to concat
        results = pd.concat((results, pd.Series([m])))
t2 = time.time()
assert_array_almost_equal(results_ols_lstsq, results)
print(f"Dereference with iloc and continuous build {t2 - t1}")

t1 = time.time()
ms = []
for row_idx in range(df.shape[0]):
    row = df.iloc[row_idx]
    m = ols_lstsq(row)
    ms.append(m)
results = pd.Series(ms)
t2 = time.time()

assert_array_almost_equal(results_ols_lstsq, results)
print(f"Dereference with iloc {t2 - t1}")

t1 = time.time()
ms = []
for row_idx, row in df.iterrows():
    m = ols_lstsq(row)
    ms.append(m)
results = pd.Series(ms)
t2 = time.time()
assert_almost_equal(results_ols_lstsq[0], results[0])
assert_array_almost_equal(results, results_ols_lstsq)  
print(f"Dereference with iterrows {t2 - t1}")


t1 = time.time()
ms = df.apply(ols_lstsq, axis=1)
results = pd.Series(ms)
t2 = time.time()
print(f"apply {t2 - t1}")
assert_almost_equal(results_ols_lstsq[0], results[0])
assert_array_almost_equal(results, results_ols_lstsq)  

t1 = time.time()
ms = df.apply(ols_lstsq_raw, axis=1, raw=True)
results = pd.Series(ms)
t2 = time.time()
print(f"apply raw=True {t2 - t1}")
assert_almost_equal(results_ols_lstsq[0], results[0])
assert_array_almost_equal(results, results_ols_lstsq)  

#@numba.jit(nopython=True)
#def ols_lstsq_raw_values_numba_ORIG(row):
#    # np.arange(row.shape[0], dtype=np.float) fails
#    # np.arange(row.shape[0], dtype=np.float_) fails
#    # vstack # note [] no good if non-homogenous types, needs ()
#    idx = np.arange(row.shape[0]) 
#    ones = np.ones(row.shape[0])
#    A = np.vstack((idx, ones)).T 
#    m, c = np.linalg.lstsq(A, row, rcond=-1.0)[0]
#    return m

#@numba.jit(nopython=True)
#def ols_lstsq_raw_values_numba(row):
#    X = np.arange(row.shape[0]) 
#    ones = np.ones(row.shape[0])
#    A = np.vstack((X, ones)).T 
#    m, c = np.linalg.lstsq(A, row, rcond=-1.0)[0]
#    return m

ols_lstsq_raw_values_numba = jit(ols_lstsq_raw, nopython=True)

t1 = time.time()
results = df.apply(ols_lstsq_raw_values_numba, axis=1, raw=True)
t2 = time.time()
print(f"Numba 1 ols_lstsq_raw_values_numba raw=True compilation pass {t2 - t1}")
assert_almost_equal(results_ols_lstsq[0], results[0])
assert_array_almost_equal(results, results_ols_lstsq)  
t1 = time.time()
results = df.apply(ols_lstsq_raw_values_numba, axis=1, raw=True)
t2 = time.time()
print(f"Numba 2 {t2 - t1}")
t1 = time.time()
results = df.apply(ols_lstsq_raw_values_numba, axis=1, raw=True)
t2 = time.time()
print(f"Numba 3 {t2 - t1}")



import dask.dataframe as dd
import dask
import swifter

N_PARTITIONS = 8
ddf = dd.from_pandas(df, npartitions=N_PARTITIONS, sort=False)
#SCHEDULER = "threads"
SCHEDULER = "processes"
# met provides the return type as a name & dtype

t1 = time.time()
results = ddf.apply(ols_lstsq, axis=1, meta=(None, 'float64',)).compute(scheduler=SCHEDULER)
t2 = time.time()
assert_array_almost_equal(results, results_ols_lstsq)  
print(f"Dask ols_lstsq {t2 - t1}")
t1 = time.time()
results = ddf.apply(ols_lstsq_raw, axis=1, meta=(None, 'float64',), raw=True).compute(scheduler=SCHEDULER)
t2 = time.time()
assert_array_almost_equal(results, results_ols_lstsq)  
print(f"Dask ols_lstsq_raw raw=True {t2 - t1}")

# without the meta arg it tells us what return type it inferred
#results_df_ols_np_distributed = ddf.apply(ols_np_distributed, axis=1).compute(scheduler=SCHEDULER)
assert_array_almost_equal(results, results_ols_lstsq)  



t1 = time.time()
results = df.swifter.progress_bar(False).apply(ols_lstsq_raw, axis=1, raw=True)
t2 = time.time()
print(f"swifter ols_lstsq_raw raw=True {t2 - t1}")
#results = df.swifter.progress_bar(False).apply(ols_lstsq_raw, axis=1)
assert_array_almost_equal(results, results_ols_lstsq)  

t1 = time.time()
results = ddf.apply(ols_lstsq_raw_values_numba, axis=1, meta=(None, 'float64',), raw=True).compute(scheduler=SCHEDULER)
t2 = time.time()
assert_array_almost_equal(results, results_ols_lstsq)  
print(f"Dask ols_lstsq_raw_values_numba  {t2 - t1}")
assert_array_almost_equal(results, results_ols_lstsq)  

