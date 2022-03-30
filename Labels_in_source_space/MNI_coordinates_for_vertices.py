

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
subjects_dir = "/home/vtretyakova/Рабочий стол/speach_learn/Labels/freesurfer"

# усредненные данные по 3ем интервалам, нам нужен средний
stc = mne.read_source_estimate('/net/server/data/home/inside/Niherus_work_transfer/Make_source_for_beta/MAIN_SCRIPT/Source/SourceEstimate/beta_reactclean_15_26/p_val/p-val_full_fdr_r2-end_sub22_interv_merged-lh.stc')
stc.subject = "avg_platon_27sub"

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

#max_pval = []
#index_max_pval = []
for l in chosen_labels: 

    stc_in_label = donor.in_label(l)
    stc_in_label_data = stc_in_label.data
    n = len(stc_in_label_data)
    stc_in_label_data_reshape = np.reshape(stc_in_label_data, (n,))
    
    # sort p_value descending, take 10 first
    stc_in_label_data_reshape_sorted = -np.sort(-stc_in_label_data_reshape)
    max_pval_10 = stc_in_label_data_reshape_sorted[:10]
    #max_pval.append(stc_in_label_data_reshape_sorted[:10])
    # indexes of max pvalue, take 10 first

    ind = np.argsort(-stc_in_label_data_reshape)
    
    
    #index_max_pval.append(ind[:10])
    #print(len(max_pval))  
    #print(len(index_max_pval))

    #common indexes for vertices in label
    vertices_max_list = ind[:10].tolist()
    
    common_indexes_max = []
    for ind in vertices_max_list:
        # for left hemishere 
        #common_indexes_max.append(stc_in_label.vertices[0][ind])
        # for left hemishere
        common_indexes_max.append(stc_in_label.vertices[1][ind])
        
        
    common_indexes_max = np.array(common_indexes_max)
    
    #for left hemishere
    #mni_coordinate = mne.vertex_to_mni(common_indexes_max, 0, 'avg_platon_27sub', subjects_dir=subjects_dir)  
    
    #for right hemishere
    mni_coordinate = mne.vertex_to_mni(common_indexes_max, 1, 'avg_platon_27sub', subjects_dir=subjects_dir) 
    
    df = pd.DataFrame()
    df['p_value'] = max_pval_10.tolist()
    df['MNI_coordinates'] = mni_coordinate.tolist()
    
    df.to_csv('/home/vtretyakova/Рабочий стол/speach_learn/Labels/p_val_mne_coordinate/{0}.csv'.format(l))
    
    
    
    
    
    
