# Milestone 2: Python Pipeline

**Team 5**: Olivia Donoghue, Lily Powell

## How to Run

Instructions to run the pipeline from a fresh clone:

```bash
#1. Clone the repository
git clone https://github.com/{username}/wvu-ieng-331-m2-{team_number}.git
cd wvu-ieng-331-m2-{team_number}
#2. Install dependecies using uv
uv sync
#3. place olist.duckdb in the data/ directory
#4. Run the default analysis
uv run wvu-ieng-331-m2-{team_number}
#5. Run a parameteriazed analysis
uv run wvu-ieng-331-m2-{team_number} --start-date 2026-01-01 --seller-state SP
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--db-path` | string | data/olist.duckdb | Path to the DuckDb database file |
| `--start-date` | date | None (no filter) | Filters orders occuring after this date (YYYY-MM-DD) |
| `--end-date` | date | None (no filter) | Filters orders occuring after this date (YYYY-MM-DD) |
| `--seller-state | string | none | Filters results to a specific Brazilian state |

## Outputs

summary.csv: Aggregated table providing high-level metrics for quick review
detail.parquet: Comprehensive, columnar dataset containing the full results of the analysis
chart.html: Interactive Altair visualization displaying top product categories by revenue

## Validation Checks

Schema Verification: Ensures all 9 tables exist in database
Completeness Check: Ensures key indetity columns do not contain null values
Temporal Sanity: Verifies that order dates are not empty
Volume Threshold: Confirms core tables meet minimum row count requirements

## Analysis Summary

Focused on finding primary drivers of revenue within the Olist:
Top Categorie: "bed_bath_table" and "health_beauty" drive the largest share of total revenue.
Revenue Concentrarion: small percentage of sellers in specific states contribute disproportionately to the total order volume.
AOV Trends: Average order value changes significantly between product categories, suggesting varied customer purchasing power across different segments.


## Limitations & Caveats

Data Quality: The pipeline assumes the underlying DuckDB file follows the Olist schema; significant schema changes require query updates.
Memory Constraint: Large-scale data ranges utilize in-memory polars processing and performance may degrade.
Data Precison: Filters are applied based on the order_purchase_timestamp and results may vary slightly if comparing against shipping or delivery dates.

# *** The dataset has been date-shifted. The valid order purchase date range is approximately 2023-11-05 to 2025-12-17, so date filters must fall within this range. Using dates outside this window may return no results.
