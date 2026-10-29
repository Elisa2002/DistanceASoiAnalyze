import glob
import pandas as pd
from functions_for_sre_analysis import count_items_per_avatar

AVATARS = ['vous', 'ami', 'autrui', 'robot']

# store participant-level data
participants_data = []

for file in glob.glob("M2 Internship/data_analysis/mergeddata/*"):

    participant_id = file[-10:-4]
    print(participant_id)

    all_data = pd.read_csv(file)

    participant_results = {
        'participant': participant_id
    }

    # -------------------------
    # OLD correctly recognized
    # -------------------------
    all_hits = all_data[
        (all_data['item'] == 'OLD') &
        (all_data['réponse'] == 'OLD')
    ]
    participant_results[f'all_hits'] = (len(all_hits))

    # total hits per avatar
    for avatar in AVATARS:
        participant_results[f'total_hits_{avatar}'] = (
            all_hits['encoded_avatar'] == avatar
        ).sum()

    # -------------------------
    # source hits
    # -------------------------
    all_source_hits = all_hits[
        all_hits['encoded_avatar'] == all_hits['source (avatar)']
    ]

    participant_results[f'all_source_hits'] = (len(all_source_hits))

    for avatar in AVATARS:
        participant_results[f'source_hits_{avatar}'] = (
            all_source_hits['encoded_avatar'] == avatar
        ).sum()

    # -------------------------
    # source errors
    # -------------------------
    all_source_errors = all_hits[
        all_hits['encoded_avatar'] != all_hits['source (avatar)']
    ]

    participant_results[f'all_source_errors'] = (len(all_source_errors))

    for avatar in AVATARS:
        participant_results[f'source_errors_to_{avatar}'] = (
            all_source_errors['source (avatar)'] == avatar
        ).sum()

    # save this participant
    participants_data.append(participant_results)

# -----------------------------------
# convert to dataframe for averaging
# -----------------------------------
results_df = pd.DataFrame(participants_data)

print(results_df)

# Example averages
mean_scores = results_df.mean(numeric_only=True)

print(mean_scores)

