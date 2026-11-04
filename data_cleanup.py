
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
