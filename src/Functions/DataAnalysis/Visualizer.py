from typing import List
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

def show_bar_chart() -> None:
    pass 

def show_pie_chart() -> None:
    pass 

def show_line_chart() -> None:
    pass 

def show_histogram(series: pd.Series) -> None:
    IQR = series.quantile(0.75) - series.quantile(0.25)
    if IQR == 0: return
    diff_range = series.max - series.min
    bin_width = 2 * IQR / pow(series.count(), 1/3) 
    num_bins = int(diff_range / bin_width)
    series.hist(bins=num_bins) 

    plt.title(series.name)
    plt.show()

def show_scatter(dataframe: pd.DataFrame) -> None:
    if len(dataframe.columns) != 2: 
        raise Exception("incorrect argument for 2x2 matrix") 

    pd.plotting.scatter_matrix(dataframe)
    plt.show()   
    return NotImplemented 
