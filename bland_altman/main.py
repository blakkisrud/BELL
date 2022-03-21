# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 20:24:25 2022

@author: blakk
"""

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def bland_altman_plot(data1, data2, true_on_x = False, *args, **kwargs):
    
    """
    The flag true_on_x decide to plot the mean of the two data sets (False)
    on the x-axis, or (True) use the data2-dataset as the x-xis
    """
    
    data1     = np.asarray(data1)
    data2     = np.asarray(data2)
    mean      = np.mean([data1, data2], axis=0)
    diff      = ((data1 - data2)/data2)*100                   # Relative difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference

    if true_on_x:
        sns.scatterplot(x = data2, y = diff, *args, **kwargs)
    else:
        sns.scatterplot(x = mean, y = diff, *args, **kwargs)
        
    plt.axhline(md,           color='k', linestyle='--')
    plt.axhline(md + 1.96*sd, color='k', linestyle='--')
    plt.axhline(md - 1.96*sd, color='k', linestyle='--')
    
