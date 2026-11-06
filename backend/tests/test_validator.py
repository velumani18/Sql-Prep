import pytest
from app.engine.types import QueryResult
from app.engine.validator import evaluate_query_results

def test_validator_ordered_exact_match():
    actual = QueryResult(
        success=True,
        columns=["name", "salary"],
        rows=[["Alice", 100000.0], ["Bob", 90000.0]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["name", "salary"],
        expected_rows=[["Alice", 100000.0], ["Bob", 90000.0]],
        order_matters=True,
    )
    assert res.passed is True

def test_validator_ordered_mismatch():
    actual = QueryResult(
        success=True,
        columns=["name", "salary"],
        rows=[["Bob", 90000.0], ["Alice", 100000.0]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["name", "salary"],
        expected_rows=[["Alice", 100000.0], ["Bob", 90000.0]],
        order_matters=True,
    )
    assert res.passed is False
    assert "Ordering/value mismatch at row 1" in res.reason

def test_validator_unordered_multiset_match():
    # Rows in different order should pass when order_matters=False
    actual = QueryResult(
        success=True,
        columns=["name", "salary"],
        rows=[["Bob", 90000.0], ["Alice", 100000.0]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["name", "salary"],
        expected_rows=[["Alice", 100000.0], ["Bob", 90000.0]],
        order_matters=False,
    )
    assert res.passed is True

def test_validator_duplicate_rows_mismatch_frequencies():
    # Both have 2 rows, but actual has ["A"] duplicated twice instead of ["A"] and ["B"]
    actual = QueryResult(
        success=True,
        columns=["item"],
        rows=[["A"], ["A"]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["item"],
        expected_rows=[["A"], ["B"]],
        order_matters=False,
    )
    assert res.passed is False
    assert "missing" in res.reason.lower() or "unexpected" in res.reason.lower()

def test_validator_row_count_mismatch():
    actual = QueryResult(
        success=True,
        columns=["item"],
        rows=[["A"], ["A"], ["B"]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["item"],
        expected_rows=[["A"], ["B"]],
        order_matters=False,
    )
    assert res.passed is False
    assert "row count mismatch" in res.reason.lower()

def test_validator_null_values():
    actual = QueryResult(
        success=True,
        columns=["id", "discount"],
        rows=[[1, None], [2, 0.15]],
    )
    # Expected matches None
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["id", "discount"],
        expected_rows=[[1, None], [2, 0.15]],
    )
    assert res.passed is True

    # Expected has string "None" or 0 which should NOT match SQL NULL
    res_bad = evaluate_query_results(
        actual=actual,
        expected_columns=["id", "discount"],
        expected_rows=[[1, 0], [2, 0.15]],
    )
    assert res_bad.passed is False

def test_validator_float_tolerance():
    actual = QueryResult(
        success=True,
        columns=["ratio"],
        rows=[[0.3333333333333333]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["ratio"],
        expected_rows=[[0.3333]],
        order_matters=True,
    )
    assert res.passed is True

def test_validator_empty_result_sets():
    actual = QueryResult(
        success=True,
        columns=["id", "name"],
        rows=[],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["id", "name"],
        expected_rows=[],
    )
    assert res.passed is True

def test_validator_column_count_mismatch():
    actual = QueryResult(
        success=True,
        columns=["id"],
        rows=[[1]],
    )
    res = evaluate_query_results(
        actual=actual,
        expected_columns=["id", "name"],
        expected_rows=[[1, "Alice"]],
    )
    assert res.passed is False
    assert "Column count mismatch" in res.reason
