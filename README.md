# Mutual Fund Analytics -- Bluestocks Fintech Capstone

An end-to-end **Data Engineering and Analytics** project developed
during the **Bluestocks Data Analyst Internship**. It covers data
ingestion, ETL, data cleaning, SQL database design, exploratory data
analysis (EDA), and dashboard-ready datasets.

------------------------------------------------------------------------

## Tech Stack

Python • Pandas • NumPy • SQLite • SQLAlchemy • Plotly • Matplotlib •
Seaborn • Jupyter • Git

------------------------------------------------------------------------

## Features

-   CSV data ingestion & Live NAV integration
-   ETL pipeline with data validation
-   SQLite Star Schema
-   SQL analytics
-   Exploratory Data Analysis (EDA)
-   Dashboard-ready datasets

------------------------------------------------------------------------

## Project Structure

``` text
Capstone-ProjectI_Bluestocks/
├── data/
├── notebooks/
├── reports/
├── scripts/
├── sql/
├── dashboard/
├── database/
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

## Workflow

``` text
Raw Data → Data Ingestion → Data Cleaning → SQLite → EDA → Dashboard
```

------------------------------------------------------------------------

## Project Summary

### Day 1 -- Project Setup & Data Ingestion

-   Created project structure
-   Loaded and validated 10 datasets
-   Integrated Live NAV API
-   Generated data quality reports

### Day 2 -- Data Cleaning & Database Design

-   Cleaned datasets
-   Designed SQLite Star Schema
-   Loaded data into SQLite
-   Generated SQL queries and data dictionary

**Database Statistics**

  Table                   Rows
  ------------------- --------
  dim_fund                  40
  dim_date               1,296
  fact_nav              46,000
  fact_transactions     32,778
  fact_performance          40
  fact_aum                  90

### Day 3 -- Exploratory Data Analysis

Completed: - 12 visualizations - Business insights - EDA notebook -
Exported PNG charts

**Highlights** - Strong NAV growth in 2023 - SBI MF reached \~₹12.5 lakh
crore AUM - SIP inflows peaked at ₹31,002 crore (Dec 2025) - Retail
investor participation continued to grow

------------------------------------------------------------------------

## Future Work

-   Power BI Dashboard
-   Tableau Dashboard
-   Predictive Analytics
-   Portfolio Risk Analysis

------------------------------------------------------------------------

## Author

**Sandib Jena**\
B.Tech -- Computer Science & Engineering\
Government College of Engineering, Kalahandi

GitHub: https://github.com/SandibJena/Capstone-ProjectI_Bluestocks

------------------------------------------------------------------------

## License

Developed for educational purposes as part of the Bluestocks Data
Analyst Internship.
