import re
from typing import Optional, Set
import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError
from app.config import settings
from app.engine.types import ExecutionMode

DANGEROUS_FUNCTIONS: Set[str] = {
    "load_extension",
    "writefile",
    "readfile",
    "edit",
    "fts3_tokenizer",
}

DISALLOWED_READONLY_EXPRESSIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Alter,
    exp.Command,
    exp.Pragma,
    exp.Create,
    exp.Transaction,
)

DISALLOWED_ALWAYS_EXPRESSIONS = (
    exp.Pragma,
    exp.Command,
)


class SecurityViolation(ValueError):
    """Raised when a query violates security policies or contains forbidden AST nodes."""
    pass


class SQLSyntaxViolation(ValueError):
    """Raised when a query fails SQL parsing due to syntax errors."""
    pass


def clean_ansi(text: str) -> str:
    """Removes terminal ANSI color codes from parser error strings."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def validate_sql_security(sql: str, mode: ExecutionMode = ExecutionMode.READ_ONLY) -> None:
    """
    Validates that the SQL statement complies with strict security guidelines.
    Parses SQL into an AST via sqlglot, blocking injection, multi-statement queries,
    system commands, and unauthorized DDL/DML.
    """
    cleaned = sql.strip()
    if not cleaned:
        raise SecurityViolation("SQL query cannot be empty.")

    # 1. Resource protection: Enforce query character length limit
    if len(cleaned) > settings.MAX_QUERY_LENGTH_CHARS:
        raise SecurityViolation(
            f"Query exceeds maximum permitted length of {settings.MAX_QUERY_LENGTH_CHARS} characters."
        )

    # 2. Block ATTACH / DETACH before parsing
    cleaned_lower = cleaned.lower()
    if re.search(r"\b(attach|detach)\s+database\b", cleaned_lower) or re.search(r"\battach\s+", cleaned_lower):
        raise SecurityViolation("ATTACH and DETACH operations are strictly prohibited.")

    # 3. Parse via sqlglot
    try:
        statements = sqlglot.parse(cleaned, read="sqlite")
    except ParseError as pe:
        # Syntax error during parsing
        raise SQLSyntaxViolation(clean_ansi(str(pe)))
    except Exception as e:
        raise SQLSyntaxViolation(f"Unable to parse SQL statement: {clean_ansi(str(e))}")

    if not statements or len(statements) == 0:
        raise SecurityViolation("No valid SQL statement recognized.")

    # 4. Prevent multi-statement attacks (e.g. "SELECT 1; DROP TABLE users;")
    if len(statements) > 1:
        raise SecurityViolation("Multi-statement queries are strictly prohibited. Submit exactly one SQL statement.")

    statement = statements[0]
    if statement is None:
        raise SecurityViolation("Invalid or empty SQL statement.")

    # 5. Always block dangerous expressions (PRAGMA, Command)
    if isinstance(statement, DISALLOWED_ALWAYS_EXPRESSIONS):
        raise SecurityViolation(f"Unauthorized command '{statement.__class__.__name__}' is disabled.")

    # 6. Check for dangerous SQLite functions across all AST nodes
    for func in statement.find_all(exp.Anonymous):
        func_name = func.this.lower() if isinstance(func.this, str) else ""
        if func_name in DANGEROUS_FUNCTIONS:
            raise SecurityViolation(f"Dangerous SQL function '{func_name}()' is strictly prohibited.")

    # 7. Check practice read-only restrictions
    if mode == ExecutionMode.READ_ONLY:
        is_select = isinstance(statement, (exp.Select, exp.Union))
        if isinstance(statement, DISALLOWED_READONLY_EXPRESSIONS) or not is_select:
            raise SecurityViolation(
                f"Practice mode is restricted to read-only queries (SELECT / CTE). "
                f"Statement type '{statement.__class__.__name__}' is not permitted."
            )

    elif mode == ExecutionMode.DDL_DML:
        if "attach " in cleaned_lower or "detach " in cleaned_lower:
            raise SecurityViolation("ATTACH and DETACH operations are prohibited.")
