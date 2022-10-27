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
from ef1_alpha_properties import recordings_1_channel, recordings_2_channels, channels_dict, genotypes

#paths 
recording_path = '/home/melissa/PREPROCESSING/EF1_ALPHA'
brain_state_path = '/home/melissa/PREPROCESSING/EF1_ALPHA/reformatted_brain_states'

recordings_letters_1 =  ['A', 'A_1', 'B', 'C', 'D']
recordings_letters_2 = ['A', 'A_1', 'B', 'B_1', 'C', 'D']
recording_letters_notrunning_2 = ['A', 'B', 'D']
recording_letters_notrunning_1 = ['C']


brainstates = ['seizure']


for brainstate in brainstates:
    one_recording = []
    for headstage_letters in recordings_letters_1:
        print(headstage_letters)
        for anim_id in recordings_1_channel[headstage_letters]:
            print('processing ' + str(anim_id))
            preprocessing_steps = ExtractBrainStateEF1ALPHA(anim_id, recording_path, brain_state_path, 
                                                            headstage_letters, recording_number=1)
            npy_recording = preprocessing_steps.load_npy_recordings()
            br_state_file = preprocessing_steps.load_brain_state_file()
            br_state_indices = preprocessing_steps.process_brainstate_file(br_state_file, brainstate)
            if len(br_state_indices) > 0:
                epoch_bins = preprocessing_steps.create_epoch_bins(br_state_file, br_state_indices)    
                for column, channel in zip(npy_recording.T, channels_dict[headstage_letters]):
                    filter_steps = Filter(column, epoch_bins)
                    filtered_data = filter_steps.butter_bandpass()
                    power_steps = PowerSpectrum(filtered_data)
                    power_array, frequency_array = power_steps.average_psd()
                    print(str(anim_id) + str(headstage_letters))
                    if anim_id + headstage_letters in genotypes['wildtypes']:
                        genotype = 'WT'
                    if anim_id + headstage_letters in genotypes['ef1_alpha_knockouts']:
                        genotype = 'EF1'
                    dict_data = {'Animal_ID': [anim_id + headstage_letters]*len(power_array), 'Headstage':[headstage_letters]*len(power_array),
                            'Channel': [channel]*len(power_array), 'Brainstate': [brainstate]*len(power_array),
                            'Power': power_array, 'Frequency': frequency_array, 'Genotype' : [genotype]*len(frequency_array)}
                    df_test = pd.DataFrame(data = dict_data)
                    one_recording.append(pd.DataFrame(data = dict_data))
            else: 
                print('no epochs for ' + str(anim_id) + ' ' + str(brainstate))
    merged_power_file = pd.concat(one_recording, axis = 0).drop_duplicates().reset_index(drop = True)
    os.chdir('/home/melissa/RESULTS/EF1_ALPHA/debug')
    merged_power_file.to_csv(str(brainstate) + '_1_rec.csv', index = True)
    print('data saved for one recording ' + str(brainstate))


for brainstate in brainstates: 
    two_recording = []        
    for headstage_letters in recordings_letters_2:
        print(headstage_letters)
        for anim_id in recordings_2_channels[headstage_letters]:
            print('processing data for ' + str(anim_id) + 'for ' + str(brainstate))    
            preprocessing_steps = ExtractBrainStateEF1ALPHA(anim_id, recording_path, brain_state_path, headstage_letters, recording_number=2)
            part_1, part_2 = preprocessing_steps.load_npy_recordings()
            part_1_br_state, part_2_br_state = preprocessing_steps.load_brain_state_file()
            epoch_indices_1 = preprocessing_steps.process_brainstate_file(part_1_br_state, brainstate)
            epoch_indices_2 = preprocessing_steps.process_brainstate_file(part_2_br_state, brainstate)
            if type(epoch_indices_1) == list:
                epoch_bins_1 = preprocessing_steps.create_epoch_bins(part_1_br_state, epoch_indices_1)
                for column, channel in zip(part_1.T, channels_dict[headstage_letters]):
                    filter_steps = Filter(column, epoch_bins_1)
                    filtered_data_1 = filter_steps.butter_bandpass()
                    power_steps = PowerSpectrum(filtered_data_1)
                    power_array_part_1, frequency_array_part_1 = power_steps.average_psd()
                    if anim_id + headstage_letters in genotypes['wildtypes']:
                        genotype = 'WT'
                    if anim_id + headstage_letters in genotypes['ef1_alpha_knockouts']:
                        genotype = 'EF1'
                    dict_data = {'Animal_ID': [anim_id + headstage_letters]*len(frequency_array_part_1), 'Headstage':[headstage_letters]*len(frequency_array_part_1),
                            'Channel': [channel]*len(frequency_array_part_1), 'Brainstate': [brainstate]*len(frequency_array_part_1),
                            'Power': power_array_part_1, 'Frequency': frequency_array_part_1, 'Genotype' : [genotype]*len(frequency_array_part_1)}
                    print('data saved for ' + str(anim_id))
                    two_recording.append(pd.DataFrame(data=dict_data))
            else:
                print('no epochs for ' + str(anim_id) + ' ' + str(brainstate))
            if len(epoch_indices_2) > 0:
                epoch_bins_2 = preprocessing_steps.create_epoch_bins(part_2_br_state, epoch_indices_2)
                for column, channel in zip(part_2.T, channels_dict[headstage_letters]):
                    filter_steps = Filter(column, epoch_bins_2)
                    filtered_data_2 = filter_steps.butter_bandpass()
                    power_steps = PowerSpectrum(filtered_data_2)
                    power_array_part_2, frequency_array_part_2 = power_steps.average_psd()
                    if anim_id + headstage_letters in genotypes['wildtypes']:
                        genotype = 'WT'
                    if anim_id + headstage_letters in genotypes['ef1_alpha_knockouts']:
                        genotype = 'EF1'
                    dict_data = {'Animal_ID': [anim_id + headstage_letters]*len(frequency_array_part_2), 'Headstage':[headstage_letters]*len(frequency_array_part_2),
                            'Channel': [channel]*len(frequency_array_part_2), 'Brainstate': [brainstate]*len(frequency_array_part_2),
                             'Power': power_array_part_2, 'Frequency': frequency_array_part_2, 'Genotype' : [genotype]*len(frequency_array_part_2)}
                    print('data saved for ' + str(anim_id))
                    two_recording.append(pd.DataFrame(data=dict_data))
            else:
                print('no epochs for ' + str(anim_id) + ' ' + str(brainstate))
            
            
    merged_power_file = pd.concat(two_recording, axis = 0).drop_duplicates().reset_index(drop = True)
    os.chdir('/home/melissa/RESULTS/EF1_ALPHA/debug')
    merged_power_file.to_csv(str(brainstate) + '_2_rec.csv', index = True)
    
