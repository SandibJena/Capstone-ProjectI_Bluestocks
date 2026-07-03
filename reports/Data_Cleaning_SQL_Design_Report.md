# Day 2 Report — Mutual Fund Analytics (Bluestocks)

**Date:** 2026-06-25

## Objectives
- Clean `nav_history`, `investor_transactions`, and `scheme_performance` datasets
- Design SQLite star schema and create `schema.sql`
- Load cleaned datasets into SQLite via SQLAlchemy
- Produce analytical queries and a data dictionary

## Actions Completed
- Implemented `day2_etl.py` to perform:
  - `nav_history` cleaning: parse dates, sort by `amfi_code`+`date`, drop duplicates, forward-fill NAVs, validate `nav > 0`.
  - `investor_transactions` cleaning: standardize `transaction_type`, parse dates, validate `amount_inr > 0`, normalize `kyc_status`.
  - `scheme_performance` cleaning: coerce returns to numeric, flag non-numeric rows, validate `expense_ratio_pct` range (0.1%–2.5%).
  - Other cleaning for AUM, holdings, benchmarks.
- Generated `schema.sql` (star schema with `dim_fund`, `dim_date`, and fact tables `fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum`).
- Generated `queries.sql` with 10 analytical queries (top funds by AUM, avg NAV per month, SIP YoY growth, transactions by state, expense ratio filter, and more).
- Created `data_dictionary.md` documenting tables, columns, types, and sources.
- ETL run results (row counts loaded into SQLite `bluestock_mf.db`):
  - `dim_fund`: 40 rows
  - `dim_date`: 1,296 rows
  - `fact_nav`: 46,000 rows
  - `fact_transactions`: 32,778 rows
  - `fact_performance`: 40 rows
  - `fact_aum`: 90 rows
- Cleaned CSVs written to `data/processed/` and database `bluestock_mf.db` created.
- Committed and pushed Day 2 changes: commit message "Day 2: Cleaned data + SQLite DB loaded".

## Artifacts (Day 2)
- `day2_etl.py`
- `schema.sql`, `queries.sql`, `data_dictionary.md`
- `bluestock_mf.db`
- Cleaned CSVs in `data/processed/` (11 files including live NAVs)

## Data Quality & Findings
- Date parsing warnings encountered for mixed formats; ETL coerces where possible and logs warnings.
- Expense ratio outliers flagged (see `data/processed/07_scheme_performance_cleaned.csv`).
- `02_nav_history_cleaned.csv` forward-filled missing NAVs for non-trading days; manual review recommended for gaps.

## Next steps (recommended)
- Add notebooks with EDA and visualizations under `notebooks/`.
- Implement data tests to catch date parse failures, negative NAVs, and AMFI mismatches.
- Build dashboard prototype to visualize AUM, NAV trends, and SIP flows.

## Repo
- https://github.com/SandibJena/Capstone-ProjectI_Bluestocks
