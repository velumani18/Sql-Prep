import logging
from datetime import datetime, date, timedelta, timezone
from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.session import SessionLocal, init_db
from app.db.models import (
    User,
    UserTopicProgress,
    UserQuestionStatus,
    Submission,
    Badge,
    LevelMilestone,
    utcnow,
)

logger = logging.getLogger("sqlforge.progress")

# Badge Metadata Configuration
TOPIC_BADGES = {
    "select-distinct-projection": {
        "title": "Projection Pioneer",
        "description": "Mastered column projections, SELECT queries, and DISTINCT deduplication.",
        "icon": "Compass",
    },
    "where-filtering-operators": {
        "title": "Filter Specialist",
        "description": "Mastered WHERE clauses, numeric boundaries, string comparisons, and boolean filtering.",
        "icon": "Filter",
    },
    "in-between-like-pattern-matching": {
        "title": "Logic Artisan",
        "description": "Mastered AND/OR logic, set membership with IN, range searches, and LIKE wildcards.",
        "icon": "Zap",
    },
    "sorting-pagination-null-handling": {
        "title": "Pagination Pro",
        "description": "Mastered ORDER BY sorting, LIMIT, OFFSET pagination, and deterministic tie-breaking.",
        "icon": "ArrowDownUp",
    },
    "aggregate-functions-foundations": {
        "title": "Aggregation Champion",
        "description": "Mastered COUNT, SUM, AVG, MIN, MAX, and dataset summary statistics.",
        "icon": "Calculator",
    },
    "group-by-having-clauses": {
        "title": "Grouping Guru",
        "description": "Mastered multi-column grouping and distinguishing WHERE from post-aggregate HAVING clauses.",
        "icon": "Layers",
    },
    "case-when-conditional-aggregation": {
        "title": "Conditional Maestro",
        "description": "Mastered CASE WHEN branching, COALESCE null fallbacks, and conditional aggregation pivots.",
        "icon": "GitFork",
    },
    "inner-and-left-outer-joins": {
        "title": "Join Architect",
        "description": "Mastered INNER JOIN, LEFT JOIN, foreign key navigation, and anti-join data isolation.",
        "icon": "Link2",
    },
    "self-joins-cross-joins-unions": {
        "title": "Hierarchy Virtuoso",
        "description": "Mastered hierarchical self joins, Cartesian products, and set unification with UNION.",
        "icon": "Workflow",
    },
    "subqueries-and-exists": {
        "title": "Subquery Strategist",
        "description": "Mastered nested subqueries, scalar expressions, and correlated EXISTS predicates.",
        "icon": "Box",
    },
}

LEVEL_MILESTONES = {
    1: {"title": "Level 1 Milestone: Fundamentals Certified", "xp": 250, "icon": "Award"},
    2: {"title": "Level 2 Milestone: Aggregations Certified", "xp": 250, "icon": "BarChart3"},
    3: {"title": "Level 3 Milestone: Relational Pioneer", "xp": 250, "icon": "Database"},
    4: {"title": "Level 4 Milestone: Advanced Analytics Certified", "xp": 250, "icon": "Cpu"},
    5: {"title": "Level 5 Milestone: Window Functions Certified", "xp": 250, "icon": "Sparkles"},
    6: {"title": "Level 6 Milestone: Database Systems Architect", "xp": 250, "icon": "ShieldCheck"},
}

STREAK_MILESTONES = {
    3: {"key": "badge_streak_3", "title": "3-Day Consistency", "desc": "Completed SQL practice for 3 days in a row.", "icon": "Flame"},
    7: {"key": "badge_streak_7", "title": "Weekly Habit", "desc": "Maintained an active query streak for a full week.", "icon": "Flame"},
    14: {"key": "badge_streak_14", "title": "Fortnight Dedication", "desc": "Completed two continuous weeks of SQL practice.", "icon": "Flame"},
    30: {"key": "badge_streak_30", "title": "Monthly Mastery", "desc": "Maintained a 30-day continuous learning streak.", "icon": "Crown"},
}


