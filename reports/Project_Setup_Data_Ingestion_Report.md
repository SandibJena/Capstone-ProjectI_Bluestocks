# Day 1 Report — Mutual Fund Analytics (Bluestocks)

**Date:** 2026-06-25

## Objectives
- Project scaffold and folder structure
- Install dependencies and create `requirements.txt`
- Load provided CSV datasets and inspect shapes/dtypes/head
- Implement ingestion and live NAV fetch scripts
- Validate AMFI codes
- Initialize Git and push Day 1 commit

## Actions Completed
- Created folders: `data/raw`, `data/processed`, `notebooks/`, `sql/`, `dashboard/`, `reports/`.
- Added `.gitignore` and `requirements.txt` (pandas, numpy, matplotlib, seaborn, plotly, sqlalchemy, requests, scipy, jupyter).
- Implemented `data_ingestion.py` to locate CSVs (data/raw, Downloads, workspace root), print `.shape`, `.dtypes`, `.head()`, detect basic anomalies, and write `data/processed/load_summary.txt` and `data/processed/data_quality_summary.txt`.
- Implemented `live_nav_fetch.py` to fetch NAV JSON from `https://api.mfapi.in/mf/<AMFI>` and save JSON+CSV to `data/raw/`.
- Ran `data_ingestion.py` — all 10 provided CSVs loaded successfully.
- AMFI validation: All AMFI codes in `01_fund_master.csv` were present in `02_nav_history.csv` sample.
- Initialized Git and made commit: "Day 1: Data ingestion complete".

## Artifacts (Day 1)
- `data_ingestion.py`
- `live_nav_fetch.py`
- `requirements.txt`, `.gitignore`, `README.md`
- `data/processed/load_summary.txt` and `data/processed/data_quality_summary.txt`
- Git commit pushed to: https://github.com/SandibJena/Capstone-ProjectI_Bluestocks

## Notes / Data Quality
- Observed missing `yoy_growth_pct` in `04_monthly_sip_inflows.csv`.
- Some CSVs had mixed date formats; ingestion coerces dates where possible.

## Next steps (recommended)
- Run live NAV fetch for key schemes (implemented and executed in Day 2).
- Proceed to Day 2: data cleaning and database loading.
