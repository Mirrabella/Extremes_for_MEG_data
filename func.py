import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul




###############################################################################################    
############################ FUNCTION FOR TTEST ############################
######################### парный ttest #########################################

def ttest_pair(data_path, hands, subjects, tmin, tmax): # n - количество временных отчетов
	contr = np.zeros((len(subjects), 2, 102)) # avarage data in time interval

	for ind, subj in enumerate(subjects):
		temp1 = mne.Evoked(op.join(data_path, 'beta_ave_comb_planar_self_paced_{0}_hand_15_25/{1}_comb_planar_{0}_hand_self_paced.fif'.format(hands[0], subj))).crop(tmin=tmin, tmax=tmax)
		data1 = temp1.data.mean(axis = 1)
		
		temp2 = mne.Evoked(op.join(data_path, 'beta_ave_comb_planar_self_paced_{0}_hand_15_25/{1}_comb_planar_{0}_hand_self_paced.fif'.format(hands[1], subj))).crop(tmin=tmin, tmax=tmax)
		data2 = temp2.data.mean(axis = 1)
		

		contr[ind, 0, :] = data1
		contr[ind, 1, :] = data2
		
	comp1 = contr[:, 0, :]
	comp2 = contr[:, 1, :]
	t_stat, p_val = stats.ttest_rel(comp2, comp1, axis=0)

    #averaging by subjects
	comp1_mean = comp1.mean(axis=0)
	comp2_mean = comp2.mean(axis=0)
	
	return t_stat, p_val, comp1_mean, comp2_mean

#############################################################################
##################### непарный ttest #######################################	
def ttest_vs_zero(data_path, h, subjects, tmin, tmax): 
	contr = np.zeros((len(subjects), 1, 102))

	for ind, subj in enumerate(subjects):
		temp1 = mne.Evoked(op.join(data_path, 'beta_ave_comb_planar_self_paced_{0}_hand_15_25/{1}_comb_planar_{0}_hand_self_paced.fif'.format(h, subj))).crop(tmin=tmin, tmax=tmax)
		data1 = temp1.data.mean(axis = 1)
		contr[ind, 0, :] = data1
				
	comp1 = contr[:, 0, :]
	t_stat, p_val = stats.ttest_1samp(comp1, 0, axis=0)

	comp1_mean = comp1.mean(axis=0)
		
	return t_stat, p_val, comp1_mean	

##############################################################################################
#################################### FDR CORRECTION ########################################

############ space FDR for each sensor independently ######################################

def space_fdr(p_val_n):
    #print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    for i in range(temp.shape[1]):
        _, temp[:,i] = mul.fdrcorrection(p_val_n[:,i])
    return temp

'''
def space_fdr(p_val_n):
    print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    _, temp = mul.fdrcorrection(temp)
    return temp
'''


################## Full FDR -the correction is made once for the intire data array ############
def full_fdr(p_val_n):
    s = p_val_n.shape
    #print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    pval = np.ravel(temp)
    _, pval_fdr = mul.fdrcorrection(pval)
    pval_fdr_shape = pval_fdr.reshape(s)
    return pval_fdr_shape

################ make binary dataframe from pvalue (0 or 1) #########################
def p_val_binary(p_val_n, treshold):
	p_val =  copy.deepcopy(p_val_n)
	for raw in range(p_val.shape[0]):
		for collumn in range(p_val.shape[1]):
			if p_val[raw, collumn] < treshold:
				p_val[raw, collumn] = 1
			else:
				p_val[raw, collumn] = 0
	return p_val


###########################################################################################################
######################################### PLOT TOPOMAPS  ################################################

###################### строим topomaps со статистикой, для разницы между условиями #########################

def plot_deff_topo(p_val, temp, mean1, mean2): 	
    # plotting topomaps
        
    t = np.linspace(0, 0, num=1) 
    data = mean2 - mean1
    
    binary = p_val_binary(p_val, treshold = 0.05)
        
    evk_mean = mne.EvokedArray(data, temp.info)
                                 
    fig = evk_mean.plot_topomap(times = t, ch_type='planar1', units = 'dB', 
                             scalings = 1, show = False, colorbar = True, vmin = -3.0, vmax = 3.0, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o', markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))                          
                             
    return fig   

###################### строим topomaps со статистикой, для разницы c 0 #########################

def plot_topo_vs_zero(p_val, temp, mean1): 	
    
    t = np.linspace(0, 0, num=1) 
    data = mean1
    
    binary = p_val_binary(p_val, treshold = 0.05)
        
    evk_mean = mne.EvokedArray(data, temp.info)
                                 
    fig = evk_mean.plot_topomap(times = t, ch_type='planar1', units = 'dB', 
                             scalings = 1, show = False, colorbar = True, vmin = -3.0, vmax = 3.0, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o', markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

	
    return fig

