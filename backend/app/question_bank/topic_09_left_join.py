from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_09_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q57: All Departments and Staff Count (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-057",
        slug="departments-headcount-including-zeroes",
        title="Department Census Including Empty Divisions",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="easy",
        problem_description="""Corporate planning needs an exhaustive headcount across all departments,
guaranteeing that divisions with zero employees are still reported with a count of 0.
Perform a `LEFT JOIN` from `departments` to `employees` on `d.id = e.department_id`.
Group by `d.id` and `d.name`.
Return `d.id` (as `department_id`), `d.name` (as `department_name`), and `COUNT(e.id)` as `employee_count`.
Order by `employee_count` in descending order (`DESC`), then `department_id` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["departments", "employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="departments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(80)"),
                ],
            ),
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="department_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
        ],
        sample_input_data={
            "departments": [
                {"id": 1, "name": "Engineering"},
                {"id": 7, "name": "Human Resources"},
            ],
            "employees": [
                {"id": 1, "department_id": 1},
                {"id": 2, "department_id": 1},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["department_id", "department_name", "employee_count"],
            sample_rows=[
                [1, "Engineering", 15],
                [3, "Sales", 10],
                [2, "Marketing", 8],
                [4, "Finance", 8],
                [5, "Product", 6],
                [6, "Legal", 4],
                [7, "Human Resources", 4],
            ],
            total_row_count=7,
        ),
        starter_code="-- LEFT JOIN departments and employees; use COUNT(e.id)\nSELECT \nFROM departments d\n",
        expected_solution="""SELECT 
    d.id AS department_id,
    d.name AS department_name,
    COUNT(e.id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.name
ORDER BY employee_count DESC, department_id ASC;""",
        alternative_solution="""SELECT 
    d.id AS department_id,
    d.name AS department_name,
    COALESCE(sub.cnt, 0) AS employee_count
FROM departments d
LEFT JOIN (
    SELECT department_id, COUNT(*) AS cnt 
    FROM employees 
    WHERE department_id IS NOT NULL 
    GROUP BY department_id
) sub ON d.id = sub.department_id
ORDER BY employee_count DESC, department_id ASC;""",
        hints=[
            "Use `LEFT JOIN employees e ON d.id = e.department_id`.",
            "Crucial: Use `COUNT(e.id)` instead of `COUNT(*)`. `COUNT(*)` would count unmatched null rows as 1!",
            "Group by `d.id, d.name` and order by `employee_count DESC, department_id ASC`.",
        ],
        detailed_explanation="""In a `LEFT JOIN`, if a left-table row has no matching right-table row,
the right-table attributes are filled with NULLs.
Using `COUNT(*)` on an unmatched group counts the single NULL row, yielding an incorrect count of 1.
In contrast, `COUNT(e.id)` correctly ignores NULL values, producing the accurate count of 0.""",
        related_concepts=["LEFT JOIN", "COUNT(column) vs COUNT(*)", "Preserving Unmatched Left Rows"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-057-pub",
                name="Default Departments",
                description="7 departments with staff counts.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-057-hid1",
                name="Hidden Test Case 1: Empty Newly Created Department",
                description="New department with 0 employees must show count 0.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO departments (id, name, budget, location)
VALUES (99, 'Empty Division', 100000.00, 'Austin');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q58: Customers with Zero Orders (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-058",
        slug="customers-with-zero-orders-anti-join",
        title="Zero-Purchase Customer Re-engagement (Anti-Join)",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="easy",
        problem_description="""Marketing wants to send a promotional discount to registered customers who have never placed an order.
Use a `LEFT JOIN` between `customers` and `orders` on `c.id = o.customer_id`.
Filter for customers where no matching order exists (`WHERE o.id IS NULL`).
Return `c.id` (as `customer_id`), `c.name` (as `customer_name`), and `c.email`.
Order by `customer_id` in ascending order (`ASC`).""",
        database_id="db-ecommerce",
        relevant_tables=["customers", "orders"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(100)"),
                    ColumnSchema(name="email", type="VARCHAR(120)"),
                ],
            ),
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
        ],
        sample_input_data={
            "customers": [
                {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
                {"id": 21, "name": "Jack Vance", "email": "jack@example.com"},
            ],
            "orders": [
                {"id": 1, "customer_id": 1},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["customer_id", "customer_name", "email"],
            sample_rows=[
                [21, "Jack Vance", "jack.vance@example.com"],
                [22, "Karen Blixen", "karen.blixen@example.com"],
            ],
            total_row_count=10,
        ),
        starter_code="-- LEFT JOIN customers and orders; filter WHERE o.id IS NULL\nSELECT \nFROM customers c\n",
        expected_solution="""SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.email
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL
ORDER BY customer_id ASC;""",
        alternative_solution="""SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.email
FROM customers c
WHERE c.id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY customer_id ASC;""",
        hints=[
            "Use `LEFT JOIN orders o ON c.id = o.customer_id`.",
            "Add `WHERE o.id IS NULL` to filter for rows that had no match in orders.",
            "Order by `customer_id ASC`.",
        ],
        detailed_explanation="""The `LEFT JOIN ... WHERE right_table.id IS NULL` idiom is known as an Anti-Join.
It identifies rows in relation A that possess no corresponding foreign key link in relation B.
In modern cost-based query planners, anti-joins with indexed foreign keys frequently outperform `NOT IN` or `NOT EXISTS` subqueries.""",
        related_concepts=["Anti-Join Pattern", "LEFT JOIN", "IS NULL", "Set Difference"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-058-pub",
                name="Default Customers",
                description="10 customers with 0 orders.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-058-hid1",
                name="Hidden Test Case 1: Inactive Customer Places Order",
                description="Customer 21 places order; count drops to 9.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO orders (id, customer_id, order_date, total_amount, status)
VALUES (999, 21, '2024-03-01', 99.00, 'completed');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q59: Courses Without Enrolled Students (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-059",
        slug="courses-without-enrollments-anti-join",
        title="Zero-Enrollment Course Detection (Anti-Join)",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="easy",
        problem_description="""Academic scheduling evaluates low-demand courses for cancellation.
Write a query to identify all courses that have zero enrolled students.
Perform a `LEFT JOIN` from `courses` to `enrollments` on `c.id = e.course_id`.
Filter for courses where no enrollment record exists (`WHERE e.id IS NULL`).
Return `c.id` (as `course_id`), `c.code`, and `c.title`.
Order by `course_id` in ascending order (`ASC`).""",
        database_id="db-university",
        relevant_tables=["courses", "enrollments"],
        table_schemas=[
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="code", type="VARCHAR(15)"),
                    ColumnSchema(name="title", type="VARCHAR(120)"),
                ],
            ),
            TableSchemaInfo(
                table_name="enrollments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="course_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
        ],
        sample_input_data={
            "courses": [
                {"id": 1, "code": "CS101", "title": "Intro to CS"},
                {"id": 12, "code": "ECON101", "title": "Microeconomics"},
            ],
            "enrollments": [
                {"id": 1, "course_id": 1},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["course_id", "code", "title"],
            sample_rows=[
                [12, "ECON101", "Principles of Microeconomics"],
            ],
            total_row_count=1,
        ),
        starter_code="-- LEFT JOIN courses and enrollments; filter WHERE e.id IS NULL\nSELECT \nFROM courses c\n",
        expected_solution="""SELECT 
    c.id AS course_id,
    c.code,
    c.title
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
WHERE e.id IS NULL
ORDER BY course_id ASC;""",
        alternative_solution="""SELECT 
    c.id AS course_id,
    c.code,
    c.title
FROM courses c
WHERE NOT EXISTS (
    SELECT 1 FROM enrollments e WHERE e.course_id = c.id
)
ORDER BY course_id ASC;""",
        hints=[
            "Join `courses c` to `enrollments e` on `c.id = e.course_id` using a `LEFT JOIN`.",
            "Filter for unmatched records with `WHERE e.id IS NULL`.",
            "Order by `course_id ASC`.",
        ],
        detailed_explanation="""The anti-join technique works seamlessly across any One-to-Many relationship.
When a course has never appeared in `enrollments`, the `LEFT JOIN` synthesizes a row with NULLs in all enrollment columns.
Checking `WHERE e.id IS NULL` discards all successfully joined courses, isolating courses with zero demand.""",
        related_concepts=["Anti-Join", "Zero-Match Detection", "NOT EXISTS Alternative"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-059-pub",
                name="Default Courses",
                description="1 course with zero enrollments (ECON101).",
                is_hidden=False,
            ),
            TestCase(
                id="tc-059-hid1",
                name="Hidden Test Case 1: Additional Empty Course",
                description="New Sociology course with 0 students.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO courses (id, code, title, department_id, professor_id, credits)
VALUES (999, 'SOC101', 'Introduction to Sociology', 1, 1, 3);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q60: Unassigned Staff Identification (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-060",
        slug="unassigned-staff-audit-left-join",
        title="Unassigned Department Personnel Audit",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="medium",
        problem_description="""Internal organization audits require identifying all personnel lacking departmental placement.
Write a query using a `LEFT JOIN` from `employees` to `departments` on `e.department_id = d.id`.
Filter for employees who have no valid department assignment (`WHERE d.id IS NULL`).
Return `e.id` (as `employee_id`), concatenated full name as `employee_name` (`e.first_name || ' ' || e.last_name`),
`e.title`, and `e.hire_date`.
Order by `employee_id` in ascending order (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees", "departments"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(100)"),
                    ColumnSchema(name="department_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="hire_date", type="DATE"),
                ],
            ),
            TableSchemaInfo(
                table_name="departments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                ],
            ),
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "department_id": 1},
                {"id": 56, "first_name": "Grace", "department_id": None},
            ],
            "departments": [{"id": 1}],
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "employee_name", "title", "hire_date"],
            sample_rows=[
                [56, "Grace Hopper", "Chief Research Advisor", "2020-01-15"],
                [57, "Linus Torvalds", "Distinguished Architect", "2020-02-01"],
            ],
            total_row_count=5,
        ),
        starter_code="-- LEFT JOIN employees and departments; filter WHERE d.id IS NULL\nSELECT \nFROM employees e\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.title,
    e.hire_date
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id
WHERE d.id IS NULL
ORDER BY employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.title,
    e.hire_date
