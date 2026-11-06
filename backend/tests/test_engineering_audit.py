import concurrent.futures
import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.engine.sqlite_executor import SQLiteExecutor
from app.engine.types import ExecutionMode, QueryResult
from app.engine.validator import evaluate_query_results
from app.engine.db_manager import db_manager

client = TestClient(app)

SAMPLE_INIT_DDL = """
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    budget NUMERIC(12, 2) NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept_id INTEGER,
    salary NUMERIC(10, 2),
    FOREIGN KEY (dept_id) REFERENCES departments(id)
);
"""

SAMPLE_SEED_DML = """
INSERT INTO departments (id, name, budget) VALUES (1, 'Engineering', 500000.00);
INSERT INTO departments (id, name, budget) VALUES (2, 'Marketing', 200000.00);

INSERT INTO employees (id, name, dept_id, salary) VALUES (101, 'Alice Smith', 1, 95000.00);
INSERT INTO employees (id, name, dept_id, salary) VALUES (102, 'Bob Jones', 1, 80000.00);
INSERT INTO employees (id, name, dept_id, salary) VALUES (103, 'Charlie Brown', 2, 60000.00);
INSERT INTO employees (id, name, dept_id, salary) VALUES (104, 'Diana Prince', NULL, NULL);
"""


# ==============================================================================
# 1. SQL EXECUTION CORRECTNESS & TEST CASES
# ==============================================================================

def test_valid_sql_query():
    """Verify standard SELECT query executes and returns correct columns and rows."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    res = executor.execute_query("SELECT id, name FROM departments ORDER BY id ASC;")
    assert res.success is True
    assert res.columns == ["id", "name"]
    assert res.row_count == 2
    assert res.rows[0] == [1, "Engineering"]
    assert res.rows[1] == [2, "Marketing"]


def test_invalid_sql_syntax():
    """Verify syntax error is caught and accurately classified as SYNTAX_ERROR."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    res = executor.execute_query("SELECT * FORM departments;")
    assert res.success is False
    assert res.error_type == "SYNTAX_ERROR"
    assert "syntax" in res.error.lower()


def test_multiple_sql_statements():
    """Verify multi-statement injection attempts are blocked."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    res = executor.execute_query("SELECT 1; DROP TABLE departments;")
    assert res.success is False
    assert res.error_type == "RESTRICTED_OPERATION"
    assert "Multi-statement" in res.error


def test_drop_table_attempt():
    """Verify DROP TABLE is rejected in read-only practice mode."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    res = executor.execute_query("DROP TABLE departments;", mode=ExecutionMode.READ_ONLY)
    assert res.success is False
    assert res.error_type == "RESTRICTED_OPERATION"
    assert "Drop" in res.error


def test_insert_or_update_in_read_only_mode():
    """Verify INSERT and UPDATE are rejected in read-only practice mode."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)

    res_insert = executor.execute_query("INSERT INTO departments VALUES (3, 'HR', 100000);", mode=ExecutionMode.READ_ONLY)
    assert res_insert.success is False
    assert res_insert.error_type == "RESTRICTED_OPERATION"
    assert "Insert" in res_insert.error

    res_update = executor.execute_query("UPDATE departments SET budget = 999999 WHERE id = 1;", mode=ExecutionMode.READ_ONLY)
    assert res_update.success is False
    assert res_update.error_type == "RESTRICTED_OPERATION"
    assert "Update" in res_update.error


def test_missing_table():
    """Verify query against non-existent table is trapped with MISSING_TABLE."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    res = executor.execute_query("SELECT * FROM non_existent_table_xyz;")
    assert res.success is False
    assert res.error_type == "MISSING_TABLE"
    assert "Table Not Found" in res.error


