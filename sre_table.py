import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from functions_for_sre_analysis import separate_hit_type
from functions_for_sre_analysis import count_items_per_avatar
from functions_for_sre_analysis import valence_separation
from plottable import Table

'''Ce script compte les ratios de hits, false alarms, misses par participant 
puis calcule la moyenne de tous ces ratios avec les données de tous les participants
il resort: un png pour la moyenne des miss, false alarms et les hits non corrigés et corrigés
et un tableau des données (hits corrigees, non corrigees, fa et miss) pour tous les participants
--> corrigés correspond a la proportion des false alarms par avatar soustraites de la proportion de hits par avatar'''

#CHANGE divide by number of items old per avatar (correct or incorrect response) or new 
#fa proportion is nb new items assigned avatar / total number new items 

#initialise dictrionnaries to regroup all participant data at the end 
all_data_noncorrected = {}
all_data_corrected = {}
fa_data = {}
cr_data = {}
miss_data = {}
pos_noncorrected = {}
neg_noncorrected = {}
neut_noncorrected = {}
pos_corrected = {}
neg_corrected = {}
neut_corrected = {}
pos_fa = {}
neg_fa = {}
neut_fa = {}
pos_miss = {}
neg_miss = {}
neut_miss = {}

for file in glob.glob("M2 Internship/data_analysis/mergeddata/*"):

    participant_id = file[-10:-4]
    print(participant_id) #show participant id being handled 

    all_data = pd.read_csv(file) #read file 

    negative_data, positive_data, neutral_data = valence_separation(all_data)

    datas = {'all': all_data, 'neg': negative_data, 'pos': positive_data, 'neut': neutral_data}

    for valence, data in datas.items():
        avatars = ['vous', 'ami', 'autrui', 'robot']
        
        #total hits, fas, miss, cr - regardless of avatar
        #function adds all rows of response type to apporpriate list 
        #RUN THIS ON NEG, POS, NEUTRAL DATA 
        hit, fa, miss, cr = separate_hit_type(data, 'item', 'réponse', 'OLD')

        items_per_avatar = {}

        TOTAL_NEW_ITEMS = 72
        WORDS_PER_AVATAR = 18 

        for avatar in avatars:
            count_items_per_avatar(avatar, data, items_per_avatar)

        #counting NEW items
        new_items = []
        for item, row in data.iterrows():
            if row['item'] == 'NEW':
                new_items.append(row)
        num_new_items = len(new_items)

        #counting each
        number_hits = len(hit)
        number_fa = len(fa)
        number_miss = len(miss)
        number_cr = len(cr)
        #print(number_cr, number_fa, number_hits, number_miss)

        #dataframes separate for response type
        hit = pd.DataFrame(hit)
        fa = pd.DataFrame(fa)
        miss = pd.DataFrame(miss)
        cr = pd.DataFrame(cr)

        #initialize empty dicts for response type to sort per avatar info
        hits = {}
        fas = {}
        misses = {}
        crs = {}

        def number_hits_per_avatar(name_of_avatar, df_to_use, dict_name, row_to_search_for_avatar): 
            '''
            this function takes the name of an avatar 
            it compares that name to the avatar participants encoded
            this gives you the number of rows from the dataset used that have that avatar
            adds this to a chosen dictionnary of the following format {avatar: number items} 
            fa and cr will be sorted by avatar sourced not encoded 
            hits and misses will be sorted by avatar encoded 
            specify this with row_to_search_for_avatar'''

            avatar_hits = []
            for item, row in df_to_use.iterrows():
                if row[row_to_search_for_avatar] == name_of_avatar:
                    avatar_hits.append(row)
            number_hits = len(avatar_hits) #for the avatar in the function you get the number of hits (or fa, cr etc depending on dict used)
            dict_name[name_of_avatar] = number_hits

        for avatar in avatars: #run a loop over the list of avatars to get the number of hits etc for each avatar in the dict 'hits' etc
            number_hits_per_avatar(avatar, hit, hits, 'encoded_avatar')
            number_hits_per_avatar(avatar, fa, fas, 'source (avatar)')
            #CORRECT REJECTIONS PER AVATAR ISN'T POSSIBLE IT WILL BE 0
            number_hits_per_avatar(avatar, miss, misses, 'encoded_avatar')

        #ititialize empty dictionaries that will have the ratio of hits per avatar to total hits etc
        hit_ratios = {}
        fa_ratios = {}
        miss_ratios = {}

        #MAKE THIS INTO FUCNTION OR LOOP OVER THE FOUR DICTS AND RESPONSE TYPES
        
        def calculate_response_ratio(ratio_dict, response_dict, response_count, avatar):
            if response_count == 0:
                ratio_dict[avatar] = 0
            else:
                ratio_dict[avatar] = response_dict[avatar] / response_count
        
        for avatar in avatars: #for each avatar calculate the hits per avatar over the total hits 
            calculate_response_ratio(hit_ratios, hits, items_per_avatar[avatar], avatar)
            calculate_response_ratio(fa_ratios, fas, num_new_items, avatar)
            calculate_response_ratio(miss_ratios, misses, items_per_avatar[avatar], avatar)
            

        #corrected ratios per avatar for item memory
        corrected_item_memory = {}
        for avatar in avatars:
            corrected_item_memory[avatar] = hit_ratios[avatar] - fa_ratios[avatar] 
        #print(corrected_item_memory)
        
        #dictionnary per participant with all the ratios corrected or not 
        def make_dicts_for_data(dict_to_fill_nc, dict_to_fill_c, dict_to_fill_fa, dict_to_fill_miss):
            dict_to_fill_nc[participant_id] = {
                'me': hit_ratios['vous'],
                'friend': hit_ratios['ami'],
                'other': hit_ratios['autrui'],
                'robot': hit_ratios['robot']
            }

            dict_to_fill_c[participant_id] = {
                'me': corrected_item_memory['vous'],
                'friend': corrected_item_memory['ami'],
                'other': corrected_item_memory['autrui'],
                'robot': corrected_item_memory['robot']
            }

            dict_to_fill_fa[participant_id] = {
                'me': fa_ratios['vous'],
                'friend': fa_ratios['ami'],
                'other': fa_ratios['autrui'],
                'robot': fa_ratios['robot']
            }

            dict_to_fill_miss[participant_id] = {
                'me': miss_ratios['vous'],
                'friend': miss_ratios['ami'],
                'other': miss_ratios['autrui'],
                'robot': miss_ratios['robot']
            }
        
        if valence == 'all':
            make_dicts_for_data(all_data_noncorrected, all_data_corrected, fa_data, miss_data)
        elif valence == 'pos':
            make_dicts_for_data(pos_noncorrected, pos_corrected, pos_fa, pos_miss)
        elif valence == 'neg':
            make_dicts_for_data(neg_noncorrected, neg_corrected, neg_fa, neg_miss)
        elif valence == 'neut':
            make_dicts_for_data(neut_noncorrected, neut_corrected, neut_fa, neut_miss)

