# Walmart transaction analysis

This is a reproducible SQL/Pandas analysis of the committed Walmart sales sample. It is
portfolio data, not evidence of Walmart employment or actual branch performance.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python analysis.py
```

`analysis.py` reads `Walmart.csv`, removes duplicate and incomplete records, parses the
dollar-prefixed prices and dates, derives transaction value and margin-derived profit, and
writes `walmart_clean_data.csv` plus four result tables and `summary.json` under `outputs/`.
Currency is unspecified, and `profit` uses the source's supplied `profit_margin` field.

## Verified current sample

- 10,051 raw rows → 9,969 clean rows (51 duplicates and 31 incomplete rows removed).
- 100 branches.
- Credit card is the most frequent payment method: 4,256 transactions (42.69%).
- Fashion accessories and Home and lifestyle together represent 80.91% of derived transaction value.
- The largest 2022→2023 branch decline in this sample is WALM045 (−62.62%). This is a
  descriptive sample result; it does not establish a real Walmart branch trend or cause.

Three categories appear only in 2019 in the committed sample, so cross-year category totals
are not like-for-like. See `outputs/` for computed tables.

## SQL

`MySQL Queries.sql` and `PSQL Queries.sql` retain business-question examples. `sql_load.sql`
shows an idempotent MySQL demo table definition. Database execution is NOT VERIFIED without a
local server; the Pandas analysis is the supported reproducible path.

The original notebook and visual assets remain for reference. The supported clean run is the
script above, which avoids hidden notebook state and machine-specific credentials.
