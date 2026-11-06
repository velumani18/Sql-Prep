from typing import Dict, List, Optional
from app.engine.types import TestCase
from app.question_bank.models import BankQuestion
from app.repositories.question_repo import Question

# Import all 10 topics
from app.question_bank.topic_01_select import TOPIC_01_QUESTIONS
from app.question_bank.topic_02_where import TOPIC_02_QUESTIONS
from app.question_bank.topic_03_logical import TOPIC_03_QUESTIONS
from app.question_bank.topic_04_order_limit import TOPIC_04_QUESTIONS
from app.question_bank.topic_05_aggregations import TOPIC_05_QUESTIONS
from app.question_bank.topic_06_group_by import TOPIC_06_QUESTIONS
from app.question_bank.topic_07_case_coalesce import TOPIC_07_QUESTIONS
from app.question_bank.topic_08_inner_join import TOPIC_08_QUESTIONS
from app.question_bank.topic_09_left_join import TOPIC_09_QUESTIONS
from app.question_bank.topic_10_multi_self_joins import TOPIC_10_QUESTIONS


TOPIC_ID_TO_SLUG = {
    "top-01": "select-distinct-projection",
    "top-02": "where-filtering-operators",
    "top-03": "in-between-like-pattern-matching",
    "top-04": "sorting-pagination-null-handling",
    "top-05": "aggregate-functions-foundations",
    "top-06": "group-by-having-clauses",
    "top-07": "case-when-conditional-aggregation",
    "top-08": "inner-and-left-outer-joins",
    "top-09": "self-joins-cross-joins-unions",
    "top-10": "subqueries-and-exists",
}


class QuestionBankRegistry:
    """
    Central repository and index for the 70-question SQL question bank.
    Provides fast lookup by ID, slug, topic, difficulty, and database.
    """

    def __init__(self):
        self._all_questions: List[BankQuestion] = (
            TOPIC_01_QUESTIONS
            + TOPIC_02_QUESTIONS
            + TOPIC_03_QUESTIONS
            + TOPIC_04_QUESTIONS
            + TOPIC_05_QUESTIONS
            + TOPIC_06_QUESTIONS
            + TOPIC_07_QUESTIONS
            + TOPIC_08_QUESTIONS
            + TOPIC_09_QUESTIONS
            + TOPIC_10_QUESTIONS
        )

        self._questions_by_id: Dict[str, BankQuestion] = {}
        self._questions_by_slug: Dict[str, BankQuestion] = {}

        for q in self._all_questions:
            self._questions_by_id[q.id] = q
            self._questions_by_slug[q.slug] = q

    def get_all(self) -> List[BankQuestion]:
        """Returns all 70 questions in canonical sequence."""
        return self._all_questions

    def get_by_id(self, question_id: str) -> Optional[BankQuestion]:
        """Finds question by ID or slug."""
        if question_id in self._questions_by_id:
            return self._questions_by_id[question_id]
        return self._questions_by_slug.get(question_id)

    def get_by_topic(self, topic_id: str) -> List[BankQuestion]:
        """Returns all questions for a specific topic (e.g. 'top-01')."""
        return [q for q in self._all_questions if q.topic_id == topic_id]

    def get_by_difficulty(self, difficulty: str) -> List[BankQuestion]:
        """Returns questions filtered by difficulty ('easy', 'medium', 'hard')."""
        diff_lower = difficulty.lower()
        return [q for q in self._all_questions if q.difficulty.lower() == diff_lower]

    def get_by_database(self, database_id: str) -> List[BankQuestion]:
        """Returns questions querying a specific synthetic database."""
        return [q for q in self._all_questions if q.database_id == database_id]

    def to_question_model(self, bank_q: BankQuestion) -> Question:
        """
        Converts a BankQuestion into the core Question model required by
        the execution engine's QueryEvaluator.
        """
        topic_slug = TOPIC_ID_TO_SLUG.get(bank_q.topic_id, "select-distinct-projection")
        return Question(
            id=bank_q.id,
            slug=bank_q.slug,
            title=bank_q.title,
            difficulty=bank_q.difficulty,
            database_id=bank_q.database_id,
            prompt=bank_q.problem_description,
            starter_code=bank_q.starter_code,
            solution_sql=bank_q.expected_solution,
            order_matters=bank_q.order_matters,
            check_column_names=bank_q.check_column_names,
            topic=bank_q.topic,
            topic_slug=topic_slug,
            test_cases=bank_q.test_cases,
        )


question_bank_registry = QuestionBankRegistry()
