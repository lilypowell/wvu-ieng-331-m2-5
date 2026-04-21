# Milestone 2 Grade

**Team 5**

| Criterion | Score | Max |
|-----------|------:|----:|
| Pipeline Functionality | 6 | 6 |
| Parameterization & Configuration | 5 | 6 |
| Code Quality | 6 | 6 |
| Project Structure & M1 Integration | 3 | 3 |
| Design Rationale (DESIGN.md) | 3 | 3 |
| **Total** | **23** | **24** |

## Pipeline Functionality (6/6)

Pipeline runs end-to-end without errors using the standard DB. All three output files are produced: `output/summary.csv`, `output/detail.parquet`, and `output/chart.html` (interactive Altair bar chart). The holdout run with `olist_extended.duckdb` succeeds identically — validation passes, the query adapts to the larger date range, and outputs are regenerated cleanly. No hardcoded paths or schema assumptions break under the extended dataset.

## Parameterization & Configuration (5/6)

Three CLI parameters are declared via argparse: `--db-path`, `--start-date`, and `--end-date`. The date filters are properly wired through `get_category_revenue_analysis` into the SQL file via DuckDB's `$1`/`$2` positional placeholders, providing safe, injection-resistant parameterization. A fourth parameter, `--seller-state`, is defined and logged but is never passed to any query — `get_seller_scorecard` exists in `queries.py` but is never called from `main()`. This makes `--seller-state` dead code with no effect on output. Deducting 1 point for the non-functional parameter. Validation in `validation.py` is thorough: table existence (9 tables), minimum row counts, key column null checks, and temporal sanity checks.

## Code Quality (6/6)

Exemplary quality throughout. Every function carries full type annotations (including `str | Path` union types, `Sequence[Any] | None`, and `-> bool`/`-> pl.DataFrame` return types). All functions have Google-style docstrings with Args, Returns, and Raises sections. Loguru is used at appropriate levels (INFO/WARNING) in both `pipeline.py` and `validation.py`. Pathlib is used exclusively for all file path operations. Specific, meaningful exceptions are raised and caught: `FileNotFoundError` for missing DB/SQL files, `duckdb.Error` for query failures, and `ValueError` for empty result sets. No bare `print()` statements or bare `except` clauses.

## Project Structure & M1 Integration (3/3)

Proper `src/` layout with `wvu_ieng_331_m2_5/` package. SQL queries are in a dedicated `sql/` directory containing five analytical queries plus a `Milestone_1_Summary.sql` demonstrating M1 integration. `pyproject.toml` has the correct `[project.scripts]` entry point. `README.md` includes setup steps, parameter table, outputs list, validation descriptions, and a data-range caveat. `DESIGN.md` is present and substantive.

## Design Rationale (3/3)

DESIGN.md contains five well-defined sections: Parameter Flow (traces data from CLI args through layers to SQL), SQL Parameterization (justifies `.sql` file separation, security rationale, readability), Validation Logic (explains each check and its business purpose), Error Handling (explains each exception type and the risk of bare except), and Scaling & Adaptation (addresses 10M-row scenario with Polars LazyFrames and a JSON output extension). References are specific to actual code constructs (`$1`/`$2` placeholders, `.pl()` method, `pathlib`, etc.) rather than generic boilerplate.
