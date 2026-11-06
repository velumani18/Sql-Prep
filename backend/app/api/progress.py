from typing import Any, Dict, List, Optional
from fastapi import APIRouter
from app.curriculum.repository import curriculum_repo
from app.question_bank.registry import question_bank_registry
from app.services.progress_service import (
    progress_service,
    ProgressSummaryDTO,
    LevelProgressDTO,
    TopicProgressDTO,
    WeakTopicDTO,
    RecommendedTopicDTO,
    SubmissionRecordDTO,
    BadgeDTO,
)

router = APIRouter(prefix="/api/progress", tags=["User Progress & Motivation System"])


def _get_curriculum_metadata():
    all_q = question_bank_registry.get_all()
    q_by_diff = {
        "easy": [q.id for q in all_q if q.difficulty.lower() == "easy"],
        "medium": [q.id for q in all_q if q.difficulty.lower() == "medium"],
        "hard": [q.id for q in all_q if q.difficulty.lower() == "hard"],
    }

    levels = curriculum_repo.get_levels()
    curriculum_levels = []
    for lvl in levels:
        topics_data = []
        for t in lvl.topics:
            full_t = curriculum_repo.get_topic_by_slug(t.slug)
            q_ids = [q.id for q in full_t.practice_questions] if full_t else []
            topics_data.append({
                "slug": t.slug,
                "title": t.title,
                "question_ids": q_ids,
            })
        curriculum_levels.append({
            "level_number": lvl.level_number,
            "title": lvl.title,
            "description": lvl.description,
            "topics": topics_data,
        })
    return all_q, q_by_diff, curriculum_levels


@router.get("/summary", response_model=ProgressSummaryDTO)
def get_progress_summary() -> ProgressSummaryDTO:
    """
    Returns full data-driven progress summary:
    - Overall learning progress %
    - Progress per curriculum level
    - Progress per topic
    - Solved vs attempted counts and accuracy %
    - Daily streak and 7-day activity timeline
    - Data-driven weak topics with diagnosis
    - Recommended next topic
    - Earned badges and recent submissions.
    """
    all_q, q_by_diff, curriculum_levels = _get_curriculum_metadata()

    return progress_service.get_progress_summary(
        total_questions=len(all_q),
        questions_by_difficulty=q_by_diff,
        curriculum_levels=curriculum_levels,
    )


@router.get("/levels", response_model=List[LevelProgressDTO])
def get_level_progress() -> List[LevelProgressDTO]:
    """Returns progress breakdown across all 6 curriculum levels."""
    summary = get_progress_summary()
    return summary.level_progress


@router.get("/topics", response_model=List[TopicProgressDTO])
def get_topic_progress() -> List[TopicProgressDTO]:
    """Returns progress and completion status for every individual topic."""
    summary = get_progress_summary()
    return summary.topic_progress


@router.get("/weak-topics", response_model=List[WeakTopicDTO])
def get_weak_topics() -> List[WeakTopicDTO]:
    """Returns identified weak topics with failure metrics and actionable remediation steps."""
    summary = get_progress_summary()
    return summary.weak_topics


@router.get("/recommended", response_model=Optional[RecommendedTopicDTO])
def get_recommended_topic() -> Optional[RecommendedTopicDTO]:
    """Returns the smartly recommended next topic based on prerequisites and weak areas."""
    summary = get_progress_summary()
    return summary.recommended_topic


@router.get("/badges", response_model=List[BadgeDTO])
def get_user_badges() -> List[BadgeDTO]:
    """Returns all badges and milestones earned by the user."""
    return progress_service.get_earned_badges()


@router.get("/submissions", response_model=List[SubmissionRecordDTO])
def get_submission_history(limit: int = 20) -> List[SubmissionRecordDTO]:
    """Returns recent submission records with execution metrics and pass counts."""
    return progress_service.get_recent_submissions(limit=limit)


@router.post("/reset")
def reset_progress() -> Dict[str, str]:
    """Resets progress data in persistent storage to demo baseline."""
    progress_service.reset_progress()
    return {"message": "User progress successfully reset in persistent storage."}
