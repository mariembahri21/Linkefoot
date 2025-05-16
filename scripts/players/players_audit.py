import pandas as pd
import os
import re
import unicodedata
import numpy as np
import logging
from datetime import datetime

RAW_DIR = 'data/raw/players'
LOG_PATH = 'logs/full_pre_cleaning_report.txt'
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_PATH,
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def contains_diacritics(s):
    return any(unicodedata.category(c).startswith('M') for c in unicodedata.normalize('NFD', str(s)))

def has_mixed_characters(s):
    s = str(s)
    return bool(re.search(r'(?=.*[A-Za-z])(?=.*\d)|(?=.*[^\w\s])', s))

def flag_domain_outliers(df):
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
        if 'Player' in df.columns:
            duplicate_names = df[df.duplicated(subset=['Player'], keep=False)]
            for index, row in duplicate_names.iterrows():
                msg = f"Row {index}: Duplicate name {row['Player']}"
                flagged_issues.append(msg)
                logging.warning(msg)
    except Exception as e:
        logging.error(f"Duplicate check failed: {e}")

    try:
        numeric_cols = df.select_dtypes(include=np.number)
        if 'Player' in df.columns:
            zero_rows = df[(numeric_cols.sum(axis=1) == 0) & (df['Player'] != '')]
            for index in zero_rows.index:
                msg = f"Row {index}: All numeric values zero."
                flagged_issues.append(msg)
                logging.warning(msg)
    except Exception as e:
        logging.error(f"Zero numeric row check failed: {e}")

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

def check_issues(df, filename):
    logging.info(f"=== Analyzing: {filename} ===")
    logging.info(f"Shape: {df.shape}")

    original_headers = list(df.columns)
    for col in original_headers:
        if col != col.strip():
            logging.warning(f"Header '{col}' has leading/trailing spaces")

    for col in df.columns:
        issues = []
        if ' ' in col:
            issues.append("contains spaces")
        if contains_diacritics(col):
            issues.append("diacritics")
        if has_mixed_characters(col):
            issues.append("mixed characters")
        if issues:
            logging.warning(f"Column '{col}' has issues: {', '.join(issues)}")

    header_row = [str(c).strip().lower() for c in df.columns]
    similar_rows = df.apply(lambda row: sum([str(cell).strip().lower() == h for cell, h in zip(row, header_row)]), axis=1)
    partial_header_rows = (similar_rows >= int(0.1 * len(header_row))) & (similar_rows < len(header_row))

    if partial_header_rows.sum():
        logging.warning(f"Rows matching headers partially: {partial_header_rows.sum()}")

    duplicate_rows = df[df.duplicated()]
    logging.info(f"Duplicated rows: {len(duplicate_rows)}")

    logging.info("Missing values (%):")
    for col in df.columns:
        count = df[col].isnull().sum()
        perc = (count / len(df)) * 100
        if count > 0:
            logging.warning(f" - {col}: {count} missing ({perc:.1f}%)")

    logging.info("Column Data Types:")
    for col, dtype in df.dtypes.items():
        logging.info(f" - {col}: {dtype}")

    diacritics_count = 0
    mixed_char_count = 0
    extra_spaces_count = 0
    suspicious_char_count = 0

    for col in df.select_dtypes(include=['object']):
        for val in df[col].dropna():
            val_str = str(val)
            if contains_diacritics(val_str):
                diacritics_count += 1
            if has_mixed_characters(val_str):
                mixed_char_count += 1
            if re.search(r'\s{2,}', val_str):
                extra_spaces_count += 1
            if re.search(r'[^\w\s\.\-\,\(\)\/:]', val_str):
                suspicious_char_count += 1

    logging.info("Text issues summary:")
    logging.info(f" - Rows with diacritics: {diacritics_count}")
    logging.info(f" - Rows with mixed characters: {mixed_char_count}")
    logging.info(f" - Rows with extra spaces: {extra_spaces_count}")
    logging.info(f" - Rows with suspicious characters: {suspicious_char_count}")

    flagged = flag_domain_outliers(df)
    if flagged:
        logging.warning("Domain-specific flagged issues:")
        for issue in flagged:
            logging.warning(f" - {issue}")

def analyze_all_files():
    for filename in os.listdir(RAW_DIR):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(RAW_DIR, filename)
            try:
                df = pd.read_excel(filepath)
                check_issues(df, filename)
            except Exception as e:
                logging.error(f"Failed to read {filename}: {str(e)}")

if __name__ == '__main__':
    analyze_all_files()
    logging.info(f"\nAudit completed. Log saved to {LOG_PATH}")