from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_02_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q8: Numerical Budget Comparison (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-008",
        slug="departments-high-budget-threshold",
        title="High Budget Department Filtering",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="easy",
        problem_description="""Corporate finance is auditing high-expenditure divisions.
Write a query to retrieve all departments with a `budget >= 300000.00`.
Return `id`, `name`, and `budget`.""",
        database_id="db-company",
        relevant_tables=["departments"],
        table_schemas=[
            TableSchemaInfo(
                table_name="departments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(80)"),
                    ColumnSchema(name="budget", type="DECIMAL(12,2)"),
                    ColumnSchema(name="location", type="VARCHAR(100)"),
                ],
            )
        ],
        sample_input_data={
            "departments": [
                {"id": 1, "name": "Engineering", "budget": 1200000.00},
                {"id": 2, "name": "Marketing", "budget": 450000.00},
                {"id": 6, "name": "Legal", "budget": 200000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["id", "name", "budget"],
            sample_rows=[
                [1, "Engineering", 1200000.00],
                [2, "Marketing", 450000.00],
                [3, "Sales", 600000.00],
                [5, "Product", 500000.00],
            ],
            total_row_count=4,
        ),
        starter_code="-- Filter departments with budget >= 300,000\nSELECT \nFROM departments\n",
        expected_solution="""SELECT id, name, budget
FROM departments
WHERE budget >= 300000.00;""",
        alternative_solution="""SELECT d.id, d.name, d.budget
FROM departments d
WHERE NOT (d.budget < 300000.00);""",
        hints=[
            "Use the WHERE clause with the greater-than-or-equal operator: `WHERE budget >= 300000.00`.",
            "Select only the requested columns: `id`, `name`, `budget`.",
        ],
        detailed_explanation="""The `WHERE` clause filters rows before any grouping or aggregation takes place.
Comparison operators (`=`, `!=`, `<`, `<=`, `>`, `>=`) evaluate row values against literals.
When applied to indexed numeric columns, B-Tree index range seeks can satisfy `>=` filters in $O(\\log N)$ time.""",
        related_concepts=["WHERE", "Comparison Operators", "Range Predicates"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-008-pub",
                name="Default Department Budgets",
                description="Standard corporate department roster.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-008-hid1",
                name="Hidden Test Case 1: Additional R&D Department",
                description="New AI Research division with $2.5M budget.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO departments (id, name, budget, location)
VALUES (99, 'AI Research', 2500000.00, 'San Francisco');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q9: String Literal Equality Filter (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-009",
        slug="cancelled-ecommerce-orders",
        title="Cancelled Orders Investigation",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="easy",
        problem_description="""Customer support is analyzing order drop-offs and cancellation causes.
Write a query to retrieve all orders where `status = 'cancelled'`.
Return `id` (as `order_id`), `customer_id`, `order_date`, and `total_amount`.""",
        database_id="db-ecommerce",
        relevant_tables=["orders"],
        table_schemas=[
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="order_date", type="DATE"),
                    ColumnSchema(name="total_amount", type="DECIMAL(10,2)"),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                ],
            )
        ],
        sample_input_data={
            "orders": [
                {"id": 1, "customer_id": 1, "order_date": "2024-01-10", "total_amount": 129.99, "status": "completed"},
                {"id": 5, "customer_id": 4, "order_date": "2024-01-15", "total_amount": 599.98, "status": "cancelled"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["order_id", "customer_id", "order_date", "total_amount"],
            sample_rows=[
                [5, 4, "2024-01-15", 599.98],
                [12, 10, "2024-01-28", 249.50],
            ],
            total_row_count=5,
        ),
        starter_code="-- Select cancelled orders\nSELECT \nFROM orders\n",
        expected_solution="""SELECT 
    id AS order_id,
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE status = 'cancelled';""",
        alternative_solution="""SELECT 
    o.id AS order_id,
    o.customer_id,
    o.order_date,
    o.total_amount
FROM orders o
WHERE LOWER(o.status) = 'cancelled';""",
        hints=[
            "Filter rows using `WHERE status = 'cancelled'` (single quotes for string literals).",
            "Remember to alias `id` as `order_id`.",
        ],
        detailed_explanation="""In SQL, string literals are enclosed in single quotes (`'cancelled'`).
Double quotes (`"identifier"`) denote table or column identifiers in ANSI SQL standards.
String equality comparisons are case-sensitive by default in standard SQL and SQLite unless a case-insensitive collation (`COLLATE NOCASE`) is configured.""",
        related_concepts=["String Comparison", "WHERE", "Literals vs Identifiers"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-009-pub",
                name="Public Orders",
                description="Default 35 e-commerce orders.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-009-hid1",
                name="Hidden Test Case 1: Extra Cancellation",
                description="Dataset with newly cancelled order.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO orders (id, customer_id, order_date, total_amount, status)
VALUES (999, 1, '2024-03-01', 89.95, 'cancelled');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q10: Low Balance Checking Accounts (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-010",
        slug="low-balance-checking-accounts",
        title="Low Balance Checking Account Alert",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="easy",
        problem_description="""Retail banking risk officers want to identify checking accounts approaching overdraft.
Write a query to find all accounts where `account_type = 'Checking'` and `balance < 2000.00`.
Return `id` (as `account_id`), `customer_id`, and `balance`.""",
        database_id="db-banking",
        relevant_tables=["accounts"],
        table_schemas=[
            TableSchemaInfo(
                table_name="accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER"),
                    ColumnSchema(name="account_type", type="VARCHAR(30)"),
                    ColumnSchema(name="balance", type="DECIMAL(12,2)"),
                ],
            )
        ],
        sample_input_data={
            "accounts": [
                {"id": 1, "customer_id": 1, "account_type": "Checking", "balance": 8450.25},
                {"id": 3, "customer_id": 2, "account_type": "Checking", "balance": 1250.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["account_id", "customer_id", "balance"],
            sample_rows=[
                [3, 2, 1250.00],
                [7, 5, 850.50],
            ],
            total_row_count=5,
        ),
        starter_code="-- Find checking accounts with balance under 2,000\nSELECT \nFROM accounts\n",
        expected_solution="""SELECT 
    id AS account_id,
    customer_id,
    balance
FROM accounts
WHERE account_type = 'Checking' AND balance < 2000.00;""",
        alternative_solution="""SELECT 
    a.id AS account_id,
    a.customer_id,
    a.balance
FROM accounts a
WHERE a.account_type = 'Checking' AND a.balance <= 1999.99;""",
        hints=[
            "Combine conditions using `AND`: `account_type = 'Checking' AND balance < 2000.00`.",
            "Alias `id` as `account_id`.",
        ],
        detailed_explanation="""Combining multiple predicates with `AND` requires that both conditions evaluate to TRUE.
Database query planners evaluate conjunctions by executing the most selective filter first,
reducing the number of row candidates examined in subsequent checks.""",
        related_concepts=["AND", "Conjunction", "Predicate Evaluation Order"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-010-pub",
                name="Default Accounts",
                description="Standard account balance dataset.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-010-hid1",
                name="Hidden Test Case 1: Additional Low Balance Account",
                description="Checking account with $150 balance.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 3, 1, 'CHK-999111', 'Checking', 150.00, 'active', '2024-02-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q11: Date-based Comparison & Department Assignment (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-011",
        slug="recent-hires-with-departments",
        title="Recent Hires with Assigned Departments",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="medium",
        problem_description="""Human resources is tracking staffing growth since the start of 2022.
Write a query to find all employees hired on or after `'2022-01-01'` who have an assigned department (`department_id IS NOT NULL`).
Return `id` (as `employee_id`), `first_name`, `last_name`, `hire_date`, and `department_id`.""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="hire_date", type="DATE"),
                    ColumnSchema(name="department_id", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "hire_date": "2020-03-15", "department_id": 1},
                {"id": 20, "first_name": "Marcus", "hire_date": "2022-06-01", "department_id": 2},
                {"id": 56, "first_name": "Grace", "hire_date": "2022-08-15", "department_id": None},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "first_name", "last_name", "hire_date", "department_id"],
            sample_rows=[
                [20, "Marcus", "Aurelius", "2022-06-01", 2],
                [21, "Julia", "Roberts", "2022-07-15", 3],
            ],
            total_row_count=20,
        ),
        starter_code="-- Find staff hired >= '2022-01-01' with non-null department_id\nSELECT \nFROM employees\n",
        expected_solution="""SELECT 
    id AS employee_id,
    first_name,
    last_name,
    hire_date,
    department_id
FROM employees
WHERE hire_date >= '2022-01-01' AND department_id IS NOT NULL;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.hire_date,
    e.department_id
FROM employees e
WHERE e.hire_date >= '2022-01-01' AND NOT (e.department_id IS NULL);""",
        hints=[
            "Use ISO-8601 formatted date strings: `'2022-01-01'`.",
            "Test for non-missing values with `IS NOT NULL`, never `!= NULL`.",
            "Alias `id` as `employee_id`.",
        ],
        detailed_explanation="""Dates in standard ISO format (`YYYY-MM-DD`) can be safely compared using standard lexicographical comparison operators (`>=`, `<=`, `=`).
In SQL, NULL signifies unknown or missing data.
Because `NULL = NULL` evaluates to UNKNOWN (three-valued logic), you must always use `IS NOT NULL` to verify presence of values.""",
        related_concepts=["Date Comparisons", "IS NOT NULL", "Three-Valued Logic"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-011-pub",
                name="Default Company Hires",
                description="Company roster with 2020-2023 hire dates.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-011-hid1",
                name="Hidden Test Case 1: Unassigned New Hire",
                description="Staff hired in 2023 but department_id is NULL.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Unassigned', 'Worker', 'unassigned@co.com', NULL, 'Contractor', '2023-01-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q12: Credit Score and Income Thresholds (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-012",
        slug="prime-mortgage-qualified-customers",
        title="Prime Mortgage Qualification Criteria",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="medium",
        problem_description="""The lending committee is pre-qualifying customers for premier mortgage rates.
To qualify, a customer must have a `credit_score >= 720` AND an `annual_income >= 80000.00`.
Write a query to retrieve `id` (as `customer_id`), `first_name`, `last_name`, `credit_score`, and `annual_income`.""",
        database_id="db-banking",
        relevant_tables=["customers"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="credit_score", type="INTEGER"),
                    ColumnSchema(name="annual_income", type="DECIMAL(12,2)"),
                ],
            )
        ],
        sample_input_data={
            "customers": [
                {"id": 1, "first_name": "Alice", "credit_score": 750, "annual_income": 95000.00},
                {"id": 2, "first_name": "Bob", "credit_score": 680, "annual_income": 120000.00},
                {"id": 3, "first_name": "Charlie", "credit_score": 740, "annual_income": 65000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["customer_id", "first_name", "last_name", "credit_score", "annual_income"],
            sample_rows=[
                [1, "Alice", "Smith", 750, 95000.00],
                [4, "Diana", "Prince", 810, 140000.00],
            ],
            total_row_count=8,
        ),
        starter_code="-- Pre-qualify customers: credit_score >= 720 and annual_income >= 80,000\nSELECT \nFROM customers\n",
        expected_solution="""SELECT 
    id AS customer_id,
    first_name,
    last_name,
    credit_score,
    annual_income
FROM customers
WHERE credit_score >= 720 AND annual_income >= 80000.00;""",
        alternative_solution="""SELECT 
    c.id AS customer_id,
    c.first_name,
    c.last_name,
    c.credit_score,
    c.annual_income
FROM customers c
WHERE c.credit_score > 719 AND c.annual_income >= 80000;""",
        hints=[
            "Combine criteria: `credit_score >= 720 AND annual_income >= 80000.00`.",
            "Alias `id` as `customer_id`.",
        ],
        detailed_explanation="""Multi-attribute qualification logic filters prospective clients on independent credit risk dimensions.
Because both predicates must be satisfied simultaneously, if either fails, the row is discarded.
Engineers typically place composite indexes `(credit_score, annual_income)` on tables supporting these query filters.""",
        related_concepts=["Conjunctive Filtering", "Composite Indexes", "Risk Thresholds"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-012-pub",
                name="Default Banking Customers",
                description="25 bank customers with various credit profiles.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-012-hid1",
                name="Hidden Test Case 1: Borderline Profile",
                description="Customer with credit_score 719 (should fail).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO customers (id, first_name, last_name, email, credit_score, annual_income, registered_branch_id, joined_date)
VALUES (999, 'Edge', 'Case', 'edge@bank.com', 719, 150000.00, 1, '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q13: Inventory Depletion Warning (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-013",
        slug="active-low-stock-products",
        title="Active Products Approaching Depletion",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="medium",
        problem_description="""Warehouse logistics needs an immediate restock trigger for popular active products.
Write a query to retrieve all active products (`is_active = 1` or `TRUE`) with `stock_quantity <= 25`.
Return `id` (as `product_id`), `name` (as `product_name`), `price`, and `stock_quantity`.""",
        database_id="db-ecommerce",
        relevant_tables=["products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="products",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(150)"),
                    ColumnSchema(name="price", type="DECIMAL(10,2)"),
                    ColumnSchema(name="stock_quantity", type="INTEGER"),
                    ColumnSchema(name="is_active", type="BOOLEAN"),
                ],
            )
        ],
        sample_input_data={
            "products": [
                {"id": 1, "name": "Wireless Ergonomic Mouse", "stock_quantity": 120, "is_active": 1},
                {"id": 4, "name": "Ultra HD 4K Monitor", "stock_quantity": 12, "is_active": 1},
                {"id": 18, "name": "Discontinued Headset", "stock_quantity": 5, "is_active": 0},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["product_id", "product_name", "price", "stock_quantity"],
            sample_rows=[
                [4, "Ultra HD 4K Monitor 27-inch", 399.99, 12],
                [8, "Ergonomic Standing Desk", 499.99, 14],
            ],
            total_row_count=5,
        ),
        starter_code="-- Find active products with stock_quantity <= 25\nSELECT \nFROM products\n",
        expected_solution="""SELECT 
    id AS product_id,
    name AS product_name,
    price,
    stock_quantity
FROM products
WHERE is_active = 1 AND stock_quantity <= 25;""",
        alternative_solution="""SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.price,
    p.stock_quantity
FROM products p
WHERE p.is_active = TRUE AND p.stock_quantity < 26;""",
        hints=[
            "Filter for active items: `is_active = 1`.",
            "Filter for low stock: `stock_quantity <= 25`.",
            "Combine both using `AND`.",
        ],
        detailed_explanation="""Filtering on active status alongside operational metrics (like inventory levels)
prevents dead or retired inventory from triggering automated procurement workflows.
In SQLite, boolean values are stored as integers (1 for TRUE, 0 for FALSE).""",
        related_concepts=["Boolean Flags", "Operational Thresholds", "WHERE"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-013-pub",
                name="Default Products",
                description="20 products with varied stock.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-013-hid1",
                name="Hidden Test Case 1: Inactive Depleted Product",
                description="Discontinued item with 0 stock (should be ignored).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, 'Legacy Modem', 19.99, 0, 0);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q14: Multi-Boundary Course Credit & Code Filter (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-014",
        slug="advanced-stem-course-criteria",
        title="Curriculum Committee: High Credit STEM Course Criteria",
        topic_id="top-02",
        topic="WHERE & Comparison Operators",
        difficulty="hard",
        problem_description="""The university curriculum accreditation board is auditing intensive STEM courses.
Write a query to identify courses meeting EITHER of the following two standards:
1. Standard A: The course grants 4 or more credits (`credits >= 4`).
2. Standard B: The course belongs to Computer Science (`code LIKE 'CS%'`) and grants at least 3 credits (`credits >= 3`).
Return `id` (as `course_id`), `code`, `title`, and `credits`.""",
        database_id="db-university",
        relevant_tables=["courses"],
        table_schemas=[
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="code", type="VARCHAR(15)"),
                    ColumnSchema(name="title", type="VARCHAR(120)"),
                    ColumnSchema(name="credits", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "courses": [
                {"id": 1, "code": "CS101", "title": "Intro to CS", "credits": 4},
                {"id": 3, "code": "MATH101", "title": "Calculus I", "credits": 4},
                {"id": 4, "code": "CS201", "title": "Data Structures", "credits": 3},
                {"id": 10, "code": "ECON101", "title": "Microeconomics", "credits": 3},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["course_id", "code", "title", "credits"],
            sample_rows=[
                [1, "CS101", "Introduction to Computer Science", 4],
                [2, "CS201", "Data Structures & Algorithms", 4],
                [3, "CS301", "Operating Systems", 4],
                [5, "MATH101", "Calculus I", 4],
                [6, "MATH201", "Linear Algebra", 4],
                [8, "PHYS101", "Classical Mechanics", 4],
                [9, "PHYS201", "Electromagnetism", 4],
                [10, "CHEM101", "General Chemistry", 4],
                [11, "BIO101", "Cellular Biology", 4],
                [4, "CS401", "Distributed Systems", 3],
            ],
            total_row_count=10,
        ),
        starter_code="-- Complex OR/AND logic: credits >= 4 OR (code LIKE 'CS%' AND credits >= 3)\nSELECT \nFROM courses\n",
        expected_solution="""SELECT 
    id AS course_id,
    code,
    title,
    credits
FROM courses
WHERE credits >= 4 OR (code LIKE 'CS%' AND credits >= 3);""",
        alternative_solution="""SELECT 
    c.id AS course_id,
    c.code,
    c.title,
    c.credits
FROM courses c
WHERE c.credits >= 4
UNION
SELECT 
    c.id AS course_id,
    c.code,
    c.title,
    c.credits
FROM courses c
WHERE c.code LIKE 'CS%' AND c.credits >= 3;""",
        hints=[
            "Use parentheses to enforce logical precedence between `OR` and `AND`.",
            "Write `WHERE credits >= 4 OR (code LIKE 'CS%' AND credits >= 3)`.",
        ],
        detailed_explanation="""Logical operator precedence in SQL evaluates `AND` before `OR`.
Failing to enclose `(code LIKE 'CS%' AND credits >= 3)` in parentheses would produce an unintended evaluation:
`(credits >= 4 OR code LIKE 'CS%') AND credits >= 3`, which filters out valid 4-credit courses with credits >= 4 regardless of code.
Explicit parentheses prevent subtle logical precedence bugs.""",
        related_concepts=["Operator Precedence", "AND vs OR", "Disjunction"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-014-pub",
                name="Default University Courses",
                description="12 university catalog courses.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-014-hid1",
                name="Hidden Test Case 1: 3-Credit Art Course",
                description="Non-CS 3 credit course (must be excluded).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO courses (id, code, title, department_id, professor_id, credits)
VALUES (999, 'ART101', 'Art History I', 1, 1, 3);""",
            ),
        ],
    ),
]
