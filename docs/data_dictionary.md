# Data Dictionary

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
