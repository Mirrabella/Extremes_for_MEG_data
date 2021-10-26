
import mne
import os.path as op
import numpy as np
import pandas as pd
from functions_right_baseline import *

L_freq = 15
H_freq = 26
f_step = 2

period_start = -0.800
period_end = 2.000

baseline = [-0.5, -0.1]

tmin = [-0.550, 0.100, 0.550]
tmax = [-0.100, 0.550, 1.000]

#active1 start
pref = ('active1', "st")


#active2 end
#pref = ('active2', "end")


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

freq_range = 'beta_15_25'

description = 'Получение таблиц для LMEM, средние значения беты на трех интервалах PreM, M, PostM и минимумы PreM, максимумы PostM, от времени реакции испытуемого RT'


data_path = '/net/synology/volume1/data/programs/ANYA/SPEECH_LEARN/RAW_trans/'

os.makedirs('/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/table_for_mem', exist_ok = True)
os.makedirs('/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/table_for_mem/table_for_mem_{0}_{1}'.format(pref[0], pref[1]), exist_ok = True)

PreM = []
M = []
PostM = []

minimum = []
maximum = []

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open("/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/table_for_mem/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')

###################################################################################################

for subj in subjects:
	mean_PreM, mean_M, mean_PostM, min_PreM, max_PostM = make_beta_signal(subj, pref, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, tmin, tmax)
	PreM.append(mean_PreM)
	M.append(mean_M)
	PostM.append(mean_PostM)
	
	minimum.append(min_PreM)
	maximum.append(max_PostM)

for j in range(102):
	df = pd.DataFrame()
	sensor_num = j
	for i, subj in enumerate(subjects):
		df_subj = make_subjects_df(subj, pref, PreM[i], M[i], PostM[i], minimum[i], maximum[i], sensor_num = j)
		df = df.append(df_subj)
	df.to_csv('/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/table_for_mem/table_for_mem_{0}_{1}/{0}_{1}_{2}.csv'.format(pref[0], pref[1], sensor_num))
	
	
		

