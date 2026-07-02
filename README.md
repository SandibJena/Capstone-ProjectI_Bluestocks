# Mutual Fund Analytics – Bluestocks Fintech Capstone

A comprehensive Data Engineering and Analytics project developed as part of the **Bluestocks Data Analyst Internship**. This project demonstrates an end-to-end ETL workflow, data cleaning, database design, SQL analytics, and documentation using real-world mutual fund datasets.

---

# Table of Contents

- Project Overview
- Tech Stack
- Features
- Project Structure
- ETL Workflow
- Quick Start
- Day 1 Report
- Day 2 Report
- Future Enhancements
- Author
- License

---

# Project Overview

This project was developed as part of the **Bluestocks Data Analyst Internship**. It demonstrates an end-to-end data engineering and analytics workflow for mutual fund datasets.

The project includes:

- Data ingestion from multiple CSV datasets
- Live NAV integration using the MFAPI
- Data cleaning and validation
- SQLite Star Schema design
- ETL pipeline development
- Analytical SQL queries
- Documentation and reporting

The primary objective is to transform raw mutual fund datasets into a clean, analysis-ready database that can support financial analytics and dashboard development.

---

# Tech Stack

- Python
- Pandas
- NumPy
- SQLAlchemy
- SQLite
- Requests
- Matplotlib
- Seaborn
- Plotly
- Jupyter Notebook
- Git & GitHub

---

# Features

- Automated CSV data ingestion
- Live NAV API integration
- Data validation and quality checks
- ETL pipeline
- SQLite Star Schema
- Analytical SQL queries
- Processed datasets
- Technical documentation and reports

---

# Project Structure

```
Capstone-ProjectI_Bluestocks/
│
├── data/
│   ├── raw/                 # Original datasets and Live NAV JSON/CSV
│   └── processed/           # Cleaned datasets, summaries and reports
│
├── notebooks/              # Exploratory Data Analysis (EDA)
├── dashboard/              # Power BI / Tableau dashboards
├── reports/                # Internship reports
├── sql/                    # SQL schema and analytical queries
│
├── data_ingestion.py
├── live_nav_fetch.py
├── day2_etl.py
├── data_dictionary.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ETL Workflow

```text
Raw CSV Files
      │
      ▼
Data Ingestion
      │
      ▼
Data Cleaning
      │
      ▼
SQLite Database
      │
      ▼
SQL Analytics
      │
      ▼
Dashboard & Reports
```

---

# Quick Start

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Place the provided datasets

Copy all provided CSV datasets into:

```
data/raw/
```

or keep them in your **Downloads** folder.

### 4. Run Data Ingestion

```bash
python data_ingestion.py
```

### 5. Fetch Live NAV Data

```bash
python live_nav_fetch.py --codes 125497 119551 120503 118632 119092 120841
```

---

# Day 1 Report — Project Setup & Data Ingestion (ETL)

**Date:** 25 June 2026

## Objectives

- Create project folder structure
- Install required dependencies
- Create requirements.txt
- Load all provided datasets
- Inspect data (.shape, .head(), .dtypes)
- Implement Live NAV API integration
- Validate AMFI codes
- Initialize Git repository

## Actions Completed

- Created project folders:
  - data/raw
  - data/processed
  - notebooks
  - sql
  - dashboard
  - reports

- Added:
  - requirements.txt
  - .gitignore

- Installed required libraries:

  - pandas
  - numpy
  - matplotlib
  - seaborn
  - plotly
  - sqlalchemy
  - requests
  - scipy
  - jupyter

- Implemented `data_ingestion.py`

  - Automatically locates datasets
  - Prints dataset shape
  - Prints data types
  - Prints sample records
  - Detects missing values
  - Detects duplicate rows
  - Generates:
    - load_summary.txt
    - data_quality_summary.txt

- Implemented `live_nav_fetch.py`

  - Fetches NAV from MFAPI
  - Saves JSON response
  - Converts JSON to CSV

- Successfully loaded all 10 provided datasets.

- Verified AMFI Codes using Fund Master and NAV History datasets.

- Git Commit

```
Day 1: Data ingestion complete
```

---

## Day 1 Deliverables

- data_ingestion.py
- live_nav_fetch.py
- requirements.txt
- .gitignore
- README.md
- load_summary.txt
- data_quality_summary.txt

---

## Data Quality Notes

- Missing values detected in `yoy_growth_pct`.
- Mixed date formats were identified and safely handled during ingestion.

---

# Day 2 Report — Data Cleaning & SQLite Database Design

**Date:** 25 June 2026

## Objectives

- Clean raw datasets
- Design SQLite Star Schema
- Load cleaned datasets into SQLite
- Write analytical SQL queries
- Create Data Dictionary

---

## Actions Completed

Implemented `day2_etl.py` including:

### NAV History

- Date parsing
- Sorting
- Duplicate removal
- Forward filling missing NAV values
- NAV validation (>0)

### Investor Transactions

- Standardized transaction types
- Parsed dates
- Validated transaction amounts
- Standardized KYC status

### Scheme Performance

- Converted returns to numeric
- Flagged invalid values
- Validated Expense Ratio (0.1%–2.5%)

### Additional Cleaning

- AUM datasets
- Portfolio holdings
- Benchmark datasets

---

Generated:

- schema.sql
- queries.sql
- data_dictionary.md
- bluestock_mf.db

---

## Database Statistics

| Table | Rows |
|------|------:|
| dim_fund | 40 |
| dim_date | 1,296 |
| fact_nav | 46,000 |
| fact_transactions | 32,778 |
| fact_performance | 40 |
| fact_aum | 90 |

---

## Day 2 Deliverables

- day2_etl.py
- schema.sql
- queries.sql
- data_dictionary.md
- bluestock_mf.db
- Processed CSV datasets

---

## Data Quality Notes

- Mixed date formats successfully handled.
- Expense Ratio outliers flagged.
- Missing NAV values forward-filled for non-trading days.
- Manual verification recommended for extended missing periods.

---

# Future Enhancements

- Exploratory Data Analysis (EDA)
- Interactive visualizations
- Power BI Dashboard
- Tableau Dashboard
- Advanced Risk Metrics
- Portfolio Performance Analytics
- Automated Data Validation Tests

---

# Author

**Sandib Jena**

B.Tech – Computer Science & Engineering

Government College of Engineering, Kalahandi

**Role:** Data Analyst Intern

**GitHub Repository**

https://github.com/SandibJena/Capstone-ProjectI_Bluestocks

**GitHub Profile**

https://github.com/SandibJena

---

# License

This project was developed for educational purposes as part of the **Bluestocks Data Analyst Internship**.