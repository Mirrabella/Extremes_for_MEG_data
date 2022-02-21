# added explanation for script see timecourse_in_max_vertexes_in_label.ipynb

import os
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul
from matplotlib import pyplot as plt
import os.path as op

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
    '383_laan'
]

os.environ["SUBJECTS_DIR"] = "/home/vtretyakova/Рабочий стол/speach_learn/Labels/freesurfer"

# усредненные данные по 3ем интервалам, нам нужен средний
stc = mne.read_source_estimate('/net/server/data/home/inside/Niherus_work_transfer/Make_source_for_beta/MAIN_SCRIPT/Source/SourceEstimate/beta_reactclean_15_26/p_val/p-val_full_fdr_r2-end_sub22_interv_merged-lh.stc')
stc.subject = "avg_platon_27sub"


# данные для таймкурсов (не усредененные)
#active1
stc_active1_mean_beta = mne.read_source_estimate('/net/server/data/home/inside/Niherus_work_transfer/Make_source_for_beta/MAIN_SCRIPT/Source/SourceEstimate/beta_reactclean_15_26/mean_conds/mean_conds_reactactive1-st_sub22_integ50-lh.stc')
stc_active1_mean_beta.subject = "avg_platon_27sub"

#active2
stc_active2_mean_beta = mne.read_source_estimate('/net/server/data/home/inside/Niherus_work_transfer/Make_source_for_beta/MAIN_SCRIPT/Source/SourceEstimate/beta_reactclean_15_26/mean_conds/mean_conds_reactactive2-end_sub22_integ50-lh.stc')
stc_active2_mean_beta.subject = "avg_platon_27sub"



time_points = list(stc_active1_mean_beta.times)

# Читаем лейблы (они должны лежать в той директории, которую мы указали, т.е. во 
#/home/vtretyakova/Рабочий стол/speach_learn/Labels/freesurfer/avg_platon_27sub/label)

# Выбор лейблов смотри timecourse_for_max_vert_in_labels.ipynb
labels = mne.read_labels_from_annot('avg_platon_27sub', 'aparc.a2009s')

#left
'''
chosen_labels_name = [
    'G_and_S_cingul-Mid-Ant-lh',
    'G_cingul-Post-ventral-lh',
    'G_oc-temp_med-Parahip-lh',
    'S_front_inf-lh',
    'S_front_sup-lh'
    ]
'''    
#rigth

chosen_labels_name = [    
    'G_and_S_cingul-Mid-Ant-rh',
    'G_cingul-Post-ventral-rh',
    'G_oc-temp_med-Parahip-rh',
    'S_front_inf-rh',
    'S_front_sup-rh'
    ]
    
    
chosen_labels = [label for label in labels if label.name in chosen_labels_name]
print(chosen_labels)

############################### Находим 10 максимальных вертехсов в каждом лейбле ########################################
#Сейчас stc состоят из 3 точек, которые соответсвуют 3 усреденным интервалам. Поскольку мы ищем максимумы только на интервале M, который #соответствует средней точке, то нам необходимо получить отдельные файлы для каждого интервала

donor = mne.read_source_estimate('/net/server/data/home/inside/Niherus_work_transfer/Make_source_for_beta/MAIN_SCRIPT/Source/SourceEstimate/beta_reactclean_15_26/p_val_fdr/p-val_no_fdr_r1-st_vs_r2-end_sub22_0.1-0.55_merged')
donor.subject = "avg_platon_27sub"

stc_M_active2 = []
for i in range(len(stc.data)):
    s = stc.data[i][1]
    stc_M_active2.append(s)
    
print(len(stc_M_active2))

stc_M_active2 = np.array(stc_M_active2)
stc_M_active2 = stc_M_active2[:, np.newaxis]
print(stc_M_active2.shape) 
donor.data = stc_M_active2


############################ Grand Average ##################################
index_max_pval = []
for l in chosen_labels: 

    stc_in_label = donor.in_label(l)
    stc_in_label_data = stc_in_label.data
    n = len(stc_in_label_data)
    stc_in_label_data_reshape = np.reshape(stc_in_label_data, (n,))
    stc_in_label_data_reshape_abs = np.abs(stc_in_label_data_reshape)

    ind = np.argpartition(stc_in_label_data_reshape_abs, -10)[-10:]
    
    index_max_pval.append(ind)
    
print(len(index_max_pval))
    
#index_max_pval_expend = index_max_pval+index_max_pval # делаем рассширенный список индексов - начала 5 элементов для левого ПШ, потом 5 для правого


################ Записываем данные и строим графики для Гранд авередж ###################################
data_for_GA_timecourses = pd.DataFrame()
data_for_GA_timecourses['time_points'] = time_points


