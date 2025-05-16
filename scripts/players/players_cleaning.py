import pandas as pd
import numpy as np
import os
from unidecode import unidecode
from datetime import datetime

RAW_DIR = 'data/raw/players'
CLEANED_DIR = 'data/cleaned'
LOG_PATH = 'logs/cleaningPlayers_log.txt'

os.makedirs(CLEANED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

log = []

def log_message(msg):
    print(msg)
    log.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def clean_dataframe(df):
    if 'Age' in df.columns:
        df['Age'] = df['Age'].astype(str).str.extract(r'^(\d+)')[0]
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

    if 'Comp' in df.columns:
        df['Comp'] = df['Comp'].astype(str).str.replace(r'^[A-Za-z]{2,3}\s+', '', regex=True).str.strip()

    if 'Nation' in df.columns:
        df['Nation'] = df['Nation'].astype(str).str.extract(r'([A-Z]{3})$')[0]

    df = df.drop_duplicates()

    header_row = [str(col).lower().strip() for col in df.columns]
    df = df[~df.apply(lambda row: [str(x).lower().strip() for x in row] == header_row, axis=1)]

    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].apply(
            lambda x: unidecode(str(x)).strip() if pd.notnull(x) else x
        )
        
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True)

    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.replace(['-', 'N/A', 'n/a', 'NA', 'na', 'null', 'None'], np.nan, inplace=True)

    excluded_cols = ['Player', 'Nation', 'Pos', 'Squad', 'Comp']
    for col in df.columns:
        if col not in excluded_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in df.columns:
        if col not in excluded_cols and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)


        else:
            df[col] = df[col].fillna('Unknown')

    return df.reset_index(drop=True)


def process_all_files():
    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".xlsx"):
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
            if filename.lower() == "playing_time.xlsx":
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
                zero_count_per_row = (df[numeric_cols] == 0).sum(axis=1)

                before = len(df)
                df = df[zero_count_per_row <= 10]
                removed = before - len(df)
                log_message(f"🧹 Removed {removed} rows with more than 10 numeric zeros in 'playing_time.xlsx'")

            
            try:
                df.to_excel(cleaned_path, index=False)
                log_message(f"✅ Cleaned file saved to {cleaned_path}")
            except Exception as e:
                log_message(f"❌ Failed to save {filename}: {str(e)}")

    
    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
        log_message(f"📜 Log saved to {LOG_PATH}")
    except Exception as e:
        log_message(f"❌ Failed to save log: {str(e)}")


if __name__ == "__main__":
    process_all_files()
