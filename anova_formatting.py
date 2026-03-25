import pandas as pd 

'''Ce script prends les données de item (sre classique), 
des hits de source et des erreurs de source
Il les regroupe en un fichier csv pour utiliser en ANOVA
Ce fichier se range dans le dossier 'figures' '''

try:
    source = pd.read_csv("M2 Internship/data_analysis/figures/pivoted_source_hits.csv")
    sre = pd.read_csv("M2 Internship/data_analysis/figures/self_reference_effect.csv")
    errors = pd.read_csv("M2 Internship/data_analysis/figures/pivoted_source_errors.csv")

except FileNotFoundError:
    print("Run les scripts output_table, source_sre_table, sre_table, exploratory_measures et réessaye")

else:
    merged = pd.merge(sre, source, on= ['participant', 'condition'])
    merged = pd.merge(merged, errors, on = ['participant','condition'])
    merged = merged.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0'], axis=1)

    merged = merged.sort_values(by = ['participant', 'condition'])

    merged.to_csv("M2 Internship/data_analysis/figures/anova_data_format.csv")

    #limit to 2 digits?
    #sort condition order differently?