class UserProfileDTO(BaseModel):
    id: str
    name: str
    email: str
    avatar_url: str
    streak_days: int
    longest_streak: int
    xp: int
    level_title: str
    rank_level: int
    next_rank_xp: int
    rank_progress_percentage: int
    last_active: Optional[str] = None


class SubmissionRecordDTO(BaseModel):
    id: str
    user_id: str
    question_id: str
    question_title: str
    database_id: str
    topic_slug: Optional[str] = None
    difficulty: str
    status: str
    submitted_sql: str
    execution_time_ms: float
    passed_test_cases: int
    total_test_cases: int
    xp_awarded: int
    error_message: Optional[str] = None
    created_at: str


class BadgeDTO(BaseModel):
    key: str
    title: str
    description: str
    badge_type: str  # topic, level_milestone, streak
    icon: str
    earned_at: str


class LevelProgressDTO(BaseModel):
    level_number: int
    title: str
    description: Optional[str] = None
    total_topics: int
    completed_topics: int
    total_questions: int
    solved_questions: int
    completion_percentage: int
    is_completed: bool
    milestone_badge: Optional[BadgeDTO] = None


class TopicProgressDTO(BaseModel):
    topic_slug: str
    title: str
    level_number: int
    level_title: str
    is_completed: bool
    total_questions: int
    attempted_questions: int
    solved_questions: int
    completion_rate: int
    accuracy_rate: int
    badge: Optional[BadgeDTO] = None


class WeakTopicDTO(BaseModel):
    topic_slug: str
    title: str
    level_number: int
    failed_attempts_count: int
    unsolved_questions_count: int
    accuracy_percentage: int
    reason: str
    recommended_action: str
    lesson_url: str
    practice_url: str


class RecommendedTopicDTO(BaseModel):
    topic_slug: str
    title: str
    level_number: int
    level_title: str
    reason: str
    recommended_action: str  # 'continue_curriculum' or 'review_weak_topic'
    lesson_url: str
    practice_url: str


class DailyActivityDTO(BaseModel):
    date: str
    day_name: str
    submissions_count: int
    active: bool


class ProgressSummaryDTO(BaseModel):
    user: UserProfileDTO
    overall_progress_percentage: int
    total_questions: int
    solved_questions_count: int
    attempted_questions_count: int
    easy_solved: int
    easy_total: int
    medium_solved: int
    medium_total: int
    hard_solved: int
    hard_total: int
    total_submissions: int
    accepted_submissions: int
    submission_accuracy_percentage: int
    question_accuracy_percentage: int
    total_topics_count: int
    completed_topics_count: int
    level_progress: List[LevelProgressDTO]
    topic_progress: List[TopicProgressDTO]
    weak_topics: List[WeakTopicDTO]
    recommended_topic: Optional[RecommendedTopicDTO] = None
    recent_submissions: List[SubmissionRecordDTO]
    badges: List[BadgeDTO]
    weekly_activity: List[DailyActivityDTO]