FROM employees e
WHERE e.department_id IS NULL
ORDER BY e.id ASC;""",
        hints=[
            "Use `LEFT JOIN departments d ON e.department_id = d.id`.",
            "Filter for unmatched records with `WHERE d.id IS NULL`.",
            "Order by `employee_id ASC`.",
        ],
        detailed_explanation="""Joining child records to parent records with a `LEFT JOIN ... WHERE parent.id IS NULL`
captures both records where the foreign key is NULL (`department_id IS NULL`)
AND orphaned records where `department_id` holds an invalid foreign key that does not exist in `departments`!
This makes it superior to a simple `WHERE department_id IS NULL` check in production integrity audits.""",
        related_concepts=["Referential Integrity Audit", "Orphaned Records", "Defensive Join Patterns"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-060-pub",
                name="Default Employees",
                description="5 unassigned senior consultants.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-060-hid1",
                name="Hidden Test Case 1: Additional Unassigned Specialist",
                description="Staff member with NULL department.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Vint', 'Cerf', 'vint@co.com', NULL, 'Chief Internet Evangelist', '2024-01-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q61: Inactive Accounts Without Transactions (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-061",
        slug="dormant-accounts-without-transactions-anti-join",
        title="Dormant Accounts with Zero Ledger Transactions",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="medium",
        problem_description="""Bank compliance requires identifying dormant accounts that have never recorded any transaction activity.
