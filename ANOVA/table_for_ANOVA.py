########### Change the lines in the function.py (lines def and data in the extremum search function)

import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
import statsmodels.stats.multitest as mul
from functions import min_beta_and_time_for_min, max_beta_and_time_for_max, dataframe_for_anova

HEMISPHERE = []
SUBJ = []
HAND = []
MIN = []
MAX = []
CONDITION = []

# Номера сенсоров для усреднения

s = pd.read_csv('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/sensors.csv', index_col ="Name")
left_group = s.loc[["MEG0432", "MEG0442", "MEG0422"]] #сенсоры для правой руки (группа сенсоров расположена слева)
right_group = s.loc[["MEG1142", "MEG1112", "MEG1132"]] #сенсоры для левой руки (группа сенсоров расположена справа)

# Получаем список порядковых номеров сенсоров
l_group_sensors = left_group['Unnamed: 0'].tolist()
r_group_sensors = right_group['Unnamed: 0'].tolist()



####################### Probing ########################
###################### RIGHT HAND (LEFT GROUP OF SENSORS) ########################


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
group_sensors = l_group_sensors
hemisphere = 'contralateral'
condition = 'probing'

#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0


data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active1_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_active1.fif"
    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova (subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)

HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit

###################### RIGHT HAND (RIGHT GROUP OF SENSORS) ########################
'''

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
'''

hands = 'right'
group_sensors = r_group_sensors
hemisphere = 'ipsilateral'
condition = 'probing'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0
'''
data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active1_right_hand_15_25'
planar = "{0]_comb_planar_right_hand_active1.fif"
'''    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova (subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)

HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit


####################### LEFT HAND (RIGHT GROUP OF SENSORS) ########################

hands = 'left'
group_sensors = r_group_sensors
hemisphere = 'contralateral'
condition = 'probing'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0


data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active1_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_active1.fif"
    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova (subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)

HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit

####################### LEFT HAND (LEFT GROUP OF SENSORS) ########################

hands = 'left'
group_sensors = l_group_sensors
hemisphere = 'ipsilateral'
condition = 'probing'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0
'''
data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active1_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_active1.fif"
'''    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova (subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)

HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit

####################### Tageted ########################
###################### RIGHT HAND (LEFT GROUP OF SENSORS) ########################

'''
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
'''

hands = 'right'
group_sensors = l_group_sensors
hemisphere = 'contralateral'
condition = 'targeted'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active2_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_active2.fif"
    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)


HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit

###################### RIGHT HAND (RIGHT GROUP OF SENSORS) ########################

'''
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
'''

hands = 'right'
group_sensors = r_group_sensors
hemisphere = 'ipsilateral'
condition = 'targeted'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0
'''
data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active2_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_active2.fif"
'''    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)


HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit



####################### LEFT HAND (RIGHT GROUP OF SENSORS) ########################
hands = 'left'
group_sensors = r_group_sensors
hemisphere = 'contralateral'
condition = 'targeted'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active2_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_active2.fif"
    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)


HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit

####################### LEFT HAND (LEFT GROUP OF SENSORS) ########################
hands = 'left'
group_sensors = l_group_sensors
hemisphere = 'ipsilateral'
condition = 'targeted'
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0
'''
data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/beta_active_hands_15_25/beta_ave_comb_planar_active1_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_active2.fif"
'''    
min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)


HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit

####################### Self Paced ########################

####################### RIGHT HAND (LEFT GROUP OF SENSORS) ########################

data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/selfpased_hands_15_25/beta_ave_comb_planar_self_paced_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_self_paced.fif"

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015')
        
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

hands = 'right'
group_sensors = l_group_sensors
hemisphere = 'contralateral'
condition = 'self_pased'

min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)


HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit                                                                                      


####################### RIGHT HAND (RIGHT GROUP OF SENSORS) ########################
'''
data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/selfpased_hands_15_25/beta_ave_comb_planar_self_paced_right_hand_15_25'
planar = "{0}_comb_planar_right_hand_self_paced.fif"

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015')
'''        
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

hands = 'right'
group_sensors = r_group_sensors
hemisphere = 'ipsilateral'
condition = 'self_pased'

min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)


HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit  
                                                                                              
####################### LEFT HAND (RIGHT GROUP OF SENSORS) ########################

data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/selfpased_hands_15_25/beta_ave_comb_planar_self_paced_left_hand_15_25'
planar = "{0}_comb_planar_left_hand_self_paced.fif"
'''
subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:
        subjects += ['L0' + str(i)]
        
subjects.remove('L015')        
'''     
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

hands = 'left'
group_sensors = r_group_sensors
hemisphere = 'contralateral'
condition = 'self_pased'

min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)

HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit                                                                                               
                                                                                              
####################### LEFT HAND (LEFT GROUP OF SENSORS) ########################
'''
data_path = '/home/vtretyakova/Рабочий стол/speach_learn/Extremes/selfpased_hands_15_30/beta_left_hand_comb_planar'
planar = "{0}_comb_planar_selfpased_left_hand.fif"

subjects = []
for i in range(1,29):
    if i < 10:
        subjects += ['L00' + str(i)]
    else:                                                                              
          
        subjects += ['L0' + str(i)]
        
subjects.remove('L015') 
'''    
#tmin = -1.0
#tmax = 1.4

# минимумы ищем в интервала pre movements        
tmin_min = -0.55
tmax_min = -0.1


# максимумы ищем в интервала post movements 
tmin_max = 0.55
tmax_max = 1.0

hands = 'left'
group_sensors = l_group_sensors
hemisphere = 'ipsilateral'
condition = 'self_pased'

min_ave, max_ave, h, condit, hemi = dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hands, condition, hemisphere)

HEMISPHERE = HEMISPHERE + hemi
SUBJ = SUBJ + subjects
HAND = HAND + h
MIN = MIN + min_ave
MAX = MAX + max_ave
CONDITION = CONDITION + condit                
             
                
                                                                                              
table_for_anova = pd.DataFrame()
table_for_anova['Subject'] = SUBJ
table_for_anova['Condition'] = CONDITION
table_for_anova['Hand'] = HAND
table_for_anova['Hemisphere'] = HEMISPHERE
table_for_anova['Minimum beta'] = MIN
table_for_anova['Maximum beta'] = MAX  

table_for_anova.to_csv('/home/vtretyakova/Рабочий стол/speach_learn/Extremes/table_for_anova_hemisphere_short_int_15_25.csv', index=False)
                                                                                        
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
