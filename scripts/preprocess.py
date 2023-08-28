import os 
import pandas as pd 
import numpy as np

#path for loading recording files 
recording_path = '/home/melissa/PREPROCESSING/EF1_ALPHA'
brain_state_path = '/home/melissa/PREPROCESSING/EF1_ALPHA/reformatted_brain_states'

 
class ExtractBrainStateEF1ALPHA:
    
    sample_rate = 1000 
    epoch_length = int(sample_rate * 5)
    
    
    def __init__(self, animal_id, recording_folder_path, br_st_folder_path, letter, recording_number):
        self.animal_id = animal_id 
        self.recording_folder_path = recording_folder_path 
        self.br_st_folder_path = br_st_folder_path
        self.letter = letter
        self.recording_number = recording_number 
        
    
    def load_npy_recordings(self):
        
        if self.recording_number == 1:
            folder_path_1_rec = self.recording_folder_path + '/one_recording'
            os.chdir(folder_path_1_rec)
            list_file_names = os.listdir(folder_path_1_rec)
            for file in list_file_names:
                if file.startswith(self.animal_id) and file.endswith(self.letter + '.npy'):
                    one_recording_file = np.load(file)
                    return one_recording_file
                else:
                    pass
         
        if self.recording_number == 2:
            os.chdir(self.recording_folder_path + '/two_recording/Part_1')
            list_file_names_1 = os.listdir(self.recording_folder_path + '/two_recording/Part_1')
            for file in list_file_names_1:
                if file.startswith(self.animal_id) and file.endswith(self.letter + '.npy'):
                    part_1 = np.load(file)
            os.chdir(self.recording_folder_path + '/two_recording/Part_2')
            list_file_names_2 = os.listdir(self.recording_folder_path + '/two_recording/Part_2')
            for file in list_file_names_2:
                if file.startswith(self.animal_id) and file.endswith(self.letter + '.npy'):
                    part_2 = np.load(file)
                    return part_1, part_2
        
        
    def load_brain_state_file(self):
        os.chdir(self.br_st_folder_path)
        state_file_names = os.listdir(self.br_st_folder_path)
        if self.recording_number == 1:
            for file in state_file_names:
                if file.startswith(self.animal_id) and file.endswith(self.letter + '.csv'):
                    brain_state_file = pd.read_csv(file)
                    return brain_state_file
        
        elif self.recording_number == 2:
            for file in state_file_names:
                part_1_brain_state = pd.read_csv(self.animal_id  + '_' + self.letter + '_part_1.csv')
                part_2_brain_state = pd.read_csv(self.animal_id + '_' + self.letter + '_part_2.csv')
                return part_1_brain_state, part_2_brain_state
        
        #function to select brain state of interest and remove indices marked with E

    
    def process_brainstate_file(self, brainstate_file, brainstate_number):
    
        brainstate_indices = brainstate_file.loc[brainstate_file['brain_state'] == brainstate_number].index
        discard_indices = brainstate_file.loc[brainstate_file['epoch_discard_numbers'] == 'E'].index.tolist()
        
        if brainstate_number == 'seizure':
            new_indices = brainstate_file.loc[brainstate_file['epoch_discard_numbers'] == 'E'].index.tolist()
            if len(new_indices) > 0:
                starting_index = new_indices[0]
                epoch_indices = []
       
            for epoch_index in range(len(new_indices)-1):
                if new_indices[epoch_index] + 1 != new_indices[epoch_index + 1]:
                    epoch_indices.append([starting_index, new_indices[epoch_index]])
                    starting_index = new_indices[epoch_index + 1]

                #append last value outside of the loop as the loop is for len -1
            epoch_indices.append([starting_index, new_indices[-1]])
            return epoch_indices
        
        else:
            new_indices = []
            for i in brainstate_indices:
                if i not in discard_indices:
                    new_indices.append(i)
        if len(new_indices) > 0:
            starting_index = new_indices[0]
            epoch_indices = []
       
            for epoch_index in range(len(new_indices)-1):
                if new_indices[epoch_index] + 1 != new_indices[epoch_index + 1]:
                    epoch_indices.append([starting_index, new_indices[epoch_index]])
                    starting_index = new_indices[epoch_index + 1]

                #append last value outside of the loop as the loop is for len -1
            epoch_indices.append([starting_index, new_indices[-1]])
            return epoch_indices
        
        else:
            pass

        

    def create_epoch_bins(self, brain_state_file, epoch_indices):
        
        time_start_values = []
        time_end_values = []
        
        for epoch_index in epoch_indices:
            time_start_values.append(brain_state_file.iloc[epoch_index[0], 5])
        
        for epoch_index in epoch_indices:
            time_end_values.append(brain_state_file.iloc[epoch_index[1], 5])

        zipped_time_values = list(zip([int(element*self.sample_rate) for element in time_start_values],
                                    [int(element*self.sample_rate) for element in time_end_values]))
        
        function_timebins = lambda epoch_start, epoch_end : list(range(epoch_start, epoch_end, self.epoch_length))
        
        timevalues_epochs = list(map(lambda x: function_timebins(x[0], x[1]), (zipped_time_values)))
        timevalues_array = list(np.concatenate(timevalues_epochs).flat)
        timevalues_array = [int(x) for x in timevalues_array]
        return timevalues_array
    
    
    def seizure_epoch_bins(self, file_path, brain_state_file):
        
        seizure_times = pd.read_csv(file_path + brain_state_file)
        seizure_start = seizure_times.iloc[:, 1]
        seizure_end = seizure_times.iloc[:, 2]

        zipped_time_values = list(zip([int(element*self.sample_rate) for element in seizure_start],
                                    [int(element*self.sample_rate) for element in seizure_end]))
        
        function_timebins = lambda epoch_start, epoch_end : list(range(epoch_start, epoch_end, self.epoch_length))
        
        timevalues_epochs = list(map(lambda x: function_timebins(x[0], x[1]), (zipped_time_values)))
        timevalues_array = list(np.concatenate(timevalues_epochs).flat)
        timevalues_array = [int(x) for x in timevalues_array]
        return timevalues_array

