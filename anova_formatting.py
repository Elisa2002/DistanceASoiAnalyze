import pandas as pd 

'''Ce script prends les données de item (sre classique), 
des hits de source et des erreurs de source
Il les regroupe en un fichier csv pour utiliser en ANOVA
Ce fichier se range dans le dossier 'figures' '''

#open all data files for source hits, item hits misses and false alarms, errors to avatars, number of adjectives per avatar and embodiment scores per avatar

try: # use try cuz if haven't run other scripts won't have the files
    source = pd.read_csv("M2 Internship/data_analysis/figures/pivoted_source_hits.csv")
    sre = pd.read_csv("M2 Internship/data_analysis/figures/self_reference_effect.csv")
    errors = pd.read_csv("M2 Internship/data_analysis/figures/pivoted_source_errors.csv")
    number_adj = pd.read_csv("M2 Internship/data_analysis/figures/word_count_per_avatar.csv")
    embo = pd.read_csv("M2 Internship/data_analysis/figures/embodiment_data.csv")

except FileNotFoundError: #print if one of the files doesn't exist
    print("Run les scripts output_table, source_sre_table, sre_table, exploratory_measures et réessaye")

#if all files found
else: #merging all files together
    merged = pd.merge(sre, source, on= ['participant', 'condition'])
    merged = pd.merge(merged, errors, on = ['participant','condition'])
    merged = merged.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0'], axis=1)

    merged = merged.sort_values(by = ['participant', 'condition'])

    #limit to 2 digits?
    #sort condition order differently?

#the files were in wide format with one line per pp but want column per variable 
for col in merged:
    if col.split()[-1] != "pos" and col.split()[-1] != "neg" and col.split()[-1] != 'neut' and col != 'condition' and col != 'participant':
        merged.rename(columns={col: col + " all"}, inplace= True)

#melt to get a valence, condition and participant column and each measure as a numseparate col
melted = merged.melt(id_vars= ['participant', 'condition'], var_name= 'variable', value_name= 'value')
melted[['measure', 'valence']] = melted["variable"].str.rsplit(" ", n=1, expand=True)
melted = melted.drop(columns=["variable"])
melted = melted.pivot_table(values= 'value', index= ['participant', 'condition', 'valence'], columns= 'measure')
melted = melted.reset_index()[['participant', 'condition', 'valence', 'corrected hits', 'hits (uncorrected)', 'false alarms', 'misses', 'source hits', 'o source hits','source errors to avatars']]

#adding the adj col which was already right format 
melted = pd.merge(melted, number_adj, on =['participant','condition', 'valence'])
melted = pd.merge(melted, embo, on = ['participant', 'condition'])
melted.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis = 1, inplace= True)
melted.to_csv("M2 Internship/data_analysis/figures/anova_data_format_2.csv") #saving file

#long format to use .describe on 
merged_long = merged.pivot_table(index='participant', columns='condition')
describe = merged_long.describe().round(2)

describe.to_csv("M2 Internship/data_analysis/figures/all_descrptives.csv")#saving the descriptives (but better see in R)