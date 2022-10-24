import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.colors as mcolors
import seaborn as sns



#building genotype function
def build_genotype_df(results_dataframe, mutant_list):
    '''build_genotype_df(results_dataframe, mutant_list, gender_list, animal_line) takes dataframe and adds a column with genotypes to the dataframe'''
    int_mutant_list = [ID for ID in mutant_list]
    genotype = []
    
    def check_availability(element, variables: iter):
        return element in variables
    
    animal_numbers = results_dataframe['Animal_ID'] 
    animal_numbers = list(animal_numbers)
    for animal in animal_numbers:
        if check_availability(animal, int_mutant_list):
            genotype.append('EF1')
        else:
            genotype.append('WT')
    
    genotype_df = pd.DataFrame({'Genotype': genotype})
    
    final_dataframe = results_dataframe.join(genotype_df)
    
    return final_dataframe

#separating large df into channels and animal_ids

