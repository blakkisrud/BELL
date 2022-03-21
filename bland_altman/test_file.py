# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 20:24:43 2022

@author: johbla@ous-hf.no

Some very specific testing code

"""

#%% Lib import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#%% Data loading    
    
data = pd.read_excel("C:/Users/blakk/Documents/PRRT/Tumor/final_dataset_tumour_slava_ukraini.xlsx")

# Add the error-part in the data frame

data["DeltaAD"] = ((data["ADpred"]-data["Absorbed Dose"])/data["Absorbed Dose"])*100

# New column with the numbers stripped from the location name

data['organ_no_num'] = data['organ'].str.replace('\d+', '')

#%% Test the function

from main import bland_altman_plot


fig = plt.figure()
ax = fig.add_subplot(111)

bland_altman_plot(data["ADpred"], data["Absorbed Dose"], 
                  true_on_x=True, 
                  s = 35)

ax.set_xlabel("Measured absorbed dose [Gy]")
ax.set_ylabel("Relative difference [%]")
ax.set_xlim(left = 0)

sns.despine()

plt.savefig("Fig3_Bland_Alttman_true_on_x.png", dpi = 600)