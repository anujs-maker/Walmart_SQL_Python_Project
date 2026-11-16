-- MySQL 8+ example. Replace the table intentionally for a repeatable demo load.
DROP TABLE IF EXISTS walmart;
CREATE TABLE walmart (
 invoice_id BIGINT PRIMARY KEY, branch VARCHAR(20), city VARCHAR(100), category VARCHAR(100),
 unit_price DECIMAL(12,2), quantity INT, date DATE, time TIME, payment_method VARCHAR(30),
 rating DECIMAL(4,2), profit_margin DECIMAL(6,4), total DECIMAL(14,2), profit DECIMAL(14,2)
);
-- Load the generated walmart_clean_data.csv with the database's secure import command.
