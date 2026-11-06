from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.engine.types import TestCase


class ColumnSchema(BaseModel):
    name: str
    type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references: Optional[str] = None
    description: Optional[str] = None


class TableSchemaInfo(BaseModel):
    table_name: str
    description: Optional[str] = None
    columns: List[ColumnSchema]


class ExpectedOutput(BaseModel):
    columns: List[str]
    sample_rows: List[List[Any]]
    total_row_count: int


class BankQuestion(BaseModel):
    id: str
    slug: str
    title: str
    topic_id: str
    topic: str
    difficulty: str  # 'easy', 'medium', 'hard'
    problem_description: str
    database_id: str  # 'db-company', 'db-ecommerce', 'db-university', 'db-banking'
    relevant_tables: List[str]
    table_schemas: List[TableSchemaInfo]
    sample_input_data: Dict[str, List[Dict[str, Any]]]
    expected_output: ExpectedOutput
    starter_code: str
    expected_solution: str
    alternative_solution: Optional[str] = None
    hints: List[str]
    detailed_explanation: str
    related_concepts: List[str]
    order_matters: bool = False
    check_column_names: bool = True
    test_cases: List[TestCase] = Field(default_factory=list)
