"""
Project Setup + Data Ingestion (ETL)

Description:
Loads all mutual fund datasets from the raw data folder,
performs initial data inspection, detects anomalies,
explores the fund master dataset, validates AMFI codes,
and generates summary reports.

Author: Sandib Jena
Project: Bluestocks Data Analyst Capstone
"""

from pathlib import Path
from typing import Dict, List

import pandas as pd

# ==========================================================
# Project Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Locate CSV Files
# ==========================================================

def find_csv_files() -> List[Path]:
    """
    Locate all CSV files in the raw data folder.
    """
    return sorted(RAW_DATA_DIR.glob("*.csv"))


# ==========================================================
# Detect Basic Data Quality Issues
# ==========================================================

def basic_anomalies(df: pd.DataFrame) -> List[str]:
    issues = []

    missing = df.isna().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        issues.append(f"Missing Values: {missing.to_dict()}")

    duplicate_rows = df.duplicated().sum()

    if duplicate_rows:
        issues.append(f"Duplicate Rows: {duplicate_rows}")

    for column in df.columns:

        if df[column].dtype == "object":

            sample = df[column].dropna().astype(str).head(50)

            if not sample.empty:

                numeric_like = (
                    sample.str.replace(",", "", regex=False)
                    .str.replace("%", "", regex=False)
                    .str.replace(" ", "", regex=False)
                    .str.isnumeric()
                    .all()
                )

                if numeric_like:
                    issues.append(f"Column '{column}' appears to contain numeric values.")

    return issues


# ==========================================================
# Load CSV Files
# ==========================================================

def load_and_report(files: List[Path]) -> Dict[str, pd.DataFrame]:

    loaded = {}
    summary = []

    for file in files:

        try:
            df = pd.read_csv(file)

        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding="latin1")

        except Exception as e:
            summary.append(f"FAILED: {file.name} -> {e}")
            continue

        loaded[file.name] = df

        print("=" * 70)
        print(f"Dataset : {file.name}")
        print(f"Shape   : {df.shape}")

        print("\nData Types")
        print(df.dtypes)

        print("\nFirst Five Rows")
        print(df.head())

        issues = basic_anomalies(df)

        if issues:

            print("\nDetected Issues")

            for issue in issues:
                print(f"• {issue}")

        else:
            print("\nNo obvious data quality issues found.")

        summary.append(
            f"{file.name}\n"
            f"Shape: {df.shape}\n"
            f"Issues: {issues}\n"
        )

    with open(
        PROCESSED_DATA_DIR / "load_summary.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(summary))

    return loaded


# ==========================================================
# Explore Fund Master Dataset
# ==========================================================

def explore_fund_master(loaded: Dict[str, pd.DataFrame]) -> None:

    fund_master = None

    for filename, dataframe in loaded.items():

        if "fund_master" in filename.lower():
            fund_master = dataframe
            break

    if fund_master is None:
        print("\nFund Master dataset not found.")
        return

    print("\n" + "=" * 70)
    print("FUND MASTER EXPLORATION")
    print("=" * 70)

    columns_to_check = [
        ("fund_house", "Fund Houses"),
        ("category", "Categories"),
        ("sub_category", "Sub Categories"),
    ]

    for column, title in columns_to_check:

        if column in fund_master.columns:

            print(f"\n{title}")

            print(sorted(fund_master[column].dropna().unique()))

    risk_column = None

    for column in fund_master.columns:

        if "risk" in column.lower():
            risk_column = column
            break

    if risk_column:

        print("\nRisk Grades")

        print(sorted(fund_master[risk_column].dropna().unique()))


# ==========================================================
# Validate AMFI Codes
# ==========================================================

def validate_amfi_codes(loaded: Dict[str, pd.DataFrame]):

    report = []

    fund_master = None
    nav_history = None

    for filename, dataframe in loaded.items():

        if "fund_master" in filename.lower():
            fund_master = dataframe

        if "nav_history" in filename.lower():
            nav_history = dataframe

    if fund_master is not None and nav_history is not None:

        missing_codes = sorted(
            set(fund_master["amfi_code"].astype(str))
            - set(nav_history["amfi_code"].astype(str))
        )

        if missing_codes:

            report.append(
                f"{len(missing_codes)} missing AMFI codes."
            )

            report.append(
                f"Examples: {missing_codes[:5]}"
            )

        else:

            report.append(
                "All AMFI codes are present in NAV History."
            )

    else:

        report.append(
            "Unable to validate AMFI codes."
        )

    with open(
        PROCESSED_DATA_DIR / "data_quality_summary.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report))

    print("\n")

    for item in report:
        print(item)


# ==========================================================
# Main
# ==========================================================

def main():

    files = find_csv_files()

    if not files:

        print("=" * 70)
        print("No CSV files found.")
        print(f"Expected location:\n{RAW_DATA_DIR}")
        print("=" * 70)
        return

    loaded = load_and_report(files)

    explore_fund_master(loaded)

    validate_amfi_codes(loaded)

    print("\n" + "=" * 70)
    print("Project Setup + Data Ingestion completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()