Perform a `LEFT JOIN` between `accounts` and `transactions` on `a.id = t.account_id`.
Filter for accounts with zero transactions (`WHERE t.id IS NULL`).
Return `a.id` (as `account_id`), `a.account_number`, `a.account_type`, and `a.balance`.
Order by `account_id` in ascending order (`ASC`).""",
        database_id="db-banking",
        relevant_tables=["accounts", "transactions"],
        table_schemas=[
            TableSchemaInfo(
                table_name="accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="account_number", type="VARCHAR(20)"),
                    ColumnSchema(name="account_type", type="VARCHAR(30)"),
                    ColumnSchema(name="balance", type="DECIMAL(12,2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="transactions",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="account_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
        ],
        sample_input_data={
            "accounts": [
                {"id": 1, "account_number": "ACC-1001", "balance": 8450.25},
                {"id": 19, "account_number": "ACC-1019", "balance": 5200.00},
            ],
            "transactions": [{"id": 1, "account_id": 1}],
        },
        expected_output=ExpectedOutput(
            columns=["account_id", "account_number", "account_type", "balance"],
            sample_rows=[
                [19, "ACC-1019", "Checking", 5200.00],
                [20, "ACC-1020", "Savings", 18500.00],
                [21, "ACC-1021", "Checking", 4100.00],
            ],
            total_row_count=17,
        ),
        starter_code="-- LEFT JOIN accounts and transactions; filter WHERE t.id IS NULL\nSELECT \nFROM accounts a\n",
        expected_solution="""SELECT 
    a.id AS account_id,
    a.account_number,
    a.account_type,
    a.balance
