# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 20:39:40 2022

TODO: Write as functions - now it is all a mess...

@author: blakk
"""

#%% Lib import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve


#%% Data loading    
    
data = pd.read_excel("C:/Users/blakk/Documents/PRRT/Tumor/final_dataset_tumour_slava_ukraini.xlsx")

# Add the error-part in the data frame

data["DeltaAD"] = ((data["ADpred"]-data["Absorbed Dose"])/data["Absorbed Dose"])*100

# New column with the numbers stripped from the location name

data['organ_no_num'] = data['organ'].str.replace('\d+', '')


# ROC-curve analysis

end_point_cutoff = np.median(data["Absorbed Dose"])
P = data["Absorbed Dose"] > end_point_cutoff 

pred_vars = ["SUVavg", "SUVmax"]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.array([0,1]), np.array([0,1]), 'k-')

line_styles = ['--', '-']

for pred_var, line_style in zip(pred_vars, line_styles):

    X = data[pred_var].values
    X = X.reshape(-1,1)
    
    clf = LogisticRegression(solver="liblinear").fit(X, P)
    y_score = clf.predict_proba(X)[:, 1]
    
    AUC_str = str(round(roc_auc_score(P, clf.decision_function(X)),2))
    
    fpr, tpr, ths  =  roc_curve(P, y_score)
    
    ax.plot(fpr, tpr, line_style, label = "AUC " + pred_var + ": " + AUC_str)

ax.set_xlim([0,1])
ax.set_ylim([0,1])

ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")

plt.legend(loc = 4)
sns.despine()

plt.tight_layout()

plt.savefig("Fig5.png",dpi = 600)
