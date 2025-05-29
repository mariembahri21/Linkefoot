import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import numpy as np

# Enhanced UTF-8 logging
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Create log directory if it doesn't exist
LOG_FILE = 'logs/test.log'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
data_dir = 'data/raw/players'

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def check_dataframe(df):
    flagged_issues = []

    def has_cols(cols):
        return all(col in df.columns for col in cols)

    for index, row in df.iterrows():
        try:
            pos = row['Pos'] if 'Pos' in df.columns else None

            if pos == 'GK':
                if has_cols(['Gls']) and row['Gls'] > 1:
                    msg = f"Row {index}: GK has more than 1 goal."
                    flagged_issues.append(msg)
                    logging.warning(msg)

                if has_cols(['Ast']) and row['Ast'] > 2:
                    msg = f"Row {index}: GK has more than 2 assists."
                    flagged_issues.append(msg)
                    logging.warning(msg)

            elif pos == 'DF':
                if has_cols(['xG']) and row['xG'] > 1:
                    msg = f"Row {index}: DF has xG > 1."
                    flagged_issues.append(msg)
                    logging.warning(msg)
                if has_cols(['Shots']) and row['Shots'] > 5:
                    msg = f"Row {index}: DF has Shots > 5."
                    flagged_issues.append(msg)
                    logging.warning(msg)

            elif pos == 'FW':
                if has_cols(['xG', 'Min']) and row['xG'] == 0 and row['Min'] > 200:
                    msg = f"Row {index}: FW has 0 xG despite {row['Min']} minutes."
                    flagged_issues.append(msg)
                    logging.warning(msg)
                if has_cols(['Shots', 'Min']) and row['Shots'] == 0 and row['Min'] > 200:
                    msg = f"Row {index}: FW has 0 Shots despite {row['Min']} minutes."
                    flagged_issues.append(msg)
                    logging.warning(msg)
                if has_cols(['Gls', 'Min']) and row['Gls'] == 0 and row['Min'] > 200:
                    msg = f"Row {index}: FW has 0 Goals despite {row['Min']} minutes."
                    flagged_issues.append(msg)
                    logging.warning(msg)
        except Exception as e:
            logging.error(f"Position-specific check failed at row {index}: {e}")

    for col in ['Per 90 Minutes xG', 'Shots/90', 'Passes/90', 'Tackles/90']:
        try:
            if col in df.columns:
                outliers = df[(df[col] < 0) | (df[col] > 100)]
                for idx in outliers.index:
                    msg = f"Row {idx}: {col} is out of range (0-100)."
                    flagged_issues.append(msg)
                    logging.warning(msg)
        except Exception as e:
            logging.error(f"Per-90 check failed for column {col}: {e}")

    try:
        if has_cols(['Min']):
            for index, row in df.iterrows():
                if row['Min'] > 9900:
                    msg = f"Row {index}: Minutes > 9900."
                    flagged_issues.append(msg)
                    logging.warning(msg)
                if has_cols(['MP']):
                    if row['Min'] == 0 and row['MP'] > 0:
                        msg = f"Row {index}: Min = 0 but MP > 0."
                        flagged_issues.append(msg)
                        logging.warning(msg)
                    if row['Min'] > 0 and row['MP'] == 0:
                        msg = f"Row {index}: Min > 0 but MP = 0."
                        flagged_issues.append(msg)
                        logging.warning(msg)
    except Exception as e:
        logging.error(f"Minutes logic failed: {e}")

    for col in ['Pass%', 'Save%', 'Shot%', 'Tkl%', 'Cross%']:
        try:
            if col in df.columns:
                invalid_values = df[(df[col] < 0) | (df[col] > 100)]
                for index in invalid_values.index:
                    msg = f"Row {index}: {col} is out of range."
                    flagged_issues.append(msg)
                    logging.warning(msg)
        except Exception as e:
            logging.error(f"Percentage field {col} check failed: {e}")

    try:
        if has_cols(['PK', 'PKatt']):
            for index, row in df.iterrows():
                if row['PK'] > row['PKatt']:
                    msg = f"Row {index}: PK > PKatt."
                    flagged_issues.append(msg)
                    logging.warning(msg)
    except Exception as e:
        logging.error(f"PK/PKatt logic failed: {e}")

    try:
        if has_cols(['CrdY']):
            for index, row in df.iterrows():
                if row['CrdY'] > 30:
                    msg = f"Row {index}: Yellow cards > 30."
                    flagged_issues.append(msg)
                    logging.warning(msg)
                if has_cols(['MP']) and row['CrdY'] > row['MP']:
                    msg = f"Row {index}: CrdY > MP."
                    flagged_issues.append(msg)
                    logging.warning(msg)
    except Exception as e:
        logging.error(f"CrdY logic failed: {e}")

    try:
        if has_cols(['CrdR']):
            for index, row in df.iterrows():
                if row['CrdR'] > 5:
                    msg = f"Row {index}: Red cards > 5."
                    flagged_issues.append(msg)
                    logging.warning(msg)
                if has_cols(['MP']) and row['CrdR'] > row['MP']:
                    msg = f"Row {index}: CrdR > MP."
                    flagged_issues.append(msg)
                    logging.warning(msg)
    except Exception as e:
        logging.error(f"CrdR logic failed: {e}")

    try:
        if has_cols(['G+A', 'Gls', 'Ast']):
            for index, row in df.iterrows():
                if row['G+A'] != row['Gls'] + row['Ast']:
                    msg = f"Row {index}: G+A mismatch."
                    flagged_issues.append(msg)
                    logging.warning(msg)
    except Exception as e:
        logging.error(f"G+A mismatch check failed: {e}")

    try:
        if has_cols(['xG+xA', 'xG', 'xA']):
            for index, row in df.iterrows():
                if row['xG+xA'] != row['xG'] + row['xA']:
                    msg = f"Row {index}: xG+xA mismatch."
                    flagged_issues.append(msg)
                    logging.warning(msg)
    except Exception as e:
        logging.error(f"xG+xA mismatch check failed: {e}")

    for col in ['Shots', 'Passes', 'xG', 'Touches']:
        try:
            if col in df.columns and df[col].std() > 0:
                z_score = (df[col] - df[col].mean()) / df[col].std()
                outliers = df[z_score.abs() > 3]
                for index in outliers.index:
                    msg = f"Row {index}: {col} z-score > 3."
                    flagged_issues.append(msg)
                    logging.warning(msg)
        except Exception as e:
            logging.error(f"Z-score check failed for {col}: {e}")

    try:
        if 'Comp' in df.columns:
            inconsistent_values = df['Comp'].value_counts().loc[lambda x: x < 3]
            for value in inconsistent_values.index:
                msg = f"Rare competition value in Comp: {value}"
                flagged_issues.append(msg)
                logging.warning(msg)
    except Exception as e:
        logging.error(f"Comp value counts check failed: {e}")

    return flagged_issues

def analyze_file(filepath):
    filename = os.path.basename(filepath)
    try:
        df = pd.read_excel(filepath)
        logging.info(f"\n📊 Starting analysis: {filename}")
        issues = check_dataframe(df)
        logging.info(f"✅ Completed analysis: {filename} — {len(issues)} issues flagged.")
    except Exception as e:
        logging.error(f"❌ Error processing {filename}: {e}")

def analyze_all_files():
    for filename in os.listdir(data_dir):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            analyze_file(os.path.join(data_dir, filename))

if __name__ == "__main__":
    analyze_all_files()