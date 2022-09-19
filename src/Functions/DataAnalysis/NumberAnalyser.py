import os 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

from Functions.DataAnalysis import Validator

def summarize(series: pd.Series) -> pd.DataFrame:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Describe companies dataset collected from CrunchBase
    >>> param: None # no param required 
    >>> funct: 0    # read data from comma-delimited file
    >>> funct: 1    # convert data into the right types
    >>> funct: 2    # show general information about dataset
    >>> funct: 3    # show detailed data records in dataset
    >>> funct: 4    # describe key stats of numeric fields
    >>> funct: 5    # visualize univariate data with histograms
    >>> funct: 6    # visualize multivariate data with scatterplots
    >>> funct: 7    # include correlation analysis for relevant pairs
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if Validator.is_number(series) == False:
        raise Exception("incorrect data type")

    df = pd.DataFrame(columns=["Count", "Sum", "Mean", "Median", "Mode", \
        "Std", "Min", "Max", "25%", "50%", "75%", "Skewness", "Kurtosis"])
    
    count = series.count()
    sum = series.sum()
    mean = series.mean()
    median = series.median()
    mode = [m for _, m in series.mode().iteritems()]
    std = series.std()
    min = series.min()
    max = series.max()
    q25 = series.quantile(0.25)
    q50 = series.quantile(0.50)
    q75 = series.quantile(0.75)
    skew = series.skew()
    kurt = series.kurtosis()

    df.loc[len(df.index)] = \
        [count, sum, mean, median, mode, std, min, max, q25, q50, q75, skew, kurt]

    return df 
