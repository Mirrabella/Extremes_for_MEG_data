# Plot only vertexes with max p_value to see their location

import os
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul
from matplotlib import pyplot as plt
import os.path as op


os.environ["SUBJECTS_DIR"] = "/home/vtretyakova/Рабочий стол/speach_learn/Labels/freesurfer"

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

brain_view = ['med', 'med', 'med', 'lat', 'lat']
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


############################ Index of maximal vertexes in labels ##################################
index_max_pval = []
for l in chosen_labels: 

    stc_in_label = donor.in_label(l)
    stc_in_label_data = stc_in_label.data
    n = len(stc_in_label_data)
    stc_in_label_data_reshape = np.reshape(stc_in_label_data, (n,))
    stc_in_label_data_reshape_abs = np.abs(stc_in_label_data_reshape)

    ind = np.argpartition(stc_in_label_data_reshape_abs, -10)[-10:]
    
    index_max_pval.append(ind)

#stc_in_label_max = donor.in_label(chosen_labels[0])


for ind, label in enumerate(chosen_labels):
    stc_in_label_max = donor.in_label(label)
    #stc_in_label_max

    n = len(stc_in_label_max.data)
    data_in_label_10_max_vert = np.zeros((n,1))

    for j in index_max_pval[ind]:
        #print(j)
        data_in_label_10_max_vert[j] = 1
        
    stc_in_label_max.data = data_in_label_10_max_vert

    scale = [0.95, 0.99, 1.0]

    brain = mne.viz.plot_source_estimates(stc_in_label_max, hemi='rh', views = [brain_view[ind]], time_viewer='auto', clim = dict(kind = 'value', pos_lims = scale), smoothing_steps = 1, background = 'white', spacing ='ico5')
    brain.add_label(label, color = 'green', borders=True)
        
    brain.save_image("/home/vtretyakova/Рабочий стол/speach_learn/Labels/labels_choosen_from_aparc2009_10_max_vert1/{0}.jpeg".format(chosen_labels_name[ind]))
    brain.close








