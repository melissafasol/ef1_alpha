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

#plot average genotype in selective channels 

def plot_geno_average_by_channel(channel_number, color_list, hue_order_list, data_rem, data_nrem, data_wake,
                                 save_path ):
    
    sns.set_style("white") 
    colors = color_list 
    hue_order = hue_order_list

    #f.suptitle('REM', fontsize = 36)
    fig, ax = plt.subplots(1,3, figsize=(20,10), sharex = True, sharey=True)
    line_rem = sns.lineplot(x= 'Frequency', y='Power', hue='Genotype', hue_order = hue_order, ci= 95, data = data_rem, palette= colors, linewidth = 2, ax = ax[0])
    ax[0].set(xlabel = 'Frequency (Hz)', ylabel = 'PSD [V**2/Hz]')
    line_nrem = sns.lineplot(x= 'Frequency', y='Power', hue='Genotype', hue_order = hue_order, ci= 95, data = data_nrem, palette= colors, linewidth = 2, ax = ax[1])
    ax[1].set(xlabel = 'Frequency (Hz)', ylabel = 'PSD [V**2/Hz]')
    line_wake = sns.lineplot(x= 'Frequency', y='Power', hue='Genotype', hue_order = hue_order, ci= 95, data = data_wake, palette= colors, linewidth = 2, ax = ax[2])
    ax[2].set(xlabel = 'Frequency (Hz)', ylabel = 'PSD [V**2/Hz]')

    sns.despine()
    plt.yscale('log')
    plt.xlim(1, 100)
    #plt.ylim(10**-2, 10**)

    plt.suptitle('Channel ' + str(channel_number), fontsize = 'x-large', fontweight = 'bold')
    line_rem.title.set_text('REM')
    line_nrem.title.set_text('Non-REM')
    line_wake.title.set_text(' Wake')

    os.chdir(save_path )
    plt.savefig('channel_' + str(channel_number) + '_average_genotype.jpg')
    return plt.plot()

