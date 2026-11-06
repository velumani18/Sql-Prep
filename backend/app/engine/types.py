from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ExecutionMode(str, Enum):
    READ_ONLY = "read_only"       # Default for practice mode: strictly SELECT/CTE
    DDL_DML = "ddl_dml"           # Controlled mode for future exercises: INSERT, UPDATE, DELETE, CREATE

class QueryResult(BaseModel):
    success: bool
    columns: List[str] = Field(default_factory=list)
    rows: List[List[Any]] = Field(default_factory=list)
    row_count: int = 0
    execution_time_ms: float = 0.0
    truncated: bool = False
    error: Optional[str] = None
    error_type: Optional[str] = None  # SYNTAX_ERROR, TIMEOUT, RESTRICTED_OPERATION, RUNTIME_ERROR

class TestCase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_hidden: bool = False
    custom_seed_dml: Optional[str] = None
    expected_columns: Optional[List[str]] = None
    expected_rows: Optional[List[List[Any]]] = None

class TestCaseEvaluation(BaseModel):
    test_case_id: str
    name: str
    is_hidden: bool
    passed: bool
    execution_time_ms: float
    mismatch_reason: Optional[str] = None
    actual_output: Optional[Dict[str, Any]] = None
    expected_output: Optional[Dict[str, Any]] = None

class SubmissionResult(BaseModel):
    status: str  # ACCEPTED, WRONG_ANSWER, SYNTAX_ERROR, TIME_LIMIT_EXCEEDED, RESTRICTED_OPERATION
    all_passed: bool
    total_test_cases: int
    passed_test_cases: int
    execution_time_ms: float
    error_message: Optional[str] = None
    xp_awarded: int = 0
    is_first_solve: bool = False
    gamification_message: Optional[str] = None
    test_case_results: List[TestCaseEvaluation] = Field(default_factory=list)

