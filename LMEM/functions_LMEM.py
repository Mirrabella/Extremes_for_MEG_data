
import mne
import os.path as op
import os
import numpy as np
import pandas as pd

def read_events(filename):
    with open(filename, "r") as f:
        b = f.read().replace("[","").replace("]", "")
        b = b.split("\n")
        b = list(map(str.split, b))
        b = list(map(lambda x: list(map(int, x)), b))
        return np.array(b)


def combine_planar_Epoches_TFR(EpochsTFR):
	ep_TFR_planar1 = EpochsTFR.copy(); 
	ep_TFR_planar2 = EpochsTFR.copy()
	ep_TFR_planar1.pick_types(meg='planar1')
	ep_TFR_planar2.pick_types(meg='planar2')

	#grad_RMS = np.power((np.power(evk_planar1.data, 2) + np.power(evk_planar2.data, 2)), 1/2)
	combine = ep_TFR_planar1.data + ep_TFR_planar2.data
	ep_TFR_planar1.data = combine

	return ep_TFR_planar1

def make_beta_signal(subj, pref, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, tmin, tmax):
    freqs = np.arange(L_freq, H_freq, f_step)
    raw_file = op.join(data_path, "{0}/{0}_{1}_raw_tsss_bads_trans.fif".format(subj, pref[0]))

    raw_data = mne.io.Raw(raw_file, preload=True)


    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		
	#read events
	#events for baseline
    events = read_events('/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/mark_of_stim/{0}_{1}_w_{2}.txt'.format(subj, pref[0], pref[1]))
	#events for reaction, which we need
    events_react = read_events('/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/mark_of_stim/{0}_{1}_r_{2}.txt'.format(subj, pref[0], pref[1]))
	
#epochs for baseline
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, picks = picks, preload = True)
    epochs.resample(300)

    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	
    #add up all values according to the frequency axis
    b_line = freq_show_baseline.data.sum(axis=-2)
	
	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
    
    # выстраиваем в ряд бейзлайны для каждого из 28 эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    b_line = b_line.reshape(a, b * c)
	

	####### ДЛЯ ДАННЫХ ##############

    epochs = mne.Epochs(raw_data, events_react, event_id = None, tmin = period_start, 
		            tmax = period_end, picks = picks, preload = True)
		   
    epochs.resample(300)

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False)

    temp = freq_show.data.sum(axis=2)
	
	####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
	
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
	
    b = b_line.mean(axis=-1)
	
    b_line_new_shape = b[:, np.newaxis, np.newaxis]
        
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = np.log10(data/b_line_new_shape)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    
    freq_show.data = data
    
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
    
    # freq_show.data.shape - (28, 306, 1, 840) - epochs x channel x freq x time point
    
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
	
    comb_planar = combine_planar_Epoches_TFR(freq_show)
    # comb_planar.data.shape - (28, 102, 1, 840) - epochs x channel x freq x time point

    PreM = comb_planar.copy().crop(tmin=tmin[0], tmax=tmax[0])
    #PreM.data.shape - (28, 102, 1, 136) - epochs x channel x freq x time point	    
    M = comb_planar.copy().crop(tmin=tmin[1], tmax=tmax[1])   #crop - mne function	    
    PostM = comb_planar.copy().crop(tmin=tmin[2], tmax=tmax[2])

    #averaging by time points
    mean_PreM  = PreM.data.mean(axis=-1)
    #mean_PreM.shape - (28, 102, 1) - pochs x channel x freq
    mean_M  = M.data.mean(axis=-1)
    mean_PostM  = PostM.data.mean(axis=-1)
    
    # looking for extremes
    min_PreM = np.min(PreM.data, axis = -1)
    max_PostM = np.max(PostM.data, axis = -1)
    #max_PostM.shape - (28, 102, 1) - pochs x channel x freq
    
    
    # removing frequency axis
    mean_PreM_rsh = mean_PreM.reshape(28,102)
    mean_M_rsh = mean_M.reshape(28,102)
    mean_PostM_rsh = mean_PostM.reshape(28,102)
    
    min_PreM_rsh = min_PreM.reshape(28,102)
    max_PostM_rsh = max_PostM.reshape(28,102)
    

    return (mean_PreM_rsh, mean_M_rsh, mean_PostM_rsh, min_PreM_rsh, max_PostM_rsh)



def make_subjects_df(subj, pref, mean_PreM_rsh, mean_M_rsh, mean_PostM_rsh, min_PreM_rsh, max_PostM_rsh, sensor_num):

	events = read_events('/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/mark_of_stim/{0}_{1}_r_{2}.txt'.format(subj, pref[0], pref[1]))
	events_list = []

	for i in range(28):
		a = events[i][2]
		events_list.append(a)
	    
	RTs = np.loadtxt("/home/vtretyakova/Рабочий стол/speach_learn/MEM_old_new_baseline_swift/times/{1}_{2}/{0}_{1}_{2}.txt".format(subj, pref[0], pref[1], dtype='float'))

	RTs = RTs.tolist()
	# Вычитаем лаг в 30 мс (задержка между меткой и тем, когда человек слышит сигнал)
	RTs[:] = [x - 0.03 for x in RTs]

	subject = [subj]*28

	beta_power_PreM = []
    
    ############## mean beta power on interval ###############
	for i in range(28):
		a = mean_PreM_rsh[i][sensor_num]
		beta_power_PreM.append(a)
	    
	beta_power_M = []

	for i in range(28):
		a = mean_M_rsh[i][sensor_num]
		beta_power_M.append(a)
	    
	beta_power_PostM = []

	for i in range(28):
		a = mean_PostM_rsh[i][sensor_num]
		beta_power_PostM.append(a)

    ############# Extremes ################

	min_beta_PreM = []
    #min_beta_PreM = []

	for i in range(28):
		a = min_PreM_rsh[i][sensor_num]
		min_beta_PreM.append(a)

	max_beta_PostM = []		
    #max_beta_PostM = []

	for i in range(28):
		a = max_PostM_rsh[i][sensor_num]
		max_beta_PostM.append(a)		
		
	    
	df = pd.DataFrame()


	df['beta_power_PreM'] = beta_power_PreM
	df['beta_power_M'] = beta_power_M
	df['beta_power_PostM'] = beta_power_PostM
	df['min_beta_PreM'] = min_beta_PreM
	df['max_beta_PostM'] = max_beta_PostM
	df['stimulus'] = events_list
	df['RTs'] = RTs
	df['subjects'] = subject

	return (df)
