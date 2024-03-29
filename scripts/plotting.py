import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.colors as mcolors
import seaborn as sns


#building genotype function
def build_genotype_df(results_dataframe, mutant_list, wt_list):
    '''build_genotype_df(results_dataframe, mutant_list, gender_list, animal_line) takes dataframe and adds a column with genotypes to the dataframe'''
    int_mutant_list = [ID for ID in mutant_list]
    int_wt_list = [ID for ID in wt_list]
    print(int_wt_list)
    genotype = []
    
    animal_numbers = results_dataframe['Animal_ID'] 
    animal_numbers = list(animal_numbers)
    for animal in animal_numbers:
        if animal in int_wt_list:
            genotype.append('WT')
        else:
            genotype.append('EF1')
    
    genotype_df = pd.DataFrame({'Genotype': genotype})
    
    final_dataframe = results_dataframe.join(genotype_df)
    
    return final_dataframe

#parsing out individual channels

def separate_by_channel(df, channel_number_list):
    
    channel_1 = df[df['Channel'] == channel_number_list[0]]
    channel_2 = df[df['Channel'] == channel_number_list[1]]
    channel_3 = df[df['Channel'] == channel_number_list[2]]
    channel_4 = df[df['Channel'] == channel_number_list[3]]   
    if len(channel_number_list) == 4:
        return channel_1, channel_2, channel_3, channel_4
    else:
        channel_5 = df[df['Channel'] == channel_number_list[3]]
        return channel_1, channel_2, channel_3, channel_4, channel_5
    


#parsing out by genotype

def separate_by_genotype(df, genotype, wildtype):
    mutant_df = df[df['Genotype'] == genotype]
    wildtype_df = df[df['Genotype'] == wildtype]
    
    return mutant_df, wildtype_df

#plot average genotype in selective channels 

def plot_geno_average_by_channel(channel_group, color_list, hue_order_list, data_rem, data_nrem, data_wake,
                                 ylim_lower, ylim_upper, save_path ):
    
    '''
    color_list = ['orange', 'blue']
    hue_order_list = ['EF1', 'WT']
    data_rem = dataframe containing rem data
    data_nrem = dataframe containing nrem data
    data_wake = dataframe containing wake data
    ylim_lower = 10**-2
    ylim_upper = 10**5
    save_path = path to save folder
    '''
    
    sns.set_style("white") 
    colors = color_list 
    hue_order = hue_order_list

    #f.suptitle('REM', fontsize = 36)
    fig, ax = plt.subplots(1,3, figsize=(20,8), sharex = True, sharey=True)
    line_rem = sns.lineplot(x= 'Frequency', y='Power', hue='Genotype', hue_order = hue_order, errorbar = ('ci', 95), data = data_rem, 
                            palette= colors, linewidth = 2, ax = ax[0])
    ax[0].set(xlabel = 'Frequency (Hz)', ylabel = 'PSD [V**2/Hz]')
    line_nrem = sns.lineplot(x= 'Frequency', y='Power', hue='Genotype', hue_order = hue_order, errorbar= ('ci', 95), data = data_nrem, 
                             palette= colors, linewidth = 2, ax = ax[1])
    ax[1].set(xlabel = 'Frequency (Hz)', ylabel = 'PSD [V**2/Hz]')
    line_wake = sns.lineplot(x= 'Frequency', y='Power', hue='Genotype', hue_order = hue_order, errorbar= ('ci', 95), data = data_wake, 
                             palette= colors, linewidth = 2, ax = ax[2])
    ax[2].set(xlabel = 'Frequency (Hz)', ylabel = 'PSD [V**2/Hz]')

    sns.despine()
    plt.yscale('log')
    plt.xlim(1, 100)
    plt.ylim(ylim_lower, ylim_upper)

    plt.suptitle(str(channel_group), fontsize = 'x-large', fontweight = 'bold')
    line_rem.title.set_text('REM')
    line_nrem.title.set_text('Non-REM')
    line_wake.title.set_text(' Wake')

    os.chdir(save_path )
    plt.savefig(str(channel_group) + '_average_genotype.svg')
    
