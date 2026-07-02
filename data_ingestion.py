
"""
data_ingestion.py
Day 1 - Data Ingestion (ETL)
"""

import glob
import os
from typing import Dict, List

import pandas as pd


def find_csv_files() -> List[str]:
    paths = []
    paths.extend(glob.glob(os.path.join("data", "raw", "*.csv")))
    downloads = os.path.join("C:\\Users", os.getenv("USERNAME", ""), "Downloads")
    if os.path.isdir(downloads):
        paths.extend(glob.glob(os.path.join(downloads, "*.csv")))
    paths.extend(glob.glob("*.csv"))
    seen = set()
    out = []
    for p in paths:
        name = os.path.basename(p)
        if name not in seen:
            out.append(p)
            seen.add(name)
    return out


def basic_anomalies(df: pd.DataFrame) -> List[str]:
    issues = []
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        issues.append(f"Missing Values: {missing.to_dict()}")
    dup = df.duplicated().sum()
    if dup:
        issues.append(f"Duplicate Rows: {dup}")
    for col in df.columns:
        if df[col].dtype == "object":
            sample = df[col].dropna().astype(str).head(50)
            if not sample.empty:
                numeric_like = (
                    sample.str.replace(",", "", regex=False)
                    .str.replace("%", "", regex=False)
                    .str.replace(" ", "", regex=False)
                    .str.isnumeric()
                    .all()
                )
                if numeric_like:
                    issues.append(f"Column '{col}' looks numeric.")
    return issues


def load_and_report(files: List[str]) -> Dict[str, pd.DataFrame]:
    os.makedirs(os.path.join("data", "processed"), exist_ok=True)
    loaded = {}
    summary = []
    for file in files:
        try:
            df = pd.read_csv(file)
        except Exception:
            try:
                df = pd.read_csv(file, encoding="latin1")
            except Exception as e:
                summary.append(f"FAILED {file}: {e}")
                continue
        name = os.path.basename(file)
        loaded[name] = df
        print("="*60)
        print(name)
        print(df.shape)
        print(df.dtypes)
        print(df.head())
        issues = basic_anomalies(df)
        if issues:
            print("Issues:")
            for i in issues:
                print("-", i)
        summary.append(f"{name}: shape={df.shape}, issues={issues}")
    with open(os.path.join("data","processed","load_summary.txt"),"w",encoding="utf-8") as f:
        f.write("\n".join(summary))
    return loaded


def explore_fund_master(loaded: Dict[str,pd.DataFrame]) -> None:
    fm=None
    for n,df in loaded.items():
        if "fund_master" in n.lower():
            fm=df
            break
    if fm is None:
        print("Fund master not found.")
        return
    print("\n===== FUND MASTER EXPLORATION =====")
    for col,title in [("fund_house","Fund Houses"),("category","Categories"),("sub_category","Sub Categories")]:
        if col in fm.columns:
            print(f"\n{title}:")
            print(sorted(fm[col].dropna().unique()))
    risk=None
    for c in fm.columns:
        if "risk" in c.lower():
            risk=c
            break
    if risk:
        print("\nRisk Grades:")
        print(sorted(fm[risk].dropna().unique()))


def validate_amfi_codes(loaded: Dict[str,pd.DataFrame]) -> List[str]:
    report=[]
    fm=nh=None
    for n,df in loaded.items():
        if "fund_master" in n.lower():
            fm=df
        if "nav_history" in n.lower():
            nh=df
    if fm is not None and nh is not None:
        missing=sorted(set(fm["amfi_code"].astype(str))-set(nh["amfi_code"].astype(str)))
        if missing:
            report.append(f"{len(missing)} missing AMFI codes. Examples: {missing[:5]}")
        else:
            report.append("All AMFI codes are present in NAV history.")
    else:
        report.append("Unable to validate AMFI codes.")
    with open(os.path.join("data","processed","data_quality_summary.txt"),"w",encoding="utf-8") as f:
        f.write("\n".join(report))
    print("\n".join(report))
    return report


def main():
    files=find_csv_files()
    if not files:
        print("No CSV files found.")
        return
    loaded=load_and_report(files)
    explore_fund_master(loaded)
    validate_amfi_codes(loaded)
    print("\nDay 1 Data Ingestion Completed Successfully.")


if __name__=="__main__":
    main()
