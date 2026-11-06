import os
import logging
from datetime import datetime, timezone, date, timedelta
from typing import Generator
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from .models import (
    Base,
    User,
    UserTopicProgress,
    UserQuestionStatus,
    Submission,
    Badge,
    LevelMilestone,
    utcnow,
)

logger = logging.getLogger("sqlforge.db")

# Default PostgreSQL connection URL (can be overridden by DATABASE_URL env var)
DEFAULT_POSTGRES_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/sqlforge",
)
SQLITE_FALLBACK_URL = "sqlite:///./sqlforge_progress.db"

engine = None
SessionLocal = None
ACTIVE_DB_TYPE = "unknown"


def _create_database_engine():
    global engine, SessionLocal, ACTIVE_DB_TYPE

    # First attempt: Try PostgreSQL if DATABASE_URL is provided or default postgres URL
    target_url = os.getenv("DATABASE_URL", DEFAULT_POSTGRES_URL)
    
    if target_url.startswith("postgresql"):
        try:
            logger.info("Attempting connection to PostgreSQL at %s", target_url.split("@")[-1] if "@" in target_url else target_url)
            test_engine = create_engine(
                target_url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
            )
            # Test connection
            with test_engine.connect() as conn:
                pass
            engine = test_engine
            ACTIVE_DB_TYPE = "postgresql"
            logger.info("Successfully connected to PostgreSQL database!")
        except Exception as e:
            logger.warning(
                "Could not connect to PostgreSQL (%s). Falling back to persistent SQLite at '%s'. "
                "To connect to PostgreSQL, set DATABASE_URL=postgresql://user:password@host:5432/dbname.",
                str(e),
                SQLITE_FALLBACK_URL,
            )
            engine = create_engine(
                SQLITE_FALLBACK_URL,
                connect_args={"check_same_thread": False},
            )
            ACTIVE_DB_TYPE = "sqlite"
    else:
        # User explicitly supplied sqlite or another URL
        engine = create_engine(
            target_url,
            connect_args={"check_same_thread": False} if "sqlite" in target_url else {},
        )
        ACTIVE_DB_TYPE = "sqlite" if "sqlite" in target_url else "other"

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine


_create_database_engine()


def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_demo_data_if_empty(db: Session):
    """Seeds demo user, initial solved questions, and initial badge if table is empty."""
    user = db.query(User).filter(User.id == "usr-demo").first()
    if not user:
        today_str = date.today().isoformat()
        user = User(
            id="usr-demo",
            email="alex.dev@sqlforge.dev",
            name="Alex Developer",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces",
            xp=850,
            streak_days=5,
            longest_streak=7,
            last_activity_date=today_str,
            level_title="Query Practitioner",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        db.add(user)
        db.commit()

        # Seed initial topic progress (Topic 1: SELECT)
        topic1 = UserTopicProgress(
            user_id="usr-demo",
            topic_slug="select-distinct-projection",
            is_completed=True,
            completed_at=utcnow(),
        )
        db.add(topic1)

        # Seed initial solved questions
        initial_solves = [
            ("q-001", "select-distinct-projection", "easy", "SELECT first_name, last_name, email FROM employees;"),
            ("q-002", "select-distinct-projection", "easy", "SELECT DISTINCT country FROM customers ORDER BY country ASC;"),
            ("q-008", "where-filtering-operators", "medium", "SELECT id, name, budget FROM departments WHERE budget >= 300000.00;"),
        ]

        for q_id, t_slug, diff, sql in initial_solves:
            q_status = UserQuestionStatus(
                user_id="usr-demo",
                question_id=q_id,
                topic_slug=t_slug,
                difficulty=diff,
                is_solved=True,
                first_solved_at=utcnow(),
                attempts_count=1,
                failed_attempts_count=0,
                last_status="ACCEPTED",
                last_submitted_sql=sql,
                updated_at=utcnow(),
            )
            db.add(q_status)

            sub = Submission(
                id=f"sub-seed-{q_id}",
                user_id="usr-demo",
                question_id=q_id,
                question_title=f"Sample Practice: {q_id}",
                database_id="db-company" if q_id != "q-002" else "db-ecommerce",
                topic_slug=t_slug,
                difficulty=diff,
                status="ACCEPTED",
                submitted_sql=sql,
                execution_time_ms=1.2,
                passed_test_cases=2,
                total_test_cases=2,
                xp_awarded=20 if diff == "easy" else 50,
                created_at=utcnow(),
            )
            db.add(sub)

        # Seed initial badges
        badge1 = Badge(
            user_id="usr-demo",
            badge_key="badge_select_projection",
            title="Projection Pioneer",
            description="Successfully completed Topic 1: Column Projections, SELECT, and DISTINCT.",
            badge_type="topic",
            icon="Compass",
            earned_at=utcnow(),
        )
        badge2 = Badge(
            user_id="usr-demo",
            badge_key="badge_streak_3",
            title="3-Day Consistency",
            description="Maintained an active query learning streak for 3 consecutive days.",
            badge_type="streak",
            icon="Flame",
            earned_at=utcnow(),
        )
        db.add_all([badge1, badge2])
        db.commit()


def init_db():
    """Initializes tables and default data."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_data_if_empty(db)