class ProgressService:
    """
    Data-driven persistent progress service backed by PostgreSQL / SQLite.
    Tracks questions, submissions, topics, streaks, XP, badges, and weak areas.
    """

    def __init__(self):
        # Initialize schema and seed data on startup
        init_db()

    def _get_rank_info(self, xp: int) -> Tuple[str, int, int, int]:
        """Calculates rank title, rank level, target XP for next rank, and progress %."""
        thresholds = [
            (1, "SQL Apprentice", 0, 300),
            (2, "Query Practitioner", 300, 800),
            (3, "Relational Specialist", 800, 1500),
            (4, "Senior Query Engineer", 1500, 2500),
            (5, "SQL Architect", 2500, 5000),
        ]

        for lvl, title, min_xp, max_xp in thresholds:
            if xp < max_xp:
                pct = int(((xp - min_xp) / (max_xp - min_xp)) * 100)
                return title, lvl, max_xp, min(max(pct, 0), 100)

        return "SQL Architect", 5, 5000, 100

    def get_or_create_user(self, db: Session, user_id: str = "usr-demo") -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            today_str = date.today().isoformat()
            user = User(
                id=user_id,
                email="alex.dev@sqlforge.dev",
                name="Alex Developer",
                xp=0,
                streak_days=1,
                longest_streak=1,
                last_activity_date=today_str,
                level_title="SQL Apprentice",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def authenticate_demo(
        self, email: str = "alex.dev@sqlforge.dev", name: str = "Alex Developer", user_id: str = "usr-demo"
    ) -> UserProfileDTO:
        with SessionLocal() as db:
            user = self.get_or_create_user(db, user_id)
            user.email = email
            user.name = name
            user.updated_at = utcnow()
            db.commit()
            return self._build_user_dto(user)

    def _build_user_dto(self, user: User) -> UserProfileDTO:
        rank_title, rank_level, next_xp, rank_pct = self._get_rank_info(user.xp)
        return UserProfileDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar_url=user.avatar_url or "",
            streak_days=user.streak_days,
            longest_streak=user.longest_streak,
            xp=user.xp,
            level_title=rank_title,
            rank_level=rank_level,
            next_rank_xp=next_xp,
            rank_progress_percentage=rank_pct,
            last_active=user.updated_at.isoformat() if user.updated_at else None,
        )

    def get_current_user_dto(self, user_id: str = "usr-demo") -> UserProfileDTO:
        with SessionLocal() as db:
            user = self.get_or_create_user(db, user_id)
            return self._build_user_dto(user)

    def _update_streak(self, db: Session, user: User) -> None:
        """Maintains daily streak based on calendar date difference."""
        today = date.today()
        today_str = today.isoformat()

        if not user.last_activity_date:
            user.streak_days = 1
            user.longest_streak = max(user.longest_streak, 1)
            user.last_activity_date = today_str
            return

        try:
            last_date = date.fromisoformat(user.last_activity_date)
        except Exception:
            last_date = today

        delta = (today - last_date).days

        if delta == 0:
            # Already active today; streak maintained
            pass
        elif delta == 1:
            # Active consecutive day; increment streak
            user.streak_days += 1
            user.longest_streak = max(user.longest_streak, user.streak_days)
            user.last_activity_date = today_str
        else:
            # Missed a day or more; reset streak to 1
            user.streak_days = 1
            user.last_activity_date = today_str

        # Check streak milestone badges
        for days, info in STREAK_MILESTONES.items():
            if user.streak_days >= days:
                badge_key = info["key"]
                existing = db.query(Badge).filter(Badge.user_id == user.id, Badge.badge_key == badge_key).first()
                if not existing:
                    new_badge = Badge(
                        user_id=user.id,
                        badge_key=badge_key,
                        title=info["title"],
                        description=info["desc"],
                        badge_type="streak",
                        icon=info["icon"],
                        earned_at=utcnow(),
                    )
                    db.add(new_badge)

    def is_question_solved(self, question_id: str, user_id: str = "usr-demo") -> bool:
        with SessionLocal() as db:
            status = (
                db.query(UserQuestionStatus)
                .filter(UserQuestionStatus.user_id == user_id, UserQuestionStatus.question_id == question_id)
                .first()
            )
            return status.is_solved if status else False

    def is_topic_completed(self, topic_slug: str, user_id: str = "usr-demo") -> bool:
        with SessionLocal() as db:
            prog = (
                db.query(UserTopicProgress)
                .filter(UserTopicProgress.user_id == user_id, UserTopicProgress.topic_slug == topic_slug)
                .first()
            )
            return prog.is_completed if prog else False

    def mark_topic_completed(self, topic_slug: str, user_id: str = "usr-demo") -> Tuple[bool, int]:
        """
        Marks topic completed. Awards +100 XP and topic badge on first completion.
        Returns (newly_completed, xp_awarded).
        """
        with SessionLocal() as db:
            user = self.get_or_create_user(db, user_id)
            self._update_streak(db, user)

            prog = (
                db.query(UserTopicProgress)
                .filter(UserTopicProgress.user_id == user_id, UserTopicProgress.topic_slug == topic_slug)
                .first()
            )

            if prog and prog.is_completed:
                # Already completed; no duplicate XP
                return False, 0

            if not prog:
                prog = UserTopicProgress(
                    user_id=user_id,
                    topic_slug=topic_slug,
                    is_completed=True,
                    completed_at=utcnow(),
                )
                db.add(prog)
            else:
                prog.is_completed = True
                prog.completed_at = utcnow()

            # Award topic completion XP
            xp_gain = 100
            user.xp += xp_gain
            rank_title, _, _, _ = self._get_rank_info(user.xp)
            user.level_title = rank_title
            user.updated_at = utcnow()

            # Award Topic Badge if configured
            badge_info = TOPIC_BADGES.get(topic_slug)
            if badge_info:
                badge_key = f"badge_topic_{topic_slug.replace('-', '_')}"
                existing_badge = db.query(Badge).filter(Badge.user_id == user_id, Badge.badge_key == badge_key).first()
                if not existing_badge:
                    db.add(
                        Badge(
                            user_id=user_id,
                            badge_key=badge_key,
                            title=badge_info["title"],
                            description=badge_info["description"],
                            badge_type="topic",
                            icon=badge_info["icon"],
                            earned_at=utcnow(),
                        )
                    )

            db.commit()
            return True, xp_gain

    def record_submission(
        self,
        question_id: str,
        question_title: str,
        database_id: str,
        status: str,
        submitted_sql: str,
        execution_time_ms: float,
        passed_test_cases: int,
        total_test_cases: int,
        error_message: Optional[str] = None,
        difficulty: str = "easy",
        topic_slug: Optional[str] = None,
        user_id: str = "usr-demo",
    ) -> Tuple[SubmissionRecordDTO, int, bool]:
        """
        Records submission and applies anti-exploit XP rules:
        - Only awards XP on FIRST successful solve.
        - Repeated submissions on already solved questions give +0 XP.
        Returns: (SubmissionRecordDTO, xp_awarded, is_first_solve).
        """
        with SessionLocal() as db:
            user = self.get_or_create_user(db, user_id)
            self._update_streak(db, user)

            # Check existing question status
            q_status = (
                db.query(UserQuestionStatus)
                .filter(UserQuestionStatus.user_id == user_id, UserQuestionStatus.question_id == question_id)
                .first()
            )

            is_first_solve = False
            xp_awarded = 0

            if not q_status:
                q_status = UserQuestionStatus(
                    user_id=user_id,
                    question_id=question_id,
                    topic_slug=topic_slug,
                    difficulty=difficulty.lower(),
                    attempts_count=1,
                    failed_attempts_count=0 if status == "ACCEPTED" else 1,
                    last_status=status,
                    last_submitted_sql=submitted_sql,
                    updated_at=utcnow(),
                )
                if status == "ACCEPTED":
                    q_status.is_solved = True
                    q_status.first_solved_at = utcnow()
                    is_first_solve = True
                db.add(q_status)
            else:
                q_status.attempts_count += 1
                q_status.last_status = status
                q_status.last_submitted_sql = submitted_sql
                q_status.updated_at = utcnow()
                if topic_slug:
                    q_status.topic_slug = topic_slug

                if status == "ACCEPTED":
                    if not q_status.is_solved:
                        q_status.is_solved = True
                        q_status.first_solved_at = utcnow()
                        is_first_solve = True
                else:
                    q_status.failed_attempts_count += 1

            # XP calculation: anti-exploit rule enforces XP is only granted on first solve
            if is_first_solve:
                diff_lower = difficulty.lower()
                xp_awarded = 20 if diff_lower == "easy" else (50 if diff_lower == "medium" else 100)
                user.xp += xp_awarded
                rank_title, _, _, _ = self._get_rank_info(user.xp)
                user.level_title = rank_title

            user.updated_at = utcnow()

            # Generate unique submission ID
            total_subs_count = db.query(Submission).count()
            sub_id = f"sub-{total_subs_count + 1001}"

            submission = Submission(
                id=sub_id,
                user_id=user_id,
                question_id=question_id,
                question_title=question_title,
                database_id=database_id,
                topic_slug=topic_slug,
                difficulty=difficulty.lower(),
                status=status,
                submitted_sql=submitted_sql,
                execution_time_ms=execution_time_ms,
                passed_test_cases=passed_test_cases,
                total_test_cases=total_test_cases,
                error_message=error_message,
                xp_awarded=xp_awarded,
                created_at=utcnow(),
            )
            db.add(submission)
            db.commit()

            sub_dto = SubmissionRecordDTO(
                id=submission.id,
                user_id=submission.user_id,
                question_id=submission.question_id,
                question_title=submission.question_title,
                database_id=submission.database_id,
                topic_slug=submission.topic_slug,
                difficulty=submission.difficulty,
                status=submission.status,
                submitted_sql=submission.submitted_sql,
                execution_time_ms=submission.execution_time_ms,
                passed_test_cases=submission.passed_test_cases,
                total_test_cases=submission.total_test_cases,
                xp_awarded=submission.xp_awarded,
                error_message=submission.error_message,
                created_at=submission.created_at.isoformat(),
            )

            return sub_dto, xp_awarded, is_first_solve

    def get_recent_submissions(self, limit: int = 20, user_id: str = "usr-demo") -> List[SubmissionRecordDTO]:
        with SessionLocal() as db:
            subs = (
                db.query(Submission)
                .filter(Submission.user_id == user_id)
                .order_by(desc(Submission.created_at))
                .limit(limit)
                .all()
            )
            return [
                SubmissionRecordDTO(
                    id=s.id,
                    user_id=s.user_id,
                    question_id=s.question_id,
                    question_title=s.question_title,
                    database_id=s.database_id,
                    topic_slug=s.topic_slug,
                    difficulty=s.difficulty,
                    status=s.status,
                    submitted_sql=s.submitted_sql,
                    execution_time_ms=s.execution_time_ms,
                    passed_test_cases=s.passed_test_cases,
                    total_test_cases=s.total_test_cases,
                    xp_awarded=s.xp_awarded,
                    error_message=s.error_message,
                    created_at=s.created_at.isoformat(),
                )
                for s in subs
            ]

    def get_earned_badges(self, user_id: str = "usr-demo") -> List[BadgeDTO]:
        with SessionLocal() as db:
            badges = db.query(Badge).filter(Badge.user_id == user_id).order_by(desc(Badge.earned_at)).all()
            return [
                BadgeDTO(
                    key=b.badge_key,
                    title=b.title,
                    description=b.description,
                    badge_type=b.badge_type,
                    icon=b.icon,
                    earned_at=b.earned_at.isoformat(),
                )
                for b in badges
            ]

    def _get_weekly_activity(self, db: Session, user_id: str) -> List[DailyActivityDTO]:
        """Builds a 7-day activity timeline ending today."""
        today = date.today()
        activity_list: List[DailyActivityDTO] = []

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i in range(6, -1, -1):
            target_date = today - timedelta(days=i)
            target_str = target_date.isoformat()

            # Count submissions for this day
            start_dt = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=timezone.utc)
            end_dt = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, tzinfo=timezone.utc)

            subs_count = (
                db.query(Submission)
                .filter(Submission.user_id == user_id, Submission.created_at >= start_dt, Submission.created_at <= end_dt)
                .count()
            )

            activity_list.append(
                DailyActivityDTO(
                    date=target_str,
                    day_name=day_names[target_date.weekday()],
                    submissions_count=subs_count,
                    active=(subs_count > 0 or (i == 0 and True)),  # mark active today if on streak
                )
            )

        return activity_list

    def get_progress_summary(
        self,
        total_questions: int,
        questions_by_difficulty: Dict[str, List[str]],
        curriculum_levels: List[Dict],
        user_id: str = "usr-demo",
    ) -> ProgressSummaryDTO:
        with SessionLocal() as db:
            user = self.get_or_create_user(db, user_id)
            user_dto = self._build_user_dto(user)

            # Solved & attempted question statuses
            all_statuses = db.query(UserQuestionStatus).filter(UserQuestionStatus.user_id == user_id).all()
            solved_q_ids = {s.question_id for s in all_statuses if s.is_solved}
            attempted_q_ids = {s.question_id for s in all_statuses if s.attempts_count > 0}

            easy_ids = set(questions_by_difficulty.get("easy", []))
            medium_ids = set(questions_by_difficulty.get("medium", []))
            hard_ids = set(questions_by_difficulty.get("hard", []))

            easy_solved = len(solved_q_ids.intersection(easy_ids))
            medium_solved = len(solved_q_ids.intersection(medium_ids))
            hard_solved = len(solved_q_ids.intersection(hard_ids))
            total_solved = len(solved_q_ids)
            total_attempted = len(attempted_q_ids)

            # Submissions metrics
            all_submissions = db.query(Submission).filter(Submission.user_id == user_id).all()
            total_subs = len(all_submissions)
            accepted_subs = sum(1 for s in all_submissions if s.status == "ACCEPTED")
            sub_accuracy = int((accepted_subs / total_subs * 100)) if total_subs > 0 else 100
            q_accuracy = int((total_solved / total_attempted * 100)) if total_attempted > 0 else 100

            # Topic progress & level progress
            all_topic_prog = db.query(UserTopicProgress).filter(UserTopicProgress.user_id == user_id).all()
            completed_topic_slugs = {tp.topic_slug for tp in all_topic_prog if tp.is_completed}

            # Map badges by key
            earned_badges_db = db.query(Badge).filter(Badge.user_id == user_id).all()
            badges_map = {b.badge_key: b for b in earned_badges_db}

            level_progress_list: List[LevelProgressDTO] = []
            topic_progress_list: List[TopicProgressDTO] = []

            total_curriculum_topics = 0
            completed_curriculum_topics = 0

            for lvl in curriculum_levels:
                lvl_num = lvl["level_number"]
                lvl_title = lvl["title"]
                lvl_desc = lvl.get("description", "")
                topics_in_lvl = lvl.get("topics", [])

                total_lvl_topics = len(topics_in_lvl)
                completed_lvl_topics = 0
                lvl_total_questions = 0
                lvl_solved_questions = 0

                total_curriculum_topics += total_lvl_topics

                for top in topics_in_lvl:
                    t_slug = top["slug"]
                    t_title = top["title"]
                    q_ids = top.get("question_ids", [])
                    t_total_q = len(q_ids)
                    lvl_total_questions += t_total_q

                    t_solved_q = len(solved_q_ids.intersection(set(q_ids)))
                    lvl_solved_questions += t_solved_q

                    t_attempted_q = len(attempted_q_ids.intersection(set(q_ids)))

                    is_top_completed = t_slug in completed_topic_slugs
                    if is_top_completed:
                        completed_lvl_topics += 1
                        completed_curriculum_topics += 1

                    t_comp_rate = int((t_solved_q / t_total_q * 100)) if t_total_q > 0 else (100 if is_top_completed else 0)
                    t_acc_rate = int((t_solved_q / t_attempted_q * 100)) if t_attempted_q > 0 else 100

                    badge_key = f"badge_topic_{t_slug.replace('-', '_')}"
                    top_badge = None
                    if badge_key in badges_map:
                        b = badges_map[badge_key]
                        top_badge = BadgeDTO(
                            key=b.badge_key,
                            title=b.title,
                            description=b.description,
                            badge_type=b.badge_type,
                            icon=b.icon,
                            earned_at=b.earned_at.isoformat(),
                        )

                    topic_progress_list.append(
                        TopicProgressDTO(
                            topic_slug=t_slug,
                            title=t_title,
                            level_number=lvl_num,
                            level_title=lvl_title,
                            is_completed=is_top_completed,
                            total_questions=t_total_q,
                            attempted_questions=t_attempted_q,
                            solved_questions=t_solved_q,
                            completion_rate=t_comp_rate,
                            accuracy_rate=t_acc_rate,
                            badge=top_badge,
                        )
                    )

                is_lvl_completed = total_lvl_topics > 0 and completed_lvl_topics == total_lvl_topics
                lvl_pct = int((completed_lvl_topics / total_lvl_topics * 100)) if total_lvl_topics > 0 else 0

                milestone_key = f"milestone_level_{lvl_num}"
                lvl_badge = None
                if milestone_key in badges_map:
                    b = badges_map[milestone_key]
                    lvl_badge = BadgeDTO(
                        key=b.badge_key,
                        title=b.title,
                        description=b.description,
                        badge_type=b.badge_type,
                        icon=b.icon,
                        earned_at=b.earned_at.isoformat(),
                    )

                level_progress_list.append(
                    LevelProgressDTO(
                        level_number=lvl_num,
                        title=lvl_title,
                        description=lvl_desc,
                        total_topics=total_lvl_topics,
                        completed_topics=completed_lvl_topics,
                        total_questions=lvl_total_questions,
                        solved_questions=lvl_solved_questions,
                        completion_percentage=lvl_pct,
                        is_completed=is_lvl_completed,
                        milestone_badge=lvl_badge,
                    )
                )

            # Overall progress calculation
            topic_weight = 0.5
            question_weight = 0.5
            topic_pct = (completed_curriculum_topics / total_curriculum_topics * 100) if total_curriculum_topics > 0 else 0
            question_pct = (total_solved / total_questions * 100) if total_questions > 0 else 0
            overall_pct = int(topic_pct * topic_weight + question_pct * question_weight)

            # Weak-Topic Identification (Data-Driven)
            weak_topics: List[WeakTopicDTO] = []
            topic_by_slug = {t.topic_slug: t for t in topic_progress_list}

            # Group failures and attempts per topic
            topic_attempts: Dict[str, int] = {}
            topic_fails: Dict[str, int] = {}

            for s in all_statuses:
                t_slug = s.topic_slug
                if not t_slug:
                    continue
                topic_attempts[t_slug] = topic_attempts.get(t_slug, 0) + s.attempts_count
                topic_fails[t_slug] = topic_fails.get(t_slug, 0) + s.failed_attempts_count

            for t_slug, fails in topic_fails.items():
                attempts = topic_attempts.get(t_slug, fails)
                t_info = topic_by_slug.get(t_slug)
                if not t_info:
                    continue

                fail_rate = (fails / attempts) if attempts > 0 else 0.0
                unsolved = t_info.total_questions - t_info.solved_questions

                # Condition for weak topic: multiple failures or low accuracy
                if fails >= 1 and (fail_rate >= 0.3 or unsolved > 0):
                    accuracy = int((1.0 - fail_rate) * 100)
                    weak_topics.append(
                        WeakTopicDTO(
                            topic_slug=t_slug,
                            title=t_info.title,
                            level_number=t_info.level_number,
                            failed_attempts_count=fails,
                            unsolved_questions_count=unsolved,
                            accuracy_percentage=max(accuracy, 0),
                            reason=f"Recorded {fails} failed execution attempts with {unsolved} unsolved challenges.",
                            recommended_action=f"Review '{t_info.title}' lesson theory and re-test syntax edge cases.",
                            lesson_url=f"/lesson/{t_slug}",
                            practice_url=f"/practice/{t_slug}",
                        )
                    )

            # Sort weak topics by failed attempts count descending
            weak_topics.sort(key=lambda w: w.failed_attempts_count, reverse=True)

            # Recommended Next Topic Engine
            recommended: Optional[RecommendedTopicDTO] = None
            if weak_topics:
                # Prioritize reinforcing weak topic
                wt = weak_topics[0]
                recommended = RecommendedTopicDTO(
                    topic_slug=wt.topic_slug,
                    title=wt.title,
                    level_number=wt.level_number,
                    level_title=f"Level {wt.level_number}",
                    reason=f"Recommended for reinforcement: Address challenging edge cases in {wt.title} to solidify fundamentals.",
                    recommended_action="review_weak_topic",
                    lesson_url=wt.lesson_url,
                    practice_url=wt.practice_url,
                )
            else:
                # Next incomplete topic in chronological curriculum sequence
                for t in topic_progress_list:
                    if not t.is_completed:
                        recommended = RecommendedTopicDTO(
                            topic_slug=t.topic_slug,
                            title=t.title,
                            level_number=t.level_number,
                            level_title=t.level_title,
                            reason=f"Next step in curriculum: Master {t.title} to advance your Level {t.level_number} progression.",
                            recommended_action="continue_curriculum",
                            lesson_url=f"/lesson/{t.topic_slug}",
                            practice_url=f"/practice/{t.topic_slug}",
                        )
                        break

            # If all topics completed, recommend advanced practice
            if not recommended and topic_progress_list:
                first_t = topic_progress_list[0]
                recommended = RecommendedTopicDTO(
                    topic_slug=first_t.topic_slug,
                    title="Curriculum Completed!",
                    level_number=6,
                    level_title="Mastery",
                    reason="Outstanding! You have mastered all structured topics. Continue practicing hard interview queries.",
                    recommended_action="continue_curriculum",
                    lesson_url="/curriculum",
                    practice_url="/practice/q-070",
                )

            # Recent submissions and weekly activity
            recent_subs = (
                db.query(Submission)
                .filter(Submission.user_id == user_id)
                .order_by(desc(Submission.created_at))
                .limit(10)
                .all()
            )
            recent_dto = [
                SubmissionRecordDTO(
                    id=s.id,
                    user_id=s.user_id,
                    question_id=s.question_id,
                    question_title=s.question_title,
                    database_id=s.database_id,
                    topic_slug=s.topic_slug,
                    difficulty=s.difficulty,
                    status=s.status,
                    submitted_sql=s.submitted_sql,
                    execution_time_ms=s.execution_time_ms,
                    passed_test_cases=s.passed_test_cases,
                    total_test_cases=s.total_test_cases,
                    xp_awarded=s.xp_awarded,
                    error_message=s.error_message,
                    created_at=s.created_at.isoformat(),
                )
                for s in recent_subs
            ]

            badges_dto = [
                BadgeDTO(
                    key=b.badge_key,
                    title=b.title,
                    description=b.description,
                    badge_type=b.badge_type,
                    icon=b.icon,
                    earned_at=b.earned_at.isoformat(),
                )
                for b in earned_badges_db
            ]

            weekly_act = self._get_weekly_activity(db, user_id)

            return ProgressSummaryDTO(
                user=user_dto,
                overall_progress_percentage=overall_pct,
                total_questions=total_questions,
                solved_questions_count=total_solved,
                attempted_questions_count=total_attempted,
                easy_solved=easy_solved,
                easy_total=len(easy_ids),
                medium_solved=medium_solved,
                medium_total=len(medium_ids),
                hard_solved=hard_solved,
                hard_total=len(hard_ids),
                total_submissions=total_subs,
                accepted_submissions=accepted_subs,
                submission_accuracy_percentage=sub_accuracy,
                question_accuracy_percentage=q_accuracy,
                total_topics_count=total_curriculum_topics,
                completed_topics_count=completed_curriculum_topics,
                level_progress=level_progress_list,
                topic_progress=topic_progress_list,
                weak_topics=weak_topics,
                recommended_topic=recommended,
                recent_submissions=recent_dto,
                badges=badges_dto,
                weekly_activity=weekly_act,
            )

    def reset_progress(self, user_id: str = "usr-demo") -> None:
        """Resets user progress to initial demo baseline."""
        with SessionLocal() as db:
            db.query(Submission).filter(Submission.user_id == user_id).delete()
            db.query(UserQuestionStatus).filter(UserQuestionStatus.user_id == user_id).delete()
            db.query(UserTopicProgress).filter(UserTopicProgress.user_id == user_id).delete()
            db.query(Badge).filter(Badge.user_id == user_id).delete()
            db.query(LevelMilestone).filter(LevelMilestone.user_id == user_id).delete()
            db.query(User).filter(User.id == user_id).delete()
            db.commit()

            # Re-seed baseline demo state
            from app.db.session import seed_demo_data_if_empty
            seed_demo_data_if_empty(db)


progress_service = ProgressService()
