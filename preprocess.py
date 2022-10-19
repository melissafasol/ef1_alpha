import os 
import pandas as pd 
import numpy as np

#path for loading recording files 
recording_path = '/home/melissa/PREPROCESSING/EF1_ALPHA'
brain_state_path = '/home/melissa/PREPROCESSING/EF1_ALPHA/brain_state_folder'

def load_npy_recordings(animal_id, folder_path, letter, recording_number):
    if recording_number == 1:
        os.chdir(folder_path + '/one_recording')
        list_file_names = os.listdir(folder_path)
        for file in list_file_names:
            if file.startswith(animal_id) and file.endswith(letter + '.npy'):
                one_recording_file = np.load(file)
            else:
                pass
        return one_recording_file
    
    if recording_number == 2:
        os.chdir(folder_path + '/two_recording/Part_1')
        list_file_names_1 = os.listdir(folder_path)
        for file in list_file_names_1:
            if file.startswith(animal_id) and file.endswith(letter + '.npy'):
                part_1 = np.load(file)
        os.chdir(folder_path + '/two_recording/Part_2')
        list_file_names_2 = os.listdir(folder_path)
        for file in list_file_names_2:
            if file.startswith(animal_id) and file.endswith(letter + '.npy'):
                part_2 = np.load(file)
        
        return part_1, part_2 
    

def load_brain_state_file(animal_id, folder_path, letter, recording_number):
    os.chdir(folder_path)
    state_file_names = os.listdir(folder_path)
    if recording_number == 1:
        for file in state_file_names:
            if file.startswith(animal_id) and file.endswith(letter + '.csv'):
                brain_state_file = pd.read_csv(file)
        
        return brain_state_file
    
    if recording_number == 2:
        for file in state_file_names:
            if file.startswith(animal_id) and file.endswith(letter + '_part_1.csv'):
                part_1_brain_state = pd.read_csv(file)
            if file.startswith(animal_id) and file.endswith(letter + '_part_2.csv'):
                part_2_brain_state = pd.read_csv(file)
        
        return part_1_brain_state, part_2_brain_state


#function to select brain state of interest and remove indices marked with E

def remove_E_epochs(brain_state_file, brain_state_letter):
     
     def non_match_elements(list_a, list_b):
         non_match = []
         for i in list_a:
            if i not in list_b:
                non_match.append(i)
            
            return non_match
     
     brain_state_indices = brain_state_file.loc[brain_state_file['brain_state'] == brain_state_letter].index.tolist()
     discard_indices = brain_state_file.loc[brain_state_file['epoch_discard+numbers'] == 'E'].index.tolist()
     new_indices = non_match_elements(brain_state_indices, discard_indices)
     
     return new_indices

def create_epoch_bins(new_indices):
    epoch_indices = []
    starting_index = new_indices[0]
    
    for i in range(len(new_indices)-1):
        if new_indices[i] +1 != new_indices[i + 1]:
            epoch_indices.append([starting_index, new_indices[i]])
            starting_index = new_indices[i + 1]
            
    epoch_indices.append([starting_index, new_indices[-1]])
    
    return epoch_indices



 
# class ExtractBrainStateEF1ALPHA:
    
#     sample_rate = 1000 
#     epoch_length = int(sample_rate * 5)
    
#     def __init__(self, brain_state_file, brain_state_letter):
#         self.brain_state_file = brain_state_file
#         self.brain_state_letter = brain_state_letter

#     def discard_E_epochs(self):
#         brain_state_indices = self.brain_state_file.loc[self.brain_state_file['brain_state'] == self.brain_state_letter]
#         discard_indices = self.brain_state_file.loc[self.brain_state_file['epoch_discard_numbers'] == 'E']
#         brain_state_indices_list = brain_state_indices.tolist()
#         discard_indices_list = discard_indices.tolist()
        
#         def non_match_elements(list_a, list_b):
#             non_match = []
#             for i in list_a:
#                 if i not in list_b:
#                     non_match.append(i)
#             return non_match
        
#         new_brain_state_indices = non_match_elements(brain_state_indices_list, discard_indices_list)
        
#         return new_brain_state_indices