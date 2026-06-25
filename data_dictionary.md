# Data Dictionary

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
