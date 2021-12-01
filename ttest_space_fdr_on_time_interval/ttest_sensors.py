import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
import statsmodels.stats.multitest as mul
import os
from func import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero

#load donor
temp = mne.Evoked("/home/vera/MNE/speach_learning/donor-ave.fif")


# for selfpaced

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015') # для данного испытуемого не нашлось подходящих эвентов


data_path = '/home/vera/MNE/speach_learning/MIN_MAX/selfpased_hands_15_25'

hands = ['left', 'right']

tmin = [-0.550, 0.100, 0.550]

tmax = [-0.100, 0.550, 1.000]

intervals = ['PreM', 'M', 'PostM']

######### 1 контраст 0 vs SP left hands, full fdr correction #########################
for ind, inter in enumerate(intervals):
    for h in hands:
	
        t_stat, p_val, mean1 = ttest_vs_zero(data_path, h, subjects, tmin[ind], tmax[ind])
        
        mean1 = mean1[:, np.newaxis]
        
        p_val = p_val[:, np.newaxis]

        p_val_space_fdr = space_fdr(p_val)

        fig = plot_topo_vs_zero(p_val_space_fdr, temp, mean1)

        fig.savefig(f'/home/vera/MNE/speach_learning/Final_november_21/self_paced_hands_ttest_on_ave_intervals/{inter}_0_vs_sp_{h}_hand_space_fdr.jpeg', dpi = 900)


######### 2. self paced left vs right hands, with full fdr correction #########################
for ind, inter in enumerate(intervals):
	
    t_stat, p_val, comp1_mean, comp2_mean = ttest_pair(data_path, hands, subjects, tmin[ind], tmax[ind])
    
    comp1_mean = comp1_mean[:, np.newaxis]
    
    comp2_mean = comp2_mean[:, np.newaxis]

    p_val = p_val[:, np.newaxis]
    
    p_val_space_fdr = space_fdr(p_val)

    fig = plot_deff_topo(p_val_space_fdr, temp, comp1_mean, comp2_mean)

    fig.savefig(f'/home/vera/MNE/speach_learning/Final_november_21/self_paced_hands_ttest_on_ave_intervals/{inter}_sp_left_vs_right_hand_space_fdr.jpeg', dpi = 900)

