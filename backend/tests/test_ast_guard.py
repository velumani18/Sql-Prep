import pytest
from app.engine.ast_guard import validate_sql_security, SecurityViolation
from app.engine.types import ExecutionMode

def test_valid_select_query():
    sql = "SELECT id, name FROM customers WHERE country = 'United States';"
    # Should not raise
    validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_valid_cte_query():
    sql = """
    WITH ActiveOrders AS (
        SELECT customer_id, COUNT(*) AS cnt
        FROM orders
        GROUP BY customer_id
    )
    SELECT * FROM ActiveOrders WHERE cnt > 1;
    """
    validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_reject_empty_query():
    with pytest.raises(SecurityViolation, match="cannot be empty"):
        validate_sql_security("   ", mode=ExecutionMode.READ_ONLY)

def test_reject_multi_statement_injection():
    sql = "SELECT * FROM customers; DROP TABLE orders;"
    with pytest.raises(SecurityViolation, match="Multi-statement queries are strictly prohibited"):
        validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_reject_drop_table_in_readonly():
    sql = "DROP TABLE customers;"
    with pytest.raises(SecurityViolation, match="restricted to read-only queries"):
        validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_reject_insert_in_readonly():
    sql = "INSERT INTO customers (id, name) VALUES (999, 'Hacker');"
    with pytest.raises(SecurityViolation, match="restricted to read-only queries"):
        validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_reject_pragma():
    sql = "PRAGMA table_info(customers);"
    with pytest.raises(SecurityViolation, match="Unauthorized command"):
        validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_reject_load_extension():
    sql = "SELECT load_extension('malicious.so');"
    with pytest.raises(SecurityViolation, match="Dangerous SQL function"):
        validate_sql_security(sql, mode=ExecutionMode.READ_ONLY)

def test_ddl_dml_mode_allows_insert():
    sql = "INSERT INTO customers (id, name) VALUES (999, 'Student');"
    # In DDL_DML mode, this should pass
    validate_sql_security(sql, mode=ExecutionMode.DDL_DML)

def test_ddl_dml_mode_blocks_attach():
    sql = "ATTACH DATABASE 'other.db' AS other;"
    with pytest.raises(SecurityViolation):
        validate_sql_security(sql, mode=ExecutionMode.DDL_DML)

