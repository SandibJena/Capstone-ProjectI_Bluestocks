-- ==========================================================
-- Mutual Fund Analytics
-- Analytical SQL Queries
-- Bluestocks Data Analyst Internship
-- ==========================================================

-- 1. Top 5 Fund Houses by Total AUM

SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

------------------------------------------------------------

-- 2. Average Monthly NAV for Each Scheme

SELECT
    amfi_code,
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

------------------------------------------------------------

-- 3. SIP Investment Growth by Year

SELECT
    strftime('%Y', transaction_date) AS year,
    SUM(amount_inr) AS total_sip
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;

------------------------------------------------------------

-- 4. Transactions by State

SELECT
    state,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

------------------------------------------------------------

-- 5. Funds with Expense Ratio below 1%

SELECT
    fp.amfi_code,
    df.scheme_name,
    fp.expense_ratio_pct
FROM fact_performance fp
JOIN dim_fund df
ON fp.amfi_code = df.amfi_code
WHERE fp.expense_ratio_pct < 1
ORDER BY fp.expense_ratio_pct;

------------------------------------------------------------

-- 6. Top 5 Funds by Average 3-Year Return

SELECT
    amfi_code,
    ROUND(AVG(return_3yr_pct), 2) AS avg_return_3yr
FROM fact_performance
GROUP BY amfi_code
ORDER BY avg_return_3yr DESC
LIMIT 5;

------------------------------------------------------------

-- 7. Monthly NAV Range (Volatility Approximation)

SELECT
    amfi_code,
    strftime('%Y-%m', date) AS month,
    ROUND(MAX(nav) - MIN(nav), 4) AS nav_range
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY month;

------------------------------------------------------------

-- 8. SIP vs Redemption Transactions by Year

SELECT
    strftime('%Y', transaction_date) AS year,
    transaction_type,
    COUNT(*) AS transaction_count
FROM fact_transactions
WHERE transaction_type IN ('SIP', 'Redemption')
GROUP BY year, transaction_type
ORDER BY year;

------------------------------------------------------------

-- 9. Top 10 Funds by 5-Year Return

SELECT
    fp.amfi_code,
    df.scheme_name,
    fp.return_5yr_pct
FROM fact_performance fp
JOIN dim_fund df
ON fp.amfi_code = df.amfi_code
ORDER BY fp.return_5yr_pct DESC
LIMIT 10;

------------------------------------------------------------

-- 10. Number of Schemes in Each Category

SELECT
    category,
    COUNT(DISTINCT amfi_code) AS number_of_schemes
FROM dim_fund
GROUP BY category
ORDER BY number_of_schemes DESC;