def plot_individual_animals_wt(dataframe_to_plot, genotype, sleepstage, save_path, palette_list):
    wt_plot_list_1 = ['210423D', '210705C', '210706C', '191216C']
    wt_plot_list_2 = ['191125A', '191126A', '191107A', '191104B']
    wt_plot_list_3 = [ '191108A', '210422B_1', '210423B_1', '191217C'] 
    single =  [ '210422D'] 
    
    plots_list = [wt_plot_list_1, wt_plot_list_2, wt_plot_list_3]
    
    
    def pos_idx_to_animal_idx(row_idx, col_idx):
        return row_idx * 2 + col_idx
    
    
    for plot in plots_list:
        print(plot)
        sns.set_style("white") 
        fig, axs = plt.subplots(2,2, figsize=(30,20), sharex = True, sharey=True)
        for row_idx in range(2):
            for col_idx in range(2):
                animal_idx = pos_idx_to_animal_idx(row_idx, col_idx)
                animal_data = dataframe_to_plot[dataframe_to_plot["Animal_ID"] == plot[animal_idx]]
                sns.lineplot(data=animal_data, x='Frequency', y='Power', hue='Channel', ax=axs[row_idx, col_idx],palette = palette_list)
                #axs[row_idx, col_idx].text(0.5, 0.5, plot[animal_idx], fontsize=12) #test that plt functions are rendering correctly 
                plt.suptitle(str(genotype) + ' ' + str(sleepstage), fontsize = 30, fontweight = 'bold') 
                sns.despine()
                plt.yscale('log')
                axs[1, 0].set_xlim(1, 100)
                axs[1, 1].set_xlim(1, 100)
                axs[1, 0].set(xlabel = 'Frequency')
                axs[1, 1].set(xlabel = 'Frequency')
                axs[1, 1].set_xlim(1, 100)
                axs[0, 0].set_ylim(10**-2, 10**5)
                axs[1, 1].set_ylim(10**-2, 10**5)
                axs[0,0].set(ylabel = 'PSD [V**2/Hz]')
                axs[1,0].set(ylabel = 'PSD [V**2/Hz]')
            for row_idx in range(2):
                for col_idx in range(2):
                        axs[row_idx, col_idx].set_title(plot[pos_idx_to_animal_idx(row_idx, col_idx)], 
                                                fontsize = 10, fontweight = 'bold')
        os.chdir(save_path)
        plt.savefig(str(genotype) + '_' + str(sleepstage) + '_' + str(plot[animal_idx]) + '.jpg', bbox_inches = 'tight')
       
    for plot in single:
        sns.set_style("white") 
        fig, axs = plt.subplots(1,1, figsize=(10,10), sharex = True, sharey=True)
        animal_data = dataframe_to_plot[dataframe_to_plot["Animal_ID"] == plot]
        sns.lineplot(data=animal_data, x='Frequency', y='Power', hue='Channel', ax=axs,palette = palette_list)
        #axs.text(0.5, 0.5, plot[animal_idx], fontsize=12)
        plt.suptitle(str(genotype) + ' ' + str(sleepstage), fontsize = 10, fontweight = 'bold') 
        sns.despine()
        plt.yscale('log')
        axs.set_xlim(1, 100)
        axs.set_ylim(10**-2, 10**5)
        axs.set(xlabel = 'Frequency')
        axs.set(ylabel = 'PSD [V**2/Hz]')
        axs.set_title(plot, fontsize = 10, fontweight = 'bold')
        os.chdir(save_path)
        plt.savefig(str(genotype) + '_' + str(sleepstage) + '_' + str(plot) + '.jpg', bbox_inches = 'tight')
    
    
    
def plot_individual_animals_mutant(dataframe_to_plot, genotype, sleepstage, save_path, palette_list):
    mutant_list_1 = ['210705B', '210705A', '210706A', '210706B']
    mutant_list_2 = ['191216A_1', '191217A_1', '191216B', '191217B']
    mutant_list_3 =  ['210429C','210430C', '210705D', '210706D']
    
    plots_list = [mutant_list_1, mutant_list_2, mutant_list_3]
    
    
    def pos_idx_to_animal_idx(row_idx, col_idx):
        return row_idx * 2 + col_idx
    
    for plot in plots_list:
        sns.set_style("white") 
        fig, axs = plt.subplots(2,2, figsize=(30,20), sharex = True, sharey=True)
        print(plot)
        for row_idx in range(2):
            for col_idx in range(2):
                animal_idx = pos_idx_to_animal_idx(row_idx, col_idx)
                animal_data = dataframe_to_plot[dataframe_to_plot["Animal_ID"] == plot[animal_idx]]
                sns.lineplot(data=animal_data, x='Frequency', y='Power', hue='Channel', ax=axs[row_idx, col_idx],palette = palette_list)
                #axs[row_idx, col_idx].text(0.5, 0.5, plot[animal_idx], fontsize=12) #test that plt functions are rendering correctly 
                plt.suptitle(str(genotype) + ' ' + str(sleepstage), fontsize = 30, fontweight = 'bold') 
                sns.despine()
                plt.yscale('log')
                axs[1, 0].set_xlim(1, 100)
                axs[1, 1].set_xlim(1, 100)
                axs[1, 0].set(xlabel = 'Frequency')
                axs[1, 1].set(xlabel = 'Frequency')
                axs[1, 1].set_xlim(1, 100)
                axs[0, 0].set_ylim(10**-2, 10**5)
                axs[1, 1].set_ylim(10**-2, 10**5)
                axs[0,0].set(ylabel = 'PSD [V**2/Hz]')
                axs[1,0].set(ylabel = 'PSD [V**2/Hz]')
            for row_idx in range(2):
                for col_idx in range(2):
                        axs[row_idx, col_idx].set_title(plot[pos_idx_to_animal_idx(row_idx, col_idx)], 
                                                fontsize = 10, fontweight = 'bold')
        os.chdir(save_path)
        plt.savefig(str(genotype) + '_' + str(sleepstage) + '_' + str(plot[animal_idx]) + '.jpg', bbox_inches = 'tight')
       
    