# Design Rationale

## Parameter Flow

When a user executes the pipeline with parameters such as --start-date and --end-date, the data flows through the following layers:

Parsing: In pipeline.py, the main() function uses argparse to capture the provided date values (e.g., "2024-01-01") and store them in a namespace object.

Orchestration: The main() function passes these variables as arguments to the analytical function get_category_revenue_analysis in queries.py.

Data Access: Inside queries.py, the function get_category_revenue_analysis receives the parameters and passes them into the duckdb.execute() method as a list.

SQL Execution: DuckDB maps the Python variables to the $1 and $2 placeholders in the category_revenue_analysis.sql file, ensuring the database only returns rows within the specified date range.

## SQL Parameterization

The team chose to store SQL in standalone .sql files rather than inline Python strings for several reasons:

Raw SQL Structure: The files ise native DuckDB placeholders:
  WHERE ($1 IS NULL OR DATE(order_purchase_timestamp) >= $1)
    AND ($2 IS NULL OR DATE(order_purchase_timestamp)<= $2)).

Integration: queries.py uses the pathlib library to locate the file and .read_text() to pull the raw string. 

Security & Safety: We use parameterized queries instead of Python f-strings to prevent SQL Injection. Even though this is a local analysis, using $1 ensures that DuckDB treats the input as data, not as executable code.

Readability: Keeping SQL in .sql files allows for syntax highlighting and easier debugging in database IDEs.

## Validation Logic

The validation logic in `validation.py` ensures data integrity before analysis:

Row Count Check: The team implemented a check to ensure the orders table has at least 1,000 rows. This matters because if a data transfer failed and the table is empty, the analysis would produce misleading "zeros."

NULL Detection: We check that key columns such as order_id, customer_id, and product_id are not entirely NULL. This is critical because our joins depend on these keys; if they are missing, the resulting DataFrames would be empty.

Outcome: If a validation check fails, the pipeline stops execution to prevent invalid analysis results. Warnings may still be logged for non-critical issues to provide additional context.

## Error Handling

FileNotFoundError: Caught when attempting to connect to the DuckDB file. If the database is missing from the data/ folder, we provide a clear instruction to the user instead of a confusing Python traceback.

duckdb.Error: Caught during query execution. This handles cases where a SQL syntax error exists or a table is locked.

The "Bare Except" Risk: If I used a bare except:, the program might hide critical system errors (like a keyboard interrupt Ctrl+C or memory failures), making it impossible for the user to know why the program crashed or how to fix it.

ValueError: Raised when a query returns no rows (e.g., when filters fall outside the valid date range), helping users understand that the issue is related to input parameters rather than system failure.

This structured approach ensures that users receive clear, actionable feedback when errors occur, improving overall usability of the pipeline.

## Scaling & Adaptation

Scaling to 10M Rows: At 10 million rows, the Polars `.pl()` method used after DuckDB execution, may exceed the system's RAM. To fix this, the pipeline could be refactored to use Polars LazyFrames (scan_parquet() or other lazy loading methods). This would allow Polars to optimize the query plan and only load the necessary data into memory using "streaming" mode.

Adding a JSON API Output: To add a third format, the main() function in pipeline.py could be extended. Adding a line using df.write_json("output/data.json"), after the data is returned from queries.py. No changes would be needed in the SQL or validation layers, demonstrating the benefit of our modular "separation of concerns."

Overall, the pipeline is designed with modularity, scalability, and robustness in mind, allowing for easy extension and reliable execution across different analysis scenarios.
