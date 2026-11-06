from collections import Counter
import math
from typing import Any, List, Optional, Tuple
from app.engine.types import QueryResult


def normalize_value(val: Any) -> Any:
    """
    Normalizes a single SQL value for semantic equality comparison:
    - Coerces int/float numeric representations so 5 == 5.0
    - Preserves None (NULL) strictly
    - Strips whitespace from strings if desired
    """
    if val is None:
        return None
    if isinstance(val, (int, float)):
        # Normalize whole floats like 42.0 to int 42 for hashability, or keep rounded float
        if isinstance(val, float) and val.is_integer():
            return int(val)
        if isinstance(val, float):
            return round(val, 4)
        return val
    if isinstance(val, str):
        return val.strip()
    return val


def are_values_equal(val_a: Any, val_b: Any, float_tol: float = 1e-4) -> bool:
    """
    Checks semantic equivalence between two cell values, handling NULLs and float precision.
    """
    if val_a is None and val_b is None:
        return True
    if val_a is None or val_b is None:
        return False

    # Check numeric types
    if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
        return math.isclose(float(val_a), float(val_b), rel_tol=float_tol, abs_tol=float_tol)

    # General equality
    norm_a = normalize_value(val_a)
    norm_b = normalize_value(val_b)
    return norm_a == norm_b


def canonical_row(row: List[Any]) -> Tuple[Any, ...]:
    """Converts a row to a normalized, hashable tuple for multiset (bag) comparison."""
    return tuple(normalize_value(v) for v in row)


class ValidationResult:
    def __init__(self, passed: bool, reason: Optional[str] = None):
        self.passed = passed
        self.reason = reason


def evaluate_query_results(
    actual: QueryResult,
    expected_columns: List[str],
    expected_rows: List[List[Any]],
    order_matters: bool = False,
    check_column_names: bool = True,
    check_column_order: bool = True,
) -> ValidationResult:
    """
    Semantically evaluates user query output against expected benchmark output.
    Does not rely on SQL strings.
    Handles:
    - Column names and column sequence order
    - Row ordering when explicitly required (order_matters=True)
    - Unordered result comparison using multiset (bag) comparison (order_matters=False)
    - Duplicate rows handling
    - NULL value strict comparison
    - Numeric floating-point tolerance
    - Empty result sets comparison.
    """
    if not actual.success:
        return ValidationResult(
            passed=False,
            reason=f"Query failed to execute successfully: {actual.error}",
        )

    # 1. Column Count Check
    if len(actual.columns) != len(expected_columns):
        return ValidationResult(
            passed=False,
            reason=f"Column count mismatch: Expected {len(expected_columns)} columns, but query returned {len(actual.columns)} columns.",
        )

    actual_rows_aligned = actual.rows

    # 2. Column Names & Ordering Check (case-insensitive)
    if check_column_names:
        actual_cols_norm = [c.strip().lower() for c in actual.columns]
        expected_cols_norm = [c.strip().lower() for c in expected_columns]

        if check_column_order:
            if actual_cols_norm != expected_cols_norm:
                return ValidationResult(
                    passed=False,
                    reason=f"Column name/order mismatch: Expected columns {expected_columns}, but query produced {actual.columns}.",
                )
        else:
            # Column order does not matter, but all required columns must be present
            if set(actual_cols_norm) != set(expected_cols_norm):
                missing = [expected_columns[i] for i, c in enumerate(expected_cols_norm) if c not in actual_cols_norm]
                return ValidationResult(
                    passed=False,
                    reason=f"Column mismatch: Missing expected columns {missing}.",
                )
            # Realign user rows to match expected column order
            col_index_map = [actual_cols_norm.index(c) for c in expected_cols_norm]
            actual_rows_aligned = [
                [row[idx] for idx in col_index_map]
                for row in actual.rows
            ]

    # 3. Row Count Check
    if len(actual_rows_aligned) != len(expected_rows):
        return ValidationResult(
            passed=False,
            reason=f"Row count mismatch: Expected {len(expected_rows)} rows, but query returned {len(actual_rows_aligned)} rows.",
        )

    # 4. Empty Result Set Check
    if len(expected_rows) == 0 and len(actual_rows_aligned) == 0:
        return ValidationResult(passed=True)

    # 5. Row Values & Ordering Comparison
    if order_matters:
        # Strict row-by-row sequence comparison
        for i, (act_row, exp_row) in enumerate(zip(actual_rows_aligned, expected_rows)):
            if len(act_row) != len(exp_row):
                return ValidationResult(
                    passed=False,
                    reason=f"Row {i + 1} column count mismatch.",
                )
            for j, (act_val, exp_val) in enumerate(zip(act_row, exp_row)):
                if not are_values_equal(act_val, exp_val):
                    col_name = expected_columns[j] if j < len(expected_columns) else f"col_{j+1}"
                    return ValidationResult(
                        passed=False,
                        reason=f"Ordering/value mismatch at row {i + 1}, column '{col_name}': Expected '{exp_val}', but query produced '{act_val}'.",
                    )
        return ValidationResult(passed=True)

    else:
        # Unordered Multiset (Bag) comparison (handles duplicate rows properly)
        actual_bag = Counter(canonical_row(r) for r in actual_rows_aligned)
        expected_bag = Counter(canonical_row(r) for r in expected_rows)

        if actual_bag == expected_bag:
            return ValidationResult(passed=True)

        # Diagnose mismatch for clean feedback
        missing_rows = expected_bag - actual_bag
        extra_rows = actual_bag - expected_bag

        if missing_rows:
            sample_missing, count = next(iter(missing_rows.items()))
            return ValidationResult(
                passed=False,
                reason=f"Missing expected row: {list(sample_missing)} (missing {count} occurrence(s)).",
            )
        if extra_rows:
            sample_extra, count = next(iter(extra_rows.items()))
            return ValidationResult(
                passed=False,
                reason=f"Unexpected extra row in query output: {list(sample_extra)} ({count} extra occurrence(s)).",
            )

        return ValidationResult(
            passed=False,
            reason="Result set values do not match expected dataset.",
        )
