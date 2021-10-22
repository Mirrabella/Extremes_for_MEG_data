import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
import statsmodels.stats.multitest as mul
import os


# We get an array with data for each subjects, and each sensor

############ MINIMUM ###############

#def min_beta_and_time_for_min(subjects, data_path, planar, tmin, tmax, h): # for extremums_search
def min_beta_and_time_for_min(subjects, data_path, planar, tmin, tmax):  # for ANOVA table
#Make list of evoked
    all_evoked = []
    for subj in subjects:
        #data = op.join(data_path, planar.format(subj, h)) # for extremums_search
        data = op.join(data_path, planar.format(subj)) # for ANOVA table
        evk = mne.Evoked(data)
        all_evoked.append(evk)

    #shift time scale if it is needed
    #what the hell is going on here????????
    #for i in all_evoked:
    #   i.shift_time(-2.0, relative=False)

# calculate average data for interval. You have to choose interval - downward, upward or susteined (look at the beggining of script)
    interval = []
    
    for i in all_evoked:
        x = i.crop(tmin=tmin, tmax=tmax)   #crop - mne function
        interval.append(x)
        
        # x = list of Evoked

    min_beta = []
    index_min_beta = []    #for searching of time point of min beta on sensor
    for i in interval:
        m = np.min(i.data, axis = 1)
        t = np.argmin(i.data, axis = 1) #indexes of min
        a = m.tolist()
        b = t.tolist()

        min_beta.append(a)
        index_min_beta.append(b)
    
    # search time of beta minimum
    time = []
    for i in range(len(index_min_beta)):
        time_per_subj = [] # 102 time point for every sensors
        for j in index_min_beta[i]:
            # find time between time points
            #interval[0].data.shape[1] - amount of points on interval
            # j - index of extremum point
            time_between_points = (tmin - tmax)/(interval[0].data.shape[1]-1)
            t = tmin - time_between_points*j
            time_per_subj.append(t)
        time.append(time_per_subj)

    #make np.array from list
    min_interval_array = np.array(min_beta)
    min_time_array = np.array(time)
    
    return(min_interval_array, min_time_array) 
#return array 102x28, e.g. sets power of min beta signal and time of min for each sensor for each subject
#28 - amount of subjects
#102 - amount of combined planars


############ MAXIMUM ###############

#def max_beta_and_time_for_max(subjects, data_path, planar, tmin, tmax, h): # for extremums_search
def max_beta_and_time_for_max(subjects, data_path, planar, tmin, tmax): # for ANOVA table
#Make list of evoked
    all_evoked = []
    for subj in subjects:
        #data = op.join(data_path, planar.format(subj, h)) # for extremums_search
        data = op.join(data_path, planar.format(subj)) # for ANOVA table
        evk = mne.Evoked(data)
        all_evoked.append(evk)

    #shift time scale if it is needed
    #what the hell is going on here????????
    #for i in all_evoked:
    #    i.shift_time(-2.0, relative=False)

# calculate average data for interval. You have to choose interval - downward, upward or sustained (look at the beggining of script)
    interval = []
    
    for i in all_evoked:
        x = i.crop(tmin=tmin, tmax=tmax)   #crop - mne function
        interval.append(x)

    #calculate mean beta on choosen interval for each subjects
    
    max_beta = []
    index_max_beta = []    
    for i in interval:
        m = np.max(i.data, axis = 1)
        t = np.argmax(i.data, axis = 1) #indexes of min
        a = m.tolist()
        b = t.tolist()

        max_beta.append(a)
        index_max_beta.append(b)
    
    # search time of beta minimum
    time = []
    for i in range(len(index_max_beta)):
        time_per_subj = [] # 102 time point for every sensors
        for j in index_max_beta[i]:
            # find time between time points
            #interval[0].data.shape[1] - amount of points on interval
            # j - index of extremum point
            time_between_points = (tmin - tmax)/(interval[0].data.shape[1]-1)
            t = tmin - time_between_points*j
            time_per_subj.append(t)
        time.append(time_per_subj)
        
    ############### Another method to find times ##################
    #np.array with time point the same for every sensors and every subjects
    
    '''
    time_array = interval[0].times
    
    for i in range(len(index_max_beta)):
        time_per_subj = [] # 102 time point for every sensors
        for j in index_max_beta[i]:
            time_per_subj.append(time_array[j])
    
        time.append(time_per_subj)
    '''

    #make np.array from list
    max_interval_array = np.array(max_beta)
    max_time_array = np.array(time)
    
    return(max_interval_array, max_time_array)        

#return array 102x28, e.g. sets power of max beta signal and time of max for each sensor for each subject   
#28 - amount of subjects
#102 - amount of combined planars



def dataframe_for_anova(subjects, data_path, planar, tmin_min, tmax_min, tmin_max, tmax_max, group_sensors, hand, condition, hemisphere):
    min_array, min_time_array = min_beta_and_time_for_min(subjects, data_path, planar, tmin = tmin_min, tmax = tmax_min)

    max_array, max_time_array = max_beta_and_time_for_max(subjects, data_path, planar, tmin = tmin_max, tmax = tmax_max)
    
    
    ################ MINIMUM ##################
    min_three_chan = [] # формируем список списков сотоящий из трех списков (сенсора), в каждом по 27 элементов (число испытуемых)
    for i in group_sensors:
        minimum = [] #для каждого из выбранных сенсоров выбираем максимум у для каждого испытуемого
        for j in range(len(min_array)):
            a = min_array[j][i]
            minimum.append(a)
        min_three_chan.append(minimum)
        
    # делаем np.array из списка
    min_three_chan = np.array(min_three_chan)   
    
    #Усредняем по каналам
    min_ave = np.mean(min_three_chan, axis = 0).tolist()
    
    ################### MAXIMUM ####################
    max_three_chan = [] # формируем список списков сотоящий из трех списков (сенсора), в каждом по 27 элементов (число испытуемых)
    for i in group_sensors:
        maximum = [] #для каждого из выбранных сенсоров выбираем максимум у для каждого испытуемого
        for j in range(len(max_array)):
            a = max_array[j][i]
            maximum.append(a)
        max_three_chan.append(maximum)
        
    # делаем np.array из списка
    max_three_chan = np.array(max_three_chan)   
    
    #Усредняем по каналам
    max_ave = np.mean(max_three_chan, axis = 0).tolist()
    
    h = [hand]*len(max_ave) # делаем список с количество элеметов, равному количеству испытуемых для наименования руки
    hemi = [hemisphere]*len(max_ave)
    
    сondit = [condition]*len(max_ave) #тоже что и предыдущее для кондищена
    
    return(min_ave, max_ave, h, сondit, hemi)
  
  
