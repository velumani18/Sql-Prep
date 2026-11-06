from fastapi import APIRouter, HTTPException, status
from app.engine.db_manager import db_manager
from app.engine.evaluator import query_evaluator
from app.engine.types import QueryResult, SubmissionResult
from app.models.execution import ExecuteRequest, SubmitRequest
from app.repositories.question_repo import question_repo
from app.services.progress_service import progress_service

router = APIRouter(prefix="/api/sql", tags=["SQL Execution & Evaluation"])


@router.post("/execute", response_model=QueryResult)
def execute_query(payload: ExecuteRequest) -> QueryResult:
    """
    Executes a user query in a completely isolated, fresh in-memory SQLite database.
    Enforces AST security, statement timeouts, and output limits.
    """
    db = db_manager.get_by_id(payload.database_id)
    if not db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Database '{payload.database_id}' not found.",
        )

    executor = db_manager.get_executor(payload.database_id)
    return executor.execute_query(sql=payload.sql, mode=payload.mode)


@router.post("/submit", response_model=SubmissionResult)
def submit_query(payload: SubmitRequest) -> SubmissionResult:
    """
    Evaluates a user query against all visible and hidden test datasets for the exercise.
    Validates output semantically (handling ordering, multiset comparison, NULLs, and floats).
    Records submission in user progress history and awards XP on acceptance.
    """
    question = question_repo.get_by_id(payload.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question '{payload.question_id}' not found.",
        )

    eval_result = query_evaluator.evaluate_submission(
        question=question,
        submitted_sql=payload.sql,
        mode=payload.mode,
    )

    # Record submission in progress tracker with anti-exploit XP rules
    topic_slug = getattr(question, "topic_slug", None) or getattr(question, "topic", None)
    sub_record, xp_awarded, is_first_solve = progress_service.record_submission(
        question_id=question.id,
        question_title=question.title,
        database_id=question.database_id,
        topic_slug=topic_slug,
        status=eval_result.status,
        submitted_sql=payload.sql,
        execution_time_ms=eval_result.execution_time_ms,
        passed_test_cases=eval_result.passed_test_cases,
        total_test_cases=eval_result.total_test_cases,
        error_message=eval_result.error_message,
        difficulty=question.difficulty,
    )

    eval_result.xp_awarded = xp_awarded
    eval_result.is_first_solve = is_first_solve
    if eval_result.status == "ACCEPTED":
        if is_first_solve:
            eval_result.gamification_message = f"Challenge Solved! +{xp_awarded} XP Awarded."
        else:
            eval_result.gamification_message = "Accepted! (Already Solved: +0 XP duplicate prevention)"

    return eval_result
