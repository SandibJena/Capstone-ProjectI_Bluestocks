import os
import glob

import pandas as pd


def find_csv_files():
    """
    Locate all CSV datasets required for the project.

    Search order:
    1. data/raw
    2. Downloads
    3. Workspace root

    Returns:
        list[str]: Paths to discovered CSV files.
    """
    paths = []
    # prefer project data/raw
    paths.extend(glob.glob(os.path.join("data", "raw", "*.csv")))
    # fallback to common Downloads folder (Windows)
    downloads = os.path.join("C:\\Users", os.getenv("USERNAME", ""), "Downloads")
    if os.path.isdir(downloads):
        paths.extend(glob.glob(os.path.join(downloads, "*.csv")))
    # also allow any CSV at workspace root
    paths.extend(glob.glob("*.csv"))
    # deduplicate and return
    seen = set()
    out = []
    for p in paths:
        bn = os.path.basename(p)
        if bn not in seen:
            out.append(p)
            seen.add(bn)
    return out


def basic_anomalies(df: pd.DataFrame):
    issues = []
    na_counts = df.isna().sum()
    cols_with_na = na_counts[na_counts > 0]
    if not cols_with_na.empty:
        issues.append(f"Columns with NAs: {cols_with_na.to_dict()}")
    dup_rows = df.duplicated().sum()
    if dup_rows:
        issues.append(f"Duplicate rows: {dup_rows}")
    # columns with mixed types (object but numeric-like)
    for col in df.columns:
        if df[col].dtype == 'object':
            sample = df[col].dropna().head(50)
            if not sample.empty:
                num_like = sample.str.replace(',', '').str.replace(' ', '').str.replace('%','').str.isnumeric().all()
                if num_like:
                    issues.append(f"Column {col} is object but looks numeric-like")
    return issues


def load_and_report(files):
    os.makedirs(os.path.join("data", "processed"), exist_ok=True)
    summary_lines = []
    loaded = {}
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            try:
                df = pd.read_csv(f, encoding='latin1')
            except Exception as e:
                summary_lines.append(f"FAILED load {f}: {e}")
                continue
        name = os.path.basename(f)
        loaded[name] = df
        print(f"--- {name} ---")
        print("shape:", df.shape)
        print(df.dtypes)
        print(df.head())
        issues = basic_anomalies(df)
        if issues:
            print("Anomalies:")
            for it in issues:
                print(" -", it)
        summary_lines.append(f"{name}: shape={df.shape}, anomalies={issues}")
    # save summary
    with open(os.path.join("data", "processed", "load_summary.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(summary_lines))
    return loaded


def validate_amfi_codes(loaded):
    # require fund_master and nav_history
    fm = None
    nh = None
    for k in loaded:
        if k.lower().startswith('01_') or 'fund_master' in k.lower():
            fm = loaded[k]
        if k.lower().startswith('02_') or 'nav_history' in k.lower():
            nh = loaded[k]
    report = []
    if fm is None:
        report.append('fund_master not found; cannot validate AMFI codes')
    if nh is None:
        report.append('nav_history not found; cannot validate AMFI codes')
    if fm is not None and nh is not None:
        fm_codes = set(fm['amfi_code'].astype(str).unique())
        nh_codes = set(nh['amfi_code'].astype(str).unique())
        missing_in_nav = sorted(list(fm_codes - nh_codes))
        if missing_in_nav:
            report.append(f"{len(missing_in_nav)} AMFI codes in fund_master missing from nav_history sample. Example: {missing_in_nav[:5]}")
        else:
            report.append("All fund_master AMFI codes present in nav_history sample.")
    # write report
    with open(os.path.join("data", "processed", "data_quality_summary.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(report))
    print('\n'.join(report))
    return report


def main():
    files = find_csv_files()
    if not files:
        print("No CSVs found in data/raw, Downloads, or workspace root. Please place the provided CSVs in data/raw or Downloads.")
        return
    loaded = load_and_report(files)
    validate_amfi_codes(loaded)


if __name__ == '__main__':
    main()
