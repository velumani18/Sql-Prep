from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status
from app.curriculum.repository import curriculum_repo
from app.services.progress_service import progress_service

router = APIRouter(prefix="/api/curriculum", tags=["Curriculum & Topics"])


@router.get("/levels", response_model=List[Dict[str, Any]])
def get_curriculum_levels() -> List[Dict[str, Any]]:
    """Returns all 6 curriculum levels with topics and completion indicators."""
    levels = curriculum_repo.get_levels()
    results = []

    for lvl in levels:
        topics_data = []
        completed_in_level = 0
        for topic in lvl.topics:
            is_completed = progress_service.is_topic_completed(topic.slug)
            if is_completed:
                completed_in_level += 1
            topics_data.append({
                "id": topic.id,
                "slug": topic.slug,
                "title": topic.title,
                "order_index": topic.order_index,
                "questions_count": topic.questions_count,
                "database_id": topic.database_id,
                "is_completed": is_completed,
            })

        total_topics = len(lvl.topics)
        pct = int((completed_in_level / total_topics * 100)) if total_topics > 0 else 0

        results.append({
            "level_number": lvl.level_number,
            "slug": lvl.slug,
            "title": lvl.title,
            "subtitle": lvl.subtitle,
            "description": lvl.description,
            "difficulty": lvl.difficulty,
            "estimated_hours": lvl.estimated_hours,
            "total_topics": total_topics,
            "completed_topics": completed_in_level,
            "completion_percentage": pct,
            "topics": topics_data,
        })

    return results


@router.get("/levels/{level_number}", response_model=Dict[str, Any])
def get_level(level_number: int) -> Dict[str, Any]:
    """Retrieves single curriculum level metadata and topic lessons."""
    lvl = curriculum_repo.get_level(level_number)
    if not lvl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curriculum Level {level_number} not found.",
        )
    return lvl.model_dump()


@router.get("/topics/{topic_slug}", response_model=Dict[str, Any])
def get_topic_lesson(topic_slug: str) -> Dict[str, Any]:
    """Retrieves full pedagogical lesson content, syntax, worked examples, and practice questions."""
    lesson = curriculum_repo.get_topic_by_slug(topic_slug)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic '{topic_slug}' not found in curriculum.",
        )

    lesson_dict = lesson.model_dump()
    lesson_dict["is_completed"] = progress_service.is_topic_completed(topic_slug)

    # Attach solved status to each practice question
    for q in lesson_dict.get("practice_questions", []):
        q["is_solved"] = progress_service.is_question_solved(q["id"])

    return lesson_dict


@router.post("/topics/{topic_slug}/complete")
def complete_topic(topic_slug: str) -> Dict[str, Any]:
    """Marks a curriculum topic lesson as completed and awards 100 XP."""
    lesson = curriculum_repo.get_topic_by_slug(topic_slug)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic '{topic_slug}' not found.",
        )

    newly_completed, xp_gain = progress_service.mark_topic_completed(topic_slug)
    user = progress_service.get_current_user_dto()
    return {
        "success": True,
        "topic_slug": topic_slug,
        "is_completed": True,
        "xp_awarded": xp_gain,
        "total_xp": user.xp,
    }