#make dataframes for corrected and non-corrected ratios 
all_data_correctedframe = pd.DataFrame(data = all_data_corrected)
pos_corrected_frame = pd.DataFrame(data = pos_corrected)
neg_corrected_frame = pd.DataFrame(data = neg_corrected)
neut_corrected_frame = pd.DataFrame(data = neut_corrected)

pivoted_corr = pd.DataFrame(all_data_correctedframe.stack()).reset_index()
pivoted_corr.columns = ['condition', 'participant', 'corrected hits']  
pivoted_corr_pos = pd.DataFrame(pos_corrected_frame.stack()).reset_index()
pivoted_corr_pos.columns = ['condition', 'participant', 'corrected hits pos']  
pivoted_corr_neg = pd.DataFrame(neg_corrected_frame.stack()).reset_index()
pivoted_corr_neg.columns = ['condition', 'participant', 'corrected hits neg']  
pivoted_corr_neut = pd.DataFrame(neut_corrected_frame.stack()).reset_index()
pivoted_corr_neut.columns = ['condition', 'participant', 'corrected hits neut']  

all_data_noncorrectedframe = pd.DataFrame(data = all_data_noncorrected)
pos_noncorrected_frame = pd.DataFrame(data = pos_noncorrected)
neg_noncorrected_frame = pd.DataFrame(data = neg_noncorrected)
neut_noncorrected_frame = pd.DataFrame(data = neut_noncorrected)

pivoted_noncorr = pd.DataFrame(all_data_noncorrectedframe.stack()).reset_index()
pivoted_noncorr.columns = ['condition', 'participant', 'hits (uncorrected)']  
pivoted_noncorr_pos = pd.DataFrame(pos_noncorrected_frame.stack()).reset_index()
pivoted_noncorr_pos.columns = ['condition', 'participant', 'hits (uncorrected) pos']  
pivoted_noncorr_neg = pd.DataFrame(neg_noncorrected_frame.stack()).reset_index()
pivoted_noncorr_neg.columns = ['condition', 'participant', 'hits (uncorrected) neg']  
pivoted_noncorr_neut = pd.DataFrame(neut_noncorrected_frame.stack()).reset_index()
pivoted_noncorr_neut.columns = ['condition', 'participant', 'hits (uncorrected) neut']  

miss_df = pd.DataFrame(data = miss_data)
pos_miss_df = pd.DataFrame(data = pos_miss)
neg_miss_df = pd.DataFrame(data = neg_miss)
neut_miss_df = pd.DataFrame(data = neut_miss)