def test_missing_column():
    """Verify query with non-existent column is trapped with MISSING_COLUMN."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    res = executor.execute_query("SELECT non_existent_column_xyz FROM departments;")
    assert res.success is False
    assert res.error_type == "MISSING_COLUMN"
    assert "Column Not Found" in res.error


# ==============================================================================
# 2. SQL RESULT COMPARISON & VALIDATION LOGIC
# ==============================================================================

def test_empty_result_comparison():
    """Verify empty result set comparison succeeds when both are empty, fails when expected rows exist."""
    # Both empty -> PASS
    actual_empty = QueryResult(success=True, columns=["id", "name"], rows=[], row_count=0)
    v1 = evaluate_query_results(actual_empty, expected_columns=["id", "name"], expected_rows=[])
    assert v1.passed is True

    # Expected non-empty but actual empty -> FAIL
    v2 = evaluate_query_results(actual_empty, expected_columns=["id", "name"], expected_rows=[[1, "Engineering"]])
    assert v2.passed is False
    assert "Row count mismatch" in v2.reason


def test_duplicate_rows_handling():
    """Verify multiset comparison strictly checks duplicate counts."""
    actual_rows = [[1, "Dept A"], [1, "Dept A"]]
    expected_rows = [[1, "Dept A"]]  # Expected only 1 duplicate, got 2

    actual_res = QueryResult(success=True, columns=["id", "name"], rows=actual_rows, row_count=2)
    v = evaluate_query_results(actual_res, expected_columns=["id", "name"], expected_rows=expected_rows, order_matters=False)
    assert v.passed is False


def test_null_values_handling():
    """Verify NULL values (None) match exactly and do not match 0 or string 'NULL'."""
    actual_with_null = QueryResult(
        success=True,
        columns=["id", "salary"],
        rows=[[104, None]],
        row_count=1,
    )

    # Expected None -> PASS
    v_match = evaluate_query_results(actual_with_null, expected_columns=["id", "salary"], expected_rows=[[104, None]])
    assert v_match.passed is True

    # Expected 0 instead of NULL -> FAIL
    v_mismatch_zero = evaluate_query_results(actual_with_null, expected_columns=["id", "salary"], expected_rows=[[104, 0]])
    assert v_mismatch_zero.passed is False

    # Expected 'None' string instead of NULL -> FAIL
    v_mismatch_str = evaluate_query_results(actual_with_null, expected_columns=["id", "salary"], expected_rows=[[104, "None"]])
    assert v_mismatch_str.passed is False


def test_different_column_order():
    """
    Verify behavior when query returns columns in a different sequence:
    - Fails if check_column_order=True
    - Succeeds if check_column_order=False by aligning columns
    """
    actual_swapped = QueryResult(
        success=True,
        columns=["name", "id"],
        rows=[["Engineering", 1], ["Marketing", 2]],
        row_count=2,
    )
    expected_cols = ["id", "name"]
    expected_rows = [[1, "Engineering"], [2, "Marketing"]]

    # When sequence order is strictly enforced -> FAIL
    v_strict = evaluate_query_results(
        actual_swapped,
        expected_columns=expected_cols,
        expected_rows=expected_rows,
        check_column_names=True,
        check_column_order=True,
    )
    assert v_strict.passed is False
    assert "Column name/order mismatch" in v_strict.reason

    # When sequence order is flexible -> PASS
    v_flexible = evaluate_query_results(
        actual_swapped,
        expected_columns=expected_cols,
        expected_rows=expected_rows,
        check_column_names=True,
        check_column_order=False,
        order_matters=False,
    )
    assert v_flexible.passed is True


def test_unordered_results_comparison():
    """Verify multiset comparison passes when row ordering is arbitrary (order_matters=False)."""
    actual_reversed = QueryResult(
        success=True,
        columns=["id", "name"],
        rows=[[2, "Marketing"], [1, "Engineering"]],
        row_count=2,
    )
    expected_rows = [[1, "Engineering"], [2, "Marketing"]]

    # Unordered comparison -> PASS
    v_unordered = evaluate_query_results(
        actual_reversed,
        expected_columns=["id", "name"],
        expected_rows=expected_rows,
        order_matters=False,
    )
    assert v_unordered.passed is True

    # Ordered comparison -> FAIL
    v_ordered = evaluate_query_results(
        actual_reversed,
        expected_columns=["id", "name"],
        expected_rows=expected_rows,
        order_matters=True,
    )
    assert v_ordered.passed is False
    assert "Ordering/value mismatch" in v_ordered.reason


# ==============================================================================
# 3. RESOURCE CONSUMPTION & TIMEOUTS
# ==============================================================================

def test_queries_that_return_excessive_rows():
    """Verify that result sets exceeding max_rows are truncated and flagged."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML, max_rows=50)
    # Generate 200 rows via recursive CTE
    query = "WITH RECURSIVE cnt(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM cnt WHERE x < 200) SELECT x FROM cnt;"
    res = executor.execute_query(query)
    assert res.success is True
    assert res.truncated is True
    assert res.row_count == 50
    assert len(res.rows) == 50


