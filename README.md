# DistanceASoiAnalyze
Le path pour trouver les fichiers est au début de chaque script en rouge via VS Code 
  c'est le suivant - M2 Internship/data_analysis/recon_data/ ou M2 Internship/data_analysis/ref_data/ (pour le output script) 
  et M2 Internship/data_analysis/mergeddata/* pour les autres 
    ~A changer en fonction des dossiers 
    ~Il faut aussi changes les paths pour les sauvegardes de dossiers / fichiers controle F "M2 Internship" pour tous les paths 

Ce dossier contient les scripts pour analyzee les donnés de reco (recon_data) et les données de reference (ref_data)
Le scripit output_table est a lancer en premier 
  il clean le data et merge les donnés par participant
  de plus is creer les fichers d'analyze des erreurs de source
Le script source_sre_table donne les analyzes des données hits source 
Le script sre_table donne les analyzes des données hits / fa / miss item memory 
Le script exploratory_measures compte le nombre d'items par avatar par pariticpnat -- Il n'est pas complet
Le script functions_for_sre_analysis n'est pas a run, il contient juste les fonctions pour les reste 
Le script anova_formatting est a run a la fin il se base sure les analyzes de source hit, source erreurs, et item pour un fichier des données qui resume tout 
