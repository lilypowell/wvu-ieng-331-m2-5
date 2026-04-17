import argparse

from loguru import logger


def main() -> None:
    print("main is running")
    parser = argparse.ArgumentParser(description="Milestone 2 Data Pipeline")
    parser.add_argument("--db-path", default="data/olist.duckdb")
    parser.add_argument("--seller-state", default=None)

    args = parser.parse_args()

    print("after argparse")
    logger.info("Starting pipeline")
    logger.info(f"Database path: {args.db_path}")
    logger.info(f"Seller state filter: {args.seller_state}")


if __name__ == "__main__":
    main()
