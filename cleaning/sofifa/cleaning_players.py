import pandas as pd
import re

# 1. Charger le fichier
df = pd.read_excel("data/cleaned/sofifa/sofifa_players_clnd.xlsx")

# 2. Nettoyer Height et Weight
if 'Height' in df.columns:
    df['Height'] = (
        df['Height'].astype(str)
        .str.extract(r'(\d+)')
    )
    df['Height'] = pd.to_numeric(df['Height'], errors='coerce')

if 'Weight' in df.columns:
    df['Weight'] = (
        df['Weight'].astype(str)
        .str.extract(r'(\d+)')
    )
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')

# 3. Nettoyage des colonnes FIFA + suppression des "+1" et "-2"
fifa_cols = [
    'Overall_rating', 'Potential', 'Crossing', 'Finishing', 'Heading_accuracy',
    'Short_passing', 'Dribbling', 'Curve', 'FK_accuracy', 'Long_passing',
    'Ball_control', 'Acceleration', 'Sprint_speed', 'Agility', 'Reactions',
    'Balance', 'Shot_power', 'Jumping', 'Stamina', 'Strength', 'Long_shots',
    'Aggression', 'Penalties', 'Defensive_awareness', 'Standing_tackle', 'Sliding_tackle'
]

df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

for col in fifa_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'[+-].*', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 4. Nettoyage 'Joined'
if 'Joined' in df.columns:
    df['Joined'] = pd.to_datetime(df['Joined'], errors='coerce').dt.date

# 5. Nettoyage et traitement de 'Contract Dates'
if 'Contract_Dates' in df.columns:
    df['Contract_Dates'] = df['Contract_Dates'].astype(str)

    # Si la valeur contient "free" ou un format du type "Jun 30, 2025 On loan", remplacer par "2025 ~ 2025"
    df['Contract_Dates'] = df['Contract_Dates'].apply(
        lambda x: "2025 ~ 2025" if re.search(r'(?i)free|[A-Za-z]{3,9} \d{1,2}, \d{4}', x) else x
    )

    # Split en deux colonnes
    df[['Contract_Start', 'Contract_End']] = df['Contract_Dates'].str.split('~', expand=True)
    df['Contract_Start'] = pd.to_numeric(df['Contract_Start'].str.strip(), errors='coerce')
    df['Contract_End'] = pd.to_numeric(df['Contract_End'].str.strip(), errors='coerce')
# 6. Nettoyage Value et Wage
def parse_money(value):
    if pd.isna(value): return None
    value = str(value).replace('€', '').replace(',', '')
    value = value.replace('K', '*1e3').replace('M', '*1e6').replace('B', '*1e9')
    try:
        return eval(value)
    except:
        return None

for col in ['Value', 'Wage']:
    if col in df.columns:
        df[col] = df[col].apply(parse_money)

# 7. Sauvegarde
df.to_excel("data/cleaned/sofifa/sofifa_players_clnd_updated.xlsx", index=False)

print("✅ Nettoyage complet terminé avec succès.")
