from operator import index
from tkinter.tix import Tree
import numpy as np
import pandas as pd 
import os
from pytools import average 
import scipy
from scipy.fft import fft, fftfreq
from scipy import signal

from preprocess import ExtractBrainStateEF1ALPHA, preprocessing_steps_1, preprocessing_steps_2
from filter import Filter
from power import PowerSpectrum, average_power_df
from ef1_alpha_properties import recordings_1_channel, recordings_2_channels, channels_dict

#paths 
recording_path_npy = '/home/melissa/PREPROCESSING/EF1_ALPHA'
brain_state_path = '/home/melissa/PREPROCESSING/EF1_ALPHA/brain_state_folder'

recordings_letters_1 =  ['A', 'A_1', 'B', 'C', 'D']
recordings_letters_2 = ['A', 'A_1', 'B', 'B_1', 'C', 'D']
recording_letters_notrunning_2 = ['A', 'B', 'D']
recording_letters_notrunning_1 = ['C']

one_recording = []
two_recording = []

brainstates = ['W', 'R', 'N']

br_file_1, br_file_2 = preprocessing_steps_1(brainstate_list = brainstates ,headstage_dict = recordings_letters_1,
                                            animal_id_list = recordings_1_channel, recording_path = recording_path_npy,
                                            brain_state_path = brain_state_path, recording_number = 1)