pivoted_miss = pd.DataFrame(miss_df.stack()).reset_index()
pivoted_miss.columns = ['condition', 'participant', 'misses']  
pivoted_miss_pos = pd.DataFrame(pos_miss_df.stack()).reset_index()
pivoted_miss_pos.columns = ['condition', 'participant', 'misses pos']  
pivoted_miss_neg = pd.DataFrame(neg_miss_df.stack()).reset_index()
pivoted_miss_neg.columns = ['condition', 'participant', 'misses neg']  
pivoted_miss_neut = pd.DataFrame(neut_miss_df.stack()).reset_index()
pivoted_miss_neut.columns = ['condition', 'participant', 'misses neut']  

fa_df = pd.DataFrame(data = fa_data)
pos_fa_df = pd.DataFrame(data = pos_fa)
neg_fa_df = pd.DataFrame(data = neg_fa)
neut_fa_df = pd.DataFrame(data = neut_fa)

pivoted_fa = pd.DataFrame(fa_df.stack()).reset_index()
pivoted_fa.columns = ['condition', 'participant', 'false alarms']  
pivoted_fa_pos = pd.DataFrame(pos_fa_df.stack()).reset_index()
pivoted_fa_pos.columns = ['condition', 'participant', 'false alarms pos']  
pivoted_fa_neg = pd.DataFrame(neg_fa_df.stack()).reset_index()
pivoted_fa_neg.columns = ['condition', 'participant', 'false alarms neg']  
pivoted_fa_neut = pd.DataFrame(neut_fa_df.stack()).reset_index()
pivoted_fa_neut.columns = ['condition', 'participant', 'false alarms neut']  

#print(all_data_noncorrframe, all_data_correctedframe, miss_df, fa_df, pivoted_corr, pivoted_fa, pivoted_miss, pivoted_noncorr)

data_frames = [pivoted_corr, pivoted_noncorr, pivoted_fa, pivoted_miss]

merged = pd.merge(pivoted_corr, pivoted_corr_pos, on= ['participant', 'condition'])
merged = pd.merge(merged, pivoted_corr_neg, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_corr_neut, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_noncorr, on = ['participant','condition'])
merged = pd.merge(merged, pivoted_noncorr_pos, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_noncorr_neg, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_noncorr_neut, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_fa, on = ['participant','condition'])
merged = pd.merge(merged, pivoted_fa_pos, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_fa_neg, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_fa_neut, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_miss, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_miss_pos, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_miss_neg, on= ['participant','condition'])
merged = pd.merge(merged, pivoted_miss_neut, on= ['participant','condition'])

print(merged)

merged.to_csv("M2 Internship/data_analysis/figures/self_reference_effect.csv")

#calculate average accross participants 
all_data_correctedframe['average'] = all_data_correctedframe.mean(axis = 1)
all_data_noncorrectedframe['average'] = all_data_noncorrectedframe.mean(axis = 1)
miss_df['average'] = miss_df.mean(axis = 1)
fa_df['average'] = fa_df.mean(axis = 1)
#cr_df['average'] = cr_df.mean(axis = 1)


#IF I WANT TABLES FOR THE AVERAGES OF RESPONSE TYPES 

#PLOTTING 
fig, ax = plt.subplots(figsize= (6, 6))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], all_data_correctedframe['average'])
ax.set_title('Proportion of Corrected Item Memory Per Avatar')
plt.xlabel('Avatar Encoded')
plt.ylabel('Average Percentage Correct Item Memory')
plt.ylim(0, 1)
plt.savefig('M2 Internship/data_analysis/figures/corrected_item_memory')

fig, ax = plt.subplots(figsize= (5, 5))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], all_data_noncorrectedframe['average'])
ax.set_title('Proportion of Item Memory Hits Per Avatar')
plt.xlabel('Avatar Encoded')
plt.ylabel('Average Percentage Correct Item Memory')
plt.ylim(0, 1)
plt.savefig('M2 Internship/data_analysis/figures/non_corrected_item_memory')

fig, ax = plt.subplots(figsize= (5, 5))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], fa_df['average'])
ax.set_title('Proportion of False Alarms Per Avatar')
plt.xlabel('Avatar Encoded')
plt.ylabel('Average Percentage False Alarms')
plt.ylim(0, 1)
plt.savefig('M2 Internship/data_analysis/figures/false_alarms')

fig, ax = plt.subplots(figsize= (5, 5))
plt.bar(['Me', 'Friend', 'Other', 'Robot'], miss_df['average'])
ax.set_title('Proportion of Misses Per Avatar')
plt.xlabel('Avatar Encoded')
plt.ylabel('Average Percentage Misses')
plt.ylim(0, 1)
plt.savefig('M2 Internship/data_analysis/figures/misses')

    #TO DO -- CHECK IF THE NUMBERS ARE CORRECT FOR SAMPLE DATA
    #edit code to take into account spelling mistakes 
    #['Me', 'Friend', 'Other', 'Robot']