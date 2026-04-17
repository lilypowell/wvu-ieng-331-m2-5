from __future__ import annotations

from pathlib import Path

import duckdb
from loguru import logger

EXPECTED_TABLES = {
    "orders",
    "order_items",
    "order_payments",
    "order_reviews",
    "customers",
    "sellers",
    "products",
    "category_translation",
    "geolocation",
}


def check_expected_tables(db_path: str | Path) -> bool:
    """Check that all expected tables exist in the database.

    Args:
        db_path: Path to the DuckDB database file.

    Returns:
        True if all expected tables exist, otherwise False.
    """
    with duckdb.connect(str(db_path)) as conn:
        tables = {row[0] for row in conn.execute("SHOW TABLES").fetchall()}

    missing = EXPECTED_TABLES - tables

    if missing:
        logger.warning(f"Missing tables: {sorted(missing)}")
        return False

    logger.info("All expected tables exist")
    return True


def check_minimum_row_counts(db_path: str | Path) -> bool:
    """Check that core tables have at least a minimum number of rows.

    Args:
        db_path: Path to the DuckDB database file.

    Returns:
        True if all thresholds are met, otherwise False.
    """
    thresholds = {
        "orders": 1000,
        "order_items": 1000,
        "customers": 1000,
    }

    passed = True

    with duckdb.connect(str(db_path)) as conn:
        for table, threshold in thresholds.items():
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            if count < threshold:
                logger.warning(
                    f"Table {table} has only {count} rows; expected at least {threshold}"
                )
                passed = False

    if passed:
        logger.info("Minimum row count checks passed")

    return passed


def check_key_columns_not_all_null(db_path: str | Path) -> bool:
    """Check that important key columns are not entirely NULL.

    Args:
        db_path: Path to the DuckDB database file.

    Returns:
        True if all key columns have at least one non-NULL value, otherwise False.
    """
    checks = {
        "orders": "order_id",
        "customers": "customer_id",
        "products": "product_id",
        "order_items": "seller_id",
    }

    passed = True

    with duckdb.connect(str(db_path)) as conn:
        for table, column in checks.items():
            non_null_count = conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE {column} IS NOT NULL"
            ).fetchone()[0]

            if non_null_count == 0:
                logger.warning(f"Column {table}.{column} is entirely NULL")
                passed = False

    if passed:
        logger.info("Key column NULL checks passed")

    return passed


def check_order_date_range(db_path: str | Path) -> bool:
    """Check that order purchase dates exist and are not future-dated.

    Args:
        db_path: Path to the DuckDB database file.

    Returns:
        True if the date range looks reasonable, otherwise False.
    """
    with duckdb.connect(str(db_path)) as conn:
        min_date, max_date = conn.execute(
            """
            SELECT
                MIN(order_purchase_timestamp),
                MAX(order_purchase_timestamp)
            FROM orders
            """
        ).fetchone()

    if min_date is None or max_date is None:
        logger.warning("orders.order_purchase_timestamp is empty")
        return False

    with duckdb.connect(str(db_path)) as conn:
        future_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE order_purchase_timestamp > CURRENT_TIMESTAMP
            """
        ).fetchone()[0]

    if future_count > 0:
        logger.warning(
            f"Found {future_count} future-dated rows in orders.order_purchase_timestamp"
        )
        return False

    logger.info(f"Order purchase date range: {min_date} to {max_date}")
    return True


def run_validation(db_path: str | Path) -> bool:
    """Run all validation checks before analysis.

    Args:
        db_path: Path to the DuckDB database file.

    Returns:
        True if all validation checks pass, otherwise False.
    """
    logger.info("Running validation checks")

    checks = [
        check_expected_tables(db_path),
        check_minimum_row_counts(db_path),
        check_key_columns_not_all_null(db_path),
        check_order_date_range(db_path),
    ]

    passed = all(checks)

    if passed:
        logger.info("Validation passed")
    else:
        logger.warning("Validation failed")

    return passed
