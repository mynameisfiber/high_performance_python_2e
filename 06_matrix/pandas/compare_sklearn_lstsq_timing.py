import pandas as pd
import matplotlib.pyplot
import timeit
from utility import ols_lstsq, ols_sklearn
#%matplotlib

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_pickle('generated_ols_data.pickle')
print("Loaded")

number = 10_000

results = timeit.repeat("ols_lstsq(df.iloc[0])", globals=globals(), number=number)
time_of_fastest = min(results)
print(f"Time to run ols_lstsq for fastest of repeats is {time_of_fastest / number:0.6f} seconds on {number} repeats and taking fastest")

results = timeit.repeat("ols_sklearn(df.iloc[0])", globals=globals(), number=number)
time_of_fastest = min(results)
print(f"Time to run ols_sklearn for fastest of repeats is {time_of_fastest / number:0.6f} seconds")


