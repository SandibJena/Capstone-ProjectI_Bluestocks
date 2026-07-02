-- 1. Top 5 funds by latest AUM

SELECT fund_house, SUM(aum_crore) as total_aum FROM fact_aum GROUP BY fund_house ORDER BY total_aum DESC LIMIT 5;

-- 2. Average NAV per month for each scheme

SELECT amfi_code, strftime('%Y-%m', date) as ym, AVG(nav) as avg_nav FROM fact_nav GROUP BY amfi_code, ym;

-- 3. SIP YoY growth (sum of SIP amounts by year)

SELECT strftime('%Y', transaction_date) as yr, SUM(amount_inr) as total_sip FROM fact_transactions WHERE transaction_type='SIP' GROUP BY yr ORDER BY yr;

-- 4. Transactions by state

SELECT state, COUNT(*) as tx_count, SUM(amount_inr) as total_amount FROM fact_transactions GROUP BY state ORDER BY total_amount DESC;

-- 5. Funds with expense_ratio < 1%

SELECT amfi_code, scheme_name, expense_ratio_pct FROM dim_fund JOIN fact_performance USING(amfi_code) WHERE expense_ratio_pct < 1.0;

-- 6. Top 5 schemes by average 3yr return

SELECT amfi_code, AVG(return_3yr_pct) as avg_3yr FROM fact_performance GROUP BY amfi_code ORDER BY avg_3yr DESC LIMIT 5;

-- 7. Monthly NAV volatility (std dev) for each scheme

SELECT amfi_code, strftime('%Y-%m', date) as ym, ROUND(STDDEV(nav),4) as nav_std FROM fact_nav GROUP BY amfi_code, ym;

-- 8. Redemption vs SIP count by year

SELECT strftime('%Y', transaction_date) as yr, transaction_type, COUNT(*) as cnt FROM fact_transactions WHERE transaction_type IN ('SIP','Redemption') GROUP BY yr, transaction_type;

-- 9. Schemes with highest max drawdown (from scheme_performance)

SELECT amfi_code, scheme_name, max_drawdown_pct FROM fact_performance ORDER BY max_drawdown_pct ASC LIMIT 10;

-- 10. Number of schemes per category

SELECT category, COUNT(DISTINCT amfi_code) as num_schemes FROM dim_fund GROUP BY category;