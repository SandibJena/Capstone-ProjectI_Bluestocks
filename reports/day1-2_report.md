# Day 1–2 Report — Mutual Fund Analytics (Bluestocks)

**Summary**
- Completed Day 1: project scaffold, ingestion scripts, requirements, and initial data loads.
- Completed Day 2: cleaning, schema design, SQLite load, and analytical query set.

**Key Artifacts**
- **Ingestion script:** [data_ingestion.py](data_ingestion.py)
- **Live NAV fetch:** [live_nav_fetch.py](live_nav_fetch.py)
- **Day 2 ETL:** [day2_etl.py](day2_etl.py)
- **Cleaned data (processed):** [data/processed/](data/processed/)
- **SQLite DB:** [bluestock_mf.db](bluestock_mf.db)
- **Schema:** [schema.sql](schema.sql)
- **Queries:** [queries.sql](queries.sql)
- **Data dictionary:** [data_dictionary.md](data_dictionary.md)

**Data Quality & Findings**
- All `amfi_code` values in `01_fund_master.csv` were found in `02_nav_history.csv` (AMFI validation passed).
- Row counts loaded into SQLite:
  - **dim_fund:** 40 rows
  - **dim_date:** 1,296 rows
  - **fact_nav:** 46,000 rows
  - **fact_transactions:** 32,778 rows
  - **fact_performance:** 40 rows
  - **fact_aum:** 90 rows
- Noted anomalies:
  - `04_monthly_sip_inflows.csv` had missing `yoy_growth_pct` values (12 nulls).
  - Date parsing warnings occurred for some files (mixed formats); ETL coerces to ISO and may drop unparsable dates.
  - Expense ratio checks exist in the ETL; review `data/processed/07_scheme_performance_cleaned.csv` for flagged out-of-range values (<0.1% or >2.5%).

**Repro / How to run**
- Create venv and install:

```
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

- Run ingestion and Day 2 ETL:

```
python data_ingestion.py
python live_nav_fetch.py --codes 125497 119551 120503 118632 119092 120841
python day2_etl.py
```

**Next recommended steps**
- Add a notebook with exploratory analysis and visualisations under `notebooks/`.
- Build a simple dashboard (Plotly Dash / Streamlit) under `dashboard/` to surface AUM, NAV trends, and SIP flows.
- Add automated checks (unit tests or data tests) to validate date parsing, NAV > 0, and AMFI mapping.
- Review `07_scheme_performance` expense outliers and reconcile with source.

**Status**
- Day 1 and Day 2 tasks completed and pushed to the repository: https://github.com/SandibJena/Capstone-ProjectI_Bluestocks

---
Report generated: 2026-06-25
