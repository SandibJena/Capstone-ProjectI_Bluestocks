import os
import glob
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import sqlite3


def find_csv_files():
    paths = []
    # prefer project data/raw
    paths.extend(glob.glob(os.path.join("data", "raw", "*.csv")))
    # also look in Downloads
    downloads = os.path.join("C:\\Users", os.getenv("USERNAME", ""), "Downloads")
    if os.path.isdir(downloads):
        paths.extend(glob.glob(os.path.join(downloads, "*.csv")))
    # workspace root
    paths.extend(glob.glob("*.csv"))
    # deduplicate by basename
    seen = set()
    out = {}
    for p in paths:
        bn = os.path.basename(p)
        if bn not in seen:
            out[bn] = p
            seen.add(bn)
    return out


def clean_nav_history(df: pd.DataFrame):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values(['amfi_code', 'date'])
    # remove exact duplicates keeping last
    df = df.drop_duplicates(subset=['amfi_code', 'date'], keep='last')
    # forward fill missing navs per amfi_code
    df['nav'] = df.groupby('amfi_code')['nav'].ffill()
    # validate nav > 0
    bad = df[df['nav'] <= 0]
    if not bad.empty:
        print(f"Dropping {len(bad)} non-positive NAV rows")
        df = df[df['nav'] > 0]
    return df


