#nb words chosen per avatar --> response yes to encoded adj per participant per avatar
# between participants what adjectives were chosem --> count appearances of each adjective for each avatar frequency of words
#correlations with other measures such as embodiement etc?

import pandas as pd 
import matplotlib.pyplot as plt
import glob
from functions_for_sre_analysis import valence_separation

#these dicts track for all particpants the words selected for each avatar
all_robot_is_rows = []
all_other_is_rows = []
all_i_am_rows = []
all_friend_is_rows = []
amount_adj_per_avatar = {}

def separate_rows_per_avatar(df, robot_dict, other_dict, friend_dict, me_dict):
    '''this function takes the dataframe of interest and assigns 
    all rows for robot to a robot dictionnary 
    rows for other in an other dictionnary 
    rows encoded in the friend avatar in friend dict
    rows encoded in self avatar in me dict
    dicts must be defined previously 
    reference? row must exist as should encoded avatar'''
    for item, row in df.iterrows():
        if row['reference?'] == True:
            if row['encoded_avatar'] == 'robot':
                robot_dict.append(row)
            elif row['encoded_avatar'] == 'vous':
                me_dict.append(row)
            elif row['encoded_avatar'] == 'ami':
                friend_dict.append(row)
            elif row['encoded_avatar'] == 'autrui':
                other_dict.append(row)


for file in glob.glob("M2 Internship/data_analysis/mergeddata/*"):
    data = pd.read_csv(file)

    participant_id = file[-10:-4]

    negative_data, positive_data, neutral_data = valence_separation(data)

    #these dicts tracks rows per participant that were yes 
    robot_is_rows = []
    other_is_rows = []
    i_am_rows = []
    friend_is_rows = []

    robot_pos = []
    robot_neg = []
    robot_neut = []

    other_pos = []
    other_neg = []
    other_neut = []

    friend_pos = []
    friend_neg = []
    friend_neut = []

    me_pos = []
    me_neg = []
    me_neut = []

    separate_rows_per_avatar(data, robot_is_rows, other_is_rows, friend_is_rows, i_am_rows)
    separate_rows_per_avatar(data, all_robot_is_rows, all_other_is_rows, all_friend_is_rows, all_i_am_rows)
    separate_rows_per_avatar(negative_data, robot_neg, other_neg, friend_neg, me_neg)
    separate_rows_per_avatar(neutral_data, robot_neut, other_neut, friend_neut, me_neut)
    separate_rows_per_avatar(positive_data, robot_pos, other_pos, friend_pos, me_pos)

    amount_adj_per_avatar[participant_id] = {
        'robot': {
            'all': len(robot_is_rows),
            'pos': len(robot_pos),
            'neut': len(robot_neut),
            'neg': len(robot_neg)
        },
        'other': {
            'all': len(other_is_rows),
            'pos': len(other_pos),
            'neut': len(other_neut),
            'neg': len(other_neg)
        },
        'friend': {
            'all': len(friend_is_rows),
            'pos': len(friend_pos),
            'neut': len(friend_neut),
            'neg': len(friend_neg)
        },
        'me': {
            'all': len(i_am_rows),
            'pos': len(me_pos),
            'neut': len(me_neut),
            'neg': len(me_neg)
        }
    }


average_adj_per_avatar = (pd.DataFrame(data = amount_adj_per_avatar).T.stack().apply(pd.Series).unstack())

stacked_words_per_avatar = pd.DataFrame(data = average_adj_per_avatar.T.stack()).reset_index()
stacked_words_per_avatar.columns = ['valence', 'condition', 'participant', 'number_of_adj_per_avatar']
stacked_words_per_avatar.to_csv('M2 Internship/data_analysis/figures/word_count_per_avatar.csv')#this is the anova format add col names valence condition id number words

word_trends_describe = average_adj_per_avatar.describe()
word_trends_describe.to_csv("M2 Internship/data_analysis/figures/word_count_per_avatar_descrip.csv")

#instead of median do descriptive stats 
#average_adj_per_avatar['median'] = average_adj_per_avatar.median(axis = 1)

robot_yes_ref = pd.DataFrame(data = all_robot_is_rows, columns= ['adjectif', 'encoded_avatar'])
other_yes_ref = pd.DataFrame(data = all_other_is_rows,  columns= ['adjectif', 'encoded_avatar'])
friend_yes_ref = pd.DataFrame(data = all_other_is_rows,  columns= ['adjectif', 'encoded_avatar'])
me_yes_ref = pd.DataFrame(data = all_i_am_rows,  columns= ['adjectif', 'encoded_avatar'])

shape = word_trends_describe.T

fig, ax = plt.subplots(figsize = (5,5))
shape["mean"].unstack().plot(kind="bar", rot=True, ax = ax)
plt.show()

'''
adjectives_per_avatar = {}

#fem and masc words show up separately 
#also don't know if people saw the same words aka how many people saw list A and B 
#maybe could divide by number of ppl that saw that list so if one word is 5 times its 5 over x times it was seen 
def count_adj_appearance(df, avatar):
    adjectives_seen = {}
    for item, row in df.iterrows():
        adjective = row['adjectif']
        if adjective in adjectives_seen:
            #print(f'IN DICT {adjective}')
            adjectives_seen[adjective] += 1
        else:
            #print(f'NOT IN DICT {adjective}')
            adjectives_seen[adjective] = 1
    adjectives_per_avatar[avatar] = adjectives_seen

count_adj_appearance(robot_yes_ref, 'robot')
print(adjectives_per_avatar)


#merge rows with yes per avatar accross participants 
#for each row if adj isn't in the dict add it and add + 1 to the counter even if it is already in the dict 
'''