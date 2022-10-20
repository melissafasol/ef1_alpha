import os 
import pandas as pd 
import numpy as np

#path for loading recording files 
recording_path = '/home/melissa/PREPROCESSING/EF1_ALPHA'
brain_state_path = '/home/melissa/PREPROCESSING/EF1_ALPHA/brain_state_folder'

 
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
         
        elif self.recording_number == 2:
            os.chdir(self.recording_folder_path + '/two_recording/Part_1')
            list_file_names_1 = os.listdir(self.recording_folder_path + '/two_recording/Part_1')
            for file in list_file_names_1:
                if file.startswith(self.animal_id) and file.endswith('part_1_' + self.letter + '.npy'):
                    print(file)
                    part_1 = np.load(file)
            os.chdir(self.recording_folder_path + '/two_recording/Part_2')
            list_file_names_2 = os.listdir(self.recording_folder_path + '/two_recording/Part_2')
            for file in list_file_names_2:
                if file.startswith(self.animal_id) and file.endswith('part_2_'+ self.letter + '.npy'):
                    print(file)
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
                if file.startswith(self.animal_id) and file.endswith(self.letter + '_part_1.csv'):
                    part_1_brain_state = pd.read_csv(file)
                if file.startswith(self.animal_id) and file.endswith(self.letter + '_part_2.csv'):
                    part_2_brain_state = pd.read_csv(file)
                    return part_1_brain_state, part_2_brain_state
        
        #function to select brain state of interest and remove indices marked with E

    def remove_E_epochs(self, brain_state_file, brain_state_letter):
        
        brain_state_indices = brain_state_file.loc[brain_state_file['brain_state'] == brain_state_letter].index.tolist()
        discard_indices = brain_state_file.loc[brain_state_file['epoch_discard_numbers'] == 'E'].index.tolist()
        new_indices = []
        for i in brain_state_indices:
            if i not in discard_indices:
                new_indices.append(i)
        
        return new_indices

    def get_epoch_indices(self, new_indices):
        epoch_indices = []
        starting_index = new_indices[0]
        
        for i in range(len(new_indices)-1):
            if new_indices[i] +1 != new_indices[i + 1]:
                epoch_indices.append([starting_index, new_indices[i]])
                starting_index = new_indices[i + 1]
            
            else:
                pass

        epoch_indices.append([starting_index, new_indices[-1]])
        
        return epoch_indices

    def create_epoch_bins(self, brain_state_file, epoch_indices):
        
        time_start_values = []
        time_end_values = []
        
        for epoch_index in range(len(epoch_indices)):
            time_start_values.append(brain_state_file.iloc[epoch_indices[epoch_index][0], 1])
        
        for epoch_index in range(len(epoch_indices)):
            time_end_values.append(brain_state_file.iloc[epoch_indices[epoch_index][1], 1])

        zipped_time_values = list(zip([int(element*self.sample_rate) for element in time_start_values],
                                    [int(element*self.sample_rate) for element in time_end_values]))
        
        function_timebins = lambda epoch_start, epoch_end : list(range(epoch_start, epoch_end, self.epoch_length))
        
        timevalues_epochs = list(map(lambda x: function_timebins(x[0], x[1]), (zipped_time_values)))
        timevalues_array = list(np.concatenate(timevalues_epochs).flat)
        timevalues_array = [int(x) for x in timevalues_array]
        return timevalues_array
