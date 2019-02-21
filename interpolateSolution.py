import numpy as np
def nan_helper(y):
	return np.isnan(y), lambda z: z.nonzero()[0]
y= array([1, 1, 1, NaN, NaN, 2, 2, NaN, 0])
nans, x= nan_helper(y)
y[nans]= np.interp(x(nans), x(~nans), y[~nans])

