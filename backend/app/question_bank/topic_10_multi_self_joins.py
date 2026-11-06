from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_10_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q64: Three-Table Relational Join (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-064",
        slug="employee-salary-department-overview",
        title="Comprehensive Staff Compensation & Department Overview",
        topic_id="top-10",
        topic="Multi-Table Joins & Self Joins",
        difficulty="easy",
        problem_description="""Human resources management needs a unified employee compensation roster:
Join:
1. `employees e` with `departments d` on `e.department_id = d.id`.
2. `employees e` with `salaries s` on `e.id = s.employee_id`.
Retrieve `e.id` (as `employee_id`), concatenated full name as `employee_name` (`e.first_name || ' ' || e.last_name`),
`d.name` (as `department_name`), and `s.base_salary`.
Order by `employee_id` in ascending order (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees", "departments", "salaries"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="department_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
            TableSchemaInfo(
                table_name="departments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(80)"),
                ],
            ),
            TableSchemaInfo(
                table_name="salaries",
                columns=[
                    ColumnSchema(name="employee_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="base_salary", type="DECIMAL(10,2)"),
                ],
            ),
        ],
        sample_input_data={
            "employees": [{"id": 1, "first_name": "Alexander", "last_name": "Pierce", "department_id": 1}],
            "departments": [{"id": 1, "name": "Engineering"}],
            "salaries": [{"employee_id": 1, "base_salary": 220000.00}],
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "employee_name", "department_name", "base_salary"],
            sample_rows=[
                [1, "Alexander Pierce", "Engineering", 220000.00],
                [2, "Sarah Connor", "Engineering", 160000.00],
                [3, "David Chen", "Engineering", 140000.00],
            ],
            total_row_count=55,
        ),
        starter_code="-- Join employees, departments, salaries on keys; order by employee_id ASC\nSELECT \nFROM employees e\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    d.name AS department_name,
    s.base_salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
INNER JOIN salaries s ON e.id = s.employee_id
ORDER BY employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    d.name AS department_name,
    s.base_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN salaries s ON e.id = s.employee_id
ORDER BY e.id ASC;""",
        hints=[
            "Join `departments d ON e.department_id = d.id`.",
            "Join `salaries s ON e.id = s.employee_id`.",
            "Order by `employee_id ASC`.",
        ],
        detailed_explanation="""This standard 3-table join connects the central employee entity to its parent dimension (`departments`)
and its 1:1 financial extension (`salaries`).
Because both joins are INNER JOINs, only employees with both an assigned department and an active salary record are returned.""",
        related_concepts=["Multi-Table Join", "Relational Graph Traversal", "INNER JOIN"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-064-pub",
                name="Default Company Staff",
                description="55 department-linked staff with salaries.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-064-hid1",
                name="Hidden Test Case 1: Additional Employee",
                description="New hire with salary in department 1.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Maya', 'Angelou', 'maya@co.com', 1, 'Resident Scholar', '2024-01-01', 'ACTIVE');
INSERT INTO salaries (id, employee_id, base_salary, bonus, effective_date)
VALUES (999, 999, 130000.00, 15000.00, '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q65: Four-Table E-Commerce Order Flow (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-065",
        slug="customer-order-item-product-history",
        title="Customer Order Item Purchase History (Four-Table Join)",
        topic_id="top-08",
        topic="Multi-Table Joins & Self Joins",
        difficulty="easy",
        problem_description="""Customer service needs to review all items purchased by customer 1 (`c.id = 1`):
Join:
1. `customers c` with `orders o` on `c.id = o.customer_id`.
2. `orders o` with `order_items oi` on `o.id = oi.order_id`.
3. `order_items oi` with `products p` on `oi.product_id = p.id`.
Filter for `c.id = 1`.
Return `o.id` (as `order_id`), `o.order_date`, `p.name` (as `product_name`), `oi.quantity`, and `oi.unit_price`.
Order by `order_id` ascending (`ASC`), then `product_name` ascending (`ASC`).""",
        database_id="db-ecommerce",
        relevant_tables=["customers", "orders", "order_items", "products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                columns=[ColumnSchema(name="id", type="INTEGER", is_primary_key=True)],
            ),
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER"),
                    ColumnSchema(name="order_date", type="DATE"),
                ],
            ),
            TableSchemaInfo(
                table_name="order_items",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="order_id", type="INTEGER"),
                    ColumnSchema(name="product_id", type="INTEGER"),
                    ColumnSchema(name="quantity", type="INTEGER"),
                    ColumnSchema(name="unit_price", type="DECIMAL(10,2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="products",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(150)"),
                ],
            ),
        ],
        sample_input_data={
            "customers": [{"id": 1}],
            "orders": [{"id": 1, "customer_id": 1, "order_date": "2024-01-10"}],
            "order_items": [{"id": 1, "order_id": 1, "product_id": 1, "quantity": 1, "unit_price": 49.99}],
            "products": [{"id": 1, "name": "Wireless Ergonomic Mouse"}],
        },
        expected_output=ExpectedOutput(
            columns=["order_id", "order_date", "product_name", "quantity", "unit_price"],
            sample_rows=[
                [1, "2024-01-10", "USB-C Multi-Port Hub", 1, 39.99],
                [1, "2024-01-10", "Wireless Ergonomic Mouse", 1, 49.99],
            ],
            total_row_count=3,
        ),
        starter_code="-- Join customers -> orders -> order_items -> products for customer_id = 1\nSELECT \nFROM customers c\n",
        expected_solution="""SELECT 
    o.id AS order_id,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE c.id = 1
ORDER BY order_id ASC, product_name ASC;""",
        alternative_solution="""SELECT 
    o.id AS order_id,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.customer_id = 1
ORDER BY o.id ASC, p.name ASC;""",
        hints=[
            "Chain joins: customers -> orders -> order_items -> products.",
            "Filter with `WHERE c.id = 1`.",
            "Order by `order_id ASC, product_name ASC`.",
        ],
        detailed_explanation="""Traversing from customer through order header to order line items and product catalog
represents the complete 4-tier e-commerce order lifecycle.
Notice the alternative solution: because `orders.customer_id` already stores the customer ID directly,
joining the `customers` table is technically optional unless customer attributes (like name or email) are projected.""",
        related_concepts=["Multi-Tier Relational Flow", "E-Commerce Pipeline", "Join Chain"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-065-pub",
                name="Default Customer 1 Purchases",
                description="3 items purchased across 2 orders.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-065-hid1",
                name="Hidden Test Case 1: Additional Item Purchased",
                description="Customer 1 orders headphones.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO order_items (id, order_id, product_id, quantity, unit_price)
VALUES (999, 1, 5, 1, 299.99);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q66: Student Course Enrollment Record (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-066",
        slug="student-course-transcript-record",
        title="Student Academic Transcript Record (Three-Table Join)",
        topic_id="top-10",
        topic="Multi-Table Joins & Self Joins",
        difficulty="easy",
        problem_description="""The university registrar needs an official course transcript for student 1 (`s.id = 1`):
Join:
1. `students s` with `enrollments e` on `s.id = e.student_id`.
2. `enrollments e` with `courses c` on `e.course_id = c.id`.
Filter for `s.id = 1`.
Return concatenated student full name as `student_name` (`s.first_name || ' ' || s.last_name`),
`c.code`, `c.title` (as `course_title`), `e.semester`, and `e.letter_grade`.
Order by `c.code` in ascending order (`ASC`).""",
        database_id="db-university",
        relevant_tables=["students", "enrollments", "courses"],
        table_schemas=[
            TableSchemaInfo(
                table_name="students",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                ],
            ),
            TableSchemaInfo(
                table_name="enrollments",
                columns=[
                    ColumnSchema(name="student_id", type="INTEGER"),
                    ColumnSchema(name="course_id", type="INTEGER"),
                    ColumnSchema(name="semester", type="VARCHAR(20)"),
                    ColumnSchema(name="letter_grade", type="VARCHAR(2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="code", type="VARCHAR(15)"),
                    ColumnSchema(name="title", type="VARCHAR(120)"),
                ],
            ),
        ],
        sample_input_data={
            "students": [{"id": 1, "first_name": "Alice", "last_name": "Walker"}],
            "enrollments": [{"student_id": 1, "course_id": 1, "semester": "Fall", "letter_grade": "A"}],
            "courses": [{"id": 1, "code": "CS101", "title": "Intro to CS"}],
        },
        expected_output=ExpectedOutput(
            columns=["student_name", "code", "course_title", "semester", "letter_grade"],
            sample_rows=[
                ["Alice Walker", "CS101", "Introduction to Computer Science", "Fall", "A"],
                ["Alice Walker", "MATH101", "Calculus I", "Spring", "B"],
            ],
            total_row_count=2,
        ),
        starter_code="-- Join students -> enrollments -> courses for student_id = 1\nSELECT \nFROM students s\n",
        expected_solution="""SELECT 
    s.first_name || ' ' || s.last_name AS student_name,
    c.code,
    c.title AS course_title,
    e.semester,
    e.letter_grade
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c ON e.course_id = c.id
WHERE s.id = 1
ORDER BY c.code ASC;""",
        alternative_solution="""SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    c.code,
    c.title AS course_title,
    e.semester,
    e.letter_grade
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
WHERE s.id = 1
ORDER BY c.code ASC;""",
        hints=[
            "Join `students s` to `enrollments e` on `s.id = e.student_id`.",
            "Join `enrollments e` to `courses c` on `e.course_id = c.id`.",
            "Filter with `WHERE s.id = 1` and order by `c.code ASC`.",
        ],
        detailed_explanation="""Transcripts are modeled via a Many-to-Many junction table (`enrollments`)
connecting students and courses while storing associative attributes (`semester`, `letter_grade`).
Joining both outer tables through the junction resolves the full human-readable transcript record.""",
        related_concepts=["Many-to-Many Join", "Junction Table Resolution", "Academic Transcript"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-066-pub",
                name="Default Student 1 Courses",
                description="2 completed courses for Alice Walker.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-066-hid1",
                name="Hidden Test Case 1: Additional Course Completed",
                description="Student 1 completes CS201 with grade A.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO enrollments (id, student_id, course_id, semester, academic_year, letter_grade)
VALUES (999, 1, 2, 'Fall', 2024, 'A');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q67: Self Join: Employees and Their Managers (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-067",
        slug="employee-manager-hierarchy-self-join",
        title="Organizational Reporting Hierarchy (Self Join)",
        topic_id="top-10",
        topic="Multi-Table Joins & Self Joins",
        difficulty="medium",
        problem_description="""Corporate directory services require mapping each employee to their immediate reporting manager.
Perform a `SELF JOIN` on the `employees` table:
- Alias the employee table as `e`.
- Alias the manager table as `m`.
Join condition: `e.manager_id = m.id`.
Filter for active employees (`e.status = 'ACTIVE'`).
Return:
1. `e.id` as `employee_id`.
2. Employee full name as `employee_name` (`e.first_name || ' ' || e.last_name`).
3. `e.title` as `employee_title`.
4. Manager full name as `manager_name` (`m.first_name || ' ' || m.last_name`).
Order by `employee_id` in ascending order (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(100)"),
                    ColumnSchema(name="manager_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "last_name": "Pierce", "title": "VP", "manager_id": None},
                {"id": 2, "first_name": "Sarah", "last_name": "Connor", "title": "Manager", "manager_id": 1},
                {"id": 3, "first_name": "David", "last_name": "Chen", "title": "Engineer", "manager_id": 2},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "employee_name", "employee_title", "manager_name"],
            sample_rows=[
                [2, "Sarah Connor", "Engineering Manager", "Alexander Pierce"],
                [3, "David Chen", "Staff Software Engineer", "Sarah Connor"],
                [4, "Emily Watson", "Senior Software Engineer", "Sarah Connor"],
            ],
            total_row_count=45,
        ),
        starter_code="-- Self join employees e and employees m on e.manager_id = m.id\nSELECT \nFROM employees e\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.title AS employee_title,
    m.first_name || ' ' || m.last_name AS manager_name
FROM employees e
INNER JOIN employees m ON e.manager_id = m.id
WHERE e.status = 'ACTIVE'
ORDER BY employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.title AS employee_title,
    CONCAT(m.first_name, ' ', m.last_name) AS manager_name
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.status = 'ACTIVE'
ORDER BY e.id ASC;""",
        hints=[
            "Join the employees table with itself: `FROM employees e INNER JOIN employees m ON e.manager_id = m.id`.",
            "Use alias `e` for the subordinate employee and `m` for their supervisor/manager.",
            "Order by `employee_id ASC`.",
        ],
        detailed_explanation="""A `SELF JOIN` joins a table with itself to represent recursive or hierarchical relationships.
Because both instances share the exact same column names, distinct table aliases (`e` and `m`)
are strictly mandatory to prevent column name collisions.
Top-level executives without managers (`manager_id IS NULL`) are excluded by the INNER JOIN.""",
        related_concepts=["Self Join", "Hierarchical Relationship", "Adjacency List Model"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-067-pub",
                name="Default Reporting Roster",
                description="45 staff with active reporting managers.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-067-hid1",
                name="Hidden Test Case 1: New Subordinate Added",
                description="Staff member reporting to David Chen.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, manager_id, title, hire_date, status)
VALUES (999, 'New', 'Associate', 'new@co.com', 1, 3, 'Junior Engineer', '2024-03-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q68: Employees Earning More Than Their Managers (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-068",
        slug="employees-earning-more-than-manager",
        title="Employees Earning More Than Their Managers",
        topic_id="top-10",
        topic="Multi-Table Joins & Self Joins",
        difficulty="medium",
        problem_description="""One of the most famous and classic SQL technical interview questions in software engineering:
Find all employees who earn a higher base salary than their direct manager.
Join:
1. `employees e` with `employees m` on `e.manager_id = m.id`.
2. `employees e` with `salaries se` on `e.id = se.employee_id`.
3. `employees m` with `salaries sm` on `m.id = sm.employee_id`.
Filter for: `se.base_salary > sm.base_salary`.
Return:
- `e.id` as `employee_id`
- Employee full name as `employee_name` (`e.first_name || ' ' || e.last_name`)
- `se.base_salary` as `employee_salary`
- Manager full name as `manager_name` (`m.first_name || ' ' || m.last_name`)
- `sm.base_salary` as `manager_salary`
Order by `employee_salary` descending (`DESC`), then `employee_id` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees", "salaries"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="manager_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
            TableSchemaInfo(
                table_name="salaries",
                columns=[
                    ColumnSchema(name="employee_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="base_salary", type="DECIMAL(10,2)"),
                ],
            ),
        ],
        sample_input_data={
            "employees": [
                {"id": 2, "first_name": "Sarah", "manager_id": 1},
                {"id": 3, "first_name": "David", "manager_id": 2},
            ],
            "salaries": [
                {"employee_id": 2, "base_salary": 160000.00},
                {"employee_id": 3, "base_salary": 175000.00},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "employee_name", "employee_salary", "manager_name", "manager_salary"],
            sample_rows=[
                [7, "James Wilson", 145000.00, "Sarah Connor", 140000.00],
            ],
            total_row_count=2,
        ),
        starter_code="-- Self join employees e & m; join salaries se & sm; filter se.base_salary > sm.base_salary\nSELECT \nFROM employees e\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    se.base_salary AS employee_salary,
    m.first_name || ' ' || m.last_name AS manager_name,
    sm.base_salary AS manager_salary
FROM employees e
INNER JOIN employees m ON e.manager_id = m.id
INNER JOIN salaries se ON e.id = se.employee_id
INNER JOIN salaries sm ON m.id = sm.employee_id
WHERE se.base_salary > sm.base_salary
ORDER BY employee_salary DESC, employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    se.base_salary AS employee_salary,
    CONCAT(m.first_name, ' ', m.last_name) AS manager_name,
    sm.base_salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
JOIN salaries se ON e.id = se.employee_id
JOIN salaries sm ON m.id = sm.employee_id
WHERE se.base_salary > sm.base_salary
ORDER BY se.base_salary DESC, e.id ASC;""",
        hints=[
            "Self join `employees e` with `employees m` on `e.manager_id = m.id`.",
            "Join `salaries se ON e.id = se.employee_id` and `salaries sm ON m.id = sm.employee_id`.",
            "Compare salaries in the WHERE clause: `WHERE se.base_salary > sm.base_salary`.",
        ],
        detailed_explanation="""This problem tests advanced relational reasoning.
It combines a self-join (`employees` to `employees`) with dual joins to a satellite table (`salaries`),
aliasing the salary table twice (`se` for the employee and `sm` for the manager).
This allows row-level comparative arithmetic across hierarchical relationships.""",
        related_concepts=["Interview Classic", "Dual Satellite Join", "Hierarchical Comparison"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-068-pub",
                name="Default Payroll Roster",
                description="2 staff earning more than their manager.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-068-hid1",
                name="Hidden Test Case 1: Highly Paid Specialist Hire",
                description="Specialist hired reporting to Sarah Connor earning $180,000.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, manager_id, title, hire_date, status)
VALUES (999, 'Super', 'Specialist', 'super@co.com', 1, 2, 'Distinguished ML Specialist', '2024-01-01', 'ACTIVE');
INSERT INTO salaries (id, employee_id, base_salary, bonus, effective_date)
VALUES (999, 999, 180000.00, 30000.00, '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q69: Comprehensive Customer Banking Portfolio (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-069",
        slug="customer-multi-account-deposit-portfolio-join",
        title="Consolidated Customer Multi-Account Portfolio",
        topic_id="top-10",
        topic="Multi-Table Joins & Self Joins",
        difficulty="medium",
        problem_description="""Wealth advisory creates consolidated balance statements for multi-account customers:
Join `customers c`, `accounts a`, and `branches b` on `c.id = a.customer_id` and `a.branch_id = b.id`.
Group by `c.id`, `customer_name`, and `b.branch_name`.
Filter for customers who maintain at least 2 accounts at the branch (`HAVING COUNT(a.id) >= 2`).
Calculate:
1. `c.id` as `customer_id`.
2. `c.first_name || ' ' || c.last_name` as `customer_name`.
3. `b.branch_name`.
4. Total account count as `account_count` (`COUNT(a.id)`).
5. Consolidated deposit balance (`ROUND(SUM(a.balance), 2)`) as `consolidated_balance`.
Order by `consolidated_balance` in descending order (`DESC`), then `customer_id` ascending (`ASC`).""",
        database_id="db-banking",
        relevant_tables=["customers", "accounts", "branches"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                ],
            ),
            TableSchemaInfo(
                table_name="accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER"),
                    ColumnSchema(name="branch_id", type="INTEGER"),
                    ColumnSchema(name="balance", type="DECIMAL(12,2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="branches",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="branch_name", type="VARCHAR(80)"),
                ],
            ),
        ],
        sample_input_data={
            "customers": [{"id": 1, "first_name": "Alice", "last_name": "Smith"}],
            "accounts": [
                {"id": 1, "customer_id": 1, "branch_id": 1, "balance": 8450.25},
                {"id": 2, "customer_id": 1, "branch_id": 1, "balance": 24150.80},
            ],
            "branches": [{"id": 1, "branch_name": "Downtown Central"}],
        },
        expected_output=ExpectedOutput(
            columns=["customer_id", "customer_name", "branch_name", "account_count", "consolidated_balance"],
            sample_rows=[
                [4, "Diana Prince", "Midtown Plaza", 2, 50000.50],
                [1, "Alice Smith", "Downtown Central", 2, 32601.05],
            ],
            total_row_count=8,
        ),
        starter_code="-- Join customers, accounts, branches; group by customer & branch; filter count >= 2\nSELECT \nFROM customers c\n",
        expected_solution="""SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    b.branch_name,
    COUNT(a.id) AS account_count,
    ROUND(SUM(a.balance), 2) AS consolidated_balance
FROM customers c
INNER JOIN accounts a ON c.id = a.customer_id
INNER JOIN branches b ON a.branch_id = b.id
GROUP BY c.id, customer_name, b.branch_name
HAVING COUNT(a.id) >= 2
ORDER BY consolidated_balance DESC, customer_id ASC;""",
        alternative_solution="""SELECT 
    c.id AS customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    b.branch_name,
    COUNT(a.id) AS account_count,
    ROUND(SUM(a.balance), 2) AS consolidated_balance
FROM customers c
JOIN accounts a ON c.id = a.customer_id
JOIN branches b ON a.branch_id = b.id
GROUP BY c.id, c.first_name, c.last_name, b.branch_name
HAVING COUNT(a.id) > 1
ORDER BY consolidated_balance DESC, c.id ASC;""",
        hints=[
            "Join `customers c` -> `accounts a` -> `branches b`.",
            "Group by `c.id, customer_name, b.branch_name`.",
            "Filter with `HAVING COUNT(a.id) >= 2`.",
            "Order by `consolidated_balance DESC, customer_id ASC`.",
        ],
        detailed_explanation="""Joining multiple entity relations and aggregating across shared attributes
consolidates multi-product financial balances.
Notice how grouping by `c.id, customer_name, b.branch_name` cleanly aggregates checking and savings accounts
held by the same customer at a specific branch without Cartesian cross-product inflation.""",
        related_concepts=["Multi-Table Grouping", "Consolidated Portfolios", "Cross-Entity Aggregation"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-069-pub",
                name="Default Customers",
                description="8 multi-account customer branch relationships.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-069-hid1",
                name="Hidden Test Case 1: Additional High Balance Account",
                description="Customer 1 opens third account with $100K balance.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 1, 1, 'ACC-EXTRA', 'Money Market', 100000.00, 'active', '2024-03-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q70: Co-Worker Project Collaboration Pairs (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-070",
        slug="coworker-project-collaboration-pairs",
        title="Co-Worker Project Collaboration Pairs (Complex Self Join)",
        topic_id="top-10",
        topic="Multi-Table Joins & Self Joins",
        difficulty="hard",
        problem_description="""Engineering workforce analytics wants to discover collaboration networks by identifying all pairs of colleagues working together on the same project:
Join `employee_projects ep1` and `employee_projects ep2` on:
- `ep1.project_id = ep2.project_id`
- `ep1.employee_id < ep2.employee_id` (Crucial: using `<` eliminates self-pairings and avoids mirror duplicates like (A,B) and (B,A)!).
Join `projects p` on `ep1.project_id = p.id`.
Join `employees e1` on `ep1.employee_id = e1.id`.
Join `employees e2` on `ep2.employee_id = e2.id`.
Filter for projects where the combined hours allocated to the pair is at least 40 hours (`ep1.hours_allocated + ep2.hours_allocated >= 40`).
Return:
1. `p.name` as `project_name`.
2. First employee full name as `colleague_1` (`e1.first_name || ' ' || e1.last_name`).
3. Second employee full name as `colleague_2` (`e2.first_name || ' ' || e2.last_name`).
4. Total combined weekly hours (`ep1.hours_allocated + ep2.hours_allocated`) as `combined_hours`.
Order by `combined_hours` descending (`DESC`), then `project_name` ascending (`ASC`), then `colleague_1` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employee_projects", "projects", "employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employee_projects",
                columns=[
                    ColumnSchema(name="employee_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="project_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="hours_allocated", type="INTEGER"),
                ],
            ),
            TableSchemaInfo(
                table_name="projects",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(120)"),
                ],
            ),
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                ],
            ),
        ],
        sample_input_data={
            "employee_projects": [
                {"project_id": 1, "employee_id": 1, "hours_allocated": 25},
                {"project_id": 1, "employee_id": 2, "hours_allocated": 25},
            ],
            "projects": [{"id": 1, "name": "NextGen Cloud Platform"}],
            "employees": [
                {"id": 1, "first_name": "Alexander", "last_name": "Pierce"},
                {"id": 2, "first_name": "Sarah", "last_name": "Connor"},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["project_name", "colleague_1", "colleague_2", "combined_hours"],
            sample_rows=[
                ["NextGen Cloud Platform", "Alexander Pierce", "Sarah Connor", 50],
                ["NextGen Cloud Platform", "Alexander Pierce", "David Chen", 45],
            ],
            total_row_count=15,
        ),
        starter_code="-- Self join employee_projects ep1 and ep2 on project_id and ep1.employee_id < ep2.employee_id\nSELECT \nFROM employee_projects ep1\n",
        expected_solution="""SELECT 
    p.name AS project_name,
    e1.first_name || ' ' || e1.last_name AS colleague_1,
    e2.first_name || ' ' || e2.last_name AS colleague_2,
    ep1.hours_allocated + ep2.hours_allocated AS combined_hours
FROM employee_projects ep1
INNER JOIN employee_projects ep2 
    ON ep1.project_id = ep2.project_id 
   AND ep1.employee_id < ep2.employee_id
INNER JOIN projects p ON ep1.project_id = p.id
INNER JOIN employees e1 ON ep1.employee_id = e1.id
INNER JOIN employees e2 ON ep2.employee_id = e2.id
WHERE ep1.hours_allocated + ep2.hours_allocated >= 40
ORDER BY combined_hours DESC, project_name ASC, colleague_1 ASC;""",
        alternative_solution="""SELECT 
    p.name AS project_name,
    CONCAT(e1.first_name, ' ', e1.last_name) AS colleague_1,
    CONCAT(e2.first_name, ' ', e2.last_name) AS colleague_2,
    (ep1.hours_allocated + ep2.hours_allocated) AS combined_hours
FROM employee_projects ep1
JOIN employee_projects ep2 
    ON ep1.project_id = ep2.project_id 
   AND ep1.employee_id < ep2.employee_id
JOIN projects p ON ep1.project_id = p.id
JOIN employees e1 ON ep1.employee_id = e1.id
JOIN employees e2 ON ep2.employee_id = e2.id
WHERE (ep1.hours_allocated + ep2.hours_allocated) >= 40
ORDER BY combined_hours DESC, project_name ASC, colleague_1 ASC;""",
        hints=[
            "Self-join `employee_projects` with `ep1.project_id = ep2.project_id AND ep1.employee_id < ep2.employee_id`.",
            "Joining with strict inequality `<` eliminates self-pairing `(id, id)` and ensures each pair appears exactly once.",
            "Join `projects p`, `employees e1`, and `employees e2` to fetch human-readable names.",
            "Filter with `WHERE ep1.hours_allocated + ep2.hours_allocated >= 40`.",
        ],
        detailed_explanation="""Pairwise combination queries are a standard graph analysis pattern in relational databases.
Joining a relation to itself on a common grouping key (`project_id`) creates edges between related nodes.
Using `ep1.employee_id < ep2.employee_id` is a mathematical masterclass in SQL deduplication:
1. It prevents pairing an employee with themselves (`ep1.id != ep2.id`).
2. It breaks symmetry so that $(A, B)$ is kept while $(B, A)$ is eliminated, yielding exact triangular matrix pairings.""",
        related_concepts=["Pairwise Self Join", "Graph Analysis", "Symmetry Breaking via Inequality"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-070-pub",
                name="Default Collaboration Pairs",
                description="Project collaboration pairs with combined >= 40 hrs.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-070-hid1",
                name="Hidden Test Case 1: Additional Project Pair",
                description="Pair working 50 hours on project 1 takes top rank.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employee_projects (employee_id, project_id, role, hours_allocated, assigned_date)
VALUES (99, 1, 'Consultant', 30, '2024-01-01');""",
            ),
        ],
    ),
]
