import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.signal import decimate
import mne
import glob

file_path = '/home/melissa/PREPROCESSING/ef1_alpha'

def load_ef1_alpha_raw(file_path, animal_number, montage_name, head_stage_number):
    
    for animal_id in two_recordings:
        os.chdir(file_path + str('Part 1'))
        for animal_id_folder in raw_recordings_folder:
            if animal_id_folder.startsWith('191216') and .endswith('A'):
            channels = [2, 3, 7, 8]
            data= loadFolderToArray(file_path, channels, chprefix = 'CH', dtype = float, session = '0', source = '100')

            elif filename.endswith('A'):
            channels = [2,3,7,9]
            ata= loadFolderToArray(file_path, channels, chprefix = 'CH', dtype = float, session = '0', source = '100')

    if filename.startsWith('210422', '210423') and filename.endswith('B'):
        channels = [[18, 20, 23, 25]]
        data= loadFolderToArray(file_path, channels, chprefix = 'CH', dtype = float, session = '0', source = '100')
    elif filename.endswith('B'):
        channels = [18, 19, 23, 25]
        data= loadFolderToArray(file_path, channels, chprefix = 'CH', dtype = float, session = '0', source = '100')
    if filename.endswith('C'):
        channels = [34, 35, 39, 41]
        data= loadFolderToArray(file_path, channels, chprefix = 'CH', dtype = float, session = '0', source = '100')
    if filename.endswith('D'):
        channels = [50, 51, 55, 57]
        data= loadFolderToArray(file_path, channels, chprefix = 'CH', dtype = float, session = '0', source = '100')
    