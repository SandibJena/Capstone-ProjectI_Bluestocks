-- ============================================================
-- Mutual Fund Analytics - SQLite Star Schema
-- Bluestocks Data Analyst Internship
-- Author: Sandib Jena
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- Dimension Table: Fund Information
-- Stores metadata for every mutual fund scheme.
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code      INTEGER PRIMARY KEY NOT NULL,
    fund_house     TEXT NOT NULL,
    scheme_name    TEXT NOT NULL,
    category       TEXT NOT NULL,
    sub_category   TEXT NOT NULL,
    plan           TEXT,
    launch_date    TEXT
);

-- ============================================================
-- Dimension Table: Date
-- Common date dimension used by all fact tables.
-- Dates should be stored in ISO format (YYYY-MM-DD).
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date        TEXT PRIMARY KEY NOT NULL,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    iso_week    INTEGER NOT NULL
);

-- ============================================================
-- Fact Table: NAV History
-- Stores historical Net Asset Value (NAV) records.
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_nav (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code   INTEGER NOT NULL,
    date        TEXT NOT NULL,
    nav         REAL NOT NULL CHECK (nav > 0),

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date)
        REFERENCES dim_date(date)
);

-- ============================================================
-- Fact Table: Investor Transactions
-- Stores SIP, Lumpsum and Redemption transactions.
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_transactions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    amfi_code           INTEGER NOT NULL,
    transaction_date    TEXT NOT NULL,
    transaction_type    TEXT NOT NULL,
    amount_inr          REAL NOT NULL CHECK (amount_inr > 0),
    state               TEXT,
    city                TEXT,
    kyc_status          TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (transaction_date)
        REFERENCES dim_date(date)
);

-- ============================================================
-- Fact Table: Scheme Performance
-- Stores annual returns, expense ratio and AUM.
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_performance (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code           INTEGER NOT NULL,
    measurement_date    TEXT NOT NULL,

    return_1yr_pct      REAL,
    return_3yr_pct      REAL,
    return_5yr_pct      REAL,

    expense_ratio_pct   REAL
        CHECK (
            expense_ratio_pct IS NULL
            OR expense_ratio_pct BETWEEN 0.1 AND 2.5
        ),

    aum_crore           REAL
        CHECK (
            aum_crore IS NULL
            OR aum_crore >= 0
        ),

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (measurement_date)
        REFERENCES dim_date(date)
);

-- ============================================================
-- Fact Table: Assets Under Management (AUM)
-- Stores AUM statistics by fund house.
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_aum (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house      TEXT NOT NULL,
    date            TEXT NOT NULL,
    aum_crore       REAL NOT NULL CHECK (aum_crore >= 0),
    num_schemes     INTEGER NOT NULL CHECK (num_schemes >= 0),

    FOREIGN KEY (date)
        REFERENCES dim_date(date)
);

-- ============================================================
-- Helpful Indexes
-- Improves query performance for analytical workloads.
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_nav_amfi
ON fact_nav(amfi_code);

CREATE INDEX IF NOT EXISTS idx_nav_date
ON fact_nav(date);

CREATE INDEX IF NOT EXISTS idx_transaction_amfi
ON fact_transactions(amfi_code);

CREATE INDEX IF NOT EXISTS idx_transaction_date
ON fact_transactions(transaction_date);

CREATE INDEX IF NOT EXISTS idx_performance_amfi
ON fact_performance(amfi_code);

CREATE INDEX IF NOT EXISTS idx_performance_date
ON fact_performance(measurement_date);

CREATE INDEX IF NOT EXISTS idx_aum_date
ON fact_aum(date);