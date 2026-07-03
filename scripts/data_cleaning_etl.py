from pathlib import Path

import pandas as pd
import numpy as np
import sqlite3

from sqlalchemy import create_engine, text

# ==========================================================
# Project Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_FILE = DATABASE_DIR / "bluestock_mf.db"

SQL_DIR = PROJECT_ROOT / "sql"

DOCS_DIR = PROJECT_ROOT / "docs"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

def find_csv_files():
    """
    Locate all CSV files inside the project's raw data folder.

    Returns
    -------
    dict
        Dictionary where:
        key   -> filename
        value -> full Path object
    """

    csv_files = {}

    for file in RAW_DATA_DIR.glob("*.csv"):

        csv_files[file.name] = file

    return csv_files


def clean_nav_history(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the NAV history dataset.

    Steps performed:
    1. Convert the date column to datetime.
    2. Remove rows with invalid dates.
    3. Sort records by AMFI code and date.
    4. Remove duplicate NAV entries.
    5. Forward-fill missing NAV values within each scheme.
    6. Remove records where NAV is less than or equal to zero.

    Parameters
    ----------
    df : pd.DataFrame
        Raw NAV history dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned NAV history dataset.
    """

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove rows with invalid dates
    df = df.dropna(subset=["date"])

    # Sort records
    df = df.sort_values(["amfi_code", "date"])

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=["amfi_code", "date"],
        keep="last"
    )

    # Fill missing NAV values
    df["nav"] = (
        df.groupby("amfi_code")["nav"]
        .ffill()
    )

    # Remove invalid NAV values
    invalid_nav = df[df["nav"] <= 0]

    if not invalid_nav.empty:

        print(
            f"Removed {len(invalid_nav)} rows with non-positive NAV values."
        )

        df = df[df["nav"] > 0]

    return df


def clean_investor_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the investor transactions dataset.

    Steps performed:
    1. Convert transaction dates to datetime.
    2. Standardize transaction types.
    3. Convert transaction amounts to numeric values.
    4. Remove transactions with invalid or non-positive amounts.
    5. Standardize KYC status values.

    Parameters
    ----------
    df : pd.DataFrame
        Raw investor transactions dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned investor transactions dataset.
    """

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # ----------------------------------------------------------
    # Parse transaction date
    # ----------------------------------------------------------

    if "transaction_date" in df.columns:

        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"],
            errors="coerce"
        )

    elif "Payment Date" in df.columns:

        df["transaction_date"] = pd.to_datetime(
            df["Payment Date"]
            .str.split("|")
            .str[0]
            .str.strip(),
            dayfirst=True,
            errors="coerce"
        )

    # ----------------------------------------------------------
    # Standardize transaction type
    # ----------------------------------------------------------

    if "transaction_type" in df.columns:

        df["transaction_type"] = (
            df["transaction_type"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df["transaction_type"] = df["transaction_type"].replace(
            {
                "sip": "SIP",
                "sips": "SIP",
                "lumpsum": "Lumpsum",
                "lump sum": "Lumpsum",
                "redemption": "Redemption",
            }
        )

    # ----------------------------------------------------------
    # Clean transaction amount
    # ----------------------------------------------------------

    if "amount_inr" in df.columns:

        df["amount_inr"] = pd.to_numeric(
            df["amount_inr"],
            errors="coerce"
        )

        df = df[df["amount_inr"] > 0]

    elif "Amount" in df.columns:

        df["amount_inr"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

        df = df[df["amount_inr"] > 0]

    # ----------------------------------------------------------
    # Standardize KYC status
    # ----------------------------------------------------------

    if "kyc_status" in df.columns:

        df["kyc_status"] = (
            df["kyc_status"]
            .astype(str)
            .str.strip()
            .str.capitalize()
        )

        valid_status = {
            "Verified",
            "Pending",
            "Not verified",
            "Rejected",
        }

        df["kyc_status"] = df["kyc_status"].apply(
            lambda status: (
                status
                if status in valid_status
                else "Unknown"
            )
        )

    return df


def clean_scheme_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the scheme performance dataset.

    Steps performed:
    1. Convert performance metrics to numeric values.
    2. Detect rows containing invalid performance values.
    3. Validate expense ratio values.
    4. Report any anomalies found.

    Parameters
    ----------
    df : pd.DataFrame
        Raw scheme performance dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned scheme performance dataset.
    """

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # ----------------------------------------------------------
    # Identify performance-related columns
    # ----------------------------------------------------------

    performance_columns = [
        column
        for column in df.columns
        if any(
            keyword in column.lower()
            for keyword in [
                "return",
                "alpha",
                "beta",
                "sharpe",
                "sortino",
            ]
        )
    ]

    # ----------------------------------------------------------
    # Convert performance columns to numeric
    # ----------------------------------------------------------

    for column in performance_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # ----------------------------------------------------------
    # Detect invalid performance values
    # ----------------------------------------------------------

    if performance_columns:

        anomalies = df[
            df[performance_columns]
            .isnull()
            .any(axis=1)
        ]

        if not anomalies.empty:

            print(
                f"Found {len(anomalies)} rows with invalid performance metrics."
            )

    # ----------------------------------------------------------
    # Validate expense ratio
    # ----------------------------------------------------------

    if "expense_ratio_pct" in df.columns:

        df["expense_ratio_pct"] = pd.to_numeric(
            df["expense_ratio_pct"],
            errors="coerce"
        )

        invalid_expense_ratio = df[
            (df["expense_ratio_pct"] < 0.10)
            | (df["expense_ratio_pct"] > 2.50)
        ]

        if not invalid_expense_ratio.empty:

            print(
                f"Found {len(invalid_expense_ratio)} schemes with expense ratios outside the expected range (0.10%–2.50%)."
            )

    return df


def clean_aum(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Assets Under Management (AUM) dataset.

    Steps performed:
    1. Convert the date column to datetime.
    2. Convert the AUM column to numeric values.

    Parameters
    ----------
    df : pd.DataFrame
        Raw AUM dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned AUM dataset.
    """

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # ----------------------------------------------------------
    # Convert date column
    # ----------------------------------------------------------

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

    # ----------------------------------------------------------
    # Convert AUM column
    # ----------------------------------------------------------

    if "aum_crore" in df.columns:

        df["aum_crore"] = pd.to_numeric(
            df["aum_crore"],
            errors="coerce"
        )

    return df
def build_schema_sql(path: Path = SQL_DIR / "schema.sql") -> Path:
    """
    Generate the SQL schema for the Mutual Fund Analytics database.

    Parameters
    ----------
    path : Path
        Output location of the generated schema.sql file.

    Returns
    -------
    Path
        Path to the generated SQL schema file.
    """

    sql = """-- Star schema for Mutual Fund Analytics

CREATE TABLE IF NOT EXISTS dim_fund (
  amfi_code INTEGER PRIMARY KEY,
  fund_house TEXT,
  scheme_name TEXT,
  category TEXT,
  sub_category TEXT,
  plan TEXT,
  launch_date TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
  date TEXT PRIMARY KEY,
  year INTEGER,
  month INTEGER,
  day INTEGER,
  iso_week INTEGER
);

CREATE TABLE IF NOT EXISTS fact_nav (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amfi_code INTEGER,
  date TEXT,
  nav REAL,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
  FOREIGN KEY(date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  investor_id TEXT,
  amfi_code INTEGER,
  transaction_date TEXT,
  transaction_type TEXT,
  amount_inr REAL,
  state TEXT,
  city TEXT,
  kyc_status TEXT,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
  FOREIGN KEY(transaction_date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_performance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amfi_code INTEGER,
  measurement_date TEXT,
  return_1yr_pct REAL,
  return_3yr_pct REAL,
  return_5yr_pct REAL,
  expense_ratio_pct REAL,
  aum_crore INTEGER,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
  FOREIGN KEY(measurement_date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_aum (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fund_house TEXT,
  date TEXT,
  aum_crore REAL,
  num_schemes INTEGER,
  FOREIGN KEY(date) REFERENCES dim_date(date)
);
"""

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(sql)

    return path

def generate_queries(path: Path = SQL_DIR / "queries.sql") -> Path:
    """
    Generate commonly used SQL analysis queries.

    Parameters
    ----------
    path : Path
        Output location of the generated queries.sql file.

    Returns
    -------
    Path
        Path to the generated SQL queries file.
    """

    queries = []

    queries.append("-- 1. Top 5 funds by latest AUM")
    queries.append(
        "SELECT fund_house, SUM(aum_crore) AS total_aum "
        "FROM fact_aum "
        "GROUP BY fund_house "
        "ORDER BY total_aum DESC "
        "LIMIT 5;"
    )

    queries.append("-- 2. Average NAV per month for each scheme")
    queries.append(
        "SELECT amfi_code, strftime('%Y-%m', date) AS ym, AVG(nav) AS avg_nav "
        "FROM fact_nav "
        "GROUP BY amfi_code, ym;"
    )

    queries.append("-- 3. SIP YoY Growth")
    queries.append(
        "SELECT strftime('%Y', transaction_date) AS yr, "
        "SUM(amount_inr) AS total_sip "
        "FROM fact_transactions "
        "WHERE transaction_type='SIP' "
        "GROUP BY yr "
        "ORDER BY yr;"
    )

    queries.append("-- 4. Transactions by State")
    queries.append(
        "SELECT state, COUNT(*) AS tx_count, SUM(amount_inr) AS total_amount "
        "FROM fact_transactions "
        "GROUP BY state "
        "ORDER BY total_amount DESC;"
    )

    queries.append("-- 5. Funds with Expense Ratio below 1%")
    queries.append(
        "SELECT amfi_code, scheme_name, expense_ratio_pct "
        "FROM dim_fund "
        "JOIN fact_performance USING(amfi_code) "
        "WHERE expense_ratio_pct < 1.0;"
    )

    queries.append("-- 6. Top 5 Schemes by Average 3-Year Return")
    queries.append(
        "SELECT amfi_code, AVG(return_3yr_pct) AS avg_3yr "
        "FROM fact_performance "
        "GROUP BY amfi_code "
        "ORDER BY avg_3yr DESC "
        "LIMIT 5;"
    )

    queries.append("-- 7. Monthly NAV Volatility")
    queries.append(
        "SELECT amfi_code, "
        "strftime('%Y-%m', date) AS ym, "
        "ROUND(STDDEV(nav), 4) AS nav_std "
        "FROM fact_nav "
        "GROUP BY amfi_code, ym;"
    )

    queries.append("-- 8. Redemption vs SIP Count")
    queries.append(
        "SELECT strftime('%Y', transaction_date) AS yr, "
        "transaction_type, "
        "COUNT(*) AS cnt "
        "FROM fact_transactions "
        "WHERE transaction_type IN ('SIP','Redemption') "
        "GROUP BY yr, transaction_type;"
    )

    queries.append("-- 9. Schemes with Highest Drawdown")
    queries.append(
        "SELECT amfi_code, scheme_name, max_drawdown_pct "
        "FROM fact_performance "
        "ORDER BY max_drawdown_pct ASC "
        "LIMIT 10;"
    )

    queries.append("-- 10. Number of Schemes per Category")
    queries.append(
        "SELECT category, COUNT(DISTINCT amfi_code) AS num_schemes "
        "FROM dim_fund "
        "GROUP BY category;"
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n\n".join(queries))

    return path
def build_data_dictionary(path: Path = DOCS_DIR / "data_dictionary.md") -> Path:
    """
    Generate the project data dictionary.

    Parameters
    ----------
    path : Path
        Output location of the generated data dictionary.

    Returns
    -------
    Path
        Path to the generated Markdown file.
    """

    md = """# Data Dictionary

This document describes the cleaned datasets, column definitions, and data sources used in the project.

---

## Dimension Tables

### dim_fund
Source: `01_fund_master.csv`

| Column | Type | Description |
|--------|------|-------------|
| amfi_code | INTEGER | AMFI scheme code (Primary Key) |
| fund_house | TEXT | Asset Management Company |
| scheme_name | TEXT | Mutual fund scheme name |
| category | TEXT | Scheme category |
| sub_category | TEXT | Scheme sub-category |
| plan | TEXT | Direct / Regular |
| launch_date | TEXT | Scheme launch date |

---

### dim_date
Derived from date columns.

| Column | Type |
|--------|------|
| date | TEXT |
| year | INTEGER |
| month | INTEGER |
| day | INTEGER |
| iso_week | INTEGER |

---

## Fact Tables

### fact_nav
Source: `02_nav_history.csv`

| Column | Type |
|--------|------|
| amfi_code | INTEGER |
| date | TEXT |
| nav | REAL |

---

### fact_transactions
Source: `08_investor_transactions.csv`

| Column | Type |
|--------|------|
| investor_id | TEXT |
| amfi_code | INTEGER |
| transaction_date | TEXT |
| transaction_type | TEXT |
| amount_inr | REAL |
| state | TEXT |
| city | TEXT |
| kyc_status | TEXT |

---

### fact_performance
Source: `07_scheme_performance.csv`

| Column | Type |
|--------|------|
| return_1yr_pct | REAL |
| return_3yr_pct | REAL |
| return_5yr_pct | REAL |
| expense_ratio_pct | REAL |
| aum_crore | INTEGER |

---

### fact_aum
Source: `03_aum_by_fund_house.csv`

| Column | Type |
|--------|------|
| fund_house | TEXT |
| date | TEXT |
| aum_crore | REAL |
| num_schemes | INTEGER |

---

## Data Sources

- Original CSV datasets stored in `data/raw/`
- Live NAV data fetched from **MFAPI** (`https://api.mfapi.in`)
"""

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(md)

    return path

def main():

    files = find_csv_files()

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # load and clean each expected file
    # 01_fund_master.csv -> dim_fund
    if '01_fund_master.csv' in files:
        fm = pd.read_csv(files['01_fund_master.csv'])
        fm_clean = fm.copy()
        fm_clean['launch_date'] = pd.to_datetime(fm_clean['launch_date'], errors='coerce')
        fm_clean.to_csv(
    PROCESSED_DATA_DIR / "01_fund_master_cleaned.csv",
    index=False
)
    else:
        fm_clean = pd.DataFrame()

    # 02_nav_history.csv
    if '02_nav_history.csv' in files:
        nh = pd.read_csv(files['02_nav_history.csv'])
        nh_clean = clean_nav_history(nh)
        nh_clean.to_csv(
    PROCESSED_DATA_DIR / "02_nav_history_cleaned.csv",
    index=False
)
    else:
        nh_clean = pd.DataFrame()

    # 03_aum_by_fund_house.csv
    if '03_aum_by_fund_house.csv' in files:
        aum = pd.read_csv(files['03_aum_by_fund_house.csv'])
        aum_clean = clean_aum(aum)
        aum_clean.to_csv(
    PROCESSED_DATA_DIR / "03_aum_by_fund_house_cleaned.csv",
    index=False
)
    else:
        aum_clean = pd.DataFrame()

    # 04_monthly_sip_inflows.csv
    if '04_monthly_sip_inflows.csv' in files:
        sip = pd.read_csv(files['04_monthly_sip_inflows.csv'])
        sip.to_csv(
    PROCESSED_DATA_DIR / "04_monthly_sip_inflows_cleaned.csv",
    index=False
)

    # 05_category_inflows.csv
    if '05_category_inflows.csv' in files:
        cat = pd.read_csv(files['05_category_inflows.csv'])
        cat.to_csv(
    PROCESSED_DATA_DIR / "05_category_inflows_cleaned.csv",
    index=False
)

    # 06_industry_folio_count.csv
    if '06_industry_folio_count.csv' in files:
        fol = pd.read_csv(files['06_industry_folio_count.csv'])
        fol.to_csv(
    PROCESSED_DATA_DIR / "06_industry_folio_count_cleaned.csv",
    index=False
)

    # 07_scheme_performance.csv
    if '07_scheme_performance.csv' in files:
        perf = pd.read_csv(files['07_scheme_performance.csv'])
        perf_clean = clean_scheme_performance(perf)
        perf_clean.to_csv(
    PROCESSED_DATA_DIR / "07_scheme_performance_cleaned.csv",
    index=False
)
    else:
        perf_clean = pd.DataFrame()

    # 08_investor_transactions.csv
    if '08_investor_transactions.csv' in files:
        tx = pd.read_csv(files['08_investor_transactions.csv'])
        tx_clean = clean_investor_transactions(tx)
        tx_clean.to_csv(
    PROCESSED_DATA_DIR / "08_investor_transactions_cleaned.csv",
    index=False
)
    else:
        tx_clean = pd.DataFrame()

    # 09_portfolio_holdings.csv
    if '09_portfolio_holdings.csv' in files:
        ph = pd.read_csv(files['09_portfolio_holdings.csv'])
        ph.to_csv(
    PROCESSED_DATA_DIR / "09_portfolio_holdings_cleaned.csv",
    index=False
)

    # 10_benchmark_indices.csv
    if '10_benchmark_indices.csv' in files:
        bi = pd.read_csv(files['10_benchmark_indices.csv'])
        bi['date'] = pd.to_datetime(bi['date'], errors='coerce')
        bi.to_csv(
    PROCESSED_DATA_DIR / "10_benchmark_indices_cleaned.csv",
    index=False
)
    # ----------------------------------------------------------
    # Process Live NAV Files
    # ----------------------------------------------------------

    for file in RAW_DATA_DIR.glob("live_nav_*.csv"):

        df = pd.read_csv(file)

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        output_file = (
            PROCESSED_DATA_DIR /
            file.name.replace(".csv", "_cleaned.csv")
        )

        df.to_csv(output_file, index=False)

    # ----------------------------------------------------------
    # Generate SQL Files
    # ----------------------------------------------------------

    schema_path = build_schema_sql()
    queries_path = generate_queries()
    dict_path = build_data_dictionary()

    # ----------------------------------------------------------
    # Create SQLite Database
    # ----------------------------------------------------------

    engine = create_engine(
        f"sqlite:///{DATABASE_FILE}"
    )

    with open(schema_path, "r", encoding="utf-8") as file:
        sql_text = file.read()

    con = sqlite3.connect(DATABASE_FILE)

    try:
        con.executescript(sql_text)
    finally:
        con.close()

    # ----------------------------------------------------------
    # Load Dimension Table
    # ----------------------------------------------------------

    if not fm_clean.empty:

        fm_clean[
            [
                "amfi_code",
                "fund_house",
                "scheme_name",
                "category",
                "sub_category",
                "plan",
                "launch_date",
            ]
        ].to_sql(
            "dim_fund",
            engine,
            if_exists="replace",
            index=False,
        )

    # ----------------------------------------------------------
    # Create Date Dimension
    # ----------------------------------------------------------

    dates = pd.DataFrame()

    if not nh_clean.empty:

        dates = pd.DataFrame(
            {
                "date": nh_clean["date"].dt.strftime("%Y-%m-%d")
            }
        )

    if not tx_clean.empty:

        tx_dates = pd.DataFrame(
            {
                "date": tx_clean["transaction_date"].dt.strftime("%Y-%m-%d")
            }
        )

        dates = (
            pd.concat([dates, tx_dates])
            if not dates.empty
            else tx_dates
        )

    if not dates.empty:

        dates = dates.drop_duplicates().dropna()

        parsed_dates = pd.to_datetime(dates["date"])

        dates["year"] = parsed_dates.dt.year
        dates["month"] = parsed_dates.dt.month
        dates["day"] = parsed_dates.dt.day
        dates["iso_week"] = parsed_dates.dt.isocalendar().week

        dates.to_sql(
            "dim_date",
            engine,
            if_exists="replace",
            index=False,
        )

    # ----------------------------------------------------------
    # Load Fact Tables
    # ----------------------------------------------------------

    if not nh_clean.empty:

        nh_tmp = nh_clean.copy()

        nh_tmp["date"] = nh_tmp["date"].dt.strftime("%Y-%m-%d")

        nh_tmp.to_sql(
            "fact_nav",
            engine,
            if_exists="replace",
            index=False,
        )

    if not tx_clean.empty:

        tx_tmp = tx_clean.copy()

        if "transaction_date" in tx_tmp.columns:

            tx_tmp["transaction_date"] = (
                tx_tmp["transaction_date"]
                .dt.strftime("%Y-%m-%d")
            )

        tx_tmp.to_sql(
            "fact_transactions",
            engine,
            if_exists="replace",
            index=False,
        )

    if not perf_clean.empty:

        perf_clean.to_sql(
            "fact_performance",
            engine,
            if_exists="replace",
            index=False,
        )

    if not aum_clean.empty:

        aum_tmp = aum_clean.copy()

        if "date" in aum_tmp.columns:

            aum_tmp["date"] = (
                pd.to_datetime(
                    aum_tmp["date"],
                    errors="coerce",
                )
                .dt.strftime("%Y-%m-%d")
            )

        aum_tmp.to_sql(
            "fact_aum",
            engine,
            if_exists="replace",
            index=False,
        )


    # ----------------------------------------------------------
    # Verification
    # ----------------------------------------------------------

    print("\nDatabase Verification")
    print("-" * 70)

    with engine.connect() as conn:

        tables = [
            "dim_fund",
            "dim_date",
            "fact_nav",
            "fact_transactions",
            "fact_performance",
            "fact_aum",
        ]

        for table in tables:

            try:
                count = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table}")
                ).scalar()

                if count is None:
                    count = 0

            except Exception:
                count = "N/A"

            print(f"{table:<20} : {count}")

    print("\n" + "=" * 70)
    print("Data Cleaning + SQL Database Design completed successfully.")
    print("=" * 70)
    print(f"Database      : {DATABASE_FILE}")
    print(f"Processed Data: {PROCESSED_DATA_DIR}")
    print(f"SQL Schema    : {schema_path}")
    print(f"SQL Queries   : {queries_path}")
    print(f"Documentation : {dict_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()