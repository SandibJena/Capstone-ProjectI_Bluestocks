# Mutual Fund Analytics – Data Dictionary

## Overview

This document describes the datasets, database tables, column definitions, data types, business meanings, and source files used in the Mutual Fund Analytics project.

The project follows a **Star Schema** design consisting of two dimension tables and four fact tables.

---

# Database Schema

```
                    dim_fund
                       │
                       │
                  fact_nav
                       │
                       │
                    dim_date
                       │
      ┌────────────────┼────────────────┐
      │                │                │
fact_transactions  fact_performance  fact_aum
```

---

# Dimension Tables

## 1. dim_fund

**Source:** `01_fund_master.csv`

Stores metadata for all mutual fund schemes.

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | Unique AMFI Scheme Code (Primary Key) |
| fund_house | TEXT | Name of the Asset Management Company (AMC) |
| scheme_name | TEXT | Official Mutual Fund Scheme Name |
| category | TEXT | Primary Fund Category (Equity, Debt, Hybrid, etc.) |
| sub_category | TEXT | Detailed Category (Large Cap, Mid Cap, Small Cap, etc.) |
| plan | TEXT | Direct or Regular Plan |
| launch_date | TEXT | Original Scheme Launch Date |

---

## 2. dim_date

**Source:** Derived during ETL

Stores all calendar dates used across fact tables.

| Column | Data Type | Description |
|---------|-----------|-------------|
| date | TEXT | Date (YYYY-MM-DD) – Primary Key |
| year | INTEGER | Calendar Year |
| month | INTEGER | Month Number |
| day | INTEGER | Day of Month |
| iso_week | INTEGER | ISO Week Number |

---

# Fact Tables

## 3. fact_nav

**Source:** `02_nav_history.csv`

Stores historical Net Asset Value (NAV) for every scheme.

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | Foreign Key → dim_fund |
| date | TEXT | Foreign Key → dim_date |
| nav | REAL | Net Asset Value of the scheme |

---

## 4. fact_transactions

**Source:** `08_investor_transactions.csv`

Stores investor transaction records.

| Column | Data Type | Description |
|---------|-----------|-------------|
| investor_id | TEXT | Unique Investor Identifier |
| amfi_code | INTEGER | Foreign Key → dim_fund |
| transaction_date | TEXT | Foreign Key → dim_date |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption |
| amount_inr | REAL | Transaction Amount (INR) |
| state | TEXT | Investor State |
| city | TEXT | Investor City |
| kyc_status | TEXT | KYC Verification Status |

---

## 5. fact_performance

**Source:** `07_scheme_performance.csv`

Stores scheme performance metrics.

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | Foreign Key → dim_fund |
| measurement_date | TEXT | Performance Measurement Date |
| return_1yr_pct | REAL | One-Year Return (%) |
| return_3yr_pct | REAL | Three-Year Return (%) |
| return_5yr_pct | REAL | Five-Year Return (%) |
| expense_ratio_pct | REAL | Expense Ratio (%) |
| aum_crore | REAL | Assets Under Management (Crore INR) |

---

## 6. fact_aum

**Source:** `03_aum_by_fund_house.csv`

Stores Assets Under Management information.

| Column | Data Type | Description |
|---------|-----------|-------------|
| fund_house | TEXT | Fund House Name |
| date | TEXT | Reporting Date |
| aum_crore | REAL | Total Assets Under Management (Crore INR) |
| num_schemes | INTEGER | Number of Schemes Managed |

---

# Data Sources

| Dataset | Source |
|----------|--------|
| Fund Master | 01_fund_master.csv |
| NAV History | 02_nav_history.csv |
| AUM by Fund House | 03_aum_by_fund_house.csv |
| Monthly SIP Inflows | 04_monthly_sip_inflows.csv |
| Category Inflows | 05_category_inflows.csv |
| Industry Folio Count | 06_industry_folio_count.csv |
| Scheme Performance | 07_scheme_performance.csv |
| Investor Transactions | 08_investor_transactions.csv |
| Portfolio Holdings | 09_portfolio_holdings.csv |
| Benchmark Indices | 10_benchmark_indices.csv |
| Live NAV | https://api.mfapi.in |

---

# Business Definitions

### NAV (Net Asset Value)

The per-unit market value of a mutual fund.

---

### AUM (Assets Under Management)

The total market value of investments managed by a fund house.

---

### AMFI Code

A unique identifier assigned by the Association of Mutual Funds in India to every mutual fund scheme.

---

### Expense Ratio

The annual fee charged by a fund house for managing a mutual fund.

---

### SIP (Systematic Investment Plan)

A disciplined investment method where investors contribute a fixed amount at regular intervals.

---

### KYC

Know Your Customer verification status required before investing.

---

# Author

**Project:** Mutual Fund Analytics

**Intern:** Sandib Jena

**Organization:** Bluestocks Data Analyst Internship