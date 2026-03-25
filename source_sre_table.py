#Source recognition scores equal the number of sources correctly remembered in each condition (e.g., self items correctly recognized as “self”) divided by the total number of items in the condition
import glob
import pandas as pd
import matplotlib.pyplot as plt
from functions_for_sre_analysis import valence_separation, count_items_per_avatar
from plottable import Table

'''Ce script compte le nombre de hits pour la mémoire de source par avatar
les hits pour la mémoire de source est un ratio du nombre de réposes justes (old dit old) 
avec aussi la source de juste (ex. moi dit moi)
divisé par le nombre d'items par condition (items encodés par avatar)
le script fait une moyenne des ces ratios pour tous les participants
Il resort un png average_source_hits pour visualiser ces moyennes et 
un tableau avec les données de hits source par participant'''

correct_sources = {}
items_per_avatar = {}
all_data_source_hits = {}
pos_source_hits = {}
neg_source_hits = {}
neut_source_hits = {}

for file in glob.glob("M2 Internship/data_analysis/mergeddata/*"):
    participant_id = file[-10:-4]
    print(participant_id) #show participant id being handled 

    all_data = pd.read_csv(file) #read file 

    negative_data, positive_data, neutral_data = valence_separation(all_data)

    datas = {'all': all_data, 'pos': positive_data, 'neg': negative_data, 'neut': neutral_data}

    for valence, data in datas.items():
        AVATARS = ['vous', 'ami', 'autrui', 'robot']

        def count_source_hits_per_avatar(avatar_name, dataframe):
            avatar_hits = []
            for item, row in dataframe.iterrows():
                if (row['encoded_avatar'] == avatar_name) & (row['source (avatar)'] == avatar_name):
                    avatar_hits.append(row)
            number_source_hits_avatar = len(avatar_hits)
            correct_sources[avatar_name] = number_source_hits_avatar

        source_ratios = {}
        for avatar in AVATARS:
            count_items_per_avatar(avatar, data, items_per_avatar)
            count_source_hits_per_avatar(avatar, data)
            source_ratios[avatar] = correct_sources[avatar] / items_per_avatar[avatar]
        
        #print(correct_sources, items_per_avatar, source_ratios)

        def make_dicts(dict_to_make):
            dict_to_make[participant_id] = {
                'me': source_ratios['vous'],
                'friend': source_ratios['ami'],
                'other': source_ratios['autrui'],
                'robot': source_ratios['robot']
            }
        
        if valence == 'all':
            make_dicts(all_data_source_hits)
        elif valence == 'pos':
             make_dicts(pos_source_hits)
        elif valence == 'neg':
             make_dicts(neg_source_hits)
        elif valence == 'neut':
             make_dicts(neut_source_hits)


all_data_source_hits_frame = pd.DataFrame(data = all_data_source_hits)  
pos_source_hits_frame = pd.DataFrame(data = pos_source_hits)
neg_source_hits_frame = pd.DataFrame(data = neg_source_hits)
neut_source_hits_frame = pd.DataFrame(data = neut_source_hits)

#takes data from all participats on source hits and stacks them for ANOVA format 
pivoted = pd.DataFrame(all_data_source_hits_frame.stack()).reset_index()
pivoted.columns = ['condition', 'participant', 'source hits']

pivoted_pos = pd.DataFrame(pos_source_hits_frame.stack()).reset_index()
pivoted_pos.columns = ['condition', 'participant', 'source hits pos']

pivoted_neg = pd.DataFrame(neg_source_hits_frame.stack()).reset_index()
pivoted_neg.columns = ['condition', 'participant', 'source hits neg']

pivoted_neut = pd.DataFrame(neg_source_hits_frame.stack()).reset_index()
pivoted_neut.columns = ['condition', 'participant', 'source hits neut']

#mege data files for all, pos, neutral, negative 

merged = pd.merge(pivoted, pivoted_pos, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_neg, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_neut, on= ['condition', 'participant'])

merged.to_csv("M2 Internship/data_analysis/figures/pivoted_source_hits.csv")
print(merged)

#calculate average accross participants 
all_data_source_hits_frame['average'] = all_data_source_hits_frame.mean(axis = 1)

#IF I WANT A TABLE OF AVERAGE SOURCE HITS ACCROSS PP 

#PLOTTING 
fig, ax = plt.subplots(figsize= (6, 6))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], all_data_source_hits_frame['average'])
ax.set_title('Proportion of Correct Source Memory Per Avatar')
plt.xlabel('Avatar Encoded')
plt.ylabel('Average Percentage Correct Source Encoding')
plt.ylim(0, 1)
plt.savefig('M2 Internship/data_analysis/figures/average_source_hits')

# Source Memory for Self and Other in Patients With Mild Cognitive Impairment due to Alzheimer’s Disease
# see if other papers have the same calculation for corrected item memory 
# and same calculation for source memory scores 
