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
    
    def __init__(self, path, save_path, channels_dict):
        self.path = path
        self.save_path = save_path
        self.channels_dict = channels_dict

    def one_recording(self, channel_letter, recording_dict, one_recording_date_folders):
        for dict_key, value in recording_dict.items():
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
                            
    def two_recording(self, recording_dict, channel_letter):
        for dict_key, value in recording_dict.items():
            if dict_key == channel_letter:
                animal_ids = value
                print(animal_ids)
                for anim_id in animal_ids:
                    part_1_file_path = path + '/' + str(anim_id) + '/Part_1'
                    os.chdir(part_1_file_path)
                    print(part_1_file_path)
                    channel_list = self.channels_dict[channel_letter]
                    print(channel_letter)
                    data= loadFolderToArray(part_1_file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                    print(data)
                    os.chdir(save_path + '/two_recording/Part_1')
                    np.save(str(anim_id) + '_part1_' + str(channel_letter) + '.npy', data)
                    print('data saved for part 1 ' + str(anim_id))
                    part_2_file_path = path + '/' + str(anim_id) + '/Part_2'
                    os.chdir(part_2_file_path)
                    channel_list = self.channels_dict[channel_letter]
                    data= loadFolderToArray(part_2_file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                    print(data)
                    os.chdir(save_path + '/two_recording/Part_2')
                    np.save(str(anim_id) + '_part2_' + str(channel_letter) + '.npy', data)
                    print('data saved for part 2 ' + str(anim_id))
  


path = '/home/melissa/ef1_data/Grant_Recordings'
save_path =  '/home/melissa/PREPROCESSING/EF1_ALPHA'


tetheredraw = LoadTetheredRaw(path = path, save_path= save_path, channels_dict=channels_dict)
#A1_array = tetheredraw.one_recording(channel_letter='A_1', recording_dict = recordings_1_channels, one_recording_date_folders = one_recording_date_folders )
#A_array = tetheredraw.one_recording(channel_letter='A', recording_dict = recordings_1_channels, one_recording_date_folders = one_recording_date_folders)
#B_array = tetheredraw.one_recording(channel_letter='B', recording_dict = recordings_1_channels, one_recording_date_folders = one_recording_date_folders)
#C_array = tetheredraw.one_recording(channel_letter='C', recording_dict = recordings_1_channels, one_recording_date_folders = one_recording_date_folders)
#D_array = tetheredraw.one_recording(channel_letter='D', recording_dict = recordings_1_channels, one_recording_date_folders = one_recording_date_folders)

'''SOMETHING ABOUT C ARRAY THAT IS NOT WORKING?'''

A1_2_array = tetheredraw.two_recording(channel_letter='A_1', recording_dict = recordings_2_channels)
print(A1_2_array)
A_2_array = tetheredraw.two_recording(channel_letter='A', recording_dict = recordings_2_channels)
B_2_array = tetheredraw.two_recording(channel_letter='B', recording_dict = recordings_2_channels)
B_1_2_array = tetheredraw.two_recording(channel_letter = 'B_1', recording_dict = recordings_2_channels)
C_2_array = tetheredraw.two_recording(channel_letter='C', recording_dict = recordings_2_channels)
D_2_array = tetheredraw.two_recording(channel_letter='D', recording_dict = recordings_2_channels)


