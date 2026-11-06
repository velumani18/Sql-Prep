from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_08_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q50: Basic Two-Table Join (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-050",
        slug="employee-department-inner-join",
        title="Employee Roster with Department Names",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="easy",
        problem_description="""Internal communications needs a complete staff directory including department names.
Join the `employees` table with the `departments` table on `e.department_id = d.id`.
Retrieve `e.id` (as `employee_id`), `e.first_name`, `e.last_name`, `e.title`, and `d.name` (as `department_name`).
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
                ],
            ),
            TableSchemaInfo(
                table_name="departments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(80)"),
                ],
            ),
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "last_name": "Pierce", "title": "VP of Engineering", "department_id": 1},
                {"id": 15, "first_name": "Rachel", "last_name": "Green", "title": "Brand Lead", "department_id": 2},
            ],
            "departments": [
                {"id": 1, "name": "Engineering"},
                {"id": 2, "name": "Marketing"},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "first_name", "last_name", "title", "department_name"],
            sample_rows=[
                [1, "Alexander", "Pierce", "VP of Engineering", "Engineering"],
                [2, "Sarah", "Connor", "Engineering Manager", "Engineering"],
                [3, "David", "Chen", "Staff Software Engineer", "Engineering"],
            ],
            total_row_count=55,
        ),
        starter_code="-- INNER JOIN employees and departments on department_id = departments.id\nSELECT \nFROM employees e\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.title,
    d.name AS department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
ORDER BY employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.title,
    d.name AS department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
ORDER BY e.id ASC;""",
        hints=[
            "Use `INNER JOIN departments d ON e.department_id = d.id`.",
            "Alias `d.name` as `department_name` and `e.id` as `employee_id`.",
            "Order by `employee_id ASC`.",
        ],
        detailed_explanation="""The `INNER JOIN` matches rows between two relations where the join condition evaluates to TRUE.
Employees without a department (`department_id IS NULL`) or departments without employees are excluded.
In SQL, writing `JOIN` without specifying an outer type defaults to an `INNER JOIN`.""",
        related_concepts=["INNER JOIN", "Foreign Key Navigation", "Equi-Join"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-050-pub",
                name="Default Company Staff",
                description="55 department-linked employees.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-050-hid1",
                name="Hidden Test Case 1: Additional Joined Employee",
                description="New hire in Legal department.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Saul', 'Goodman', 'saul@law.com', 6, 'Legal Counsel', '2024-01-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q51: Order with Customer Profile (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-051",
        slug="orders-with-customer-profile-join",
        title="Orders with Customer Profile Navigation",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="easy",
        problem_description="""Order fulfillment logs require customer demographic information.
Join the `orders` table with the `customers` table on `o.customer_id = c.id`.
Retrieve `o.id` (as `order_id`), `o.order_date`, `o.total_amount`, `c.name` (as `customer_name`), and `c.city`.
Order by `order_id` in ascending order (`ASC`).""",
        database_id="db-ecommerce",
        relevant_tables=["orders", "customers"],
        table_schemas=[
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="order_date", type="DATE"),
                    ColumnSchema(name="total_amount", type="DECIMAL(10,2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(100)"),
                    ColumnSchema(name="city", type="VARCHAR(60)"),
                ],
            ),
        ],
        sample_input_data={
            "orders": [
                {"id": 1, "customer_id": 1, "order_date": "2024-01-10", "total_amount": 129.99},
                {"id": 2, "customer_id": 2, "order_date": "2024-01-12", "total_amount": 499.98},
            ],
            "customers": [
                {"id": 1, "name": "Alice Smith", "city": "New York"},
                {"id": 2, "name": "Bob Jones", "city": "Los Angeles"},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["order_id", "order_date", "total_amount", "customer_name", "city"],
            sample_rows=[
                [1, "2024-01-10", 129.99, "Alice Smith", "New York"],
                [2, "2024-01-12", 499.98, "Bob Jones", "Los Angeles"],
            ],
            total_row_count=35,
        ),
        starter_code="-- Join orders and customers on o.customer_id = c.id\nSELECT \nFROM orders o\n",
        expected_solution="""SELECT 
    o.id AS order_id,
    o.order_date,
    o.total_amount,
    c.name AS customer_name,
    c.city
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
ORDER BY order_id ASC;""",
        alternative_solution="""SELECT 
    o.id AS order_id,
    o.order_date,
    o.total_amount,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city
FROM orders o
JOIN customers c ON o.customer_id = c.id
ORDER BY o.id ASC;""",
        hints=[
            "Join orders to customers using `ON o.customer_id = c.id`.",
            "Alias `c.name` as `customer_name` and `o.id` as `order_id`.",
            "Order by `order_id ASC`.",
        ],
        detailed_explanation="""This is the classic One-to-Many relational join pattern:
One customer can place multiple orders, and each order belongs to exactly one customer.
Joining through the foreign key `orders.customer_id` enriches each order record
with the parent customer's metadata.""",
        related_concepts=["One-to-Many Join", "INNER JOIN", "Foreign Key Lookup"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-051-pub",
                name="Default Orders",
                description="35 e-commerce orders.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-051-hid1",
                name="Hidden Test Case 1: Additional Order",
                description="New order placed by customer 1.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO orders (id, customer_id, order_date, total_amount, status)
VALUES (999, 1, '2024-03-01', 349.00, 'completed');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q52: Course with Professor Info (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-052",
        slug="course-catalog-instructor-assignment-join",
        title="Course Catalog Instructor Directory",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="easy",
        problem_description="""Students registering for courses need to see the assigned instructor's full name.
Join `courses` and `professors` on `c.professor_id = p.id`.
Retrieve `c.code`, `c.title` (as `course_title`), `c.credits`, and concatenate the professor's full name
(`p.first_name || ' ' || p.last_name`) as `professor_name`.
Order by `c.code` in ascending order (`ASC`).""",
        database_id="db-university",
        relevant_tables=["courses", "professors"],
        table_schemas=[
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="code", type="VARCHAR(15)"),
                    ColumnSchema(name="title", type="VARCHAR(120)"),
                    ColumnSchema(name="credits", type="INTEGER"),
                    ColumnSchema(name="professor_id", type="INTEGER", is_foreign_key=True),
                ],
            ),
            TableSchemaInfo(
                table_name="professors",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                ],
            ),
        ],
        sample_input_data={
            "courses": [
                {"code": "CS101", "title": "Intro to CS", "credits": 4, "professor_id": 1},
                {"code": "MATH101", "title": "Calculus I", "credits": 4, "professor_id": 3},
            ],
            "professors": [
                {"id": 1, "first_name": "Alan", "last_name": "Turing"},
                {"id": 3, "first_name": "Carl", "last_name": "Gauss"},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["code", "course_title", "credits", "professor_name"],
            sample_rows=[
                ["BIO101", "Cellular Biology", 4, "Charles Darwin"],
                ["CHEM101", "General Chemistry", 4, "Marie Curie"],
                ["CS101", "Introduction to Computer Science", 4, "Alan Turing"],
            ],
            total_row_count=12,
        ),
        starter_code="-- Join courses and professors: code, course_title, credits, professor_name\nSELECT \nFROM courses c\n",
        expected_solution="""SELECT 
    c.code,
    c.title AS course_title,
    c.credits,
    p.first_name || ' ' || p.last_name AS professor_name
FROM courses c
INNER JOIN professors p ON c.professor_id = p.id
ORDER BY c.code ASC;""",
        alternative_solution="""SELECT 
    c.code,
    c.title AS course_title,
    c.credits,
    CONCAT(p.first_name, ' ', p.last_name) AS professor_name
FROM courses c
JOIN professors p ON c.professor_id = p.id
ORDER BY c.code ASC;""",
        hints=[
            "Join `courses c` with `professors p` on `c.professor_id = p.id`.",
            "Use `p.first_name || ' ' || p.last_name AS professor_name`.",
            "Alias `c.title` as `course_title` and order by `c.code ASC`.",
        ],
        detailed_explanation="""Joining tables allows string concatenation and computed expressions
spanning columns from multiple relations (`professors.first_name` and `professors.last_name` alongside `courses.title`).
Because this is an `INNER JOIN`, unassigned courses (`professor_id IS NULL`) are omitted automatically.""",
        related_concepts=["INNER JOIN", "Cross-Table String Formatting", "Referential Navigation"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-052-pub",
                name="Default Courses",
                description="12 courses assigned to professors.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-052-hid1",
                name="Hidden Test Case 1: Additional Course",
                description="New Robotics course assigned to Professor Turing.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO courses (id, code, title, department_id, professor_id, credits)
VALUES (999, 'CS480', 'Artificial Robotics', 1, 1, 4);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q53: Three-Table Analytical Filtering (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-053",
        slug="engineering-top-earners-three-way-join",
        title="High-Earning Engineering Personnel (Three-Table Join)",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="medium",
        problem_description="""Compensation audit wants a list of all Engineering employees earning a high base salary.
Join:
1. `employees` with `departments` on `e.department_id = d.id`.
2. `employees` with `salaries` on `e.id = s.employee_id`.
Filter for:
- `d.name = 'Engineering'`
- `s.base_salary >= 120000.00`
Return `e.id` (as `employee_id`), concatenated full name as `employee_name` (`e.first_name || ' ' || e.last_name`), `e.title`, and `s.base_salary`.
Order by `s.base_salary` in descending order (`DESC`), then `employee_id` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees", "departments", "salaries"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(100)"),
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
            "employees": [
                {"id": 1, "first_name": "Alexander", "last_name": "Pierce", "department_id": 1},
                {"id": 2, "first_name": "Sarah", "last_name": "Connor", "department_id": 1},
                {"id": 15, "first_name": "Rachel", "last_name": "Green", "department_id": 2},
            ],
            "departments": [{"id": 1, "name": "Engineering"}, {"id": 2, "name": "Marketing"}],
            "salaries": [
                {"employee_id": 1, "base_salary": 220000.00},
                {"employee_id": 2, "base_salary": 160000.00},
                {"employee_id": 15, "base_salary": 140000.00},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "employee_name", "title", "base_salary"],
            sample_rows=[
                [1, "Alexander Pierce", "VP of Engineering", 220000.00],
                [2, "Sarah Connor", "Engineering Manager", 160000.00],
                [3, "David Chen", "Staff Software Engineer", 140000.00],
            ],
            total_row_count=5,
        ),
        starter_code="-- Join employees, departments, salaries; filter Engineering >= 120,000\nSELECT \nFROM employees e\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.title,
    s.base_salary
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
INNER JOIN salaries s ON e.id = s.employee_id
WHERE d.name = 'Engineering' AND s.base_salary >= 120000.00
ORDER BY s.base_salary DESC, employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
    e.title,
    s.base_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN salaries s ON e.id = s.employee_id
WHERE d.name = 'Engineering' AND s.base_salary >= 120000
ORDER BY 4 DESC, 1 ASC;""",
        hints=[
            "Chain two INNER JOIN clauses: join to `departments` and join to `salaries`.",
            "Filter with `WHERE d.name = 'Engineering' AND s.base_salary >= 120000.00`.",
            "Order by `s.base_salary DESC, employee_id ASC`.",
        ],
        detailed_explanation="""Chaining multiple joins traverses the relational graph.
Here, `employees` acts as the hub connecting to its parent department dimension and its 1:1 salary extension.
The query engine analyzes predicate selectivity to order joins optimally,
filtering on `d.name = 'Engineering'` first before joining the salary records.""",
        related_concepts=["Multi-Table Join", "Relational Traversal", "Join Optimization"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-053-pub",
                name="Default Engineering Staff",
                description="5 Engineering employees earning >= $120K.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-053-hid1",
                name="Hidden Test Case 1: High Earning Marketing Staff",
                description="Marketing staff earning $150K (must be excluded due to department).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Marketer', 'Top', 'mtop@co.com', 2, 'CMO', '2023-01-01', 'ACTIVE');
INSERT INTO salaries (id, employee_id, base_salary, bonus, effective_date)
VALUES (999, 999, 150000.00, 30000.00, '2023-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q54: Customer Account Overview with Branch Details (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-054",
        slug="customer-account-branch-portfolio-join",
        title="High-Balance Customer Account and Branch Portfolio",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="medium",
        problem_description="""Wealth management advisors need an overview of accounts with significant balances:
Join:
1. `accounts` with `customers` on `a.customer_id = c.id`.
2. `accounts` with `branches` on `a.branch_id = b.id`.
Filter for active accounts with `balance >= 25000.00`.
Return `a.account_number`, concatenated customer full name as `customer_name` (`c.first_name || ' ' || c.last_name`),
`b.branch_name`, `a.account_type`, and `a.balance`.
Order by `a.balance` in descending order (`DESC`).""",
        database_id="db-banking",
        relevant_tables=["accounts", "customers", "branches"],
        table_schemas=[
            TableSchemaInfo(
                table_name="accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="branch_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="account_number", type="VARCHAR(20)"),
                    ColumnSchema(name="account_type", type="VARCHAR(30)"),
                    ColumnSchema(name="balance", type="DECIMAL(12,2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
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
            "accounts": [
                {"account_number": "ACC-1005", "customer_id": 5, "branch_id": 1, "account_type": "Business", "balance": 112400.00},
                {"account_number": "ACC-1002", "customer_id": 2, "branch_id": 2, "account_type": "Savings", "balance": 24150.80},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["account_number", "customer_name", "branch_name", "account_type", "balance"],
            sample_rows=[
                ["ACC-1023", "Tony Stark", "Silicon Hub", "Business", 250000.00],
                ["ACC-1005", "Evan Wright", "Downtown Flagship", "Business", 112400.00],
                ["ACC-1015", "Paul Allen", "Highland Branch", "Business", 68500.00],
            ],
            total_row_count=8,
        ),
        starter_code="-- Join accounts, customers, branches; filter balance >= 25,000\nSELECT \nFROM accounts a\n",
        expected_solution="""SELECT 
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    b.branch_name,
    a.account_type,
    a.balance
FROM accounts a
INNER JOIN customers c ON a.customer_id = c.id
INNER JOIN branches b ON a.branch_id = b.id
WHERE a.balance >= 25000.00
ORDER BY a.balance DESC;""",
        alternative_solution="""SELECT 
    a.account_number,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    b.branch_name,
    a.account_type,
    a.balance
FROM accounts a
JOIN customers c ON a.customer_id = c.id
JOIN branches b ON a.branch_id = b.id
WHERE a.balance >= 25000
ORDER BY a.balance DESC;""",
        hints=[
            "Join `accounts a` to `customers c` and `branches b`.",
            "Filter with `WHERE a.balance >= 25000.00`.",
            "Order by `a.balance DESC`.",
        ],
        detailed_explanation="""In relational databases, junction tables or entity tables often have multiple foreign keys pointing to distinct parent dimension tables.
Here, `accounts` references both `customers` and `branches`.
By joining both parent tables, we aggregate human-readable customer names and physical branch descriptions in a single query.""",
        related_concepts=["Multi-Parent Join", "Star Schema Navigation", "Financial Portfolio"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-054-pub",
                name="Default Accounts",
                description="8 accounts with balance >= $25,000.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-054-hid1",
                name="Hidden Test Case 1: Additional High Balance Account",
                description="New account with $500,000 balance.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 1, 1, 'ACC-MAX', 'Business', 500000.00, 'active', '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q55: Order Items with Product Catalog (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-055",
        slug="order-item-line-valuation-join",
        title="Multi-Quantity Order Line Item Valuation",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="medium",
        problem_description="""Order management audits bulk purchase items:
Join `order_items` and `products` on `oi.product_id = p.id`.
Filter for line items where `oi.quantity >= 2`.
Calculate line total (`oi.quantity * oi.unit_price`) rounded to 2 decimals as `line_total`.
Return `oi.id` (as `item_id`), `oi.order_id`, `p.name` (as `product_name`), `oi.quantity`, `oi.unit_price`, and `line_total`.
Order by `line_total` descending (`DESC`), then `item_id` ascending (`ASC`).""",
        database_id="db-ecommerce",
        relevant_tables=["order_items", "products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="order_items",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="order_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="product_id", type="INTEGER", is_foreign_key=True),
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
            "order_items": [
                {"id": 1, "order_id": 1, "product_id": 1, "quantity": 1, "unit_price": 49.99},
                {"id": 2, "order_id": 2, "product_id": 2, "quantity": 2, "unit_price": 129.99},
            ],
            "products": [
                {"id": 1, "name": "Mouse"},
                {"id": 2, "name": "Keyboard"},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["item_id", "order_id", "product_name", "quantity", "unit_price", "line_total"],
            sample_rows=[
                [4, 2, "Mechanical RGB Keyboard", 2, 129.99, 259.98],
                [8, 4, "Wireless Ergonomic Mouse", 2, 49.99, 99.98],
            ],
            total_row_count=10,
        ),
        starter_code="-- Join order_items and products; filter quantity >= 2\nSELECT \nFROM order_items oi\n",
        expected_solution="""SELECT 
    oi.id AS item_id,
    oi.order_id,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    ROUND(oi.quantity * oi.unit_price, 2) AS line_total
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.id
WHERE oi.quantity >= 2
ORDER BY line_total DESC, item_id ASC;""",
        alternative_solution="""SELECT 
    oi.id AS item_id,
    oi.order_id,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    ROUND(CAST(oi.quantity AS REAL) * oi.unit_price, 2) AS line_total
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.quantity > 1
ORDER BY 6 DESC, 1 ASC;""",
        hints=[
            "Join `order_items oi` to `products p` on `oi.product_id = p.id`.",
            "Filter with `WHERE oi.quantity >= 2`.",
            "Compute `ROUND(oi.quantity * oi.unit_price, 2) AS line_total`.",
        ],
        detailed_explanation="""Joining line items with catalog products provides descriptive product names
while preserving the historical transaction price (`oi.unit_price`).
Filtering on `quantity >= 2` isolates multi-item volume orders, and ordering by `line_total DESC, item_id ASC`
guarantees stable, deterministic output.""",
        related_concepts=["Line Item Calculation", "Price History Preservation", "Deterministic Sorting"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-055-pub",
                name="Default Order Items",
                description="45 line items across 35 orders.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-055-hid1",
                name="Hidden Test Case 1: Bulk Monitor Purchase",
                description="Bulk purchase of 5 monitors for $2,000 takes top rank.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO order_items (id, order_id, product_id, quantity, unit_price)
VALUES (999, 1, 4, 5, 399.99);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q56: Project Staffing and Budget Allocation (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-056",
        slug="project-staffing-capacity-allocation-join",
        title="Project Staffing & Capacity Allocation Analysis",
        topic_id="top-08",
        topic="INNER JOIN & Relational Navigation",
        difficulty="hard",
        problem_description="""Program management is auditing resource allocation across active enterprise initiatives:
Join `projects` and the junction table `employee_projects` on `p.id = ep.project_id`.
Group by `p.id`, `p.name`, and `p.budget`.
Calculate:
1. `p.id` as `project_id`.
2. `p.name` as `project_name`.
3. `p.budget`.
4. Total distinct employees assigned as `assigned_staff_count` (`COUNT(DISTINCT ep.employee_id)`).
5. Total weekly hours allocated as `total_allocated_hours` (`SUM(ep.hours_allocated)`).
Filter to only include projects that have at least 3 assigned employees (`HAVING COUNT(DISTINCT ep.employee_id) >= 3`).
Order by `total_allocated_hours` in descending order (`DESC`), then `project_id` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["projects", "employee_projects"],
        table_schemas=[
            TableSchemaInfo(
                table_name="projects",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(120)"),
                    ColumnSchema(name="budget", type="DECIMAL(12,2)"),
                ],
            ),
            TableSchemaInfo(
                table_name="employee_projects",
                columns=[
                    ColumnSchema(name="employee_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="project_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="hours_allocated", type="INTEGER"),
                ],
            ),
        ],
        sample_input_data={
            "projects": [
                {"id": 1, "name": "NextGen Cloud Platform", "budget": 850000.00},
                {"id": 2, "name": "Data Mesh Pipeline", "budget": 450000.00},
            ],
            "employee_projects": [
                {"project_id": 1, "employee_id": 1, "hours_allocated": 20},
                {"project_id": 1, "employee_id": 2, "hours_allocated": 25},
                {"project_id": 1, "employee_id": 3, "hours_allocated": 30},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["project_id", "project_name", "budget", "assigned_staff_count", "total_allocated_hours"],
            sample_rows=[
                [1, "NextGen Cloud Platform", 850000.00, 6, 140],
                [2, "Data Mesh Pipeline", 450000.00, 5, 115],
            ],
            total_row_count=5,
        ),
        starter_code="-- Join projects and employee_projects; group by project; filter staff >= 3\nSELECT \nFROM projects p\n",
        expected_solution="""SELECT 
    p.id AS project_id,
    p.name AS project_name,
    p.budget,
    COUNT(DISTINCT ep.employee_id) AS assigned_staff_count,
    SUM(ep.hours_allocated) AS total_allocated_hours
FROM projects p
INNER JOIN employee_projects ep ON p.id = ep.project_id
GROUP BY p.id, p.name, p.budget
HAVING COUNT(DISTINCT ep.employee_id) >= 3
ORDER BY total_allocated_hours DESC, project_id ASC;""",
        alternative_solution="""SELECT 
    p.id AS project_id,
    p.name AS project_name,
    p.budget,
    COUNT(ep.employee_id) AS assigned_staff_count,
    SUM(ep.hours_allocated) AS total_allocated_hours
FROM projects p
JOIN employee_projects ep ON p.id = ep.project_id
GROUP BY p.id, p.name, p.budget
HAVING COUNT(ep.employee_id) > 2
ORDER BY 5 DESC, 1 ASC;""",
        hints=[
            "Join `projects p` with `employee_projects ep` on `p.id = ep.project_id`.",
            "Group by `p.id, p.name, p.budget`.",
            "Use `HAVING COUNT(DISTINCT ep.employee_id) >= 3`.",
            "Order by `total_allocated_hours DESC, project_id ASC`.",
        ],
        detailed_explanation="""This query integrates relational joins, group aggregations, and post-aggregation filtering (`HAVING`).
Grouping by all non-aggregated columns (`p.id, p.name, p.budget`) satisfies standard ANSI SQL GROUP BY semantics.
`COUNT(DISTINCT ep.employee_id)` guarantees accurate headcount even if duplicate allocations exist,
and `SUM(ep.hours_allocated)` computes overall project burn rate.""",
        related_concepts=["Junction Table Join", "GROUP BY with Joins", "HAVING with Distinct Count"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-056-pub",
                name="Default Enterprise Projects",
                description="Enterprise projects with team allocations.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-056-hid1",
                name="Hidden Test Case 1: Massive Project Allocation",
                description="High priority initiative with 8 staff and 200 hours takes #1 rank.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO projects (id, name, department_id, start_date, end_date, budget)
VALUES (999, 'Quantum AI Gateway', 1, '2024-01-01', '2025-01-01', 2000000.00);
INSERT INTO employee_projects (employee_id, project_id, role, hours_allocated, assigned_date) VALUES
(1, 999, 'Lead', 40, '2024-01-01'),
(2, 999, 'Engineer', 40, '2024-01-01'),
(3, 999, 'Engineer', 40, '2024-01-01'),
(4, 999, 'Engineer', 40, '2024-01-01');""",
            ),
        ],
    ),
]
