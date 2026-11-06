from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.engine.types import TestCase

class Question(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    database_id: str
    prompt: str
    starter_code: str
    solution_sql: str
    order_matters: bool = False
    check_column_names: bool = True
    topic: Optional[str] = None
    topic_slug: Optional[str] = None
    test_cases: List[TestCase] = Field(default_factory=list)

# Predefined Exercise Catalog (Legacy initial questions)
QUESTIONS_CATALOG: Dict[str, Question] = {
    "q-101": Question(
        id="q-101",
        slug="customers-with-zero-orders",
        title="Customers with Zero Purchases",
        difficulty="easy",
        database_id="db-ecommerce",
        topic="Anti-Joins & Null Checking",
        topic_slug="inner-and-left-outer-joins",
        prompt="Write a query to return the customer_id, customer_name, and email of all customers who have never placed an order in the orders table. Order by customer_name ASC.",
        order_matters=True,
        check_column_names=True,
        starter_code="""-- Find customers with zero orders
SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.email
FROM customers c
-- Complete query below:
""",
        solution_sql="""SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.email
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL
ORDER BY c.name ASC;""",
        test_cases=[
            TestCase(
                id="tc-101-1",
                name="Default Public Dataset",
                description="Standard test case with customers who have zero orders.",
                is_hidden=False,
                custom_seed_dml=None,
            ),
            TestCase(
                id="tc-101-2",
                name="Hidden Test Case 1: Additional Inactive Customers",
                description="Altered dataset with 2 additional customers who have no orders.",
                is_hidden=True,
                custom_seed_dml="""
INSERT INTO customers (id, first_name, last_name, email, country, city, created_at) VALUES
(301, 'Amara', 'Okafor', 'amara.okafor@example.ng', 'Nigeria', 'Lagos', '2023-04-10'),
(302, 'Yuki', 'Tanaka', 'yuki.tanaka@example.jp', 'Japan', 'Tokyo', '2023-04-12');
""",
            ),
            TestCase(
                id="tc-101-3",
                name="Hidden Test Case 2: Inactive Customer Places Order",
                description="Dataset where inactive customer 201 places an order.",
                is_hidden=True,
                custom_seed_dml="""
INSERT INTO orders (id, customer_id, order_date, total_amount, status) VALUES
(2001, 201, '2023-05-10', 99.00, 'COMPLETED');
""",
            ),
        ],
    ),
    "q-102": Question(
        id="q-102",
        slug="department-top-salary",
        title="Department Maximum Compensation",
        difficulty="medium",
        database_id="db-company",
        prompt="Find each department's name and its maximum employee base salary as max_salary. Order by max_salary DESC.",
        order_matters=True,
        check_column_names=True,
        starter_code="""SELECT 
    d.name AS department_name,
    MAX(s.base_salary) AS max_salary
FROM departments d
JOIN employees e ON d.id = e.department_id
JOIN salaries s ON e.id = s.employee_id
GROUP BY d.name
ORDER BY max_salary DESC;""",
        solution_sql="""SELECT 
    d.name AS department_name,
    MAX(s.base_salary) AS max_salary
FROM departments d
JOIN employees e ON d.id = e.department_id
JOIN salaries s ON e.id = s.employee_id
GROUP BY d.name
ORDER BY max_salary DESC;""",
        test_cases=[
            TestCase(
                id="tc-102-1",
                name="Standard Company Roster",
                description="Default payroll records across departments.",
                is_hidden=False,
                custom_seed_dml=None,
            ),
        ],
    ),
}

class QuestionRepository:
    def __init__(self):
        self._cached_questions: Dict[str, Question] = dict(QUESTIONS_CATALOG)
        self._initialized = False

    def _ensure_initialized(self):
        if not self._initialized:
            try:
                from app.question_bank.registry import question_bank_registry
                for bank_q in question_bank_registry.get_all():
                    q_model = question_bank_registry.to_question_model(bank_q)
                    self._cached_questions[q_model.id] = q_model
                    self._cached_questions[q_model.slug] = q_model
                self._initialized = True
            except ImportError:
                pass

    def get_by_id(self, question_id: str) -> Optional[Question]:
        self._ensure_initialized()
        return self._cached_questions.get(question_id)

    def get_all(self) -> List[Question]:
        self._ensure_initialized()
        seen = set()
        unique_questions = []
        for q in self._cached_questions.values():
            if q.id not in seen:
                seen.add(q.id)
                unique_questions.append(q)
        return unique_questions

question_repo = QuestionRepository()
