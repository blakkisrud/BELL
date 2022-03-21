# -*- coding: utf-8 -*-

"""
Created on Mon Mar 21 20:23:05 2022

@author: johbla@ous-hf.no

"""

#%% Lib import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.stats.multicomp import pairwise_tukeyhsd

from tukey_func import group_plot_with_tukey_result

#%% Data loading    
    
data = pd.read_excel("C:/Users/blakk/Documents/PRRT/Tumor/final_dataset_tumour_slava_ukraini.xlsx")

# Add the error-part in the data frame

data["DeltaAD"] = ((data["ADpred"]-data["Absorbed Dose"])/data["Absorbed Dose"])*100

# New column with the numbers stripped from the location name

data['organ_no_num'] = data['organ'].str.replace('\d+', '')

#%% Test for some plots:
    
# Figure 4A - Absorbed dose and SUVavg

x_parameter = 'SUVavg' # Put the SUV-max in 
y_parameter = "Absorbed Dose"
ylabel = "Absorbed Dose (Gy)"
xlabel = "SUVavg"
number_of_groups = 4
hight_n_tweak = 75
output_file_name = "Figure_4A" + x_parameter + y_parameter + ".png"
ylim_top = 160

group_plot_with_tukey_result(data = data, 
                             x_parameter = x_parameter, 
                             y_parameter = y_parameter, 
                             xlabel = xlabel, 
                             ylabel = ylabel, 
                             number_of_groups = number_of_groups, 
                             hight_n_tweak = hight_n_tweak,
                             output_file_name = output_file_name,
                             ylim_top=ylim_top)

# Figure 4B - Absorbed dose and volume

x_parameter = 'Volume' # Put the SUV-max in 
y_parameter = "Absorbed Dose"
ylabel = "Absorbed Dose (Gy)"
xlabel = "Tumour mass (g)"
number_of_groups = 4
hight_n_tweak = 75
output_file_name = "Figure_4B" + x_parameter + y_parameter + ".png"
ylim_top = 160

group_plot_with_tukey_result(data = data, 
                             x_parameter = x_parameter, 
                             y_parameter = y_parameter, 
                             xlabel = xlabel, 
                             ylabel = ylabel, 
                             number_of_groups = number_of_groups, 
                             hight_n_tweak = hight_n_tweak,
                             output_file_name = output_file_name,
                             ylim_top=ylim_top)

# Figure 4C - Delta AD and SUVavg

x_parameter = 'SUVavg' # Put the SUV-max in 
y_parameter = "DeltaAD"
ylabel = "Delta Absorbed Dose (%)"
xlabel = "SUVavg"
number_of_groups = 4
hight_n_tweak = 50
output_file_name = "Figure_4C" + x_parameter + y_parameter + ".png"
ylim_top = 900

group_plot_with_tukey_result(data = data, 
                             x_parameter = x_parameter, 
                             y_parameter = y_parameter, 
                             xlabel = xlabel, 
                             ylabel = ylabel, 
                             number_of_groups = number_of_groups, 
                             hight_n_tweak = hight_n_tweak,
                             output_file_name = output_file_name,
                             ylim_top=ylim_top)


# Figure 4C - Delta AD and volume

x_parameter = 'Volume' # Put the SUV-max in 
y_parameter = "DeltaAD"
ylabel = "Delta Absorbed Dose (%)"
xlabel = "Tumour mass (g)"
number_of_groups = 4
hight_n_tweak = 50
output_file_name = "Figure_4D" + x_parameter + y_parameter + ".png"
ylim_top = 900

group_plot_with_tukey_result(data = data, 
                             x_parameter = x_parameter, 
                             y_parameter = y_parameter, 
                             xlabel = xlabel, 
                             ylabel = ylabel, 
                             number_of_groups = number_of_groups, 
                             hight_n_tweak = hight_n_tweak,
                             output_file_name = output_file_name,
                             ylim_top=ylim_top)

