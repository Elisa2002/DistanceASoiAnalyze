#Source recognition scores equal the number of sources correctly remembered in each condition (e.g., self items correctly recognized as “self”) divided by the total number of items in the condition
import glob
import pandas as pd
import matplotlib.pyplot as plt
from functions_for_sre_analysis import valence_separation, count_items_per_avatar
from plottable import Table
from functions_for_sre_analysis import count_items_per_avatar

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
all_other_source_h = {}
pos_other_source_h = {}
neg_other_source_h = {}
neut_other_source_h = {}
AVATARS = ['vous', 'ami', 'autrui', 'robot']

for file in glob.glob("M2 Internship/data_analysis/mergeddata/*"):
    participant_id = file[-10:-4]
    print(participant_id) #show participant id being handled 

    all_data = pd.read_csv(file) #read file 

    negative_data, positive_data, neutral_data = valence_separation(all_data)

    datas = {'all': all_data, 'pos': positive_data, 'neg': negative_data, 'neut': neutral_data}

    all_hits = all_data[
        (all_data['item'] == 'OLD') &
        (all_data['réponse'] == 'OLD')
    ]

    total_hits_per_avatar = {}

    for avatar in AVATARS:
        count_items_per_avatar(avatar, all_hits, total_hits_per_avatar)

    for valence, data in datas.items():

        def count_source_hits_per_avatar(avatar_name, dataframe):
            avatar_hits = []
            for item, row in dataframe.iterrows():
                if (row['encoded_avatar'] == avatar_name) & (row['source (avatar)'] == avatar_name):
                    avatar_hits.append(row)
            number_source_hits_avatar = len(avatar_hits)
            correct_sources[avatar_name] = number_source_hits_avatar

        source_ratios = {}
        source_hit_ratio = {}
        for avatar in AVATARS:
            count_items_per_avatar(avatar, data, items_per_avatar)
            count_source_hits_per_avatar(avatar, data)
            source_ratios[avatar] = correct_sources[avatar] / items_per_avatar[avatar]
            source_hit_ratio[avatar] = (correct_sources[avatar] /total_hits_per_avatar[avatar])
 
        def make_dicts(dict_to_make):
            dict_to_make[participant_id] = {
                'me': source_ratios['vous'],
                'friend': source_ratios['ami'],
                'other': source_ratios['autrui'],
                'robot': source_ratios['robot']
            }
        def make_dicts_o(dict_to_make):
            dict_to_make[participant_id] = {
                'me': source_hit_ratio['vous'],
                'friend': source_hit_ratio['ami'],
                'other': source_hit_ratio['autrui'],
                'robot': source_hit_ratio['robot']
            }

        
        if valence == 'all':
            make_dicts(all_data_source_hits)
            make_dicts_o(all_other_source_h)
        elif valence == 'pos':
             make_dicts(pos_source_hits)
             make_dicts_o(pos_other_source_h)
        elif valence == 'neg':
             make_dicts(neg_source_hits)
             make_dicts_o(neg_other_source_h)
        elif valence == 'neut':
             make_dicts(neut_source_hits)
             make_dicts_o(neut_other_source_h)


all_data_source_hits_frame = pd.DataFrame(data = all_data_source_hits)  
pos_source_hits_frame = pd.DataFrame(data = pos_source_hits)
neg_source_hits_frame = pd.DataFrame(data = neg_source_hits)
neut_source_hits_frame = pd.DataFrame(data = neut_source_hits)

all_other_source_h = pd.DataFrame(data = all_other_source_h)  
pos_other_source_h = pd.DataFrame(data = pos_other_source_h)
neg_other_source_h = pd.DataFrame(data = neg_other_source_h)
neut_other_source_h = pd.DataFrame(data = neut_other_source_h)

#takes data from all participats on source hits and stacks them for ANOVA format 
pivoted = pd.DataFrame(all_data_source_hits_frame.stack()).reset_index()
pivoted.columns = ['condition', 'participant', 'source hits']

pivoted_pos = pd.DataFrame(pos_source_hits_frame.stack()).reset_index()
pivoted_pos.columns = ['condition', 'participant', 'source hits pos']

pivoted_neg = pd.DataFrame(neg_source_hits_frame.stack()).reset_index()
pivoted_neg.columns = ['condition', 'participant', 'source hits neg']

pivoted_neut = pd.DataFrame(neut_source_hits_frame.stack()).reset_index()
pivoted_neut.columns = ['condition', 'participant', 'source hits neut']

pivoted_neut_other = pd.DataFrame(neut_other_source_h.stack()).reset_index()
pivoted_neut_other.columns = ['condition', 'participant', 'o source hits neut']

pivoted_neg_other = pd.DataFrame(neg_other_source_h.stack()).reset_index()
pivoted_neg_other.columns = ['condition', 'participant', 'o source hits neg']

pivoted_pos_other = pd.DataFrame(pos_other_source_h.stack()).reset_index()
pivoted_pos_other.columns = ['condition', 'participant', 'o source hits pos']

pivoted_o = pd.DataFrame(all_other_source_h.stack()).reset_index()
pivoted_o.columns = ['condition', 'participant', 'o source hits']

#mege data files for all, pos, neutral, negative 

merged = pd.merge(pivoted, pivoted_pos, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_neg, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_neut, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_o, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_pos_other, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_neut_other, on= ['condition', 'participant'])
merged = pd.merge(merged, pivoted_neg_other, on= ['condition', 'participant'])

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
