import pandas as pd

# Load your data
df = pd.read_excel("data/raw/sofifa/sofifa_teams.xlsx")  # Adjust delimiter if needed

# Step 1: Split the 'Name' column into 'Team' and 'League'
df[['Team', 'League']] = df['Name'].str.split('\n', expand=True)

# Step 2: Strip spaces from both new columns
df['Team'] = df['Team'].str.strip()
df['League'] = df['League'].str.strip()

# Step 3: Drop the original 'Name' column (optional)
df.drop(columns=['Name'], inplace=True)

# Save or display
df.to_excel("data/cleaned/sofifa/sofifa_teams_clnd.xlsx", index=False)
print(df.head())
