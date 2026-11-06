from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, default="usr-demo")
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False, default="Alex Developer")
    avatar_url = Column(
        Text,
        default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces",
    )
    xp = Column(Integer, default=0, nullable=False)
    streak_days = Column(Integer, default=1, nullable=False)
    longest_streak = Column(Integer, default=1, nullable=False)
    last_activity_date = Column(String(20), nullable=True)  # YYYY-MM-DD
    level_title = Column(String(100), default="SQL Apprentice", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    topic_progress = relationship("UserTopicProgress", back_populates="user", cascade="all, delete-orphan")
    question_statuses = relationship("UserQuestionStatus", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("Badge", back_populates="user", cascade="all, delete-orphan")
    level_milestones = relationship("LevelMilestone", back_populates="user", cascade="all, delete-orphan")


class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_slug = Column(String(100), nullable=False, index=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="topic_progress")

    __table_args__ = (
        UniqueConstraint("user_id", "topic_slug", name="uq_user_topic"),
    )


class UserQuestionStatus(Base):
    __tablename__ = "user_question_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(50), nullable=False, index=True)
    topic_slug = Column(String(100), nullable=True, index=True)
    difficulty = Column(String(20), default="easy", nullable=False)
    is_solved = Column(Boolean, default=False, nullable=False)
    first_solved_at = Column(DateTime(timezone=True), nullable=True)
    attempts_count = Column(Integer, default=0, nullable=False)
    failed_attempts_count = Column(Integer, default=0, nullable=False)
    last_status = Column(String(30), nullable=True)
    last_submitted_sql = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="question_statuses")

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_user_question"),
    )


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(50), nullable=False, index=True)
    question_title = Column(String(200), nullable=False)
    database_id = Column(String(50), nullable=False)
    topic_slug = Column(String(100), nullable=True, index=True)
    difficulty = Column(String(20), default="easy", nullable=False)
    status = Column(String(30), nullable=False, index=True)  # ACCEPTED, WRONG_ANSWER, SYNTAX_ERROR, etc.
    submitted_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    passed_test_cases = Column(Integer, default=0, nullable=False)
    total_test_cases = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    xp_awarded = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False, index=True)

    user = relationship("User", back_populates="submissions")


class Badge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    badge_key = Column(String(100), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    badge_type = Column(String(50), default="topic", nullable=False)  # topic, level_milestone, streak, accuracy
    icon = Column(String(50), default="Award", nullable=False)
    earned_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="badges")

    __table_args__ = (
        UniqueConstraint("user_id", "badge_key", name="uq_user_badge"),
    )


class LevelMilestone(Base):
    __tablename__ = "user_level_milestones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    level_number = Column(Integer, nullable=False, index=True)
    level_title = Column(String(150), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    xp_awarded = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="level_milestones")

    __table_args__ = (
        UniqueConstraint("user_id", "level_number", name="uq_user_level"),
    )

