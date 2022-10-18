import os 
import pandas as pd 
import numpy as np

#path for loading one recording
path_1_recording = '/home/melissa/PREPROCESSING/EF1_ALPHA/one_recording'
path_2_recording = 'home/melissa/PREPROCESSING/EF1_ALPHA/two_recording'
list_files = os.listdir(path_1_recording)


def load_npy_letter(folder_path, letter):
    os.chdir(folder_path)
    list_file_names = os.listdir(folder_path)
    for file in list_file_names:
        if file.endswith(letter + '.npy'):
            example_file = np.load(file)
            
        else:
            pass
    
    return example_file

example_A = load_npy_letter(path_1_recording, letter = 'A')


class ExtractBrainStateEF1ALPHA:
    
    sample_rate = 1000 
    epoch_length = int(sample_rate * 5)
    
    def __init__(self, brain_state_file, brain_state_letter):
        self.brain_state_file = brain_state_file
        self.brain_state_letter = brain_state_letter

    def discard_E_epochs(self):
        brain_state_indices = self.brain_state_file.loc[self.brain_state_file['brain_state'] == self.brain_state_letter]
        discard_indices = self.brain_state_file.loc[self.brain_state_file['epoch_discard_numbers'] == 'E']
        brain_state_indices_list = brain_state_indices.tolist()
        discard_indices_list = discard_indices.tolist()
        
        def non_match_elements(list_a, list_b):
            non_match = []
            for i in list_a:
                if i not in list_b:
                    non_match.append(i)
            return non_match
        
        new_brain_state_indices = non_match_elements(brain_state_indices_list, discard_indices_list)
        
        return new_brain_state_indices