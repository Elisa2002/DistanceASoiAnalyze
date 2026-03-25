#nb words chosen per avatar --> response yes to encoded adj per participant per avatar
# between participants what adjectives were chosem --> count appearances of each adjective for each avatar frequency of words
#correlations with other measures such as embodiement etc?

import pandas as pd 
import matplotlib.pyplot as plt
import glob
all_robot_is_rows = []
all_other_is_rows = []
all_i_am_rows = []
all_friend_is_rows = []
amount_adj_per_avatar = {}

for file in glob.glob("M2 Internship/data_analysis/mergeddata/*"):
    data = pd.read_csv(file)

    participant_id = file[-10:-4]

    robot_is_rows = []
    other_is_rows = []
    i_am_rows = []
    friend_is_rows = []

    for item, row in data.iterrows():
        if row['reference?'] == True:
            if row['encoded_avatar'] == 'robot':
                robot_is_rows.append(row)
                all_robot_is_rows.append(row)
            elif row['encoded_avatar'] == 'vous':
                i_am_rows.append(row)
                all_i_am_rows.append(row)
            elif row['encoded_avatar'] == 'ami':
                friend_is_rows.append(row)
                all_friend_is_rows.append(row)
            elif row['encoded_avatar'] == 'autrui':
                other_is_rows.append(row)
                all_other_is_rows.append(row)

    amount_adj_per_avatar[participant_id] = {
        'robot': len(robot_is_rows),
        'other': len(other_is_rows),
        'friend': len(friend_is_rows),
        'me': len(i_am_rows)

    }

average_adj_per_avatar = pd.DataFrame(data = amount_adj_per_avatar)
average_adj_per_avatar['median'] = average_adj_per_avatar.median(axis = 1)
print(average_adj_per_avatar)

robot_yes_ref = pd.DataFrame(data = all_robot_is_rows, columns= ['adjectif', 'encoded_avatar'])
other_yes_ref = pd.DataFrame(data = all_other_is_rows,  columns= ['adjectif', 'encoded_avatar'])
friend_yes_ref = pd.DataFrame(data = all_other_is_rows,  columns= ['adjectif', 'encoded_avatar'])
me_yes_ref = pd.DataFrame(data = all_i_am_rows,  columns= ['adjectif', 'encoded_avatar'])

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
