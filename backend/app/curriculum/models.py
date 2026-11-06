from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class WorkedExample(BaseModel):
    title: str
    explanation: str
    sql: str
    columns: List[str]
    rows: List[List[Any]]

class CommonMistake(BaseModel):
    pitfall: str
    explanation: str
    incorrect_sql: Optional[str] = None
    corrected_sql: Optional[str] = None

class PracticeQuestion(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str  # easy, medium, hard
    prompt: str
    starter_sql: str
    solution_sql: str
    hints: List[str] = Field(default_factory=list)
    order_matters: bool = False
    check_column_names: bool = True

class ClauseExplanation(BaseModel):
    keyword: str
    purpose: str
    notes: Optional[str] = None

class TopicLesson(BaseModel):
    id: str
    slug: str
    level_number: int
    level_title: str
    title: str
    order_index: int
    database_id: str
    database_name: str
    learning_objectives: List[str]
    prerequisites: List[str]
    detailed_explanation: str
    syntax_reference: str
    clause_breakdown: List[ClauseExplanation]
    worked_examples: List[WorkedExample]
    common_mistakes: List[CommonMistake]
    real_world_use_cases: List[str]
    practice_questions: List[PracticeQuestion]

class TopicSummary(BaseModel):
    id: str
    slug: str
    title: str
    order_index: int
    questions_count: int
    database_id: str

class CurriculumLevel(BaseModel):
    level_number: int
    slug: str
    title: str
    subtitle: str
    description: str
    difficulty: str
    estimated_hours: int
    topics: List[TopicSummary]