for idx, l in enumerate(chosen_labels):
    #Active 1
    stc_active1_mean_beta_in_label = stc_active1_mean_beta.in_label(l)
    stc_active1_mean_beta_in_label_data = stc_active1_mean_beta_in_label.data
    stc_active1_mean_beta_in_label_data_for_timecourse = stc_active1_mean_beta_in_label_data[index_max_pval[idx]]   
    stc_active1_mean_beta_in_label_data_for_timecourse_mean = stc_active1_mean_beta_in_label_data_for_timecourse.mean(axis = 0)

    beta_in_active1_label = list(stc_active1_mean_beta_in_label_data_for_timecourse_mean)
    data_for_GA_timecourses['beta_in_active1_label %s'%l.name] = beta_in_active1_label

    #Active2

    stc_active2_mean_beta_in_label = stc_active2_mean_beta.in_label(l)

    stc_active2_mean_beta_in_label_data = stc_active2_mean_beta_in_label.data
    stc_active2_mean_beta_in_label_data_for_timecourse = stc_active2_mean_beta_in_label_data[index_max_pval[idx]]

    stc_active2_mean_beta_in_label_data_for_timecourse_mean = stc_active2_mean_beta_in_label_data_for_timecourse.mean(axis = 0)
    beta_in_active2_label = list(stc_active2_mean_beta_in_label_data_for_timecourse_mean)
    data_for_GA_timecourses['beta_in_active2_label %s'%l.name] = beta_in_active2_label


    plt.figure() #создаем рисунок 
    plt.rcParams['axes.facecolor'] = 'none' # делаем его прозрачным
    plt.xlim(-1.7, 1.7) #назначаем границы рисунка по х
    plt.ylim(-0.3, 0.3) #назначаем границы рисунка по у
    plt.title('active1 - blue, active2 - red, %s'%l.name, fontsize = 8) 
    plt.plot([0, 0.001], [-1, 1], color='k', linewidth=3, linestyle='--', zorder=1) # вертикальная линия, которая показывает, где находится наше событие
    plt.plot([-1.8, 1.8], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1) # нулевая линия по горизонтали

    plt.plot(time_points, beta_in_active1_label, color='b', linewidth=3) # рисует график первого кондишена (всегда синий)
    plt.plot(time_points, beta_in_active2_label, color='r', linewidth=3) # active 2    

    plt.savefig('/home/vtretyakova/Рабочий стол/speach_learn/Labels/Grand_average_in_labels_new/{0}.jpeg'.format(l.name), transparent=True)
    plt.close() 
    
    
data_for_GA_timecourses.to_csv('/home/vtretyakova/Рабочий стол/speach_learn/Labels/Grand_average_in_labels_new/data_for_GA_timecourses-rh.csv')



#################### Data for timecourses in labels for each subj #################################

data_path = '/net/server/data/home/inside/Niherus_work_transfer/Make_source_for_beta/MAIN_SCRIPT/Source/SourceEstimate/beta_reactclean_15_26'
for subj in subjects:
    data_for_indiv_timecourses = pd.DataFrame()
    data_for_indiv_timecourses['time_points'] = time_points

    stc_active1_beta = mne.read_source_estimate(op.join(data_path, '{0}_active1-st_react_int_50ms-lh.stc'.format(subj)))
    stc_active1_beta.subject = "avg_platon_27sub"
    stc_active1_beta = stc_active1_beta.resample(sfreq=20)
    
    stc_active2_beta = mne.read_source_estimate(op.join(data_path, '{0}_active2-end_react_int_50ms-lh.stc'.format(subj)))
    stc_active2_beta.subject = "avg_platon_27sub"
    stc_active2_beta = stc_active2_beta.resample(sfreq=20)
    
    for idx, l in enumerate(chosen_labels):    
        #Active 1
        stc_active1_beta_in_label = stc_active1_beta.in_label(l)
        stc_active1_beta_in_label_data = stc_active1_beta_in_label.data
        stc_active1_beta_in_label_data_for_timecourse = stc_active1_beta_in_label_data[index_max_pval[idx]]   
        stc_active1_beta_in_label_data_for_timecourse_mean = stc_active1_beta_in_label_data_for_timecourse.mean(axis = 0)

        beta_in_active1_label = list(stc_active1_beta_in_label_data_for_timecourse_mean)
        data_for_indiv_timecourses['beta_in_active1_label %s'%l.name] = beta_in_active1_label

        #Active2
        
        stc_active2_beta_in_label = stc_active2_beta.in_label(l)

        stc_active2_beta_in_label_data = stc_active2_beta_in_label.data
        stc_active2_beta_in_label_data_for_timecourse = stc_active2_beta_in_label_data[index_max_pval[idx]]

        stc_active2_beta_in_label_data_for_timecourse_mean = stc_active2_beta_in_label_data_for_timecourse.mean(axis = 0)
        beta_in_active2_label = list(stc_active2_beta_in_label_data_for_timecourse_mean)
        data_for_indiv_timecourses['beta_in_active2_label %s'%l.name] = beta_in_active2_label
    
    data_for_indiv_timecourses.to_csv('/home/vtretyakova/Рабочий стол/speach_learn/Labels/Indiv_in_labels_new/{0}_data_for_timecourses-rh.csv'.format(subj))