FROM accounts a
LEFT JOIN transactions t ON a.id = t.account_id
WHERE t.id IS NULL
ORDER BY account_id ASC;""",
        alternative_solution="""SELECT 
    a.id AS account_id,
    a.account_number,
    a.account_type,
    a.balance
FROM accounts a
WHERE NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.account_id = a.id
)
ORDER BY a.id ASC;""",
        hints=[
            "Use `LEFT JOIN transactions t ON a.id = t.account_id`.",
            "Filter for unmatched records with `WHERE t.id IS NULL`.",
            "Order by `account_id ASC`.",
        ],
        detailed_explanation="""Anti-joins are vital for regulatory dormancy audits.
In banking schemas with millions of ledger entries, joining `accounts` to `transactions` on an indexed `account_id`
and filtering `WHERE t.id IS NULL` swiftly isolates accounts that have never transacted.""",
        related_concepts=["Anti-Join", "Dormancy Audits", "IS NULL"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-061-pub",
                name="Default Accounts",
                description="17 dormant accounts with no transactions.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-061-hid1",
                name="Hidden Test Case 1: Dormant Account Receives Wire",
                description="Account 19 transacts; count drops to 16.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date)
VALUES (999, 19, 'deposit', 500.00, 5700.00, 'Initial Funding', '2024-03-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q62: Professors Without Assigned Courses (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-062",
        slug="professors-without-courses-anti-join",
        title="Faculty on Sabbatical: Professors Without Courses",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="medium",
        problem_description="""Academic deans want to identify faculty members on research leave or sabbatical who have no teaching assignments.
Perform a `LEFT JOIN` between `professors` and `courses` on `p.id = c.professor_id`.
Filter for professors with no assigned courses (`WHERE c.id IS NULL`).
Return `p.id` (as `professor_id`), concatenated full name as `professor_name` (`p.first_name || ' ' || p.last_name`), `p.title`, and `p.email`.
Order by `professor_id` in ascending order (`ASC`).""",
        database_id="db-university",
        relevant_tables=["professors", "courses"],
        table_schemas=[
            TableSchemaInfo(
                table_name="professors",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(60)"),
                    ColumnSchema(name="email", type="VARCHAR(120)"),
                ],
            ),
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="professor_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
        ],
        sample_input_data={
            "professors": [
                {"id": 1, "first_name": "Alan", "last_name": "Turing"},
                {"id": 4, "first_name": "Ada", "last_name": "Lovelace"},
            ],
            "courses": [{"id": 1, "professor_id": 1}],
        },
        expected_output=ExpectedOutput(
            columns=["professor_id", "professor_name", "title", "email"],
            sample_rows=[
                [4, "Ada Lovelace", "Assistant Professor", "ada.lovelace@university.edu"],
            ],
            total_row_count=1,
        ),
        starter_code="-- LEFT JOIN professors and courses; filter WHERE c.id IS NULL\nSELECT \nFROM professors p\n",
        expected_solution="""SELECT 
    p.id AS professor_id,
    p.first_name || ' ' || p.last_name AS professor_name,
    p.title,
    p.email
FROM professors p
LEFT JOIN courses c ON p.id = c.professor_id
WHERE c.id IS NULL
ORDER BY professor_id ASC;""",
        alternative_solution="""SELECT 
    p.id AS professor_id,
    CONCAT(p.first_name, ' ', p.last_name) AS professor_name,
    p.title,
    p.email
FROM professors p
WHERE p.id NOT IN (SELECT professor_id FROM courses WHERE professor_id IS NOT NULL)
ORDER BY p.id ASC;""",
        hints=[
            "Join `professors p` to `courses c` on `p.id = c.professor_id` using a `LEFT JOIN`.",
            "Filter with `WHERE c.id IS NULL`.",
            "Order by `professor_id ASC`.",
        ],
        detailed_explanation="""This query isolates faculty members without active teaching assignments.
