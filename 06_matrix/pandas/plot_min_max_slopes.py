import pandas as pd
import numpy as np
import matplotlib.pyplot
from utility import ols_lstsq
#%matplotlib

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

if "df" not in dir():
    print("Reading")
    df = pd.read_pickle('generated_ols_data.pickle')

# get a set of results that we'll use to double-check other methods
results_ols_lstsq = df.apply(ols_lstsq, axis=1)
print(results_ols_lstsq.shape)
results_ols_lstsq[:5]

# local copy of ols_lstsq
def variant_ols_lstsq(row):
    X = np.arange(row.shape[0]) # shape (14,)
    ones = np.ones(row.shape[0]) # constant used to build intercept
    A = np.vstack((X, ones)).T # shape(14, 2)
    # lstsq returns the coefficient and intercept as the first result 
    # followed by the residuals and other items
    m, c = np.linalg.lstsq(A, row.values, rcond=-1)[0] 
    return m, c

def make_ys(m, c, xs):
    return (m * xs) + c

idx = results_ols_lstsq.idxmax()
ols_result = results_ols_lstsq[idx]

m, c = variant_ols_lstsq(df.iloc[idx])
assert ols_result == m
xs = np.arange(df.shape[1]) 
ys = make_ys(m, c, xs)

fig, axs = plt.subplots(ncols=2, sharey=True) #, figsize=(8,4))

YMAX = 1.5
MARKER = 'o'
ax = axs[0]
df.iloc[idx].plot(ax=ax, marker=MARKER);
ax.plot(xs, ys, label='Best fit')
ax.set_ylim(ymin=0, ymax=YMAX)
ax.set_title(f"Maximum slope (row {idx:,})\nm={m:0.2f} c={c:0.2f}");
ax.set_xlabel("Days")
ax.set_ylabel("Hours of usage")

idx = results_ols_lstsq.idxmin()
ols_result = results_ols_lstsq[idx]
m, c = variant_ols_lstsq(df.iloc[idx])
assert ols_result == m
xs = np.arange(df.shape[1]) 
ys = make_ys(m, c, xs)

ax = axs[1]
df.iloc[idx].plot(ax=ax, marker=MARKER);
ax.plot(xs, ys, label='Best fit')
ax.set_ylim(ymin=0, ymax=YMAX)
ax.set_xlabel("Days")
#ax.set_title(f"Minimum slope m={ols_result:0.2f} (row {idx:,})");
ax.set_title(f"Maximum slope (row {idx:,})\nm={m:0.2f} c={c:0.2f}");

plt.savefig('random_hours_mobile_min_max_slopes.png')
