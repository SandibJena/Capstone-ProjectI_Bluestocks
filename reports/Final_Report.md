# Final Report — Mutual Fund Analytics (Bluestocks Data Analyst Internship)

## Project Overview

This project was completed as part of the **Bluestocks Data Analyst Internship**. It demonstrates a complete mutual fund analytics pipeline, beginning with raw data ingestion and ending with advanced financial performance analysis.

The project includes:

- Data Ingestion (ETL)
- Data Cleaning & Validation
- SQLite Database Design
- Exploratory Data Analysis (EDA)
- Performance Analytics
- Benchmark Comparison
- Business Reporting

---

# Task 1 — Project Setup & Data Ingestion

## Objectives Completed

- Created a professional project structure.
- Loaded and validated 10 mutual fund datasets.
- Integrated Live NAV data using MF API.
- Performed AMFI code validation.
- Generated data quality reports.

### Deliverables

- Project setup notebook
- Data ingestion script
- Live NAV fetch script
- Raw datasets
- Processed datasets

---

# Task 2 — Data Cleaning & SQL Database Design

## Objectives Completed

- Cleaned and standardized all datasets.
- Handled missing values and inconsistent formats.
- Designed SQLite Star Schema.
- Loaded cleaned datasets into SQLite.
- Created SQL analytical queries.
- Prepared data dictionary.

## Database Statistics

| Table | Rows |
|-------|------:|
| dim_fund | 40 |
| dim_date | 1,296 |
| fact_nav | 46,000 |
| fact_transactions | 32,778 |
| fact_performance | 40 |
| fact_aum | 90 |

---

# Task 3 — Exploratory Data Analysis (EDA)

## Analysis Performed

- NAV Trend Analysis
- AUM Growth Analysis
- Monthly SIP Trend
- Category-wise Inflows
- Folio Growth
- Investor Demographics
- Gender Distribution
- State-wise SIP Distribution
- Portfolio Sector Allocation
- Correlation Analysis
- Business Insights

## Outputs Generated

### Charts

- NAV Trend
- AUM Growth
- Monthly SIP Trend
- Category Heatmap
- Folio Growth
- Age Distribution
- Gender Distribution
- State Distribution
- Sector Allocation
- Correlation Matrix
- SIP Distribution
- Additional EDA Charts

---

# Task 4 — Performance Analytics

## Financial Metrics Calculated

- Daily Returns
- CAGR (1-Year, 3-Year, 5-Year)
- Sharpe Ratio
- Sortino Ratio
- Alpha & Beta
- Maximum Drawdown
- Fund Scorecard
- Tracking Error

## Benchmark Analysis

Compared the Top 5 Mutual Funds with:

- NIFTY50
- NIFTY100

Generated benchmark comparison visualization and tracking error analysis.

## Outputs Generated

### CSV Reports

- cagr_comparison.csv
- sharpe_ratio.csv
- sortino_ratio.csv
- alpha_beta.csv
- maximum_drawdown.csv
- fund_scorecard.csv
- tracking_error.csv

### Charts

- benchmark_comparison.png

---

# Data Quality Summary

- All AMFI codes successfully validated.
- Cleaned datasets exported successfully.
- SQLite database populated without errors.
- Performance metrics computed successfully.
- Benchmark comparison completed successfully.

---

# Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- SQLite
- SQLAlchemy
- Matplotlib
- Seaborn
- Plotly
- Jupyter Notebook
- Git & GitHub

---

# Project Structure

```text
Capstone-ProjectI_Bluestocks/
│
├── data/
├── database/
├── dashboard/
├── docs/
├── notebooks/
├── reports/
│   ├── charts/
│   ├── tables/
│   ├── Project_Setup_Data_Ingestion.md
│   ├── Data_Cleaning_SQL_Design.md
│   ├── Exploratory_Data_Analysis.md
│   ├── Performance_Analytics.md
│   └── Final_Report.md
├── scripts/
├── sql/
├── README.md
└── requirements.txt
```

---

# Key Achievements

- Successfully implemented a complete ETL pipeline.
- Designed a relational SQLite database using a Star Schema.
- Conducted comprehensive exploratory data analysis with business insights.
- Calculated industry-standard financial performance metrics.
- Developed a composite Fund Scorecard for ranking mutual funds.
- Compared top-performing funds with benchmark indices.
- Generated dashboard-ready datasets, charts, and analytical reports.

---

# Future Enhancements

- Interactive Power BI Dashboard
- Tableau Dashboard
- Portfolio Optimization
- Machine Learning-based Return Prediction
- Mutual Fund Recommendation System
- Automated Data Validation Pipeline

---

# Repository

GitHub Repository:

**https://github.com/SandibJena/Capstone-ProjectI_Bluestocks**

---

# Author

**Sandib Jena**

B.Tech – Computer Science & Engineering

Government College of Engineering, Kalahandi

---

# Conclusion

The Mutual Fund Analytics project successfully demonstrates an end-to-end data analytics workflow, from raw data ingestion and database design to exploratory analysis and advanced financial performance evaluation.

The project integrates ETL processes, SQL, Python-based analytics, financial metric computation, visualization, and reporting into a structured solution suitable for business intelligence and investment analysis.

All assigned internship objectives for the completed tasks have been successfully achieved.

---

**Report Generated:** July 2026