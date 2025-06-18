import pandas as pd
from fuzzywuzzy import fuzz, process

# === 1. Chargement et nettoyage des noms ===
sofifa = pd.read_excel("C:/Users/bahri/Desktop/Football_performance_analysis/data/cleaned/sofifa/sofifa_players_cleaned.xlsx")
sofascore = pd.read_excel("data/cleaned/sofascore/sofascore_preprocessed_teams_players.xlsx")

def clean_name(name):
    if isinstance(name, str):
        name = name.lower().strip().replace(" ", "_")
        return name
    return ""

sofifa['player_name_clean'] = sofifa['name'].apply(clean_name)
sofascore['player_name_clean'] = sofascore['name'].apply(clean_name)

# === 2. Appariement automatique ===
matched_rows = []
semi_matched_rows = []

threshold_auto = 90
threshold_semi = 75

for name in sofascore['player_name_clean']:
    result = process.extractOne(name, sofifa['player_name_clean'], scorer=fuzz.token_sort_ratio)
    
    if result:
        match, score, _ = result  # CORRECTION ICI ✅
        if score >= threshold_auto:
            matched_rows.append({
                'sofascore_name': name,
                'sofifa_name': match,
                'score': score
            })
        elif threshold_semi <= score < threshold_auto:
            semi_matched_rows.append({
                'sofascore_name': name,
                'sofifa_name': match,
                'score': score
            })

# === 3. Création des DataFrames de correspondance ===
df_matched = pd.DataFrame(matched_rows)
df_semi_matched = pd.DataFrame(semi_matched_rows)

# === 4. Fusion automatique Sofascore–Sofifa ===
sofascore_matched = sofascore.merge(df_matched, left_on='player_name_clean', right_on='sofascore_name')
final_merge = sofascore_matched.merge(sofifa, left_on='sofifa_name', right_on='player_name_clean', suffixes=('_sofa', '_sofi'))

# === 5. Sauvegarde des fichiers pour vérification manuelle ===
df_semi_matched.to_excel("semi_matched_players.xlsx", index=False)
final_merge.to_excel("merged_players_auto.xlsx", index=False)
