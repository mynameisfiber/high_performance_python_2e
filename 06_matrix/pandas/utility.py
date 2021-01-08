import numpy as np
from sklearn.linear_model import LinearRegression

def ols_sklearn(row):
    """Solve OLS using scikit-learn's LinearRegression"""
    est = LinearRegression() 
    X = np.arange(row.shape[0]).reshape(-1, 1) # shape (14, 1)
    # note that the intercept is built inside LinearRegression
    est.fit(X, row.values) 
    m = est.coef_[0] # note c is in est.intercept_
    return m

def ols_lstsq(row):
    """Solve OLS using numpy.linalg.lstsq"""
    # build X values for [0, 13]
    X = np.arange(row.shape[0]) # shape (14,)
    ones = np.ones(row.shape[0]) # constant used to build intercept
    A = np.vstack((X, ones)).T # shape(14, 2)
    # lstsq returns the coefficient and intercept as the first result 
    # followed by the residuals and other items
    m, c = np.linalg.lstsq(A, row.values, rcond=-1)[0] 
    return m

def ols_lstsq_raw(row):
    """Variant of `ols_lstsq` where row is a numpy array (not a Series)"""
    X = np.arange(row.shape[0])
    ones = np.ones(row.shape[0])
    A = np.vstack((X, ones)).T
    m, c = np.linalg.lstsq(A, row, rcond=-1)[0] 
    return m



def ols_sm(row):
    # by default statsmodels fit uses 
    # https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse (pinv)
    # QR method is the alternative (this add 3s to execution in 50k rows test)
    sm_X = sm.add_constant(row.index)
    model = sm.OLS(row.values, sm_X)
    results = model.fit()
    #results.params # 2 params, C followed by m
    return results.params[1]
