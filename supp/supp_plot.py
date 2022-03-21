# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 20:44:21 2022

@author: johbla@ous-hf.no

Some of this I have stolen from SO

"""



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss

from scipy.stats import pearsonr


#%% Data loading    
    
data = pd.read_excel("C:/Users/blakk/Documents/PRRT/Tumor/final_dataset_tumour_slava_ukraini.xlsx")

# Add the error-part in the data frame

data["DeltaAD"] = ((data["ADpred"]-data["Absorbed Dose"])/data["Absorbed Dose"])*100

# New column with the numbers stripped from the location name

data['organ_no_num'] = data['organ'].str.replace('\d+', '')

#%% Plot of all paramters NB! Takes some time

vars_to_plot = ["SUVavg", 
                "SUVmax", 
                "AC24", 
                "AC168", 
                "Half-life",
                "Volume",
                "ADpred",
                "Absorbed Dose"]

sns.pairplot(data, vars = vars_to_plot, corner = True)

plt.savefig("all_parameters.png", dpi = 300)

#%% Plot the residuals

residuals = data["Absorbed Dose"]-data["ADpred"]

ss.probplot(residuals, plot=plt);

sns.despine()
plt.tight_layout()

print(ss.shapiro(residuals))

plt.savefig("SuppFigure_probplot.png", dpi = 300)

#%%

# Correlation and heatmap 

def plot_cor_matrix(corr, mask=None):
    f, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, ax=ax,
                mask=mask,
                # cosmetics
                annot=True, vmin=-1, vmax=1, center=0,
                cmap='coolwarm', linewidths=0, linecolor='black', cbar_kws={'orientation': 'horizontal'})


def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues

data_only_plotting_columns = data[vars_to_plot]

corr = data_only_plotting_columns.corr()
#p_values = corr_sig(data_only_plotting_columns)    

p_values = calculate_pvalues(data_only_plotting_columns) 
                 # get p-Value
mask = np.invert(np.tril(p_values<0.05))    # mask - only get significant corr
plot_cor_matrix(corr,mask)

plt.tight_layout()

plt.savefig("heat_map_for_all_vars.png", dpi = 300)
