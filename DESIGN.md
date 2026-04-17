# Design Rationale

## Parameter Flow

When a user executes the pipeline with a flag like --seller-state SP, the data travels through the following layers:

Parsing: In pipeline.py, the main() function uses argparse to capture the string "SP" and store it in a namespace object.

Orchestration: The main() function passes this variable as an argument to the analytical functions imported from queries.py

Data Access: Inside queries.py, the function get_seller_scorecard receives the parameter. It then passes this value into the duckdb.execute() method as a list or dictionary.

SQL Execution: DuckDB maps the Python variable to the $1 placeholder in the seller_scorecard.sql file, ensuring the database only returns rows where the state matches "SP".

## SQL Parameterization

I chose to store SQL in standalone .sql files rather than inline Python strings for several reasons:

Raw SQL Structure: The files use native DuckDB placeholders (WHERE price > $1).

Integration: queries.py uses the pathlib library to locate the file and .read_text() to pull the raw string. 

Security & Safety: We use parameterized queries instead of Python f-strings to prevent SQL Injection. Even though this is a local analysis, using $1 ensures that DuckDB treats the input as data, not as executable code.

Readability: Keeping SQL in .sql files allows for syntax highlighting and easier debugging in database IDEs.

## Validation Logic

For each validation check in `validation.py`, explain:

Row Count Check: I implemented a check to ensure the orders table has at least 1,000 rows. This matters because if a data transfer failed and the table is empty, the analysis would produce misleading "zeros."

NULL Detection: We check if seller_id is entirely NULL. This is critical because our joins depend on these keys; if they are missing, the resulting DataFrames would be empty.

Outcome: If a check fails, the pipeline logs a logger.warning(). We chose to halt the pipeline for schema errors but only warn for data volume issues, allowing the user to proceed with a smaller subset if intentional.

## Error Handling

FileNotFoundError: Caught when attempting to connect to the DuckDB file. If the database is missing from the data/ folder, we provide a clear instruction to the user instead of a confusing Python traceback.

duckdb.Error: Caught during query execution. This handles cases where a SQL syntax error exists or a table is locked.

The "Bare Except" Risk: If I used a bare except:, the program might hide critical system errors (like a keyboard interrupt Ctrl+C or memory failures), making it impossible for the user to know why the program crashed or how to fix it.

## Scaling & Adaptation

Scaling to 10M Rows: At 10 million rows, the polars.read_duckdb() (e.g., .pl()) method might exceed the system's RAM. To fix this, I would refactor the pipeline to use Polars LazyFrames (scan_ds()). This would allow Polars to optimize the query plan and only load the necessary data into memory using "streaming" mode.

Adding a JSON API Output: To add a third format, I would modify the main() function in pipeline.py. After the data is returned from queries.py, I would add a line using df.write_json("output/data.json"). No changes would be needed in the SQL or validation layers, demonstrating the benefit of our modular "separation of concerns."