Using an anti-join (`LEFT JOIN ... WHERE right_table.id IS NULL`) guarantees that professors
who do not appear in any course's `professor_id` column are surfaced cleanly.""",
        related_concepts=["Anti-Join", "Faculty Allocation", "IS NULL"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-062-pub",
                name="Default Faculty",
                description="Professor Ada Lovelace has 0 assigned courses.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-062-hid1",
                name="Hidden Test Case 1: Additional Research Fellow",
                description="New research professor with no courses.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO professors (id, first_name, last_name, email, department_id, title, hired_year)
VALUES (999, 'Kurt', 'Godel', 'godel@univ.edu', 2, 'Research Fellow', 2024);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q63: Category Product Coverage Including Inactive/Zeroes (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-063",
        slug="full-category-inventory-coverage-left-join",
        title="Comprehensive Category Inventory & Stock Valuation Audit",
        topic_id="top-09",
        topic="LEFT JOIN & Handling Missing Data",
        difficulty="hard",
        problem_description="""E-commerce merchandising is auditing catalog coverage across all product categories,
ensuring newly added or depleted categories are reported with accurate zeroes:
Perform a `LEFT JOIN` between `categories` and `products` on `c.id = p.category_id`.
Group by `c.id` and `c.name`.
Calculate:
1. `c.id` as `category_id`.
2. `c.name` as `category_name`.
3. Total products cataloged as `total_products` (`COUNT(p.id)`).
4. Total active products as `active_products` (`SUM(CASE WHEN p.is_active = 1 THEN 1 ELSE 0 END)`).
5. Total inventory valuation (`ROUND(COALESCE(SUM(p.price * p.stock_quantity), 0.00), 2)`) as `category_inventory_value`.
Order by `category_inventory_value` descending (`DESC`), then `category_id` ascending (`ASC`).""",
        database_id="db-ecommerce",
        relevant_tables=["categories", "products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="categories",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(60)"),
                ],
            ),
            TableSchemaInfo(
                table_name="products",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="category_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="price", type="DECIMAL(10,2)"),
                    ColumnSchema(name="stock_quantity", type="INTEGER"),
                    ColumnSchema(name="is_active", type="BOOLEAN"),
                ],
            ),
        ],
        sample_input_data={
            "categories": [
                {"id": 1, "name": "Electronics"},
                {"id": 6, "name": "Toys & Games"},
            ],
            "products": [
                {"id": 1, "category_id": 1, "price": 49.99, "stock_quantity": 120, "is_active": 1},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["category_id", "category_name", "total_products", "active_products", "category_inventory_value"],
            sample_rows=[
                [1, "Electronics", 5, 5, 41248.55],
                [3, "Home & Kitchen", 5, 5, 34500.20],
                [6, "Toys & Games", 0, 0, 0.00],
            ],
            total_row_count=6,
        ),
        starter_code="-- LEFT JOIN categories and products; compute metrics including zeroes\nSELECT \nFROM categories c\n",
        expected_solution="""SELECT 
    c.id AS category_id,
    c.name AS category_name,
    COUNT(p.id) AS total_products,
    COALESCE(SUM(CASE WHEN p.is_active = 1 THEN 1 ELSE 0 END), 0) AS active_products,
    ROUND(COALESCE(SUM(p.price * p.stock_quantity), 0.00), 2) AS category_inventory_value
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name
ORDER BY category_inventory_value DESC, category_id ASC;""",
        alternative_solution="""SELECT 
    c.id AS category_id,
    c.name AS category_name,
    COUNT(p.id) AS total_products,
    COUNT(CASE WHEN p.is_active = 1 THEN 1 END) AS active_products,
    ROUND(COALESCE(SUM(p.price * p.stock_quantity), 0), 2) AS category_inventory_value
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name
ORDER BY category_inventory_value DESC, category_id ASC;""",
        hints=[
            "Use `LEFT JOIN products p ON c.id = p.category_id`.",
            "Use `COUNT(p.id)` so empty categories return 0.",
            "Wrap `SUM(p.price * p.stock_quantity)` in `COALESCE(..., 0.00)` to eliminate NULLs for categories without products.",
            "Order by `category_inventory_value DESC, category_id ASC`.",
        ],
        detailed_explanation="""Combining a `LEFT JOIN` with aggregate functions requires careful null defenses.
If a category contains zero products, `SUM(p.price * p.stock_quantity)` evaluates to NULL rather than 0.
Wrapping the summation inside `COALESCE(..., 0.00)` preserves clean financial data contracts.
Similarly, `COUNT(p.id)` yields 0 for empty categories, whereas `COUNT(*)` would erroneously output 1.""",
        related_concepts=["LEFT JOIN Aggregation", "COALESCE Defense", "Zero Handling"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-063-pub",
                name="Default Categories",
                description="6 categories including empty categories.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-063-hid1",
                name="Hidden Test Case 1: Additional Empty Category",
                description="New Automotive category with 0 products.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO categories (id, name, description)
VALUES (99, 'Automotive & Motorcycle', 'Auto parts and accessories');""",
            ),
        ],
    ),
]
