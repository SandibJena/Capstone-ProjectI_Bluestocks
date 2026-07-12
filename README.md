# Mutual Fund Analytics – Bluestocks Data Analyst Internship Capstone

An end-to-end **Data Engineering, Financial Analytics, and Business Intelligence** project developed during the **Bluestocks Data Analyst Internship**.

This project demonstrates a complete mutual fund analytics pipeline, covering data ingestion, ETL, data cleaning, SQL database design, exploratory data analysis (EDA), financial performance analytics, benchmark comparison, and dashboard-ready outputs.

---

## Project Objectives

- Build an end-to-end ETL pipeline for mutual fund datasets.
- Design a relational SQLite database using a Star Schema.
- Perform Exploratory Data Analysis (EDA) with business insights.
- Calculate industry-standard financial performance metrics.
- Compare mutual funds with benchmark indices.
- Generate reports, visualizations, and dashboard-ready datasets.

---

## Tech Stack

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

## Project Features

### Task 1 – Project Setup & Data Ingestion

- Professional project structure
- CSV data ingestion
- Live NAV API integration
- Data validation
- Data quality reports

### Task 2 – Data Cleaning & SQL Database Design

- Data cleaning and preprocessing
- SQLite Star Schema implementation
- SQL analytics
- Data dictionary
- Database creation

### Task 3 – Exploratory Data Analysis (EDA)

- NAV Trend Analysis
- AUM Growth Analysis
- Monthly SIP Trend
- Category-wise Inflows
- Folio Growth Analysis
- Investor Demographics
- Geographic Distribution
- Sector Allocation
- Correlation Analysis
- Business Insights

### Task 4 – Performance Analytics

- Daily Returns
- CAGR (1-Year, 3-Year & 5-Year)
- Sharpe Ratio
- Sortino Ratio
- Alpha & Beta
- Maximum Drawdown
- Composite Fund Scorecard
- Tracking Error
- Benchmark Comparison

---

# Project Structure

```text
Capstone-ProjectI_Bluestocks/
│
├── dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── docs/
│
├── notebooks/
│   ├── Project_Setup_Data_Ingestion.ipynb
│   ├── Data_Cleaning_SQL_Design.ipynb
│   ├── EDA_Analysis.ipynb
│   └── Performance_Analytics.ipynb
│
├── reports/
│   ├── charts/
│   ├── tables/
│   ├── Project_Setup_Data_Ingestion.md
│   ├── Data_Cleaning_SQL_Design.md
│   ├── Exploratory_Data_Analysis.md
│   ├── Performance_Analytics.md
│   └── Final_Report.md
│
├── scripts/
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# Workflow

```text
Raw Data
      │
      ▼
Project Setup & Data Ingestion (ETL)
      │
      ▼
Data Cleaning & Validation
      │
      ▼
SQLite Database (Star Schema)
      │
      ▼
Exploratory Data Analysis (EDA)
      │
      ▼
Performance Analytics
      │
      ▼
Benchmark Comparison
      │
      ▼
Reports & Dashboard-ready Outputs
```

---

# Database Statistics

| Table | Rows |
|-------|-----:|
| dim_fund | 40 |
| dim_date | 1,296 |
| fact_nav | 46,000 |
| fact_transactions | 32,778 |
| fact_performance | 40 |
| fact_aum | 90 |

---

# Generated Outputs

## Charts

- NAV Trend
- AUM Growth
- Monthly SIP Trend
- Category Heatmap
- Folio Growth
- Age Distribution
- Gender Distribution
- State-wise SIP Distribution
- Sector Allocation
- NAV Correlation Matrix
- Benchmark Comparison
- Additional EDA Visualizations

---

## CSV Reports

- CAGR Comparison
- Sharpe Ratio
- Sortino Ratio
- Alpha & Beta
- Maximum Drawdown
- Fund Scorecard
- Tracking Error

---

# Key Highlights

- Successfully processed **10 mutual fund datasets**.
- Designed a **SQLite Star Schema** database.
- Generated **12+ business visualizations**.
- Calculated **industry-standard financial performance metrics**.
- Developed a **composite Fund Scorecard** for ranking mutual funds.
- Compared top-performing funds with **NIFTY50** and **NIFTY100** benchmark indices.
- Generated dashboard-ready reports and analytical datasets.

---

# Future Enhancements

- Interactive Power BI Dashboard
- Tableau Dashboard
- Portfolio Optimization
- Risk Forecasting
- Machine Learning-based Return Prediction
- Mutual Fund Recommendation System

---

# Author

**Sandib Jena**

B.Tech – Computer Science & Engineering

Government College of Engineering, Kalahandi

GitHub Repository:

https://github.com/SandibJena/Capstone-ProjectI_Bluestocks

LinkedIn:

https://www.linkedin.com/in/sandib-jena

---

# License

This project was developed for educational purposes as part of the **Bluestocks Data Analyst Internship**.