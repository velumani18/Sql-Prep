from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.question_bank.registry import question_bank_registry
from app.repositories.question_repo import question_repo
from app.services.progress_service import progress_service

router = APIRouter(prefix="/api/questions", tags=["Practice Questions & Bank"])


@router.get("", response_model=Dict[str, Any])
def list_questions(
    topic_id: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    database_id: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> Dict[str, Any]:
    """
    Returns list of questions with filtering by topic, difficulty, database, and keyword search.
    Enriched with real solved status and company tags for interview practice.
    """
    all_questions = question_bank_registry.get_all()

    # Filter by topic
    if topic_id:
        all_questions = [q for q in all_questions if q.topic_id == topic_id]

    # Filter by difficulty
    if difficulty and difficulty.lower() != "all":
        all_questions = [q for q in all_questions if q.difficulty.lower() == difficulty.lower()]

    # Filter by database
    if database_id and database_id.lower() != "all":
        all_questions = [q for q in all_questions if q.database_id == database_id]

    # Search filter
    if search:
        s_lower = search.lower()
        all_questions = [
            q for q in all_questions
            if s_lower in q.title.lower() or s_lower in q.problem_description.lower() or s_lower in q.topic.lower()
        ]

    total_count = len(all_questions)
    paginated = all_questions[offset : offset + limit]

    # Synthetic company tags map for interview mode
    company_tag_map = {
        "easy": ["Amazon", "Meta"],
        "medium": ["Google", "Stripe", "Uber"],
        "hard": ["Netflix", "Databricks", "Snowflake"],
    }

    results = []
    for q in paginated:
        is_solved = progress_service.is_question_solved(q.id)
        results.append({
            "id": q.id,
            "slug": q.slug,
            "title": q.title,
            "topic_id": q.topic_id,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "database_id": q.database_id,
            "relevant_tables": q.relevant_tables,
            "is_solved": is_solved,
            "acceptance_rate": 84.5 if q.difficulty == "easy" else (62.3 if q.difficulty == "medium" else 41.2),
            "company_tags": company_tag_map.get(q.difficulty.lower(), ["Tech"]),
        })

    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "questions": results,
    }


@router.get("/{question_id}", response_model=Dict[str, Any])
def get_question(question_id: str) -> Dict[str, Any]:
    """
    Returns complete rich question workspace payload: description, database ID,
    relevant tables, schemas, sample input data, expected output, public test cases, hints, and explanations.
    """
    bank_q = question_bank_registry.get_by_id(question_id)
    if not bank_q:
        # Fallback to legacy repo
        legacy_q = question_repo.get_by_id(question_id)
        if not legacy_q:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question '{question_id}' not found.",
            )
        return {
            "id": legacy_q.id,
            "slug": legacy_q.slug,
            "title": legacy_q.title,
            "difficulty": legacy_q.difficulty,
            "database_id": legacy_q.database_id,
            "prompt": legacy_q.prompt,
            "starter_code": legacy_q.starter_code,
            "order_matters": legacy_q.order_matters,
            "check_column_names": legacy_q.check_column_names,
            "is_solved": progress_service.is_question_solved(legacy_q.id),
            "test_cases": [
                {
                    "id": tc.id,
                    "name": tc.name,
                    "description": tc.description,
                    "is_hidden": tc.is_hidden,
                }
                for tc in legacy_q.test_cases
            ],
            "hints": [],
            "detailed_explanation": "Solve the problem using standard relational SQL.",
            "related_concepts": ["SQL"],
        }

    # Protect hidden test case seed SQL statements from being leaked
    sanitized_test_cases = [
        {
            "id": tc.id,
            "name": tc.name,
            "description": tc.description,
            "is_hidden": tc.is_hidden,
        }
        for tc in bank_q.test_cases
    ]

    return {
        "id": bank_q.id,
        "slug": bank_q.slug,
        "title": bank_q.title,
        "topic_id": bank_q.topic_id,
        "topic": bank_q.topic,
        "difficulty": bank_q.difficulty,
        "database_id": bank_q.database_id,
        "prompt": bank_q.problem_description,
        "relevant_tables": bank_q.relevant_tables,
        "table_schemas": [t.model_dump() for t in bank_q.table_schemas],
        "sample_input_data": bank_q.sample_input_data,
        "expected_output": bank_q.expected_output.model_dump(),
        "starter_code": bank_q.starter_code,
        "hints": bank_q.hints,
        "detailed_explanation": bank_q.detailed_explanation,
        "related_concepts": bank_q.related_concepts,
        "order_matters": bank_q.order_matters,
        "check_column_names": bank_q.check_column_names,
        "is_solved": progress_service.is_question_solved(bank_q.id),
        "test_cases": sanitized_test_cases,
    }


@router.get("/{question_id}/solution", response_model=Dict[str, Any])
def get_question_solution(question_id: str) -> Dict[str, Any]:
    """Returns official verified solution and alternative solution for unlocked viewing."""
    bank_q = question_bank_registry.get_by_id(question_id)
    if not bank_q:
        legacy_q = question_repo.get_by_id(question_id)
        if not legacy_q:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question '{question_id}' not found.",
            )
        return {
            "id": legacy_q.id,
            "solution_sql": legacy_q.solution_sql,
            "alternative_solution": None,
            "detailed_explanation": "Official reference solution.",
        }

    return {
        "id": bank_q.id,
        "title": bank_q.title,
        "solution_sql": bank_q.expected_solution,
        "alternative_solution": bank_q.alternative_solution,
        "detailed_explanation": bank_q.detailed_explanation,
    }
