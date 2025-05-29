import pandas as pd
import numpy as np
import os
import re
from unidecode import unidecode
from datetime import datetime

# === Directories and Log Setup ===
RAW_DIR = 'data/raw/players'
CLEANED_DIR = 'data/cleaned'
LOG_PATH = 'logs/cleaningPlayers_log.txt'

os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

log = []

def log_message(msg):
    print(msg)
    timestamped = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}"
    log.append(timestamped)

# === Column and Text Cleaning Utilities ===
def clean_column_names(df):
    new_cols = []
    for col in df.columns:
        col_cleaned = col.strip().replace(" ", "_")
        col_cleaned = re.sub(r"[^A-Za-z0-9_]", "", col_cleaned)
        new_cols.append(col_cleaned)
    df.columns = new_cols
    return df

def clean_text_column(series):
    return (
        series.astype(str)
        .apply(lambda x: unidecode(x).strip())
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace("\xa0", " ")
    )

# === Main Data Cleaning Function ===
def clean_dataframe(df):
    df.dropna(axis=1, how='all', inplace=True)  # Drop empty columns

    # Clean column names
    df = clean_column_names(df)

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Drop rows that are headers mistakenly repeated in data
    header_row = [str(col).lower().strip() for col in df.columns]
    rows_to_drop = []
    for i, row in df.iterrows():
        values = [str(x).lower().strip() for x in row]
        if values == header_row:
            rows_to_drop.append(i)
    df.drop(index=rows_to_drop, inplace=True)

    # Clean text columns
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        try:
            df[col] = clean_text_column(df[col])
        except Exception:
            continue

    # Specific column cleanings
    if 'Age' in df.columns:
        df['Age'] = df['Age'].astype(str).str.extract(r'^(\d+)')[0]
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

    if 'Comp' in df.columns:
        df['Comp'] = df['Comp'].astype(str).str.replace(r'^[A-Za-z]{2,3}\s+', '', regex=True).str.strip()

    if 'Nation' in df.columns:
        df['Nation'] = df['Nation'].astype(str).str.extract(r'([A-Z]{3})$', expand=False).fillna(df['Nation'])

    # Replace empty or special values with NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.replace(['-', 'N/A', 'n/a', 'NA', 'na', 'null', 'None'], np.nan, inplace=True)

    # Conversion intelligente des colonnes numériques
    excluded_cols = ['Player', 'Nation', 'Pos', 'Squad', 'Comp']
    for col in df.columns:
        if col not in excluded_cols:
            try:
                converted = pd.to_numeric(df[col], errors='coerce')
                valid_numeric_ratio = converted.notna().mean()
                if valid_numeric_ratio > 0.8:
                    df[col] = converted
            except Exception:
                continue

    # Handle missing values
    for col in df.columns:
        if col not in excluded_cols and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna('Unknown')

    return df.reset_index(drop=True)

# === File Processing Loop ===
def process_all_files():
    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith(".xlsx"):
            raw_path = os.path.join(RAW_DIR, filename)
            cleaned_path = os.path.join(CLEANED_DIR, filename.replace(".xlsx", "_clnd.xlsx"))

            log_message(f"\n=== Processing: {filename} ===")

            try:
                df = pd.read_excel(raw_path)
                df.columns = df.columns.str.strip()
                log_message(f"🔎 Loaded with shape: {df.shape}")
            except Exception as e:
                log_message(f"❌ Failed to load {filename}: {str(e)}")
                continue

            df = clean_dataframe(df)

            # Special case: playing_time.xlsx
            if filename.lower() == "playing_time.xlsx":
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                zero_count_per_row = (df[numeric_cols] == 0).sum(axis=1)

                before = len(df)
                df = df[zero_count_per_row <= 10]
                removed = before - len(df)
                log_message(f"🧹 Removed {removed} rows with more than 10 numeric zeros in 'playing_time.xlsx'")

            # Résumé du nettoyage
            log_message(f"📊 Final shape: {df.shape}")
            log_message(f"🧾 Columns: {', '.join(df.columns)}")
            log_message(f"❔ Missing values (total): {df.isna().sum().sum()}")
            log_message("🧬 Data types after cleaning:\n" + df.dtypes.to_string())


            try:
                df.to_excel(cleaned_path, index=False)
                log_message(f"✅ Cleaned file saved to {cleaned_path}")
            except Exception as e:
                log_message(f"❌ Failed to save {filename}: {str(e)}")

    log_message(f"📜 Log saved to {LOG_PATH}")
    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
    except Exception as e:
        log_message(f"❌ Failed to save log: {str(e)}")

# === Entry Point ===
if __name__ == "__main__":
    process_all_files() 