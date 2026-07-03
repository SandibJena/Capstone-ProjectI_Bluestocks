-- 1. Top 5 funds by latest AUM

SELECT fund_house, SUM(aum_crore) AS total_aum FROM fact_aum GROUP BY fund_house ORDER BY total_aum DESC LIMIT 5;

-- 2. Average NAV per month for each scheme

SELECT amfi_code, strftime('%Y-%m', date) AS ym, AVG(nav) AS avg_nav FROM fact_nav GROUP BY amfi_code, ym;

-- 3. SIP YoY Growth

SELECT strftime('%Y', transaction_date) AS yr, SUM(amount_inr) AS total_sip FROM fact_transactions WHERE transaction_type='SIP' GROUP BY yr ORDER BY yr;

-- 4. Transactions by State

SELECT state, COUNT(*) AS tx_count, SUM(amount_inr) AS total_amount FROM fact_transactions GROUP BY state ORDER BY total_amount DESC;

-- 5. Funds with Expense Ratio below 1%

SELECT amfi_code, scheme_name, expense_ratio_pct FROM dim_fund JOIN fact_performance USING(amfi_code) WHERE expense_ratio_pct < 1.0;

-- 6. Top 5 Schemes by Average 3-Year Return

SELECT amfi_code, AVG(return_3yr_pct) AS avg_3yr FROM fact_performance GROUP BY amfi_code ORDER BY avg_3yr DESC LIMIT 5;

-- 7. Monthly NAV Volatility

SELECT amfi_code, strftime('%Y-%m', date) AS ym, ROUND(STDDEV(nav), 4) AS nav_std FROM fact_nav GROUP BY amfi_code, ym;

-- 8. Redemption vs SIP Count

SELECT strftime('%Y', transaction_date) AS yr, transaction_type, COUNT(*) AS cnt FROM fact_transactions WHERE transaction_type IN ('SIP','Redemption') GROUP BY yr, transaction_type;

-- 9. Schemes with Highest Drawdown

SELECT amfi_code, scheme_name, max_drawdown_pct FROM fact_performance ORDER BY max_drawdown_pct ASC LIMIT 10;

-- 10. Number of Schemes per Category

SELECT category, COUNT(DISTINCT amfi_code) AS num_schemes FROM dim_fund GROUP BY category;