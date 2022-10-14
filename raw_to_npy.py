import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.signal import decimate
import mne
import glob

from ef1_alpha_properties import recordings_1_channels, one_recording_date_folders, channels_dict
from ef1_alpha_properties import recordings_2_channels 
from open_ephys_functions import loadFolderToArray

class LoadTetheredRaw(): 
    
    def __init__(self, path, save_path, recording_dict, channels_dict):
        self.path = path
        self.save_path = save_path
        self.recording_dict = recording_dict
        self.channels_dict = channels_dict

    def one_recording(self, channel_letter, one_recording_date_folders):
        for dict_key, value in self.recording_dict.items():
                if dict_key == channel_letter:
                    animal_ids = value
                    print(animal_ids)
                    for anim_id in animal_ids:
                        one_recording_folder = one_recording_date_folders[anim_id]
                        file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                        os.chdir(file_path)
                        channel_list = self.channels_dict[channel_letter]
                        data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                        os.chdir(save_path + '/one_recording')
                        np.save(str(anim_id) + '_' +  str(channel_letter) + '.npy', data)
                        print( str(anim_id) + 'saved')
                            
    def two_recording(self, channel_letter):
        for dict_key, value in self.two_recording_dict.items():
            if dict_key == channel_letter:
                animal_ids = value
                print(animal_ids)
                for anim_id in animal_ids:
                    part_1_file_path = path + '/' + str(anim_id) + '/Part_1'
                    os.chdir(part_1_file_path)
                    channel_list = self.channels_dict[channel_letter]
                    data= loadFolderToArray(part_1_file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                    os.chdir(save_path + 'two_recording/Part_1')
                    np.save(str(anim_id) + '_part1_' + str(channel_letter) + '.npy', data)
                    part_2_file_path = path + '/' + str(anim_id) + '/Part_2'
                    os.chdir(part_2_file_path)
                    channel_list = self.channels_dict[channel_letter]
                    data= loadFolderToArray(part_2_file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                    os.chdir(save_path + 'two_recording/Part_2')
                    np.save(str(anim_id) + '_part2_' + str(channel_letter) + '.npy', data)
        
        return 
  


path = '/home/melissa/ef1_data/Grant_Recordings'
save_path =  '/home/melissa/PREPROCESSING/ef1_alpha_recordings'


tetheredraw = LoadTetheredRaw(path = path, save_path= save_path, recording_dict=recordings_1_channels, channels_dict=channels_dict)
#A1_array = tetheredraw.one_recording(channel_letter='A_1', one_recording_date_folders = one_recording_date_folders )
#A_array = tetheredraw.one_recording(channel_letter='A', one_recording_date_folders = one_recording_date_folders)
#B_array = tetheredraw.one_recording(channel_letter='B', one_recording_date_folders = one_recording_date_folders)
C_array = tetheredraw.one_recording(channel_letter='C', one_recording_date_folders = one_recording_date_folders)
D_array = tetheredraw.one_recording(channel_letter='D', one_recording_date_folders = one_recording_date_folders)

A1_2_array = tetheredraw.two_recording(channel_letter='A_1')
A_2_array = tetheredraw.two_recording(channel_letter='A')
B_2_array = tetheredraw.two_recording(channel_letter='B')
B_1_2_array = tetheredraw.two_recording(channel_letter = 'B_1')
C_2_array = tetheredraw.two_recording(channel_letter='C')
D_2_array = tetheredraw.two_recording(channel_letter='D')


