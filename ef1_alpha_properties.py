'''This file contains all of the properties for ef1_alpha (genotypes, males, females)'''

recording_files = {'two_recordings' : ['210422', '210423', '191107', '210705', '191217', '210422', '210423',
                    '191125', '191126', '191217', '210705', '210705', '210705', '191217'],
                  
                    'one_recording' : ['191104', '191108', '210706', '191216', '191216', '210429','210430',
                    '210706', '210706', '210706', '191216']}

one_recording_date_folders = {'191104': '2019-11-04_13-26-36', '191108': '2019-11-08_10-14-30', 
                             '210706': '2021-07-06_09-56-31', '191216': '2019-12-16_12-07-22', 
                             '210429': 'Part_2','210430' : 'Part_1'}

genotypes = {'wildtypes' : ['210422D', '210423D', '210705C', '210706C', '191216C', '191125A', '191126A', '191107A', 
                    '191104B', '191108A', '210422B', '210423B'],
                    'ef1_alpha_knockouts' : ['210705A', '210706B', '191216A_1', '191217A_1', '191216B',
                    '191217B', '210429C','210430C', '210705D', '210706D']}

wildtype_plotting = {'A': ['191125', '191126', '191107', '191108'],
                     'B': ['191104'],
                     'B_1': ['210422', '210423'],
                     'C': ['210705', '210706', '191216'],
                     'D': ['210422', '210423']}

EF1_alpha_plotting = {'A': ['210705'],
                      'A_1': ['191216', '191217'],
                      'B': ['210706', '191216', '191217'],
                      'C': ['210429', '210430'],
                      'D': ['210705', '210706']}

genders = {'wildtype_males': ['210422_D', '210423_D', '210705_C', '210706_C', '191216_C', '191125_A', '191126_A'], 
                    'wildtypes_female': ['191107_A', '191104', '191108_A', '210422_B', '210423_B'],
                    'ef1_alpha_male': ['210705_A', '210706_B', '191216_A', '191217_A'],
                    'ef1_alpha_female' : ['191216_B', '191217_B', '210429_C','210430_C', '210705_D', '210706_D']}

#dictionary for headstages of animal ids that have two recordings 
recordings_2_channels = {'A': ['191125', '191126', '210705'],
                         'A_1': ['191217'], 
                         'B': ['191217', '210705'],
                         'B_1': ['210422', '210423'],
                         'C': ['210705', '191217'],
                         'D': ['210422', '210423', '210705']}
#dictionary for headstages of animal ids that have one recordings 
recordings_1_channel = {'A': ['191107', '210706', '191108'],
                         'A_1': ['191216'],
                         'B': ['191104', '191216', '210706'],
                         'C': ['210706', '210430', '210429', '191216'],
                         'D': ['210706']}

channels_dict = {'A' : [2, 3, 7, 9],
                 'A_1' : [2, 3, 7, 8],
                 'B' : [18, 19, 23, 25],
                 'B_1': [18, 20, 23, 25],
                 'C' : [34, 35, 39, 41],
                 'D' : [50, 51, 55, 57]}