def preprocessing_steps_1(brainstate_list, headstage_dict, animal_id_list,
                        recording_path, brain_state_path, recording_number):
    '''brainstate_list = ['W', 'N', 'R'],
    headstage_dict = {'A': [2, 3, 7, 9]},
    animal_id_list = {'A': ['191125']},
    recording_path = path_to_npy_files
    br_state_path = path_to_brainstate
    recording_number = 1'''
    
    for brainstate in brainstate_list:
        for headstage in headstage_dict:
            for anim_id in animal_id_list[headstage]:
                print('preprocessing' + str(anim_id))
                preprocessing_steps = ExtractBrainStateEF1ALPHA(anim_id, recording_path, brain_state_path,
                                                               headstage, recording_number)
                npy_recording = preprocessing_steps.load_npy_recordings()
                br_state_file = preprocessing_steps.load_brain_state_file()
                print('preprocessing complete for animal id')
                return npy_recording, br_state_file

def preprocessing_steps_2(brainstate_list, headstage_dict, animal_id_list,
                        recording_path, brain_state_path, recording_number):
    '''brainstate_list = ['W', 'N', 'R'],
    headstage_dict = {'A': [2, 3, 7, 9]},
    animal_id_list = {'A': ['191125']},
    recording_path = path_to_npy_files
    br_state_path = path_to_brainstate
    recording_number = 2'''
    
    for brainstate in brainstate_list:
        for headstage in headstage_dict:
            for anim_id in animal_id_list[headstage]:
                print('preprocessing' + str(anim_id))
                preprocessing_steps = ExtractBrainStateEF1ALPHA(anim_id, recording_path, brain_state_path,
                                                               headstage, recording_number)
                part_1, part_2 = preprocessing_steps.load_npy_recordings()
                br_state_file_1, br_state_file_2 = preprocessing_steps.load_brain_state_file()
                print('preprocessing complete for animal id')
                return part_1, part_2, br_state_file_1, br_state_file_2