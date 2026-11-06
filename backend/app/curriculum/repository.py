from typing import Dict, List, Optional, Tuple
from app.curriculum.models import (
    CurriculumLevel,
    TopicLesson,
    TopicSummary,
    PracticeQuestion,
)
from app.curriculum.level_1_fundamentals import LEVEL_1_LESSONS
from app.curriculum.level_2_aggregations import LEVEL_2_LESSONS
from app.curriculum.level_3_joins import LEVEL_3_LESSONS
from app.curriculum.level_4_advanced import LEVEL_4_LESSONS
from app.curriculum.level_5_window_functions import LEVEL_5_LESSONS
from app.curriculum.level_6_database_engineering import LEVEL_6_LESSONS


class CurriculumRepository:
    """
    Central repository for all curriculum levels, topic lessons, and practice questions.
    Provides fast indexed lookups by level number, topic slug, topic id, and question id.
    """

    def __init__(self):
        self._lessons_by_level: Dict[int, List[TopicLesson]] = {
            1: LEVEL_1_LESSONS,
            2: LEVEL_2_LESSONS,
            3: LEVEL_3_LESSONS,
            4: LEVEL_4_LESSONS,
            5: LEVEL_5_LESSONS,
            6: LEVEL_6_LESSONS,
        }

        self._topics_by_slug: Dict[str, TopicLesson] = {}
        self._topics_by_id: Dict[str, TopicLesson] = {}
        self._questions_by_id: Dict[str, Tuple[PracticeQuestion, TopicLesson]] = {}

        # Index all lessons and questions
        for level_num, lessons in self._lessons_by_level.items():
            for lesson in lessons:
                self._topics_by_slug[lesson.slug] = lesson
                self._topics_by_id[lesson.id] = lesson
                for q in lesson.practice_questions:
                    self._questions_by_id[q.id] = (q, lesson)

        self._levels_metadata: List[CurriculumLevel] = [
            CurriculumLevel(
                level_number=1,
                slug="sql-fundamentals",
                title="Level 1: SQL Fundamentals",
                subtitle="Data structures, SELECT, filtering, sorting, and pagination",
                description="Master the foundational syntax and concepts of relational databases: SELECT, WHERE, comparisons, logical operations, ORDER BY, LIMIT, and NULL semantics.",
                difficulty="Beginner",
                estimated_hours=6,
                topics=[
                    TopicSummary(
                        id=les.id,
                        slug=les.slug,
                        title=les.title,
                        order_index=les.order_index,
                        questions_count=len(les.practice_questions),
                        database_id=les.database_id,
                    )
                    for les in LEVEL_1_LESSONS
                ],
            ),
            CurriculumLevel(
                level_number=2,
                slug="aggregations-and-grouping",
                title="Level 2: Aggregations & Grouping",
                subtitle="Summary functions, GROUP BY, HAVING, and conditional CASE expressions",
                description="Synthesize large datasets into actionable insights using COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING, and advanced CASE WHEN conditional logic.",
                difficulty="Beginner",
                estimated_hours=8,
                topics=[
                    TopicSummary(
                        id=les.id,
                        slug=les.slug,
                        title=les.title,
                        order_index=les.order_index,
                        questions_count=len(les.practice_questions),
                        database_id=les.database_id,
                    )
                    for les in LEVEL_2_LESSONS
                ],
            ),
            CurriculumLevel(
                level_number=3,
                slug="joins-and-relational-modeling",
                title="Level 3: Joins & Relational Modeling",
                subtitle="Multi-table relationships, INNER, OUTER, CROSS, SELF joins, and UNION",
                description="Navigate complex relational entity networks using INNER, LEFT, RIGHT, FULL OUTER joins, self-referencing joins, and UNION set operations.",
                difficulty="Intermediate",
                estimated_hours=10,
                topics=[
                    TopicSummary(
                        id=les.id,
                        slug=les.slug,
                        title=les.title,
                        order_index=les.order_index,
                        questions_count=len(les.practice_questions),
                        database_id=les.database_id,
                    )
                    for les in LEVEL_3_LESSONS
                ],
            ),
            CurriculumLevel(
                level_number=4,
                slug="advanced-sql-and-ctes",
                title="Level 4: Advanced SQL & CTEs",
                subtitle="Scalar and correlated subqueries, EXISTS, and recursive CTEs",
                description="Solve complex hierarchical and multi-step analytical challenges with scalar, multi-row, and correlated subqueries, EXISTS, and recursive Common Table Expressions.",
                difficulty="Advanced",
                estimated_hours=12,
                topics=[
                    TopicSummary(
                        id=les.id,
                        slug=les.slug,
                        title=les.title,
                        order_index=les.order_index,
                        questions_count=len(les.practice_questions),
                        database_id=les.database_id,
                    )
                    for les in LEVEL_4_LESSONS
                ],
            ),
            CurriculumLevel(
                level_number=5,
                slug="window-functions-and-analytics",
                title="Level 5: Window Functions & Analytics",
                subtitle="ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, and running aggregations",
                description="Harness state-of-the-art analytical SQL with window partitioning and framing: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, moving averages, and cumulative totals.",
                difficulty="Advanced",
                estimated_hours=12,
                topics=[
                    TopicSummary(
                        id=les.id,
                        slug=les.slug,
                        title=les.title,
                        order_index=les.order_index,
                        questions_count=len(les.practice_questions),
                        database_id=les.database_id,
                    )
                    for les in LEVEL_5_LESSONS
                ],
            ),
            CurriculumLevel(
                level_number=6,
                slug="database-engineering-and-architecture",
                title="Level 6: Database Engineering & Architecture",
                subtitle="DDL, DML, ACID transactions, normalization, indexing, and triggers",
                description="Master full-lifecycle database architecture: DDL schema design, constraints, ACID transactions, 3NF/BCNF normalization, B-Tree index optimization, and active triggers.",
                difficulty="Expert",
                estimated_hours=15,
                topics=[
                    TopicSummary(
                        id=les.id,
                        slug=les.slug,
                        title=les.title,
                        order_index=les.order_index,
                        questions_count=len(les.practice_questions),
                        database_id=les.database_id,
                    )
                    for les in LEVEL_6_LESSONS
                ],
            ),
        ]

    def get_levels(self) -> List[CurriculumLevel]:
        """Returns all 6 curriculum levels with their topic summaries."""
        return self._levels_metadata

    def get_level(self, level_number: int) -> Optional[CurriculumLevel]:
        """Returns metadata and topics for a specific level number (1-6)."""
        for lvl in self._levels_metadata:
            if lvl.level_number == level_number:
                return lvl
        return None

    def get_lessons_for_level(self, level_number: int) -> List[TopicLesson]:
        """Returns full TopicLesson objects for all topics in the given level."""
        return self._lessons_by_level.get(level_number, [])

    def get_topic_by_slug(self, slug: str) -> Optional[TopicLesson]:
        """Retrieves a full topic lesson by its URL-friendly slug."""
        return self._topics_by_slug.get(slug)

    def get_topic_by_id(self, topic_id: str) -> Optional[TopicLesson]:
        """Retrieves a full topic lesson by its unique lesson ID."""
        return self._topics_by_id.get(topic_id)

    def get_all_topics(self) -> List[TopicLesson]:
        """Returns a flat list of all topic lessons across all levels."""
        all_topics: List[TopicLesson] = []
        for lessons in self._lessons_by_level.values():
            all_topics.extend(lessons)
        return all_topics

    def get_all_questions(self) -> List[Dict]:
        """Returns all practice questions enriched with topic and database metadata."""
        results = []
        for q, lesson in self._questions_by_id.values():
            results.append({
                "id": q.id,
                "slug": q.slug,
                "title": q.title,
                "difficulty": q.difficulty,
                "prompt": q.prompt,
                "starter_sql": q.starter_sql,
                "hints": q.hints,
                "order_matters": q.order_matters,
                "check_column_names": q.check_column_names,
                "topic_id": lesson.id,
                "topic_title": lesson.title,
                "topic_slug": lesson.slug,
                "level_number": lesson.level_number,
                "level_title": lesson.level_title,
                "database_id": lesson.database_id,
                "database_name": lesson.database_name,
            })
        return results

    def get_question_by_id(self, question_id: str) -> Optional[Tuple[PracticeQuestion, TopicLesson]]:
        """Returns practice question and parent topic lesson tuple."""
        return self._questions_by_id.get(question_id)


curriculum_repo = CurriculumRepository()
