import pytest
from app.engine.sqlite_executor import SQLiteExecutor
from app.engine.types import ExecutionMode

INIT_DDL = "CREATE TABLE users (id INT PRIMARY KEY, name TEXT, score INT);"
SEED_DML = "INSERT INTO users VALUES (1, 'Alice', 95), (2, 'Bob', 80), (3, 'Charlie', 95);"

def test_sqlite_executor_basic_query():
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML)
    res = executor.execute_query("SELECT id, name FROM users WHERE score > 90 ORDER BY id ASC;")
    assert res.success is True
    assert res.columns == ["id", "name"]
    assert len(res.rows) == 2
    assert res.rows[0] == [1, "Alice"]
    assert res.rows[1] == [3, "Charlie"]
    assert res.execution_time_ms >= 0

def test_sqlite_executor_ephemeral_state_isolation():
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML)

    # In DDL_DML mode, add a row
    insert_res = executor.execute_query(
        "INSERT INTO users VALUES (4, 'David', 100);",
        mode=ExecutionMode.DDL_DML,
    )
    assert insert_res.success is True

    # Run another query: David should NOT exist because instance was reset/ephemeral!
    check_res = executor.execute_query("SELECT * FROM users WHERE id = 4;")
    assert check_res.success is True
    assert len(check_res.rows) == 0

def test_sqlite_executor_missing_table():
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML)
    res = executor.execute_query("SELECT * FROM nonexistent_table;")
    assert res.success is False
    assert res.error_type == "MISSING_TABLE"
    assert "Table Not Found" in res.error

def test_sqlite_executor_missing_column():
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML)
    res = executor.execute_query("SELECT fake_col FROM users;")
    assert res.success is False
    assert res.error_type == "MISSING_COLUMN"
    assert "Column Not Found" in res.error

def test_sqlite_executor_syntax_error():
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML)
    res = executor.execute_query("SELECT FROM users;")
    assert res.success is False
    assert res.error_type in ("SYNTAX_ERROR", "RESTRICTED_OPERATION")

def test_sqlite_executor_row_truncation():
    # Executor with max_rows = 2
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML, max_rows=2)
    res = executor.execute_query("SELECT * FROM users;")
    assert res.success is True
    assert len(res.rows) == 2
    assert res.truncated is True

def test_sqlite_executor_timeout():
    # Executor with 0.1s timeout and runaway query
    executor = SQLiteExecutor(init_ddl=INIT_DDL, seed_dml=SEED_DML, timeout_seconds=0.1)
    
    # Recursive CTE generating a large cross product loop to trigger progress handler
    runaway_sql = """
    WITH RECURSIVE cnt(x) AS (
        SELECT 1
        UNION ALL
        SELECT x + 1 FROM cnt WHERE x < 5000000
    )
    SELECT c1.x FROM cnt c1, cnt c2 WHERE c1.x = c2.x LIMIT 1000000;
    """
    res = executor.execute_query(runaway_sql)
    assert res.success is False
    assert res.error_type == "TIMEOUT"

