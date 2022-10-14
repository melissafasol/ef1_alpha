import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.signal import decimate
import mne
import glob

from ef1_alpha_properties import recordings_1_channels, one_recording_date_folders, channels_dict
from open_ephys_functions import loadFolderToArray

class LoadTetheredRaw(): 
    
    def __init__(self, path, save_path, one_recording_dict, one_recording_date_folders, channels_dict):
        self.path = path
        self.save_path = save_path
        self.one_recording_dict = one_recording_dict
        self.one_recording_date_folders = one_recording_date_folders
        self.channels_dict = channels_dict

    def one_recording(self, channel_letter):
        for dict_key, value in self.one_recording_dict.items():
                if dict_key == channel_letter:
                    animal_ids = value
                    print('loading'  + str(animal_ids))
                    for anim_id in animal_ids:
                        one_recording_folder = self.one_recording_date_folders[anim_id]
                        print(one_recording_folder)
                        for one_recording in one_recording_folder:
                            file_path = path + '/' + str(anim_id) + '/' + str(one_recording_folder)
                            os.chdir(file_path)
                            file_list = os.listdir(file_path) 
                            channel_list = self.channels_dict[channel_letter]
                            data= loadFolderToArray(file_path, channels = channel_list, chprefix = 'CH', dtype = float, session = '0', source = '100')
                            os.chdir(save_path + '/' + str(channel_letter))
                            np.save(str(anim_id) + str(channel_letter) + '.npy', data)
                            print( str(anim_id) + 'saved')
        
            
  


path = '/home/melissa/ef1_data/Grant_Recordings'
save_path =  '/home/melissa/PREPROCESSING/ef1_alpha_recordings/one_recording'

test_one_recording = LoadTetheredRaw(path = path, save_path= save_path, one_recording_dict=recordings_1_channels,
                                     one_recording_date_folders=one_recording_date_folders, channels_dict=channels_dict)
A1_array = test_one_recording.one_recording(channel_letter='A_1')