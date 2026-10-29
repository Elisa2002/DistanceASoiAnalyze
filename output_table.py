
from cmath import nan
import os
import pandas as pd 
from plottable import Table
import matplotlib.pyplot as plt
import numpy as np
from functions_for_sre_analysis import valence_separation

#change paths to be within data_analysis folder, so github friendly

''' 
Pour l'instant, ce script doit être run avant les autres puisqu'il sert au data cleanup
Pour l'instant, ce script sert au clean up des fichiers de data
les fichiers doivent être dans deux dossiers, un pour l'encodage 'ref_data'
et un pour la reco 'recon_data' 
Le cleanup change les fautes d'orthographe et met les deux fichers 
pour un participant dans un meme data frame 'mergeddataphase2' et le num de participant
Suite au clean up, le script sert à compter les erreurs de source par participant et en moyenne 
la moyenne est la moyenne du ratio nombre d'erreurs vers l'avatar divisé par le numéro total d'erreurs de source
Le script sort un merged data file par participant avec toutes les données 
et un graphique avec les erreurs moyenne par avatar
Il sort aussi un tableau qui regroupe par paritipant les ratios d'erreurs de source'''

all_data = {}
pos_data_dict = {}
neg_data_dict = {}
neut_data_dict = {}

#LOADING DATA
#pick files from ref folder that matches participant id in recon folder and assign those tho variables to use 
for reconfilename in os.listdir("M2 Internship/data_analysis/recon_data"):
    for reffilename in os.listdir("M2 Internship/data_analysis/ref_data"):
        if reconfilename.endswith('.csv') & reffilename.endswith('.csv'):
            if reconfilename[0:6] == reffilename[0:6]:
                participant_id = reconfilename[0:6]
                print(participant_id)
                recon = pd.read_csv("M2 Internship/data_analysis/recon_data/" + str(reconfilename))
                ref = pd.read_csv("M2 Internship/data_analysis/ref_data/" + str(reffilename))
                
    

                #DATA CLEANUP AND COMBINING 
                #change avatar titles in the reference task output to match titles in the recon task output
                ref['Avatar'] = ref['Avatar'].str.replace('un robot', 'robot')
                ref['Avatar'] = ref['Avatar'].str.replace('vous-même', 'vous')
                ref['Avatar'] = ref['Avatar'].str.replace('moi-même', 'vous')
                ref['Avatar'] = ref['Avatar'].str.replace("quelqu'un d'autre", 'autrui')
                ref['Avatar'] = ref['Avatar'].str.replace('votre ami', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('votre amie', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('mon ami', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('mon amie', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('amie', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('votre-amie', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('votre-ami', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('vous même', 'vous')
                ref['Avatar'] = ref['Avatar'].str.replace('julie_friend', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('sophia_friend', 'ami')
                ref['Avatar'] = ref['Avatar'].str.replace('julie_me', 'vous')
                ref['Avatar'] = ref['Avatar'].str.replace('sophia_me', 'vous')
                ref['Avatar'] = ref['Avatar'].str.replace('vous_même', 'vous')
                
                #fixing typos
                recon['adjectif']
                ref['Word'] = ref['Word'].str.replace('accomodante','accommodante')
                ref['Word'] = ref['Word'].str.replace('accomodant','accommodant')
                recon['adjectif'] = recon['adjectif'].str.replace('accomodante','accommodante')
                recon['adjectif'] = recon['adjectif'].str.replace('accomodant','accommodant')

                ref['Word'] = ref['Word'].str.replace('grognone','grognonne')
                recon['adjectif'] = recon['adjectif'].str.replace('grognone','grognonne')

                ref['Word'] = ref['Word'].str.replace('progessiste','progressiste')
                recon['adjectif'] = recon['adjectif'].str.replace('progessiste','progressiste')

                recon['adjectif'] = recon['adjectif'].str.replace('hauntain','hautain')
                ref['Word'] = ref['Word'].str.replace('hauntain', 'hautain')

                recon['adjectif'] = recon['adjectif'].str.replace('implusif','impulsif')

                ref['Word'] = ref['Word'].str.replace('fatiguant','fatigant')
                recon['adjectif'] = recon['adjectif'].str.replace('fantiguant','fatigant')
                ref['Word'] = ref['Word'].str.replace('fatiguante','fatigante')
                recon['adjectif'] = recon['adjectif'].str.replace('fatiguante','fatigante')

                ref['Word'] = ref['Word'].str.replace('Distingué', 'distingué')
                recon['adjectif'] = recon['adjectif'].str.replace('Distingué', 'distingué')

                ref['Word'] = ref['Word'].str.strip()
                recon['adjectif'] = recon['adjectif'].str.strip()
                
                
                #adding to one same dataframe information about the encoding -- the avatar, it the item was old or new, the category of the word etc
                #this is such that no mater the list that is new or old it will go through and add to the table whether it was old or new

                #merge both data files so that for all encoded words encoding info is stored with remembered info
                #recon has merged data in DataFrame format 
                for index, row in recon.iterrows(): #for reach row in the recon data 
                    matched_avatar = False
                    for index_ref, ref_row in ref.iterrows(): #check if the word is the same as the word in any row in the reference task data
                        if row['adjectif'] == ref_row['Word']:
                            matched_avatar = True
                            recon.loc[index, 'item'] = 'OLD'
                            recon.loc[index, 'encoded_avatar'] = ref_row['Avatar']
                            recon.loc[index, 'category'] = ref_row['Category']
                            recon.loc[index, 'reference?'] = ref_row['Answer']
                            recon.loc[index, 'RT'] = ref_row['ReactionTime']
                    #if matched_avatar == False:
                        #print(ref_row['Word'], row['adjectif'])
                            
                        

                for index, row in recon.iterrows(): #check if the word was not identified as old mark it as new 
                    if pd.isna(recon.loc[index, 'item']):
                        recon.loc[index, 'item'] = 'NEW'
                        

                recon.to_csv('M2 Internship/data_analysis/mergeddata/mergeddataphase2' + str(participant_id) + '.csv')

                #DATA SETUP FOR RATIO CALCULATION

                negative_data, positive_data, neutral_data = valence_separation(recon)

                datas = {'all': recon, 'pos': positive_data, 'neg' : negative_data, 'neut': neutral_data}

                hits = []
                #if item in recon task was correctly mark as old add it to correct_items list 
                for index, row in recon.iterrows():
                    if (row['réponse'] == 'OLD') & (row['item'] == 'OLD'):
                        hits.append(row)
                hit_num = len(hits)
                hits= pd.DataFrame(hits)


                true_totals = {
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
                        
                denom_me = hit_num - true_totals['me']
                denom_friend = hit_num - true_totals['friend']
                denom_other = hit_num - true_totals['other']
                denom_robot = hit_num - true_totals['robot']

                for valence, data in datas.items():
                    print(valence)
                    #empty list
                    correct_items = []
                    #if item in recon task was correctly mark as old add it to correct_items list 
                    for index, row in data.iterrows():
                        if (row['réponse'] == 'OLD') & (row['item'] == 'OLD'):
                            correct_items.append(row)

                    #adding any items rated as old even though they were new to a list 
                    new_items_seen_as_old = []
                    for index, row in data.iterrows():
                        if (row['réponse'] == 'OLD') & (row['item'] == 'NEW'):
                            new_items_seen_as_old.append(row)

                    #dataframe of correct items        
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

                    #dataframe for new items said to be old 
                    new_item_recon = pd.DataFrame(data = new_items_seen_as_old)

                    #count how many times new items are falsly marked as belonging to each encoding condition
                    for row, item in new_item_recon.iterrows():
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
                        if (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'robot'):
                            robot_to_robot = robot_to_robot + 1
                        elif (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'vous'):
                            robot_to_vous = robot_to_vous + 1
                        elif (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'autrui'):  
                            robot_to_autrui = robot_to_autrui + 1
                        elif (item['encoded_avatar'] == 'robot') & (item['source (avatar)'] == 'ami'):   
                            robot_to_ami = robot_to_ami + 1   

                        elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'robot'):
                            ami_to_robot = ami_to_robot + 1
                        elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'vous'): 
                            ami_to_vous = ami_to_vous + 1 
                        elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'autrui'):
                            ami_to_autrui = ami_to_autrui + 1
                        elif (item['encoded_avatar'] == 'ami') & (item['source (avatar)'] == 'ami'):
                            ami_to_ami = ami_to_ami + 1
                        
                        elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'robot'):
                            autrui_to_robot = autrui_to_robot + 1
                        elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'vous'): 
                            autrui_to_vous = autrui_to_vous + 1  
                        elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'autrui'):
                            autrui_to_autrui = autrui_to_autrui + 1
                        elif (item['encoded_avatar'] == 'autrui') & (item['source (avatar)'] == 'ami'):
                            autrui_to_ami = autrui_to_ami + 1

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
                        total_errors = (
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
                    #make dictionarry for data from means seen as this avatar and to is remembered as 
                    sources = {'from_me': [0, vous_to_ami, vous_to_autrui, vous_to_robot],
                                'from_friend': [ami_to_vous, 0, ami_to_autrui, ami_to_robot],
                                'from_other': [autrui_to_vous, autrui_to_ami, 0, autrui_to_robot], 
                                'from_robot': [robot_to_vous, robot_to_ami, robot_to_autrui, 0],
                                }

                    source_attributions = pd.DataFrame(data = sources,
                                                        index = ['to_me', 'to_friend','to_other', 'to_robot'])

                    '''if total_errors == 0:
                        source_attributions['errors to x / total errors'] = 0
                    else:
                        source_attributions['errors to x / total errors'] = (
                            source_attributions['from_me'] + source_attributions['from_friend'] + source_attributions['from_other'] + source_attributions['from_robot']
                            ) / total_errors'''
                    
                    # total attributed items for each true source avatar
# (INCLUDING correct responses)
                    '''
                    if valence == "all":
                        true_totals = {
                            'me': (
                                vous_to_vous +
                                vous_to_ami +
                                vous_to_autrui +
                                vous_to_robot
                            ),

                            'friend': (
                                ami_to_ami +
                                ami_to_vous +
                                ami_to_autrui +
                                ami_to_robot
                            ),

                            'other': (
                                autrui_to_autrui +
                                autrui_to_vous +
                                autrui_to_ami +
                                autrui_to_robot
                            ),

                            'robot': (
                                robot_to_robot +
                                robot_to_vous +
                                robot_to_ami +
                                robot_to_autrui
                            )
                        }'''

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


                    error_rates = {
                        'me': errors_to_me / denom_me,
                        'friend': errors_to_friend / denom_friend,
                        'other': errors_to_other / denom_other,
                        'robot': errors_to_robot / denom_robot
                    }

                    '''
                    source_attributions['errors to x / total errors'] =(
                        source_attributions['from_me'] + source_attributions['from_friend'] + source_attributions['from_other'] + source_attributions['from_robot']
                        )/ hit_num 
                    '''
                    '''
                    def dict_to_fill(dict_name):
                        dict_name[participant_id] = {
                            'me': source_attributions.loc['to_me', 'errors to x / total errors'],
                            'friend': source_attributions.loc['to_friend', 'errors to x / total errors'],
                            'other': source_attributions.loc['to_other', 'errors to x / total errors'],
                            'robot': source_attributions.loc['to_robot', 'errors to x / total errors']}
                    '''
                    def dict_to_fill(dict_name):
                        dict_name[participant_id] = {
                            'me': error_rates['me'],
                            'friend': error_rates['friend'],
                            'other': error_rates['other'],
                            'robot': error_rates['robot']
                        
                        }
                     
                    if valence == 'all':
                        dict_to_fill(all_data)
                    elif valence == 'pos':
                        dict_to_fill(pos_data_dict)
                    elif valence == 'neg':
                        dict_to_fill(neg_data_dict)
                    elif valence == 'neut':
                        dict_to_fill(neut_data_dict)

                    if valence == 'all':
                        source_attributions.to_csv('M2 Internship/data_analysis/source_attribution/source_attributions_table_' + str(participant_id) +'.csv')

all_dataframe = pd.DataFrame(data = all_data)   
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

merged.to_csv("M2 Internship/data_analysis/figures/pivoted_source_errors.csv")

all_dataframe['average'] = all_dataframe.mean(axis = 1)

fig, ax = plt.subplots(figsize= (5, 5))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], all_dataframe['average'])
ax.set_title('Distribution of Erroneous Attribution per Avatar')
plt.xlabel('Avatar Attributed To')
plt.ylabel('Average Percentage of Error')
plt.ylim(0, 1)
plt.savefig('M2 Internship/data_analysis/figures/average_error_distribution')
#['Me', 'Friend', 'Other', 'Robot']