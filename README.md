# Mutual Fund Analytics — Bluestock Fintech Capstone

**Intern:** Sandib Jena
**Role:** Data Analyst Intern
**Repo:** https://github.com/SandibJena/Capstone-ProjectI_Bluestocks

---

## Quick Start

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Place the provided CSVs into `data/raw/` or keep them in your `Downloads/` folder.

3. Run ingestion:

```bash
python data_ingestion.py
```

4. Fetch live NAVs:

```bash
python live_nav_fetch.py --codes 125497 119551 120503 118632 119092 120841
```

---

## Project Structure

```
├── data/
│   ├── raw/               # Original CSVs + live NAV JSON/CSV
│   └── processed/         # Cleaned CSVs, load summary, data quality summary
├── notebooks/             # EDA and visualisation notebooks
├── sql/                   # schema.sql, queries.sql
├── dashboard/             # Dashboard prototype
├── reports/               # Day reports and findings
├── data_ingestion.py
├── live_nav_fetch.py
├── day2_etl.py
├── data_dictionary.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Day 1 Report — Data Ingestion

**Date:** 2026-06-25

### Objectives
- Project scaffold and folder structure
- Install dependencies and create `requirements.txt`
- Load provided CSV datasets and inspect shapes/dtypes/head
- Implement ingestion and live NAV fetch scripts
- Validate AMFI codes
- Initialize Git and push Day 1 commit

### Actions Completed
- Created folders: `data/raw`, `data/processed`, `notebooks/`, `sql/`, `dashboard/`, `reports/`
- Added `.gitignore` and `requirements.txt` (pandas, numpy, matplotlib, seaborn, plotly, sqlalchemy, requests, scipy, jupyter)
- Implemented `data_ingestion.py` to locate CSVs (data/raw, Downloads, workspace root), print `.shape`, `.dtypes`, `.head()`, detect basic anomalies, and write `data/processed/load_summary.txt` and `data/processed/data_quality_summary.txt`
- Implemented `live_nav_fetch.py` to fetch NAV JSON from `https://api.mfapi.in/mf/<AMFI>` and save JSON+CSV to `data/raw/`
- Ran `data_ingestion.py` — all 10 provided CSVs loaded successfully
- AMFI validation: All AMFI codes in `01_fund_master.csv` were present in `02_nav_history.csv` sample
- Initialized Git and made commit: `"Day 1: Data ingestion complete"`

### Artifacts
- `data_ingestion.py`
- `live_nav_fetch.py`
- `requirements.txt`, `.gitignore`, `README.md`
- `data/processed/load_summary.txt`
- `data/processed/data_quality_summary.txt`

### Data Quality Notes
- Observed missing `yoy_growth_pct` in `04_monthly_sip_inflows.csv`
- Some CSVs had mixed date formats; ingestion coerces dates where possible

---

## Day 2 Report — ETL & Database Loading

**Date:** 2026-06-25

### Objectives
- Clean `nav_history`, `investor_transactions`, and `scheme_performance` datasets
- Design SQLite star schema and create `schema.sql`
- Load cleaned datasets into SQLite via SQLAlchemy
- Produce analytical queries and a data dictionary

### Actions Completed
- Implemented `day2_etl.py` with the following cleaning steps:
  - `nav_history`: parse dates, sort by `amfi_code` + `date`, drop duplicates, forward-fill NAVs, validate `nav > 0`
  - `investor_transactions`: standardize `transaction_type`, parse dates, validate `amount_inr > 0`, normalize `kyc_status`
  - `scheme_performance`: coerce returns to numeric, flag non-numeric rows, validate `expense_ratio_pct` range (0.1%–2.5%)
  - Additional cleaning for AUM, holdings, and benchmarks datasets
- Generated `schema.sql` — star schema with `dim_fund`, `dim_date`, and fact tables `fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum`
- Generated `queries.sql` with 10 analytical queries (top funds by AUM, avg NAV per month, SIP YoY growth, transactions by state, expense ratio filter, and more)
- Created `data_dictionary.md` documenting all tables, columns, types, and sources

### ETL Row Counts (loaded into `bluestock_mf.db`)

| Table | Rows |
|---|---|
| dim_fund | 40 |
| dim_date | 1,296 |
| fact_nav | 46,000 |
| fact_transactions | 32,778 |
| fact_performance | 40 |
| fact_aum | 90 |

### Artifacts
- `day2_etl.py`
- `schema.sql`, `queries.sql`, `data_dictionary.md`
- `bluestock_mf.db`
- Cleaned CSVs in `data/processed/` (11 files including live NAVs)
- Git commit pushed: `"Day 2: Cleaned data + SQLite DB loaded"`

### Data Quality Notes
- Date parsing warnings for mixed formats; ETL coerces and logs warnings
- Expense ratio outliers flagged in `data/processed/07_scheme_performance_cleaned.csv`
- `02_nav_history_cleaned.csv` forward-filled missing NAVs for non-trading days; manual review recommended for larger gaps

### Next Steps
- Add EDA notebooks with visualisations under `notebooks/`
- Implement data tests to catch date parse failures, negative NAVs, and AMFI mismatches
- Build dashboard prototype to visualize AUM, NAV trends, and SIP flows
-This i an update in the readme file so i can check wether it is being updated or not.
