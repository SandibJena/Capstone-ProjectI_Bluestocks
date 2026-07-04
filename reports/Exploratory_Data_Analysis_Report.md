# Day 3 Report — Exploratory Data Analysis (EDA) (Bluestocks)

**Date:** 2026-07-03

## Objectives
- Perform Exploratory Data Analysis (EDA) on the cleaned mutual fund datasets.
- Generate interactive and static visualizations to identify market trends, investor behavior, and portfolio insights.
- Export all charts as PNG files for reporting.
- Document key business insights derived from the analysis.

## Actions Completed
- Created `EDA_Analysis.ipynb` containing complete exploratory data analysis.
- Loaded all cleaned datasets from `data/processed/` into the notebook.
- Performed data validation and dataset overview before visualization.
- Created the following visualizations:
  - Daily NAV Trend Analysis (2022–2026) using Plotly with highlighted 2023 Bull Run and 2024 Market Correction.
  - Assets Under Management (AUM) Growth by Fund House (2022–2025) using Seaborn.
  - Monthly SIP Inflow Trend (2022–2025) using Plotly with annotation for the record ₹31,002 crore SIP inflow.
  - Category-wise Net Inflow Heatmap using Seaborn.
  - Investor Age Group Distribution Pie Chart.
  - Gender Distribution Pie Chart.
  - SIP Amount Distribution by Age Group (Box Plot).
  - State-wise SIP Investment Horizontal Bar Chart.
  - T30 vs B30 City Tier Distribution Pie Chart.
  - Industry Folio Growth Line Chart.
  - NAV Return Correlation Matrix for selected mutual fund schemes.
  - Sector Allocation Donut Chart using aggregated portfolio holdings.
- Exported all visualizations as high-resolution PNG images into `reports/charts/`.
- Documented business insights after every visualization.
- Added an Executive Summary containing 10 key analytical findings.
- Verified that the notebook executes successfully from start to finish.

## Visualizations Generated
- NAV Trend Analysis
- AUM Growth by Fund House
- Monthly SIP Inflow Trend
- Category Inflow Heatmap
- Age Group Distribution
- Gender Distribution
- SIP Amount Box Plot
- State-wise SIP Distribution
- T30 vs B30 Distribution
- Mutual Fund Folio Growth
- NAV Return Correlation Matrix
- Sector Allocation Donut Chart

## Key Business Findings
- Most mutual fund schemes recorded sustained NAV growth during the 2023 market rally.
- Market corrections during 2024 temporarily impacted NAV performance across several schemes.
- SBI Mutual Fund maintained industry leadership with approximately ₹12.5 lakh crore AUM.
- Monthly SIP inflows steadily increased, reaching a record ₹31,002 crore in December 2025.
- Flexi Cap, Mid Cap, and Large & Mid Cap categories consistently attracted strong investor inflows.
- Investors aged 26–45 years accounted for the largest share of SIP investments.
- Tier-30 cities contributed the majority of SIP investments, while Beyond-30 cities continued to show increasing participation.
- Mutual fund folios experienced significant growth, indicating expanding retail investor participation.
- Daily returns of large-cap funds showed strong positive correlations.
- Banking, Financial Services, Information Technology, and Pharma represented the largest sector allocations across equity mutual funds.

## Artifacts (Day 3)
- `EDA_Analysis.ipynb`
- Exported visualization charts in `reports/charts/`
  - `nav_trend.png`
  - `aum_growth.png`
  - `monthly_sip_trend.png`
  - `category_heatmap.png`
  - `age_distribution_pie.png`
  - `gender_distribution.png`
  - `sip_amount_boxplot.png`
  - `state_sip_distribution.png`
  - `t30_b30_distribution.png`
  - `folio_growth.png`
  - `nav_correlation_matrix.png`
  - `sector_allocation.png`

## Data Quality & Findings
- Verified consistency of all cleaned datasets before visualization.
- Converted date columns into appropriate datetime formats for time-series analysis.
- Aggregated portfolio holdings and investor transactions to generate meaningful business insights.
- Validated visualization outputs before exporting high-resolution PNG files.
- Successfully exported all charts for reporting without data loss.

## Next Steps (Recommended)
- Develop an interactive Power BI dashboard using the cleaned datasets.
- Build KPI cards for AUM, SIP inflows, folio growth, and investor statistics.
- Add interactive filters for fund house, category, scheme, and investment period.
- Publish dashboard screenshots and documentation for final internship submission.

## Repository
- [https://github.com/SandibJena/Capstone-ProjectI_Bluestocks]