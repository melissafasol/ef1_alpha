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
from ef1_alpha_properties import recordings_1_channels, recordings_2_channels, channels_dict 

#paths 
recording_path = '/home/melissa/PREPROCESSING/EF1_ALPHA'
brain_state_path = '/home/melissa/PREPROCESSING/EF1_ALPHA/brain_state_folder'

recordings_letters_1 = ['A', 'A_1', 'B', 'C', 'D']
recordings_letters_2 = ['A', 'A_1', 'B', 'B_1' 'C', 'D']

one_recording = []
two_recording = []

brainstates = ['W', 'R', 'N']

# for headstage_letters in recordings_letters_1:
#     for anim_id in recordings_1_channels[headstage_letters]:
#         preprocessing_steps = ExtractBrainStateEF1ALPHA

for brainstate in brainstates:
    for headstage_letters in recordings_letters_2:
        for anim_id in recordings_2_channels[headstage_letters]:
            preprocessing_steps = ExtractBrainStateEF1ALPHA(anim_id, recording_path, brain_state_path, 
                                                            headstage_letters, recording_number=2)
            part_1, part_2 = preprocessing_steps.load_npy_recordings()
            part_1_br_state, part_2_br_state = preprocessing_steps.load_brain_state_file()
            if part_1 and part_2 is not None:
                epoch_indices_1 = preprocessing_steps.remove_E_epochs(part_1_br_state, brain_state_letter=brainstate)
                epoch_indices_2 = preprocessing_steps.remove_E_epochs(part_2_br_state, brain_state_letter=brainstate)
                epoch_bins_1 = preprocessing_steps.get_epoch_indices(part_1_br_state, epoch_indices_1)
                epoch_bins_2 = preprocessing_steps.get_epoch_indices(part_2_br_state, epoch_indices_2)
                for column, channel in zip(part_1_br_state.T, channels_dict[headstage_letters]):
                    filter_steps = Filter(column, epoch_bins_1)
                    filtered_data_1 = filter_steps.butter_bandpass()
                    power_steps = PowerSpectrum(filtered_data_1)
                    power_array_part_1, frequency_array_part_1 = power_steps.average_psd()
                for column, channel in zip(part_2_br_state.T, channels_dict[headstage_letters]):
                    filter_steps = Filter(column, epoch_bins_2)
                    filtered_data_2 = filter_steps.butter_bandpass()
                    power_steps = PowerSpectrum(filtered_data_2)
                    power_array_part_2, frequency_array_part_2 = power_steps.average_psd()
                average_power_array = average_power_df(power_array_part_1, power_array_part_2)
                dict_data = {'Animal_ID': [anim_id]*len(average_power_array), 'Headstage':[headstage_letters]*len(average_power_array),
                            'Channel': [channel]*len(average_power_array), 'Brainstate': [brainstate]*len(average_power_array),
                            'Power': average_power_array, 'Frequency': frequency_array_part_1,}
                two_recording.append(pd.DataFrame(data=dict_data))
    merged_power_file = pd.conctenate(one_recording, axis = 0).drop_duplicates().reset_index(drop = True)
    os.chdir('/home/melissa/RESULTS/EF1_ALPHA/2_REC')
    merged_power_file.to_csv(str(brainstate) + '_2_rec.csv', index = True)
