import pandas as pd

embodiment = pd.read_csv("M2 Internship/data_analysis/embodiment_data.csv")


embodiment["merged_em_score"] = embodiment['impression_etre'] + embodiment['corps_virtuel']
embodiment['participant'] = embodiment['Participant Public ID']
embodiment = embodiment.drop(['Participant Public ID'], axis= 1)
embodiment = embodiment[['participant', 
    'condition', 
    'corps_virtuel', 
    'impression_etre', 
    'merged_em_score', 
    'difference_observee', 
    'pourquoi_difference', 
    'personnage_expressif',
    'type_expression',
    'proximite_sociale',
    'relation_image',
    'echelle_sociale'
    ]]
embodiment = embodiment.set_index(['participant', 'condition'])
embodiment = embodiment.drop(index=['DAS009b', 'DAS023'], level= 0)
embodiment.rename(index={'DAS010b': 'das010', 'DAS012(phase2)': 'das012', 'DAS013(phase2)': 'das013', 'DAS011(phase2)': 'das011'}, inplace=True)
embodiment = embodiment.drop(index='self', level=1).reset_index()

embodiment['participant'] = embodiment['participant'].str.lower()

embodiment.to_csv("M2 Internship/data_analysis/figures/embodiment_data.csv")
