
from cmath import nan
import os
import pandas as pd 
from plottable import Table
import matplotlib.pyplot as plt
import numpy as np
from functions_for_sre_analysis import valence_separation
import glob

all_data_dict = {}
pos_data_dict = {}
neg_data_dict = {}
neut_data_dict = {}

for file in glob.glob("M2_Internship/data_analysis/mergeddata/*"):
    participant_id = file[-10:-4]
    print(participant_id) #show participant id being handled 

    all_data = pd.read_csv(file) #read file 

    #DATA SETUP FOR RATIO CALCULATION

    negative_data, positive_data, neutral_data = valence_separation(all_data)

    datas = {'all': all_data, 'pos': positive_data, 'neg' : negative_data, 'neut': neutral_data}


    for valence, data in datas.items():
        print(valence)
        hits = []
        #if item in recon task was correctly marked as old add it to hits list 
        for index, row in data.iterrows():
            if (row['réponse'] == 'OLD') & (row['item'] == 'OLD'):
                hits.append(row)
        hit_num = len(hits)
        hits= pd.DataFrame(hits)

        true_totals = {#dict of number of hits per avatar seen at encoding 
        #encoded avatar is the avatar seen at encoding 
        'me': len(hits[
            hits['encoded_avatar'] == 'vous'
        ]),

        'friend': len(hits[
            hits['encoded_avatar'] == 'ami'
        ]),

        'other': len(hits[
            hits['encoded_avatar'] == 'autrui'
        ]),

        'robot': len(hits[
            hits['encoded_avatar'] == 'robot'
        ])
    }
    
        #denominator for the source error ratio calculation - number or total hits minus hits per avatar 
        # to get total number of possible source errors (all items i got right and could source wrong)
        denom_me = hit_num - true_totals['me']
        denom_friend = hit_num - true_totals['friend']
        denom_other = hit_num - true_totals['other']
        denom_robot = hit_num - true_totals['robot']
        
        #empty list
        correct_items = []
        #if item in recon task was correctly mark as old add it to correct_items list == hits per valence
        for index, row in data.iterrows():
            if (row['réponse'] == 'OLD') & (row['item'] == 'OLD'):
                correct_items.append(row)

        #adding any items rated as old even though they were new to a list == false alarms
        new_items_seen_as_old = []
        for index, row in data.iterrows():
            if (row['réponse'] == 'OLD') & (row['item'] == 'NEW'):
                new_items_seen_as_old.append(row)

        #dataframe of correct items (hits)  
        correct_item_recon = pd.DataFrame(data = correct_items)

        #initialize counters for all possible pairs of encoded avatars and avatars remembered as source 
        vous_to_robot = 0
        vous_to_ami = 0
        vous_to_autrui = 0
        vous_to_vous = 0

        robot_to_robot = 0
        robot_to_ami = 0 
        robot_to_autrui = 0
        robot_to_vous = 0

        ami_to_robot = 0
        ami_to_ami = 0 
        ami_to_autrui = 0
        ami_to_vous = 0

        autrui_to_robot = 0
        autrui_to_ami = 0
        autrui_to_autrui = 0 
        autrui_to_vous = 0 

        new_to_me = 0
        new_to_friend = 0
        new_to_other = 0
        new_to_robot = 0

        #dataframe for new items said to be old (false alarms)
        false_alarms_recon = pd.DataFrame(data = new_items_seen_as_old)

        #count false alarms per avatar (assigned to each avatar)
        for row, item in false_alarms_recon.iterrows():
            if (item['source (avatar)'] == 'vous'):
                new_to_me = new_to_me +1
            if (item['source (avatar)'] == 'ami'):
                new_to_friend = new_to_friend +1
            if (item['source (avatar)'] == 'autrui'):
                new_to_other = new_to_other +1 
            if (item['source (avatar)'] == 'robot'):
                new_to_robot = new_to_robot +1

        # counting how many times each encoded / recognized avatar pairing occurs for errors and true responses 
        for row, item in correct_item_recon.iterrows():
            #what were robot items assigned to 
            if (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'robot'):
                robot_to_robot = robot_to_robot + 1
            elif (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'vous'):
                robot_to_vous = robot_to_vous + 1
            elif (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'autrui'):  
                robot_to_autrui = robot_to_autrui + 1
            elif (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'ami'):   
                robot_to_ami = robot_to_ami + 1   

            #what were friend items assigned to
            elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'robot'):
                ami_to_robot = ami_to_robot + 1
            elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'vous'): 
                ami_to_vous = ami_to_vous + 1 
            elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'autrui'):
                ami_to_autrui = ami_to_autrui + 1
            elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'ami'):
                ami_to_ami = ami_to_ami + 1
            
            #what were other items assigned to
            elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'robot'):
                autrui_to_robot = autrui_to_robot + 1
            elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'vous'): 
                autrui_to_vous = autrui_to_vous + 1  
            elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'autrui'):
                autrui_to_autrui = autrui_to_autrui + 1
            elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'ami'):
                autrui_to_ami = autrui_to_ami + 1

            #what were self items assigned to
            elif (item['encoded_avatar'] == 'vous') & (item['source (avatar)'] == 'robot'):
                vous_to_robot = vous_to_robot + 1
            elif (item['encoded_avatar'] == 'vous') & (item['source (avatar)'] == 'ami'):
                vous_to_ami = vous_to_ami + 1
            elif (item['encoded_avatar'] == 'vous') & (item['source (avatar)'] == 'autrui'):  
                vous_to_autrui = vous_to_autrui + 1
            elif (item['encoded_avatar'] == 'vous') & (item['source (avatar)'] == 'vous'):
                vous_to_vous = vous_to_vous + 1

            #else:
                #print('Issue with matching') #if something goes wrong such as spelling it would stand out with this print statemnet

        if valence == 'all':
            total_errors = (#source error accros valence to potentially get ratio of errors per valence so what amount of errors are for positive adj etc
                vous_to_robot +
                vous_to_ami +
                vous_to_autrui +

                robot_to_vous +
                robot_to_ami +
                robot_to_autrui +

                ami_to_robot +
                ami_to_autrui +
                ami_to_vous +

                autrui_to_robot +
                autrui_to_ami +
                autrui_to_vous
            )

        #i put 0 instead of the correct responses to get the ratio over total errors 
        #make dictionary for data 'from' means seen as this avatar and 'to' is remembered as 
        sources = {'from_me': [0, vous_to_ami, vous_to_autrui, vous_to_robot],
                    'from_friend': [ami_to_vous, 0, ami_to_autrui, ami_to_robot],
                    'from_other': [autrui_to_vous, autrui_to_ami, 0, autrui_to_robot], 
                    'from_robot': [robot_to_vous, robot_to_ami, robot_to_autrui, 0],
                    }

        source_attributions = pd.DataFrame(data = sources,
                                            index = ['to_me', 'to_friend','to_other', 'to_robot'])


        #number of false attributions to each avatar
        errors_to_me = (
            ami_to_vous +
            autrui_to_vous +
            robot_to_vous
        )

        errors_to_friend = (
            vous_to_ami +
            autrui_to_ami +
            robot_to_ami
        )

        errors_to_other = (
            vous_to_autrui +
            ami_to_autrui +
            robot_to_autrui
        )

        errors_to_robot = (
            vous_to_robot +
            ami_to_robot +
            autrui_to_robot
        )

        #error rate dict per avatar (attirbuted to avatar)
        #here denom is collective accross valence but nominator is per valence per participant
        error_rates = {
            'me': errors_to_me / denom_me,
            'friend': errors_to_friend / denom_friend,
            'other': errors_to_other / denom_other,
            'robot': errors_to_robot / denom_robot
        }

        def dict_to_fill(dict_name):
            '''takes name of dict and per participant assigns error rates per avatar
            key is avatar name and filled w error rate'''
            dict_name[participant_id] = {
                'me': error_rates['me'],
                'friend': error_rates['friend'],
                'other': error_rates['other'],
                'robot': error_rates['robot']
            
            }
            
        #make a dict for each valence and accross valence 
        if valence == 'all':
            dict_to_fill(all_data_dict)
        elif valence == 'pos':
            dict_to_fill(pos_data_dict)
        elif valence == 'neg':
            dict_to_fill(neg_data_dict)
        elif valence == 'neut':
            dict_to_fill(neut_data_dict)

        #file of source attribution table accross valence 
        if valence == 'all':
            source_attributions.to_csv('M2_Internship/data_analysis/source_attribution/source_attributions_table_' + str(participant_id) +'.csv')

