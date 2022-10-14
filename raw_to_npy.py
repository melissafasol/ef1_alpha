import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.signal import decimate
import mne
import glob

from ef1_alpha_properties import recordings_1_channels, one_recording_date_folders
from open_ephys_functions import loadFolderToArray


def tethered_to_npy(path, recording_type, save_path):

    if recording_type == 1:
        for dict_key, value in recordings_1_channels.items():
            if dict_key == 'A':
                animal_ids = value
                print('saving A group' + str(animal_ids) + ' as npy')
                for anim_id in animal_ids:
                    one_recording_folder = one_recording_date_folders[anim_id]
                    print(one_recording_folder)
                    for one_recording in one_recording_folder:
                        file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                        os.chdir(file_path)
                        file_list = os.listdir(file_path) 
                        channel_list = [2, 3, 7, 9]
                        data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                        os.chdir(save_path + '/A')
                        np.save(str(anim_id) + '_A' + '.npy', data)
                        print( str(anim_id) + 'saved')
                        
            elif dict_key == 'A_1':
                animal_ids = value
                print('saving A_1 group' + str(animal_ids) + ' as npy')
                for anim_id in animal_ids:
                    one_recording_folder = one_recording_date_folders[anim_id]
                    print(one_recording_folder)
                    for one_recording in one_recording_folder:
                        file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                        os.chdir(file_path)
                        file_list = os.listdir(file_path) 
                        channel_list = [2, 3, 7, 8]
                        data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                        os.chdir(save_path + '/A_1')
                        np.save(str(anim_id) + '_A_1' + '.npy', data)
                        print( str(anim_id) + 'saved')
                        
            elif dict_key == 'B':
                animal_ids = value
                print('saving A group' + str(animal_ids) + ' as npy')
                for one_recording in one_recording_folder:
                        file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                        os.chdir(file_path)
                        file_list = os.listdir(file_path) 
                        channel_list = [18, 19, 23, 25]
                        data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                        os.chdir(save_path + '/C')
                        np.save(str(anim_id) + '_B' + '.npy', data)
                        print( str(anim_id) + 'saved')
            
            elif dict_key == 'C':
                animal_ids = value
                print('saving C group' + str(animal_ids) + ' as npy')
                for one_recording in one_recording_folder:
                        file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                        os.chdir(file_path)
                        file_list = os.listdir(file_path) 
                        channel_list = [34, 35, 39, 41]
                        data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                        os.chdir(save_path + '/C')
                        np.save(str(anim_id) + '_C' + '.npy', data)
                        print( str(anim_id) + 'saved')
                
            elif dict_key == 'D':
                animal_ids = value 
                print('saving D group' + str(animal_ids) + ' as npy') 
                for one_recording in one_recording_folder:
                        file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                        os.chdir(file_path)
                        file_list = os.listdir(file_path) 
                        channel_list = [50, 51, 55, 57]
                        data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                        os.chdir(save_path + '/D')
                        np.save(str(anim_id) + '_D' + '.npy', data)
                        print( str(anim_id) + 'saved')
            
    return 


path = '/home/melissa/ef1_data/Grant_Recordings'
save_path =  '/home/melissa/PREPROCESSING/ef1_alpha_recordings/one_recording'

tethered_to_npy(path = path, recording_type = 1, save_path = save_path)