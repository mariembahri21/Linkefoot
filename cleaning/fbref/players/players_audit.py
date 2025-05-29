import pandas as pd
import re
import unicodedata
import os

RAW_DIR = 'data/raw/players'
LOG_PATH = 'logs/pre_cleaning_report.txt'
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


def has_diacritics(s):
    return any(c != unicodedata.normalize('NFD', c)[0] for c in s)

def has_mixed_characters(s):
    return bool(re.search(r"[A-Za-z]", s)) and bool(re.search(r"\d", s))

def has_extra_spaces(s):
    return s != s.strip() or "  " in s

def has_suspicious_symbols(s):
    return bool(re.search(r"[^\w\s.,!?;:@#%&()\'\"/\[\]{}<>+=*-]", s))

def analyze_text_column(series):
    diacritics, mixed_chars, extra_spaces, weird_symbols = 0, 0, 0, 0
    for val in series.dropna().astype(str):
        if has_diacritics(val): diacritics += 1
        if has_mixed_characters(val): mixed_chars += 1
        if has_extra_spaces(val): extra_spaces += 1
        if has_suspicious_symbols(val): weird_symbols += 1
    return diacritics, mixed_chars, extra_spaces, weird_symbols

def match_headers(df):
    count = 0
    for _, row in df.iterrows():
        matches = sum([str(row[col]).strip().lower() == col.lower() for col in df.columns])
        if matches / len(df.columns) >= 0.2:
            count += 1
    return count

def analyze_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return f"\n\n### ❌ Could not read file: {file_path}\nError: {e}\n{'='*80}\n"

    report = [f"{'='*80}",
              f"📁 File Name: {os.path.basename(file_path)}",
              f"{'-'*80}",
              f"✅ Shape: {df.shape}"]
    
    # Suspicious column names
    col_issues = []
    for col in df.columns:
        if " " in col or has_mixed_characters(col):
            col_issues.append(col)
    report.append("\n⚠️ Issues in column names:")
    if col_issues:
        for col in col_issues:
            reason = []
            if " " in col: reason.append("contains spaces")
            if has_mixed_characters(col): reason.append("mixed characters")
            report.append(f"- `{col}`: {' and '.join(reason)}")
    else:
        report.append("- None")

    # Header-like rows
    header_like_rows = match_headers(df)
    report.append(f"\n🧐 Rows matching headers: {header_like_rows}")
    
    # Duplicates
    dup_count = df.duplicated().sum()
    report.append(f"🔁 Duplicated rows: {dup_count}")
    
    # Missing values
    report.append("\n❓ Missing values (%):")
    missing = df.isnull().sum()
    for col in df.columns:
        pct = (missing[col] / len(df)) * 100
        report.append(f"- `{col}`: {missing[col]} missing ({pct:.1f}%)")
    
    # Data types
    report.append("\n📦 Column Data Types:")
    report.append(str(df.dtypes))
    
    # Text issues
    diacritic_rows, mixed_char_rows, extra_space_rows, weird_sym_rows = 0, 0, 0, 0
    for col in df.select_dtypes(include=['object']).columns:
        d, m, e, w = analyze_text_column(df[col])
        diacritic_rows += d
        mixed_char_rows += m
        extra_space_rows += e
        weird_sym_rows += w
    report.append("\n🧪 Text issues summary:")
    report.append(f"- Rows with diacritics: **{diacritic_rows}**")
    report.append(f"- Rows with mixed characters: **{mixed_char_rows}**")
    report.append(f"- Rows with extra spaces: **{extra_space_rows}**")
    report.append(f"- Rows with suspicious characters: **{weird_sym_rows}**")
    
    return "\n".join(report)

def analyze_all_excel_files(folder_path):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for filename in os.listdir(folder_path):
            if filename.endswith(".xlsx") or filename.endswith(".xls"):
                file_path = os.path.join(folder_path, filename)
                report = analyze_excel_file(file_path)
                f.write(report + "\n\n")
    print(f"✅ Full report saved to: {LOG_PATH}")


analyze_all_excel_files(RAW_DIR)
