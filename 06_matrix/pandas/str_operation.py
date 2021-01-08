import time
import pandas as pd
from numpy.testing import assert_almost_equal, assert_array_almost_equal
import numba
import numpy as np
import matplotlib.pyplot
from utility import ols_lstsq, ols_lstsq_raw

df = pd.read_pickle('generated_ols_data.pickle')
print(f"Loaded {df.shape} rows")

results_ols_lstsq = df.apply(ols_lstsq, axis=1)

#df['m'] = results_ols_lstsq

#df['growth'] = pd.cut(df['m'], [-1.0, -0.01, 0.01, 1.0], labels=['declining', 'stable', 'growing'])
#display(df['growth'].value_counts())

#In [173]: %timeit df.query('growth=="growing"')['m'].mean()           
#4.85 ms ± 40.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#In [174]: %timeit df.groupby('growth')['m'].mean()['growing']       
#1.45 ms ± 8.52 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
#In [175]: mask = df['growth'] == 'growing'
#In [179]: %timeit df[mask]['m'].mean()  
#1.9 ms ± 72.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)


df['0_as_str'] = df[0].apply(lambda v: str(v))
def find_9(s): 
    """Return -1 if '9' not found else its location at position >= 0"""
    return s.split('.')[1].find('9')

#%timeit df['0_as_str'].str.split('.', expand=True)[1].str.find('9')
#183 ms ± 2.58 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
#%timeit df['0_as_str'].apply(find_9)
#51 ms ± 987 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)