all_dataframe = pd.DataFrame(data = all_data_dict)   
pos_dataframe = pd.DataFrame(data = pos_data_dict)
neg_dataframe = pd.DataFrame(data = neg_data_dict)
neut_dataframe = pd.DataFrame(data = neut_data_dict)
print(all_dataframe, pos_dataframe, neg_dataframe, neut_dataframe)

pivoted_df = pd.DataFrame(all_dataframe.stack()).reset_index()
pivoted_df.columns = ['condition', 'participant', 'source errors to avatars']  

pivoted_df_pos = pd.DataFrame(pos_dataframe.stack()).reset_index()
pivoted_df_pos.columns = ['condition', 'participant', 'source errors to avatars pos']  
pivoted_df_neg = pd.DataFrame(neg_dataframe.stack()).reset_index()
pivoted_df_neg.columns = ['condition', 'participant', 'source errors to avatars neg']  
pivoted_df_neut = pd.DataFrame(neut_dataframe.stack()).reset_index()
pivoted_df_neut.columns = ['condition', 'participant', 'source errors to avatars neut']  

print("ALL:", set(pivoted_df['participant']))
print("POS:", set(pivoted_df_pos['participant']))
print("NEG:", set(pivoted_df_neg['participant']))
print("NEUT:", set(pivoted_df_neut['participant']))

merged = pd.merge(pivoted_df, pivoted_df_pos, on= ['participant', 'condition'])
merged = pd.merge(merged, pivoted_df_neg, on= ['participant', 'condition'])
merged = pd.merge(merged, pivoted_df_neut, on= ['participant', 'condition'])

merged.to_csv("M2_Internship/figures_writing /pivoted_source_errors.csv")

all_dataframe['average'] = all_dataframe.mean(axis = 1)

fig, ax = plt.subplots(figsize= (5, 5))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], all_dataframe['average'])
ax.set_title('Distribution of Erroneous Attribution per Avatar')
plt.xlabel('Avatar Attributed To')
plt.ylabel('Average Percentage of Error')
plt.ylim(0, 1)
plt.savefig('M2_Internship/data_analysis/figures/average_error_distribution')
#['Me', 'Friend', 'Other', 'Robot']