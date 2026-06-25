Day 1 — Data Ingestion

Contents:
- `data_ingestion.py` : loads provided CSVs, prints shapes/dtypes/head and writes a data quality summary to `data/processed/`.
- `live_nav_fetch.py` : fetches NAVs from mfapi.in for provided AMFI codes and saves JSON/CSV to `data/raw/`.

Quick start

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

4. Fetch live NAVs (example):

```bash
python live_nav_fetch.py --codes 125497 119551 120503 118632 119092 120841
```

Git

Initialize and push to GitHub (replace `<remote-url>`):

```bash
git init
git add .
git commit -m "Day 1: Data ingestion complete"
git remote add origin <remote-url>
git push -u origin main
```
