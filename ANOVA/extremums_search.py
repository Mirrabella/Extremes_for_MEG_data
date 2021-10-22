########### Change the lines in the function.py (lines def and data in the extremum search function)

import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
import statsmodels.stats.multitest as mul
import os
from functions import min_beta_and_time_for_min, max_beta_and_time_for_max

#load donor
temp = mne.Evoked("/home/vtretyakova/Рабочий стол/speach_learn/Extremes/donor-ave.fif")

temp.times = np.arange(0, 2.01, 1)

# for selfpased
'''
subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015') # для данного испытуемого не нашлось подходящих эвентов
'''

# for active

subjects = [ 
    '030_koal',
    '051_vlro',
    '128_godz',
    '136_spar',
    '176_nama',
    '202_skol',
    '211_gnlu',
    '277_trev',
    '307_firo',
    '308_lodm',
    '317_arel',
    '355_slya',
    '372_skju',
    '389_revi',
    '390_shko',
    '394_tiev',
    '402_maev',
    '406_bial',
    '409_kodm',
    '415_yael',
    '436_buni',
    '383_laan']

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

hands = ['right', 'left']

for h in hands:
        # for self paced
        '''                    
        data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/selfpased_hands_15_25/beta_ave_comb_planar_self_paced_{0}_hand_15_25'.format(h)
                   #L001_comb_planar_selfpased_right_hand.fif
        planar = "{0}_comb_planar_{1}_hand_self_paced.fif"
        '''
        
        
        # for active
        
        data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active2_{0}_hand_15_25'.format(h)
        
        planar = "{0}_comb_planar_{1}_hand_active2.fif"
        
        # Находим минимумы и максимумы беты
        min_interval_array_self_pace, min_time_array_self_pace  = min_beta_and_time_for_min(subjects, data_path, planar, tmin = tmin_min, 
                                                                                       tmax = tmax_min, h = h)

        max_interval_array_self_pace, max_time_array_self_pace = max_beta_and_time_for_max(subjects, data_path, planar, tmin = tmin_max, 
                                                                                                      tmax = tmax_max, h = h)

        #  усредняем между испытуемыми
        minimum = np.mean(min_interval_array_self_pace, axis = 0)
        min_array = minimum.reshape(102, 1)
        
        max_sp = np.mean(max_interval_array_self_pace, axis = 0)
        max_array_sp = max_sp.reshape(102, 1) # change shape of array for topomaps plotting
        
        # plotting topomaps
        
        t = np.linspace(0, 0, num=1) 
        
        evk_mean = mne.EvokedArray(min_array, temp.info)
        fig1 = evk_mean.plot_topomap(times = t, ch_type='planar1', units = 'dB', 
                             scalings = 1, show = False, colorbar = True, vmin = -5.0, vmax = 5.0) 
                             
        fig1.savefig('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/topomaps/min_active2_{0}_hand_15_25.jpeg'.format(h), dpi = 300)                                 
        
        evk_mean = mne.EvokedArray(max_array_sp, temp.info) #make Evoked from np.array
        fig = evk_mean.plot_topomap(times = t, ch_type='planar1', units = 'dB', 
        scalings = 1, show = False, colorbar = True, vmin = -5.0, vmax = 5.0)
        
        fig.savefig('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/topomaps/max_active2_{0}_hand_15_25.jpeg'.format(h), dpi = 300)                              
        
        
        
        
                                                                                                      
        s = pd.read_csv('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/sensors.csv')

        maximum_list_sp = max_sp.tolist()
        minimum_list_sp = minimum.tolist()

        time_max_average_sp = np.mean(max_time_array_self_pace, axis = 0)
        time_min_average_sp = np.mean(min_time_array_self_pace, axis = 0)

        s['Maximum beta'] = maximum_list_sp
        s['Time max'] = time_max_average_sp

        s2 = pd.read_csv('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/sensors.csv')
        s2['Minimum beta'] = minimum_list_sp
        s2['Time min'] = time_min_average_sp

        sorted_max = s.sort_values(by='Maximum beta', ascending=False)
        del sorted_max['Unnamed: 0']
        sorted_max.rename(columns = {'Name' : 'Name sensors with max beta'}, inplace = True)

        sorted_min = s2.sort_values(by='Minimum beta')
        del sorted_min['Unnamed: 0']
        sorted_min.rename(columns = {'Name' : 'Name sensors with min beta'}, inplace = True)

        Name_max = sorted_max['Name sensors with max beta'].tolist()
        time_max = sorted_max['Time max'].tolist()
        Name_min = sorted_min['Name sensors with min beta'].tolist()
        beta_min = sorted_min['Minimum beta'].tolist()
        beta_max = sorted_max['Maximum beta'].tolist()
        time_min = sorted_min['Time min'].tolist()

        full = pd.DataFrame()
        full['Name sensors with max beta'] = Name_max
        full['Maximum beta'] = beta_max
        full['Time max'] = time_max
        full['Name sensors with min beta'] = Name_min
        full['Minimum beta'] = beta_min
        full['Time min'] = time_min
                                                                                                      
        full.to_csv('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/extremums_value/active2_{0}_hand_15_25.csv'.format(h))                                                                                              
                                                                                              
                                                                                            
                                                                                              
                                                                                              
