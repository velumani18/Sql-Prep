from typing import Optional
from pydantic import BaseModel, Field
from app.engine.types import ExecutionMode

class ExecuteRequest(BaseModel):
    database_id: str = Field(..., description="Target synthetic database identifier")
    sql: str = Field(..., description="SQL statement to execute")
    mode: ExecutionMode = Field(default=ExecutionMode.READ_ONLY, description="Execution safety mode")

class SubmitRequest(BaseModel):
    question_id: str = Field(..., description="Target exercise question ID or slug")
    sql: str = Field(..., description="Submitted SQL query to evaluate")
    mode: ExecutionMode = Field(default=ExecutionMode.READ_ONLY, description="Execution safety mode")

