import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import numpy
import math
import matplotlib
from sklearn.metrics import r2_score


# Define the logarithmic function to fit to the data
def log_func(x, a, b, c):
    # return a + b * numpy.log(d * x) + c * x
    return a + b * numpy.log(x) + c * x

