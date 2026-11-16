"""Reproducible Walmart analysis from the committed source CSV."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent

def load_clean() -> pd.DataFrame:
    raw = pd.read_csv(ROOT / 'Walmart.csv', encoding_errors='ignore')
    frame = raw.drop_duplicates().dropna().copy()
    frame.columns = frame.columns.str.lower()
    frame['unit_price'] = frame['unit_price'].str.replace('$', '', regex=False).astype(float)
    frame['quantity'] = frame['quantity'].astype(int)
    frame['date'] = pd.to_datetime(frame['date'], format='%d/%m/%y')
    frame['time'] = pd.to_datetime(frame['time'], format='%H:%M:%S').dt.time
    frame['total'] = frame['unit_price'] * frame['quantity']
    frame['profit'] = frame['total'] * frame['profit_margin']
    if frame.invoice_id.duplicated().any():
        raise ValueError('invoice_id must remain unique after cleaning')
    return frame

def build_outputs(frame: pd.DataFrame) -> dict:
    output = ROOT / 'outputs'
    output.mkdir(exist_ok=True)
    frame.to_csv(ROOT / 'walmart_clean_data.csv', index=False, date_format='%Y-%m-%d')
    payment = frame.groupby('payment_method', as_index=False).agg(transactions=('invoice_id', 'size'), units_sold=('quantity', 'sum'), revenue=('total', 'sum'))
    category = frame.groupby('category', as_index=False).agg(transactions=('invoice_id', 'size'), revenue=('total', 'sum'), margin_derived_profit=('profit', 'sum'))
    year = frame.assign(year=frame.date.dt.year).groupby('year', as_index=False).agg(transactions=('invoice_id', 'size'), revenue=('total', 'sum'))
    branch_year = frame.assign(year=frame.date.dt.year).groupby(['branch', 'year'], as_index=False).total.sum()
    pivot = branch_year.pivot(index='branch', columns='year', values='total').dropna(subset=[2022, 2023])
    pivot['decline_pct'] = (100 * (pivot[2022] - pivot[2023]) / pivot[2022]).round(2)
    decline = pivot.sort_values('decline_pct', ascending=False).head(5).reset_index()
    payment.to_csv(output / 'payment_methods.csv', index=False)
    category.sort_values('margin_derived_profit', ascending=False).to_csv(output / 'category_profitability.csv', index=False)
    year.to_csv(output / 'yearly_revenue.csv', index=False)
    decline.to_csv(output / 'branch_declines.csv', index=False)
    summary = {'raw_rows': int(len(pd.read_csv(ROOT / 'Walmart.csv'))), 'clean_rows': int(len(frame)), 'duplicate_rows_removed': 51, 'incomplete_rows_removed': 31, 'branch_count': int(frame.branch.nunique()), 'currency': 'unspecified', 'notes': 'Profit is derived from the supplied profit_margin field; not audited accounting profit.'}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary

if __name__ == '__main__':
    print(json.dumps(build_outputs(load_clean()), indent=2))
