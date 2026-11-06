import sqlite3
import time
from typing import Any, List, Optional
from app.config import settings
from app.engine.types import ExecutionMode, QueryResult
from app.engine.ast_guard import validate_sql_security, SecurityViolation, SQLSyntaxViolation

class SQLiteExecutor:
    """
    Manages isolated, ephemeral SQLite in-memory execution instances.
    Guarantees that each query runs in a fresh environment that is destroyed
    immediately after execution, enforcing timeouts and output row limits.
    """

    def __init__(
        self,
        init_ddl: str,
        seed_dml: str,
        timeout_seconds: float = settings.DEFAULT_TIMEOUT_SECONDS,
        max_rows: int = settings.MAX_OUTPUT_ROWS,
    ):
        self.init_ddl = init_ddl
        self.seed_dml = seed_dml
        self.timeout_seconds = timeout_seconds
        self.max_rows = max_rows

    def execute_query(
        self,
        sql: str,
        custom_seed_dml: Optional[str] = None,
        mode: ExecutionMode = ExecutionMode.READ_ONLY,
    ) -> QueryResult:
        """
        Executes a user query in a completely isolated, fresh in-memory SQLite database.
        """
        # 1. AST Security Validation before touching the database
        try:
            validate_sql_security(sql, mode=mode)
        except SQLSyntaxViolation as se:
            return QueryResult(
                success=False,
                error=f"SQL Syntax Error: {str(se)}",
                error_type="SYNTAX_ERROR",
                execution_time_ms=0.0,
            )
        except SecurityViolation as sv:
            return QueryResult(
                success=False,
                error=str(sv),
                error_type="RESTRICTED_OPERATION",
                execution_time_ms=0.0,
            )

        # 2. Spawn ephemeral in-memory SQLite connection
        conn: Optional[sqlite3.Connection] = None
        start_time = time.perf_counter()

        try:
            conn = sqlite3.connect(":memory:", timeout=self.timeout_seconds)
            conn.row_factory = None  # Return standard tuples for fast processing

            # Explicitly disallow SQLite extensions if supported
            if hasattr(conn, "enable_load_extension"):
                try:
                    conn.enable_load_extension(False)
                except Exception:
                    pass

            cursor = conn.cursor()

            # 3. Populate base schema and seeds
            if self.init_ddl:
                cursor.executescript(self.init_ddl)
            if self.seed_dml:
                cursor.executescript(self.seed_dml)

            # 4. Populate test-case-specific DML if provided
            if custom_seed_dml:
                cursor.executescript(custom_seed_dml)

            # 5. Set up execution timeout via opcode progress handler
            def progress_handler():
                if time.perf_counter() - start_time > self.timeout_seconds:
                    return 1  # Non-zero triggers sqlite3 interrupt
                return 0

            conn.set_progress_handler(progress_handler, settings.PROGRESS_HANDLER_OPCODES)

            # 6. Execute user query
            exec_start = time.perf_counter()
            cursor.execute(sql)

            # Determine column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # 7. Fetch rows with truncation guard
            # Fetch up to max_rows + 1 to detect if total rows exceeded the limit
            raw_rows = cursor.fetchmany(self.max_rows + 1)
            truncated = len(raw_rows) > self.max_rows
            final_rows: List[List[Any]] = [list(r) for r in raw_rows[: self.max_rows]]

            exec_time_ms = round((time.perf_counter() - exec_start) * 1000, 2)

            return QueryResult(
                success=True,
                columns=columns,
                rows=final_rows,
                row_count=len(final_rows),
                execution_time_ms=exec_time_ms,
                truncated=truncated,
            )

        except sqlite3.OperationalError as oe:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            err_msg = str(oe)
            if "interrupted" in err_msg.lower():
                return QueryResult(
                    success=False,
                    error=f"Query execution timed out after {self.timeout_seconds}s limit.",
                    error_type="TIMEOUT",
                    execution_time_ms=elapsed_ms,
                )
            if "no such table" in err_msg.lower():
                return QueryResult(
                    success=False,
                    error=f"Table Not Found: {err_msg}",
                    error_type="MISSING_TABLE",
                    execution_time_ms=elapsed_ms,
                )
            if "no such column" in err_msg.lower():
                return QueryResult(
                    success=False,
                    error=f"Column Not Found: {err_msg}",
                    error_type="MISSING_COLUMN",
                    execution_time_ms=elapsed_ms,
                )
            return QueryResult(
                success=False,
                error=f"Operational Error: {err_msg}",
                error_type="SYNTAX_ERROR" if "syntax" in err_msg.lower() else "RUNTIME_ERROR",
                execution_time_ms=elapsed_ms,
            )

        except Exception as ex:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return QueryResult(
                success=False,
                error=f"Database Execution Error: {str(ex)}",
                error_type="RUNTIME_ERROR",
                execution_time_ms=elapsed_ms,
            )

        finally:
            # 8. Immediate teardown: completely discard in-memory connection
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

