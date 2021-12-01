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
temp = mne.Evoked("/home/vtretyakova/Рабочий стол/speach_learn/Extremes/donor-ave.fif")


# for selfpaced

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015') # для данного испытуемого не нашлось подходящих эвентов


data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/selfpased_hands_15_25'

hands = ['left', 'right']

tmin = [-0.550, 0.100, 0.550]

tmax = [-0.100, 0.550, 1.000]

intervals = ['PreM', 'M', 'PostM']

######### 1 контраст 0 vs SP left hands, full fdr correction #########################
for h in hands:
    mean1_all = np.zeros((102, 3))

    p_val_all = np.zeros((102, 3))

    for ind, inter in enumerate(intervals):
    
	
        t_stat, p_val, mean1 = ttest_vs_zero(data_path, h, subjects, tmin[ind], tmax[ind])
        
        #mean1 = mean1[:, np.newaxis]
        
        #p_val = p_val[:, np.newaxis]
        mean1_all[:, ind] = mean1
        
        p_val_all[:, ind] = p_val

    p_val_full_fdr = full_fdr(p_val_all)

    fig = plot_topo_vs_zero(p_val_full_fdr, temp, mean1_all)

    fig.savefig(f'/home/vtretyakova/Рабочий стол/speach_learn/self_paced_hands_ttest_on_ave_intervals/0_vs_sp_{h}_hand_full_fdr.jpeg', dpi = 900)


######### 2. self paced left vs right hands, with full fdr correction #########################


comp1_mean_all = np.zeros((102, 3))
comp2_mean_all = np.zeros((102, 3))
p_val_all = np.zeros((102, 3))

for ind, inter in enumerate(intervals):
	
    t_stat, p_val, comp1_mean, comp2_mean = ttest_pair(data_path, hands, subjects, tmin[ind], tmax[ind])
    
    #comp1_mean = comp1_mean[:, np.newaxis]
    
    #comp2_mean = comp2_mean[:, np.newaxis]

    #p_val = p_val[:, np.newaxis]
    
    comp1_mean_all[:, ind] = comp1_mean
    comp2_mean_all[:, ind] = comp2_mean
    p_val_all[:, ind] = p_val
    
p_val_full_fdr = full_fdr(p_val_all)

fig = plot_deff_topo(p_val_full_fdr, temp, comp1_mean_all, comp2_mean_all)

fig.savefig('/home/vtretyakova/Рабочий стол/speach_learn/self_paced_hands_ttest_on_ave_intervals/sp_left_vs_right_hand_full_fdr.jpeg', dpi = 900)

