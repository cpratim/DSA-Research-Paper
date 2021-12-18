import numpy as np
from scipy.stats import linregress

def correlation(x, y):
	return np.corrcoef(x, y)[0, 1]

def linregress_f(x, y):
	slope, intercept, r, p, std = linregress(x, y)
	return lambda x: x*slope + intercept