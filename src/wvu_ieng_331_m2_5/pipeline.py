import argparse
from pathlib import Path

import altair as alt
from loguru import logger

from wvu_ieng_331_m2_5.queries import get_category_revenue_analysis
from wvu_ieng_331_m2_5.validation import run_validation


def main() -> None:
    """Run the Milestone 2 data pipeline."""
    parser = argparse.ArgumentParser(description="Milestone 2 Data Pipeline")
    parser.add_argument("--db-path", default="data/olist.duckdb")
    parser.add_argument("--seller-state", default=None)
    parser.add_argument("--start-date", default=None)
    parser.add_argument("--end-date", default=None)

    args = parser.parse_args()

    logger.info("Starting pipline")
    logger.info(f"Database path: {args.db_path}")
    logger.info(f"Seller state filter: {args.seller_state}")
    logger.info(f"Start date filter: {args.start_date}")
    logger.info(f"End date filter: {args.end_date}")

    if not run_validation(args.db_path):
        raise ValueError("Validation failed. Pipeline stopped.")

    df = get_category_revenue_analysis(
        args.db_path,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    logger.info("Query ran successfully")
    logger.info(df.head())

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    df.write_parquet(output_dir / "detail.parquet")
    df.write_csv(output_dir / "summary.csv")

    top_df = df.sort("total_revenue", descending=True).head(10)

    chart = (
        alt.Chart(top_df.to_pandas())
        .mark_bar()
        .encode(
            x=alt.X("category_name:N", sort="-y", title="Category"),
            y=alt.Y("total_revenue:Q", title="Total Revenue"),
            tooltip=["category_name", "total_revenue", "average_order_value"],
        )
        .properties(title="Top 10 Categories by Revenue")
    )

    chart.save(output_dir / "chart.html")

    logger.info("Output files written successfully")


if __name__ == "__main__":
    main()
