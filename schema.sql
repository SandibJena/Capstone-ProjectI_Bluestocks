-- Star schema for Mutual Fund Analytics

CREATE TABLE IF NOT EXISTS dim_fund (
  amfi_code INTEGER PRIMARY KEY,
  fund_house TEXT,
  scheme_name TEXT,
  category TEXT,
  sub_category TEXT,
  plan TEXT,
  launch_date TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
  date TEXT PRIMARY KEY,
  year INTEGER,
  month INTEGER,
  day INTEGER,
  iso_week INTEGER
);

CREATE TABLE IF NOT EXISTS fact_nav (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amfi_code INTEGER,
  date TEXT,
  nav REAL,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
  FOREIGN KEY(date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  investor_id TEXT,
  amfi_code INTEGER,
  transaction_date TEXT,
  transaction_type TEXT,
  amount_inr REAL,
  state TEXT,
  city TEXT,
  kyc_status TEXT,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
  FOREIGN KEY(transaction_date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_performance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  amfi_code INTEGER,
  measurement_date TEXT,
  return_1yr_pct REAL,
  return_3yr_pct REAL,
  return_5yr_pct REAL,
  expense_ratio_pct REAL,
  aum_crore INTEGER,
  FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
  FOREIGN KEY(measurement_date) REFERENCES dim_date(date)
);

CREATE TABLE IF NOT EXISTS fact_aum (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fund_house TEXT,
  date TEXT,
  aum_crore REAL,
  num_schemes INTEGER,
  FOREIGN KEY(date) REFERENCES dim_date(date)
);
