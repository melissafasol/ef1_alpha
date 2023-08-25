from operator import index
from tkinter.tix import Tree
import numpy as np
import pandas as pd 
import os
from pytools import average 
import scipy
from scipy.fft import fft, fftfreq
from scipy import signal

from preprocess import ExtractBrainStateEF1ALPHA
from filter import Filter
from power import PowerSpectrum, average_power_df
#from ef1_alpha_properties import mutant_seizure_ids, wildtype_seizure_ids
from ef1_alpha_properties import channels_dict, genotypes

seizure_numpy_folder = '/home/melissa/PREPROCESSING/EF1_ALPHA_preproc/seizure_npy_folder/'
seizure_csv_folder = '/home/melissa/PREPROCESSING/EF1_ALPHA_preproc/seizure_csv_files/'
seizure_files = os.listdir(seizure_csv_folder)
results_path = '/home/melissa/RESULTS/EF1_alpha_seizure_power/'


def seizure_epoch_bins(brain_state_file):
        
        sample_rate = 1000
        epoch_length = int(sample_rate * 1)
        
        seizure_start = brain_state_file.iloc[:, 1]
        seizure_end = brain_state_file.iloc[:, 2]

        zipped_time_values = list(zip([int((element + 5)*sample_rate) for element in seizure_start],
                                    [int((element + 5)*sample_rate) for element in seizure_end]))
        
        function_timebins = lambda epoch_start, epoch_end : list(range(epoch_start, epoch_end, epoch_length))
        
        timevalues_epochs = list(map(lambda x: function_timebins(x[0], x[1]), (zipped_time_values)))
        timevalues_array = list(np.concatenate(timevalues_epochs).flat)
        timevalues_array = [int(x) for x in timevalues_array]
        return timevalues_array

#for animal in mutant_seizure_ids:
seizure_power_ls = []
for file in seizure_files:
    try:
        seizure_time_file = pd.read_csv(seizure_csv_folder + file)
        anim_id = file[0:6]
        npy_file = file[0:14]
        headstage_letter = file[7:8]
        seizure_npy_file = np.load(seizure_numpy_folder + npy_file + '.npy')
        timevalues_array = seizure_epoch_bins(seizure_time_file)
        for column, channel in zip(seizure_npy_file.T, channels_dict[headstage_letter]):
            filter_steps = Filter(column, timevalues_array)
            filtered_data = filter_steps.butter_bandpass()
            power_steps = PowerSpectrum(filtered_data)
            power_array, frequency_array = power_steps.average_psd()
            frequency_values = np.linspace(0, 100, 2501)
            print(str(anim_id) + str(headstage_letter))
            if anim_id + headstage_letter in genotypes['wildtypes']:
                genotype = 'WT'
            if anim_id + headstage_letter in genotypes['ef1_alpha_knockouts']:
                genotype = 'EF1'
            dict_data = {'Animal_ID': [anim_id + headstage_letter]*len(power_array), 'Headstage':[headstage_letter]*len(power_array),
                    'Channel': [channel]*len(power_array),
                    'Power': power_array, 'Frequency': frequency_values, 'Genotype' : [genotype]*len(frequency_array)}
            df_test = pd.DataFrame(data = dict_data)
            seizure_power_ls.append(pd.DataFrame(data = dict_data))
    except:
        pass
    
    
    ## tomorrow add if recording is part 1 or part 2


seizure_power_df = pd.concat(seizure_power_ls)
seizure_power_df.to_csv(results_path + 'test_add5seconds_seizure_df_ef1.csv')
