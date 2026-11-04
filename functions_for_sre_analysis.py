from turtle import pos
import pandas as pd
import glob 

'''Ce script contient les fonctions utilisées dans les autres scripts pour l'analyze des données'''

#for file in glob.glob('M2 Internship/data_analysis/mergeddata/*'):
#    data = pd.read_csv(file) #read file 
    
#    participant_id = file[-10:-4]
    #print(participant_id) #show participant id being handled 

def count_items_per_avatar(avatar_name, dataframe, dict):
    avatar_items = []
    for item, row in dataframe.iterrows():
        if row['encoded_avatar'] == avatar_name:
            avatar_items.append(row)
    number_items_avatar = len(avatar_items)
    dict[avatar_name] = number_items_avatar

def valence_separation(df):
    '''separates given dataframe df 
    into three parts, rows with positive valence attributed to positive_data
    rows with negative valence attributed to negative_data
    rows with neutral valence attributed to neutral data
    Call by assigning function to three variables negative_data, positive_data, neutral_data'''
    positive_data = []
    negative_data = []
    neutral_data = []

    for item, row in df.iterrows(): #this will includes hits and misses --> only items which were old but said to be new or old
        #doesn't have false alarms (new items said old because no valence for word?
        # does't have cr because again new words have no valence in data file)
        if row['category'] == 'neutre':
            neutral_data.append(row)
        elif row['category'] == 'positif':
            positive_data.append(row)
        elif row['category'] == 'negatif':
            negative_data.append(row)
    
    negative_data = pd.DataFrame(data = negative_data)
    positive_data = pd.DataFrame(data = positive_data)
    neutral_data = pd.DataFrame(data = neutral_data)

    return negative_data, positive_data, neutral_data

#negative_data, positive_data, neutral_data = valence_separation(data)
#print(negative_data, positive_data, neutral_data)

#do the same but dataframe for hits, fa, miss and cr

def separate_hit_type(df, col_to_compare1, col_to_compare2, correct_response):
    '''separates rows from dataframe df into four lists
    hits, misses, false alarms, correct rejections
    based off of two columns being compared and 
    a correct response which is the content of a cell being used to define what comparison would be a hit etc
    col 2 should be the participant's reponse col 1 should be the objective answer encoded per row'''
    hit = []
    fa = []
    miss = []
    cr = []

    for item, row in df.iterrows():
        if (row[col_to_compare1] == correct_response) & (row[col_to_compare2] == correct_response):
            hit.append(row)
        elif (row[col_to_compare1] == correct_response) & (row[col_to_compare2] != correct_response):
            miss.append(row)
        elif (row[col_to_compare1] != correct_response) & (row[col_to_compare2] == correct_response):
            fa.append(row)
        elif (row[col_to_compare1] != correct_response) & (row[col_to_compare2] != correct_response):
            cr.append(row)
        else:
            print('neither hit,fa, cr or miss ')
            print(row)
    return hit, fa, miss, cr

    #hit, fa, miss, cr = separate_hit_type(data, 'item', 'réponse', 'OLD')
    #number_fa = len(fa)
    #number_cr = len(cr)
    #print (number_fa, number_cr)
    #hit = pd.DataFrame(hit)
    #fa = pd.DataFrame(fa)
    #miss = pd.DataFrame(miss)
    #cr = pd.DataFrame(cr)
    #print(hit, fa, miss, cr)


#for each response type have the number of that response type
#than split per avatar and count that response type per avatar 
#make a division for ratio 
#dataframe and plot 

#for sources the same happens but need to run the function per avatar so have hits and fa per avatar so adapt variable names accordingly