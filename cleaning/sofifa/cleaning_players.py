import pandas as pd
import re

# Load the dataset
df = pd.read_excel("data/raw/sofifa/sofifa_players.xlsx")  # Replace with your actual file path

# 1. Split Name and Positions
df[['Name', 'Positions']] = df['Name'].str.split('\n', expand=True)

# 2. Split Team & Contract
df[['Team', 'Contract Dates']] = df['Team & Contract'].str.split('\n', expand=True)

# 3. Clean Height column: remove everything after the slash
df['Height'] = df['Height'].str.split('/').str[0].str.strip()

# 4. Clean Weight column: remove everything after the slash
df['Weight'] = df['Weight'].str.split('/').str[0].str.strip()

# 5. Clean Body type: remove content inside parentheses
df['Body type'] = df['Body type'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', x).strip())

# Optional: Drop the original 'Team & Contract' column if no longer needed
df.drop(columns=['Team & Contract'], inplace=True)

# Save cleaned version (optional)
df.to_excel("data/cleaned/sofifa/sofifa_players_clnd.xlsx", index=False)

print("Cleaning completed. Sample:")
print(df[['Name', 'Positions', 'Team', 'Contract Dates', 'Height', 'Weight', 'Body type']].head())
