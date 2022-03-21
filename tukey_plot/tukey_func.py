# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:34:29 2022

@author: johbla@ous-hf.no

Functions to plot a boxplot with annotations showing significance, 
as given by the tukey-test:

https://en.wikipedia.org/wiki/Tukey%27s_range_test

Data has to be in a pandas-frame. As of now only a numerical grouping 
variable is implemented. Still learning how to do this properly...

But as of now, only for sharing code in a semi-OK-way, hei Ragnar!

TODO: 
    
    Write documentation
    Update for modularity
    Clean up dependencies
    
"""

# Import

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import scipy.integrate

#from sklearn.metrics import auc
from sklearn import metrics
from sklearn.datasets import load_breast_cancer

from statsmodels.stats.multicomp import pairwise_tukeyhsd

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

import statsmodels.stats.api as sms

from scipy.optimize import curve_fit

def group_plot_with_tukey_result(data, 
                                 x_parameter, 
                                 y_parameter, 
                                 xlabel, 
                                 ylabel, 
                                 number_of_groups, 
                                 hight_n_tweak,
                                 output_file_name,
                                 ylim_top,
                                 do_equal_groups = False,
                                 **kwargs):

    sns.set_palette("muted")
    sns.set(font_scale = 1.3)
    sns.set_style("white")
    
    if do_equal_groups:
        data['bins'] = pd.qcut(data[x_parameter], number_of_groups)
    else:
        data['bins'] = pd.cut(data[x_parameter], number_of_groups)
    
    nobs = data['bins'].value_counts().values
    nobs = [str(x) for x in nobs.tolist()]
    nobs = ["n: " + i for i in nobs]
        
    order = np.unique(data["bins"])
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    boxplot_fig = sns.boxplot(data = data, 
                              x = "bins", 
                              y = y_parameter, ax=ax,
                              order = order)
    
    # Make labels from the order-vector:
        
    label_list = []
    
    pos = range(len(nobs))
    
    for o in order:
        left_num = (str(int(np.round(o.left, 0))))
        right_num = (str(int(np.round(o.right, 0))))
        
        label_string = "(" + left_num + ", " + right_num + "]"
        label_list.append(label_string)
        
    for tick,label in zip(pos,ax.get_xticklabels()):
        ax.text(pos[tick],
                np.max(data[y_parameter]) + hight_n_tweak,
                nobs[tick],
                horizontalalignment='center',
                size='small',
                color='k',
                weight='semibold')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    plt.xticks(pos, label_list)
    
    samples = [condition for condition in data.groupby('bins')[y_parameter]]
    sample_list = []
    
    for s in samples:
        sam = s[1].values
        sample_list.append(sam)
    
    f_val, p_val = ss.f_oneway(*sample_list)
    
    tukey = pairwise_tukeyhsd(endog=data[y_parameter],
                              groups=data['bins'],
                              alpha=0.05)
    
    tukey_main_result = tukey.summary().data
    
    list_of_rejected_pairs = []
    
    for i in range(1,len(tukey_main_result)):
        res = (tukey_main_result[i])
        g1 = res[0]
        g2 = res[1]
        reject = res[6]
        
        if reject:
            list_of_rejected_pairs.append((g1,g2))
            
    list_of_tick_pos = []
            
    for p in list_of_rejected_pairs:
        I_1 = np.where(order == p[0])
        I_2 = np.where(order == p[1])
        list_of_tick_pos.append(np.array([I_1[0][0], I_2[0][0]]))
        
    h_list = np.linspace(5, 50 ,len(list_of_rejected_pairs)) # Have to be manually tweaked
        
    for l,h_add in zip(list_of_tick_pos, h_list):
        x1, x2 = l[0], l[1]
        y, h, col = data[y_parameter].max() + h_add, 2, 'k'
        ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
        
        plt.text((x1+x2)*.5, y+h-5, "*", ha='center', va='bottom', color=col)
        
    print('F value: {:.20f}, p value: {:.20f}'.format(f_val, p_val))
    print(tukey)
        
    sns.despine()
    
    ax.set_ylim(top = ylim_top)
    
    plt.tight_layout()
    
    plt.savefig(output_file_name, dpi = 600)
        
    plt.show()