def clean_investor_transactions(df: pd.DataFrame):
    df = df.copy()
    # parse date
    if 'transaction_date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    elif 'Payment Date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['Payment Date'].str.split('|').str[0].str.strip(), dayfirst=True, errors='coerce')
    # standardize transaction_type
    if 'transaction_type' in df.columns:
        df['transaction_type'] = df['transaction_type'].astype(str).str.strip().str.lower()
        df['transaction_type'] = df['transaction_type'].replace({
            'sip': 'SIP', 'sips': 'SIP', 'lumpsum': 'Lumpsum', 'lump sum': 'Lumpsum', 'redemption': 'Redemption'
        })
    # amount field
    if 'amount_inr' in df.columns:
        df['amount_inr'] = pd.to_numeric(df['amount_inr'], errors='coerce')
        df = df[df['amount_inr'] > 0]
    elif 'Amount' in df.columns:
        df['amount_inr'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df[df['amount_inr'] > 0]
    # kyc status standardize
    if 'kyc_status' in df.columns:
        df['kyc_status'] = df['kyc_status'].astype(str).str.strip().str.capitalize()
        allowed = {'Verified', 'Pending', 'Not verified', 'Rejected'}
        df['kyc_status'] = df['kyc_status'].apply(lambda x: x if x in allowed else 'Unknown')
    return df


def clean_scheme_performance(df: pd.DataFrame):
    df = df.copy()
    # numeric columns for returns
    return_cols = [c for c in df.columns if 'return' in c or 'alpha' in c or 'beta' in c or 'sharpe' in c or 'sortino' in c]
    for c in return_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    # flag anomalies
    anomalies = df[df[return_cols].isnull().any(axis=1)]
    if not anomalies.empty:
        print(f"Found {len(anomalies)} rows with non-numeric returns in scheme_performance")
    # expense ratio
    if 'expense_ratio_pct' in df.columns:
        df['expense_ratio_pct'] = pd.to_numeric(df['expense_ratio_pct'], errors='coerce')
        out_of_range = df[(df['expense_ratio_pct'] < 0.1) | (df['expense_ratio_pct'] > 2.5)]
        if not out_of_range.empty:
            print(f"Found {len(out_of_range)} schemes with expense_ratio_pct outside 0.1-2.5%")
    return df


def clean_aum(df: pd.DataFrame):
    df = df.copy()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'aum_crore' in df.columns:
        df['aum_crore'] = pd.to_numeric(df['aum_crore'], errors='coerce')
    return df


def build_schema_sql(path='schema.sql'):
    sql = '''-- Star schema for Mutual Fund Analytics

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
'''
    with open(path, 'w', encoding='utf8') as fh:
        fh.write(sql)
    return path


def generate_queries(path='queries.sql'):
    queries = []
    queries.append('-- 1. Top 5 funds by latest AUM')
    queries.append("SELECT fund_house, SUM(aum_crore) as total_aum FROM fact_aum GROUP BY fund_house ORDER BY total_aum DESC LIMIT 5;")
    queries.append('-- 2. Average NAV per month for each scheme')
    queries.append("SELECT amfi_code, strftime('%Y-%m', date) as ym, AVG(nav) as avg_nav FROM fact_nav GROUP BY amfi_code, ym;")
    queries.append('-- 3. SIP YoY growth (sum of SIP amounts by year)')
    queries.append("SELECT strftime('%Y', transaction_date) as yr, SUM(amount_inr) as total_sip FROM fact_transactions WHERE transaction_type='SIP' GROUP BY yr ORDER BY yr;")
    queries.append('-- 4. Transactions by state')
    queries.append("SELECT state, COUNT(*) as tx_count, SUM(amount_inr) as total_amount FROM fact_transactions GROUP BY state ORDER BY total_amount DESC;")
    queries.append('-- 5. Funds with expense_ratio < 1%')
    queries.append("SELECT amfi_code, scheme_name, expense_ratio_pct FROM dim_fund JOIN fact_performance USING(amfi_code) WHERE expense_ratio_pct < 1.0;")
    queries.append('-- 6. Top 5 schemes by average 3yr return')
    queries.append("SELECT amfi_code, AVG(return_3yr_pct) as avg_3yr FROM fact_performance GROUP BY amfi_code ORDER BY avg_3yr DESC LIMIT 5;")
    queries.append('-- 7. Monthly NAV volatility (std dev) for each scheme')
    queries.append("SELECT amfi_code, strftime('%Y-%m', date) as ym, ROUND(STDDEV(nav),4) as nav_std FROM fact_nav GROUP BY amfi_code, ym;")
    queries.append('-- 8. Redemption vs SIP count by year')
    queries.append("SELECT strftime('%Y', transaction_date) as yr, transaction_type, COUNT(*) as cnt FROM fact_transactions WHERE transaction_type IN ('SIP','Redemption') GROUP BY yr, transaction_type;")
    queries.append('-- 9. Schemes with highest max drawdown (from scheme_performance)')
    queries.append("SELECT amfi_code, scheme_name, max_drawdown_pct FROM fact_performance ORDER BY max_drawdown_pct ASC LIMIT 10;")
    queries.append('-- 10. Number of schemes per category')
    queries.append("SELECT category, COUNT(DISTINCT amfi_code) as num_schemes FROM dim_fund GROUP BY category;")
    with open(path, 'w', encoding='utf8') as fh:
        fh.write('\n\n'.join(queries))
    return path


def build_data_dictionary(path='data_dictionary.md'):
    md = '''# Data Dictionary

This document describes the cleaned datasets, column definitions and sources.

- `dim_fund` (from `01_fund_master.csv`):
  - `amfi_code` (INTEGER): AMFI scheme code, primary key.
  - `fund_house` (TEXT): Asset manager name.
  - `scheme_name` (TEXT): Official scheme name.
  - `category` (TEXT): High-level category (Equity/Debt/etc).
  - `sub_category` (TEXT): Sub-category (Large Cap/Mid Cap/etc).
  - `plan` (TEXT): Direct/Regular.
  - `launch_date` (TEXT): Original launch date string.

- `dim_date` (derived):
  - `date` (TEXT): ISO date string, primary key.
  - `year`, `month`, `day`, `iso_week` (INTEGER): Date breakdown fields.

- `fact_nav` (from `02_nav_history.csv`):
  - `amfi_code` (INTEGER): FK to `dim_fund`.
  - `date` (TEXT): FK to `dim_date`.
  - `nav` (REAL): Net Asset Value.

- `fact_transactions` (from `08_investor_transactions.csv`):
  - `investor_id` (TEXT): Unique investor id.
  - `amfi_code` (INTEGER): FK.
  - `transaction_date` (TEXT): FK.
  - `transaction_type` (TEXT): SIP/Lumpsum/Redemption.
  - `amount_inr` (REAL): Amount in INR.
  - `state`, `city` (TEXT): Location.
  - `kyc_status` (TEXT): KYC status (Verified/Pending/Unknown).

- `fact_performance` (from `07_scheme_performance.csv`):
  - `return_1yr_pct`, `return_3yr_pct`, `return_5yr_pct` (REAL): Returns in percent.
  - `expense_ratio_pct` (REAL): Expense ratio in percent.
  - `aum_crore` (INTEGER): AUM in crores.

- `fact_aum` (from `03_aum_by_fund_house.csv`):
  - `fund_house` (TEXT) and `date` (TEXT)
  - `aum_crore` (REAL), `num_schemes` (INTEGER)

Sources: Original CSVs provided in `data/raw/` and fetched live NAVs from `mfapi.in` saved in `data/raw/`.
'''
    with open(path, 'w', encoding='utf8') as fh:
        fh.write(md)
    return path


def main():
    files = find_csv_files()
    os.makedirs('data/processed', exist_ok=True)

    # load and clean each expected file
    # 01_fund_master.csv -> dim_fund
    if '01_fund_master.csv' in files:
        fm = pd.read_csv(files['01_fund_master.csv'])
        fm_clean = fm.copy()
        fm_clean['launch_date'] = pd.to_datetime(fm_clean['launch_date'], errors='coerce')
        fm_clean.to_csv('data/processed/01_fund_master_cleaned.csv', index=False)
    else:
        fm_clean = pd.DataFrame()

    # 02_nav_history.csv
    if '02_nav_history.csv' in files:
        nh = pd.read_csv(files['02_nav_history.csv'])
        nh_clean = clean_nav_history(nh)
        nh_clean.to_csv('data/processed/02_nav_history_cleaned.csv', index=False)
    else:
        nh_clean = pd.DataFrame()

    # 03_aum_by_fund_house.csv
    if '03_aum_by_fund_house.csv' in files:
        aum = pd.read_csv(files['03_aum_by_fund_house.csv'])
        aum_clean = clean_aum(aum)
        aum_clean.to_csv('data/processed/03_aum_by_fund_house_cleaned.csv', index=False)
    else:
        aum_clean = pd.DataFrame()

    # 04_monthly_sip_inflows.csv
    if '04_monthly_sip_inflows.csv' in files:
        sip = pd.read_csv(files['04_monthly_sip_inflows.csv'])
        sip.to_csv('data/processed/04_monthly_sip_inflows_cleaned.csv', index=False)

    # 05_category_inflows.csv
    if '05_category_inflows.csv' in files:
        cat = pd.read_csv(files['05_category_inflows.csv'])
        cat.to_csv('data/processed/05_category_inflows_cleaned.csv', index=False)

    # 06_industry_folio_count.csv
    if '06_industry_folio_count.csv' in files:
        fol = pd.read_csv(files['06_industry_folio_count.csv'])
        fol.to_csv('data/processed/06_industry_folio_count_cleaned.csv', index=False)

    # 07_scheme_performance.csv
    if '07_scheme_performance.csv' in files:
        perf = pd.read_csv(files['07_scheme_performance.csv'])
        perf_clean = clean_scheme_performance(perf)
        perf_clean.to_csv('data/processed/07_scheme_performance_cleaned.csv', index=False)
    else:
        perf_clean = pd.DataFrame()

    # 08_investor_transactions.csv
    if '08_investor_transactions.csv' in files:
        tx = pd.read_csv(files['08_investor_transactions.csv'])
        tx_clean = clean_investor_transactions(tx)
        tx_clean.to_csv('data/processed/08_investor_transactions_cleaned.csv', index=False)
    else:
        tx_clean = pd.DataFrame()

    # 09_portfolio_holdings.csv
    if '09_portfolio_holdings.csv' in files:
        ph = pd.read_csv(files['09_portfolio_holdings.csv'])
        ph.to_csv('data/processed/09_portfolio_holdings_cleaned.csv', index=False)

    # 10_benchmark_indices.csv
    if '10_benchmark_indices.csv' in files:
        bi = pd.read_csv(files['10_benchmark_indices.csv'])
        bi['date'] = pd.to_datetime(bi['date'], errors='coerce')
        bi.to_csv('data/processed/10_benchmark_indices_cleaned.csv', index=False)

    # also include live navs we fetched
    for fname in glob.glob(os.path.join('data', 'raw', 'live_nav_*.csv')):
        bn = os.path.basename(fname)
        df = pd.read_csv(fname)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        outname = os.path.join('data', 'processed', bn.replace('.csv', '_cleaned.csv'))
        df.to_csv(outname, index=False)

    # build schema.sql and queries
    schema_path = build_schema_sql('schema.sql')
    queries_path = generate_queries('queries.sql')
    dict_path = build_data_dictionary('data_dictionary.md')

    # load into sqlite
    engine = create_engine('sqlite:///bluestock_mf.db')
    # create tables from schema using sqlite3 (executescript)
    sql_text = open(schema_path, 'r', encoding='utf8').read()
    db_path = 'bluestock_mf.db'
    con = sqlite3.connect(db_path)
    try:
        con.executescript(sql_text)
    finally:
        con.close()

    # load dim_fund
    if not fm_clean.empty:
        fm_clean.rename(columns={'amfi_code':'amfi_code'}, inplace=True)
        fm_clean[['amfi_code','fund_house','scheme_name','category','sub_category','plan','launch_date']].to_sql('dim_fund', engine, if_exists='replace', index=False)
    # dim_date from nav dates and transactions
    dates = pd.DataFrame()
    if not nh_clean.empty:
        dates = pd.DataFrame({'date': nh_clean['date'].dt.strftime('%Y-%m-%d')})
    if not tx_clean.empty:
        tx_dates = pd.DataFrame({'date': tx_clean['transaction_date'].dt.strftime('%Y-%m-%d')})
        dates = pd.concat([dates, tx_dates]) if not dates.empty else tx_dates
    if not dates.empty:
        dates = dates.drop_duplicates().dropna()
        dates['year'] = pd.to_datetime(dates['date']).dt.year
        dates['month'] = pd.to_datetime(dates['date']).dt.month
        dates['day'] = pd.to_datetime(dates['date']).dt.day
        dates['iso_week'] = pd.to_datetime(dates['date']).dt.isocalendar().week
        dates.to_sql('dim_date', engine, if_exists='replace', index=False)

    # fact_nav
    if not nh_clean.empty:
        nh_tmp = nh_clean.copy()
        nh_tmp['date'] = nh_tmp['date'].dt.strftime('%Y-%m-%d')
        nh_tmp.to_sql('fact_nav', engine, if_exists='replace', index=False)

    # fact_transactions
    if not tx_clean.empty:
        tx_tmp = tx_clean.copy()
        if 'transaction_date' in tx_tmp.columns:
            tx_tmp['transaction_date'] = tx_tmp['transaction_date'].dt.strftime('%Y-%m-%d')
        tx_tmp.to_sql('fact_transactions', engine, if_exists='replace', index=False)

    # fact_performance
    if not perf_clean.empty:
        perf_tmp = perf_clean.copy()
        perf_tmp.to_sql('fact_performance', engine, if_exists='replace', index=False)

    # fact_aum
    if not aum_clean.empty:
        aum_tmp = aum_clean.copy()
        if 'date' in aum_tmp.columns:
            aum_tmp['date'] = pd.to_datetime(aum_tmp['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        aum_tmp.to_sql('fact_aum', engine, if_exists='replace', index=False)

    # verification: print row counts
    with engine.connect() as conn:
        for tbl in ['dim_fund','dim_date','fact_nav','fact_transactions','fact_performance','fact_aum']:
            try:
                res = conn.execute(text(f"SELECT COUNT(*) as cnt FROM {tbl}"))
                cnt = res.fetchone()[0]
            except Exception:
                cnt = 'NA'
            print(f"Table {tbl}: {cnt} rows")

    print('Day 2 ETL complete. Cleaned CSVs in data/processed/ and bluestock_mf.db created.')


if __name__ == '__main__':
    main()
