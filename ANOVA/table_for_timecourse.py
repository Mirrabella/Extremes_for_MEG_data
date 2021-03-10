import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
import statsmodels.stats.multitest as mul
from functions import beta
import os


# Номера сенсоров для усреднения

s = pd.read_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/sensors.csv', index_col ="Name")
left_group = s.loc[["MEG0432", "MEG0442", "MEG0422"]] #сенсоры для правой руки (группа сенсоров расположена слева)
right_group = s.loc[["MEG1142", "MEG1112", "MEG1132"]] #сенсоры для левой руки (группа сенсоров расположена справа)

# Получаем список порядковых номеров сенсоров
l_group_sensors = left_group['Unnamed: 0'].tolist()
r_group_sensors = right_group['Unnamed: 0'].tolist()



####################### Probing ########################
###################### RIGHT HAND ########################


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


hands = 'right'
condition = 'probing'
tmin = -1.0
tmax = 1.4

data_path = '/home/vtretyakova/Рабочий стол/beta_active_hands_15_25/beta_ave_comb_planar_active1_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_active1.fif"
    
interval, time = beta(subjects, data_path, planar, tmin, tmax)


three_sens_beta_all_subj = []    
for i in range(len(interval)):
    three_sens_beta = []
    for j in l_group_sensors:
        a = interval[i][j]
        three_sens_beta.append(a)
    b = np.array(three_sens_beta)    
    mean_amp = np.mean(b.data, axis = 0)
    three_sens_beta_all_subj.append(mean_amp)
    
os.makedirs('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand'.format(condition, hands), exist_ok=False)

for i in range(len(subjects)):    
    data = pd.DataFrame()
    data['Time, s'] = time.tolist()
    data['Beta average (three sens)'] = three_sens_beta_all_subj[i].tolist()
    data.to_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand/{2}.csv'.format(condition, hands, subjects[i]), index=False)


####################### LEFT HAND ########################
hands = 'left'
condition = 'probing'
tmin = -1.0
tmax = 1.4

data_path = '/home/vtretyakova/Рабочий стол/beta_active_hands_15_25/beta_ave_comb_planar_active1_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_active1.fif"
    
interval, time = beta(subjects, data_path, planar, tmin, tmax)


three_sens_beta_all_subj = []    
for i in range(len(interval)):
    three_sens_beta = []
    for j in r_group_sensors:
        a = interval[i][j]
        three_sens_beta.append(a)
    b = np.array(three_sens_beta)    
    mean_amp = np.mean(b.data, axis = 0)
    three_sens_beta_all_subj.append(mean_amp)
    
os.makedirs('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand'.format(condition, hands), exist_ok=False)

for i in range(len(subjects)):    
    data = pd.DataFrame()
    data['Time, s'] = time.tolist()
    data['Beta average (three sens)'] = three_sens_beta_all_subj[i].tolist()
    data.to_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand/{2}.csv'.format(condition, hands, subjects[i]), index=False)



####################### Tageted ########################
###################### RIGHT HAND ########################


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


hands = 'right'
condition = 'targeted'
tmin = -1.0
tmax = 1.4

data_path = '/home/vtretyakova/Рабочий стол/beta_active_hands_15_25/beta_ave_comb_planar_active2_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_active2.fif"
    
interval, time = beta(subjects, data_path, planar, tmin, tmax)


three_sens_beta_all_subj = []    
for i in range(len(interval)):
    three_sens_beta = []
    for j in l_group_sensors:
        a = interval[i][j]
        three_sens_beta.append(a)
    b = np.array(three_sens_beta)    
    mean_amp = np.mean(b.data, axis = 0)
    three_sens_beta_all_subj.append(mean_amp)
    
os.makedirs('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand'.format(condition, hands), exist_ok=False)

for i in range(len(subjects)):    
    data = pd.DataFrame()
    data['Time, s'] = time.tolist()
    data['Beta average (three sens)'] = three_sens_beta_all_subj[i].tolist()
    data.to_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand/{2}.csv'.format(condition, hands, subjects[i]), index=False)




####################### LEFT HAND ########################
hands = 'left'
condition = 'targeted'
tmin = -1.0
tmax = 1.4

data_path = '/home/vtretyakova/Рабочий стол/beta_active_hands_15_25/beta_ave_comb_planar_active2_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_active2.fif"
    
interval, time = beta(subjects, data_path, planar, tmin, tmax)


three_sens_beta_all_subj = []    
for i in range(len(interval)):
    three_sens_beta = []
    for j in r_group_sensors:
        a = interval[i][j]
        three_sens_beta.append(a)
    b = np.array(three_sens_beta)    
    mean_amp = np.mean(b.data, axis = 0)
    three_sens_beta_all_subj.append(mean_amp)
    
os.makedirs('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand'.format(condition, hands), exist_ok=False)

for i in range(len(subjects)):    
    data = pd.DataFrame()
    data['Time, s'] = time.tolist()
    data['Beta average (three sens)'] = three_sens_beta_all_subj[i].tolist()
    data.to_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand/{2}.csv'.format(condition, hands, subjects[i]), index=False)




####################### Self Paced ########################

####################### RIGHT HAND ########################

data_path = '/home/vtretyakova/Рабочий стол/selfpased_hands_15_25/beta_ave_comb_planar_self_paced_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_self_paced.fif"

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015')
        
tmin = -1.0
tmax = 1.4

hands = 'right'
condition = 'self_pased'

interval, time = beta(subjects, data_path, planar, tmin, tmax)


three_sens_beta_all_subj = []    
for i in range(len(interval)):
    three_sens_beta = []
    for j in l_group_sensors:
        a = interval[i][j]
        three_sens_beta.append(a)
    b = np.array(three_sens_beta)    
    mean_amp = np.mean(b.data, axis = 0)
    three_sens_beta_all_subj.append(mean_amp)
    
os.makedirs('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand'.format(condition, hands), exist_ok=False)

for i in range(len(subjects)):    
    data = pd.DataFrame()
    data['Time, s'] = time.tolist()
    data['Beta average (three sens)'] = three_sens_beta_all_subj[i].tolist()
    data.to_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand/{2}.csv'.format(condition, hands, subjects[i]), index=False)

                                                                                     
                                                                                              
####################### LEFT HAND ########################

data_path = '/home/vtretyakova/Рабочий стол/selfpased_hands_15_25/beta_ave_comb_planar_self_paced_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_self_paced.fif"

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
     
tmin = -1.0
tmax = 1.4

hands = 'left'
condition = 'self_pased'

interval, time = beta(subjects, data_path, planar, tmin, tmax)


three_sens_beta_all_subj = []    
for i in range(len(interval)):
    three_sens_beta = []
    for j in r_group_sensors:
        a = interval[i][j]
        three_sens_beta.append(a)
    b = np.array(three_sens_beta)    
    mean_amp = np.mean(b.data, axis = 0)
    three_sens_beta_all_subj.append(mean_amp)
    
os.makedirs('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand'.format(condition, hands), exist_ok=False)

for i in range(len(subjects)):    
    data = pd.DataFrame()
    data['Time, s'] = time.tolist()
    data['Beta average (three sens)'] = three_sens_beta_all_subj[i].tolist()
    data.to_csv('/home/vtretyakova/Рабочий стол/ANOVA_for_extrem/{0}_{1}_hand/{2}.csv'.format(condition, hands, subjects[i]), index=False)


                                                                                        
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