def test_queries_that_take_too_long():
    """Verify execution timeout halts long-running queries and returns TIMEOUT status."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML, timeout_seconds=0.5)
    # Heavy computation query that takes longer than 0.5s
    query = "WITH RECURSIVE r(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM r WHERE x < 50000000) SELECT count(*) FROM r, r;"
    res = executor.execute_query(query)
    assert res.success is False
    assert res.error_type == "TIMEOUT"
    assert "timed out" in res.error.lower()


def test_excessive_query_length_rejected():
    """Verify queries exceeding MAX_QUERY_LENGTH_CHARS are rejected before execution."""
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)
    long_query = "SELECT " + "1, " * 6000 + "1;"  # > 10,000 characters
    res = executor.execute_query(long_query)
    assert res.success is False
    assert res.error_type == "RESTRICTED_OPERATION"
    assert "maximum permitted length" in res.error


# ==============================================================================
# 4. DATABASE ISOLATION & CONCURRENCY
# ==============================================================================

def test_database_isolation_across_executions():
    """
    Verify that one user's query modifications in DDL_DML mode
    NEVER affect another user's subsequent or concurrent query.
    """
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)

    # User A executes DROP TABLE in DDL_DML mode
    res_a = executor.execute_query("DROP TABLE departments;", mode=ExecutionMode.DDL_DML)
    assert res_a.success is True

    # User B executes query against departments
    res_b = executor.execute_query("SELECT count(*) FROM departments;", mode=ExecutionMode.READ_ONLY)
    assert res_b.success is True
    assert res_b.rows[0][0] == 2  # Pristine original 2 departments intact!


def test_concurrent_query_execution():
    """
    Verify 10 concurrent threads executing queries simultaneously.
    Validates complete isolation and thread safety.
    """
    executor = SQLiteExecutor(SAMPLE_INIT_DDL, SAMPLE_SEED_DML)

    queries = [
        ("SELECT count(*) FROM employees;", 1),
        ("SELECT count(*) FROM departments;", 2),
        ("SELECT name FROM departments WHERE id = 1;", 1),
        ("SELECT max(budget) FROM departments;", 1),
        ("SELECT avg(salary) FROM employees WHERE salary IS NOT NULL;", 1),
        ("SELECT count(*) FROM employees WHERE dept_id IS NULL;", 1),
        ("SELECT id, name FROM employees WHERE salary > 70000;", 2),
        ("SELECT count(*) FROM departments;", 2),
        ("SELECT count(*) FROM employees;", 1),
        ("SELECT 100 AS benchmark;", 1),
    ]

    def run_worker(query_info):
        sql, expected_min_rows = query_info
        return executor.execute_query(sql)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(run_worker, q) for q in queries]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert len(results) == 10
    for r in results:
        assert r.success is True
        assert r.execution_time_ms < 500  # Sub-second execution


# ==============================================================================
# 5. HIDDEN TEST-CASE PROTECTION
# ==============================================================================

def test_hidden_test_cases_not_leaked_in_question_endpoint():
    """Verify /api/questions/{id} does not reveal custom_seed_dml or hidden answers."""
    res = client.get("/api/questions/q-001")
    assert res.status_code == 200
    data = res.json()
    assert len(data["test_cases"]) > 0

    for tc in data["test_cases"]:
        assert "custom_seed_dml" not in tc
        assert "expected_rows" not in tc


def test_hidden_test_case_failure_reason_sanitized():
    """
    When a submission fails on a hidden test case, verify that the mismatch reason
    does not leak benchmark expected row values.
    """
    # q-001 expects: SELECT first_name, last_name, email FROM employees;
    # Submit query with incorrect WHERE clause that fails on test case 2
    wrong_sub = client.post("/api/sql/submit", json={
        "question_id": "q-001",
        "sql": "SELECT first_name, last_name, email FROM employees WHERE id = 1;",
    })
    assert wrong_sub.status_code == 200
    data = wrong_sub.json()
    assert data["status"] == "WRONG_ANSWER"

    # Find the hidden test case in the evaluation results
    for tc in data["test_case_results"]:
        if tc["is_hidden"]:
            assert tc["actual_output"] is None
            assert tc["expected_output"] is None
            if not tc["passed"]:
                # Ensure mismatch reason is generic and does not leak seed data
                assert "Hidden test case failed" in tc["mismatch_reason"]


# ==============================================================================
# 6. AUTHENTICATION & API VALIDATION
# ==============================================================================

def test_auth_validation():
    # Empty email in login should return 400
    res_login_empty = client.post("/api/auth/login", json={"email": ""})
    assert res_login_empty.status_code == 400

    # Empty email in signup should return 400
    res_signup_empty_email = client.post("/api/auth/signup", json={"email": "", "name": "Test"})
    assert res_signup_empty_email.status_code == 400

    # Empty name in signup should return 400
    res_signup_empty_name = client.post("/api/auth/signup", json={"email": "valid@sqlforge.dev", "name": "  "})
    assert res_signup_empty_name.status_code == 400

    # Valid login succeeds
    res_valid = client.post("/api/auth/login", json={"email": "student@sqlforge.dev"})
    assert res_valid.status_code == 200
    assert "token" in res_valid.json()

