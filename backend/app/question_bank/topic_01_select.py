from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_01_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q1: Basic Column Projection (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-001",
        slug="employee-contact-directory",
        title="Employee Directory Column Projection",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="easy",
        problem_description="""The People Operations team needs a contact directory of all personnel.
Write a query to retrieve the `first_name`, `last_name`, and `email` for all employees from the `employees` table.
Do not filter or sort the results.""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                description="Staff roster and department links",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="email", type="VARCHAR(120)"),
                    ColumnSchema(name="department_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="title", type="VARCHAR(100)"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "last_name": "Pierce", "email": "alexander.pierce@company.com"},
                {"id": 2, "first_name": "Sarah", "last_name": "Connor", "email": "sarah.connor@company.com"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["first_name", "last_name", "email"],
            sample_rows=[
                ["Alexander", "Pierce", "alexander.pierce@company.com"],
                ["Sarah", "Connor", "sarah.connor@company.com"],
                ["David", "Chen", "david.chen@company.com"],
            ],
            total_row_count=60,
        ),
        starter_code="-- Select employee first_name, last_name, email\nSELECT \nFROM employees;\n",
        expected_solution="""SELECT first_name, last_name, email
FROM employees;""",
        alternative_solution="""SELECT e.first_name, e.last_name, e.email
FROM employees AS e;""",
        hints=[
            "Use the SELECT clause followed by the requested column names separated by commas.",
            "Reference the employees table in the FROM clause.",
        ],
        detailed_explanation="""The fundamental building block of SQL is column projection via the SELECT clause.
By specifying exact column names (`first_name`, `last_name`, `email`) rather than using wildcard `SELECT *`,
you improve query performance by reducing memory bandwidth and network transmission overhead.""",
        related_concepts=["SELECT", "Projection", "Table Scan"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-001-pub",
                name="Public Roster",
                description="Default company personnel dataset.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-001-hid1",
                name="Hidden Test Case 1: Extra Hires",
                description="Dataset with newly hired staff.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Marcus', 'Aurelius', 'marcus@philosophy.org', 1, 'Ethics Advisor', '2024-01-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q2: Distinct Country Selection (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-002",
        slug="distinct-customer-countries",
        title="Distinct Customer Countries",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="easy",
        problem_description="""International shipping logistics needs a deduplicated list of all countries where customers reside.
Write a query to retrieve every unique `country` present in the `customers` table.
Column name must remain `country`.""",
        database_id="db-ecommerce",
        relevant_tables=["customers"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                description="Registered customer accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(100)"),
                    ColumnSchema(name="country", type="VARCHAR(50)"),
                    ColumnSchema(name="city", type="VARCHAR(60)"),
                ],
            )
        ],
        sample_input_data={
            "customers": [
                {"id": 1, "country": "United States"},
                {"id": 2, "country": "United States"},
                {"id": 3, "country": "Canada"},
                {"id": 4, "country": "United Kingdom"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["country"],
            sample_rows=[
                ["United States"],
                ["Canada"],
                ["United Kingdom"],
                ["Germany"],
                ["Australia"],
            ],
            total_row_count=5,
        ),
        starter_code="-- Select unique countries from customers\nSELECT \nFROM customers;\n",
        expected_solution="""SELECT DISTINCT country
FROM customers;""",
        alternative_solution="""SELECT country
FROM customers
GROUP BY country;""",
        hints=[
            "Use the DISTINCT keyword immediately after SELECT to eliminate duplicate rows.",
            "Alternatively, grouping by country achieves identical deduplication.",
        ],
        detailed_explanation="""The `DISTINCT` keyword eliminates duplicate tuples from query results.
Internally, the database engine either sorts the intermediate stream or applies an in-memory hash set to deduplicate values.
In large datasets, using DISTINCT on unindexed columns incurs sort or hashing overhead.""",
        related_concepts=["DISTINCT", "Deduplication", "Hash Aggregate"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-002-pub",
                name="Default Global Customers",
                description="Default distribution of customer nationalities.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-002-hid1",
                name="Hidden Test Case 1: Additional Territory",
                description="New customer located in New Zealand.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO customers (id, first_name, last_name, email, country, city, created_at)
VALUES (999, 'Kiri', 'Te Kanawa', 'kiri@example.co.nz', 'New Zealand', 'Auckland', '2024-02-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q3: Column Aliasing and Renaming (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-003",
        slug="branch-asset-overview-aliasing",
        title="Branch Asset Overview & Column Aliasing",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="easy",
        problem_description="""Management needs an executive summary of banking branches with clear report headers.
Write a query to retrieve the `branch_name` and `total_assets` from the `branches` table.
Rename `branch_name` to `location_name` and `total_assets` to `asset_value` using column aliases.""",
        database_id="db-banking",
        relevant_tables=["branches"],
        table_schemas=[
            TableSchemaInfo(
                table_name="branches",
                description="Physical bank branches and asset capitalization",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="branch_name", type="VARCHAR(80)"),
                    ColumnSchema(name="branch_code", type="VARCHAR(10)"),
                    ColumnSchema(name="city", type="VARCHAR(60)"),
                    ColumnSchema(name="total_assets", type="DECIMAL(15,2)"),
                ],
            )
        ],
        sample_input_data={
            "branches": [
                {"id": 1, "branch_name": "Downtown Central", "total_assets": 85000000.00},
                {"id": 2, "branch_name": "Midtown Plaza", "total_assets": 62000000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["location_name", "asset_value"],
            sample_rows=[
                ["Downtown Central", 85000000.00],
                ["Midtown Plaza", 62000000.00],
            ],
            total_row_count=5,
        ),
        starter_code="-- Select and alias branch columns\nSELECT \nFROM branches;\n",
        expected_solution="""SELECT 
    branch_name AS location_name,
    total_assets AS asset_value
FROM branches;""",
        alternative_solution="""SELECT 
    b.branch_name location_name,
    b.total_assets asset_value
FROM branches b;""",
        hints=[
            "Use the AS keyword to assign column aliases: `branch_name AS location_name`.",
            "Make sure column alias names match exactly: location_name and asset_value.",
        ],
        detailed_explanation="""Column aliases rename query result attributes without mutating the underlying schema.
Aliases are defined using the `AS` keyword (optional in ANSI SQL, but recommended for readability).
Aliasing is essential when building API contracts, user-facing dashboards, or disambiguating join collisions.""",
        related_concepts=["AS", "Column Aliasing", "Projection"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-003-pub",
                name="Default Branches",
                description="Standard branch capitalization dataset.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-003-hid1",
                name="Hidden Test Case 1: Additional Branch",
                description="New branch opened in Boston.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO branches (id, branch_name, branch_code, city, state, total_assets)
VALUES (99, 'Boston Harbor', 'BOS01', 'Boston', 'MA', 95000000.00);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q4: Computed Columns & String Concatenation (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-004",
        slug="employee-full-name-formatting",
        title="Full Name Concatenation and Contact Formatting",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="medium",
        problem_description="""Generate a mailing directory where full names are concatenated into a single column.
Write a query to retrieve every employee's `id`, combined full name as `full_name` (e.g. `'Alexander Pierce'`),
and their job title as `job_title` (alias for `title`).
Concatenate `first_name`, a single space `' '`, and `last_name` using SQL string concatenation (`||`).""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                description="Staff roster",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(100)"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "last_name": "Pierce", "title": "VP of Engineering"},
                {"id": 2, "first_name": "Sarah", "last_name": "Connor", "title": "Engineering Manager"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["id", "full_name", "job_title"],
            sample_rows=[
                [1, "Alexander Pierce", "VP of Engineering"],
                [2, "Sarah Connor", "Engineering Manager"],
                [3, "David Chen", "Staff Software Engineer"],
            ],
            total_row_count=60,
        ),
        starter_code="-- Concatenate full name with space\nSELECT \nFROM employees;\n",
        expected_solution="""SELECT 
    id,
    first_name || ' ' || last_name AS full_name,
    title AS job_title
FROM employees;""",
        alternative_solution="""SELECT 
    id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    title AS job_title
FROM employees;""",
        hints=[
            "In SQLite and PostgreSQL, use the pipe operator `||` to concatenate strings: `first_name || ' ' || last_name`.",
            "Alias the resulting string expression as `full_name`.",
            "Alias `title` as `job_title`.",
        ],
        detailed_explanation="""Standard ANSI SQL uses the double-pipe operator (`||`) to concatenate strings.
When concatenating fields, note that if any operand is NULL, the result of `||` is NULL in SQL standards.
Expressions can be computed on the fly in the SELECT clause without altering physical storage.""",
        related_concepts=["String Concatenation", "Expressions", "NULL Propagation"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-004-pub",
                name="Default Staff Concatenation",
                description="Full company roster.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-004-hid1",
                name="Hidden Test Case 1: Additional Consultant",
                description="Staff member with hyphenated name.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Jean-Luc', 'Picard', 'picard@starfleet.org', 1, 'Strategic Advisor', '2024-03-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q5: Financial Arithmetic Projection (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-005",
        slug="projected-annual-interest",
        title="Projected Annual Interest Computation",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="medium",
        problem_description="""The wealth management team is forecasting annual yield for savings and money market accounts.
Write a query to retrieve `id` as `account_id`, `account_type`, `balance`, and the estimated annual interest as `projected_interest`.
Assume an annual interest rate of 4.5% (`balance * 0.045`). Round `projected_interest` to 2 decimal places using `ROUND()`.""",
        database_id="db-banking",
        relevant_tables=["accounts"],
        table_schemas=[
            TableSchemaInfo(
                table_name="accounts",
                description="Customer bank deposit accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="account_type", type="VARCHAR(30)"),
                    ColumnSchema(name="balance", type="DECIMAL(12,2)"),
                ],
            )
        ],
        sample_input_data={
            "accounts": [
                {"id": 1, "account_type": "Checking", "balance": 8450.25},
                {"id": 2, "account_type": "Savings", "balance": 24150.80},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["account_id", "account_type", "balance", "projected_interest"],
            sample_rows=[
                [1, "Checking", 8450.25, 380.26],
                [2, "Savings", 24150.80, 1086.79],
                [3, "Checking", 1250.00, 56.25],
            ],
            total_row_count=35,
        ),
        starter_code="-- Calculate 4.5% projected interest rounded to 2 decimals\nSELECT \nFROM accounts;\n",
        expected_solution="""SELECT 
    id AS account_id,
    account_type,
    balance,
    ROUND(balance * 0.045, 2) AS projected_interest
FROM accounts;""",
        alternative_solution="""SELECT 
    a.id AS account_id,
    a.account_type,
    a.balance,
    ROUND((a.balance * 4.5) / 100.0, 2) AS projected_interest
FROM accounts a;""",
        hints=[
            "Compute interest by multiplying `balance * 0.045`.",
            "Wrap the calculation inside `ROUND(..., 2)` to format as currency.",
            "Alias `id` as `account_id` and the interest expression as `projected_interest`.",
        ],
        detailed_explanation="""Mathematical expressions in the SELECT clause allow instant ad-hoc quantitative projections.
`ROUND(expr, N)` standardizes floating point calculations to the desired numeric scale.
Such expressions are calculated in memory during query execution and do not consume physical table storage.""",
        related_concepts=["Arithmetic Expressions", "ROUND", "Numeric Casting"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-005-pub",
                name="Public Accounts",
                description="Default account balances.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-005-hid1",
                name="Hidden Test Case 1: High Net Worth Deposit",
                description="Customer deposit of $500,000.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 1, 1, 'ACC-999999', 'Money Market', 500000.00, 'active', '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q6: Inventory Valuation Projection (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-006",
        slug="product-inventory-valuation",
        title="Product Inventory Valuation Calculation",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="medium",
        problem_description="""Supply chain finance requires an inventory valuation report for all active products.
Write a query to retrieve `id` as `product_id`, `name` as `product_name`, `price`, `stock_quantity`,
and the total inventory valuation (`price * stock_quantity`) as `inventory_value`.
Round `inventory_value` to 2 decimal places.""",
        database_id="db-ecommerce",
        relevant_tables=["products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="products",
                description="E-commerce merchandise catalog",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(150)"),
                    ColumnSchema(name="price", type="DECIMAL(10,2)"),
                    ColumnSchema(name="stock_quantity", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "products": [
                {"id": 1, "name": "Wireless Ergonomic Mouse", "price": 49.99, "stock_quantity": 120},
                {"id": 2, "name": "Mechanical RGB Keyboard", "price": 129.99, "stock_quantity": 85},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["product_id", "product_name", "price", "stock_quantity", "inventory_value"],
            sample_rows=[
                [1, "Wireless Ergonomic Mouse", 49.99, 120, 5998.80],
                [2, "Mechanical RGB Keyboard", 129.99, 85, 11049.15],
            ],
            total_row_count=20,
        ),
        starter_code="-- Calculate inventory valuation (price * stock_quantity)\nSELECT \nFROM products;\n",
        expected_solution="""SELECT 
    id AS product_id,
    name AS product_name,
    price,
    stock_quantity,
    ROUND(price * stock_quantity, 2) AS inventory_value
FROM products;""",
        alternative_solution="""SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.price,
    p.stock_quantity,
    ROUND(CAST(p.price AS NUMERIC) * p.stock_quantity, 2) AS inventory_value
FROM products p;""",
        hints=[
            "Multiply `price * stock_quantity`.",
            "Round the product to 2 decimal places and alias as `inventory_value`.",
            "Verify all column aliases match the prompt specification.",
        ],
        detailed_explanation="""Combining multiple columns using arithmetic operators (`*`, `+`, `-`, `/`) creates derived metrics.
When multiplying a DECIMAL with an INTEGER, SQLite promotes the expression to dynamic floating-point / real,
making `ROUND(..., 2)` essential to prevent fractional micro-cent rounding discrepancies.""",
        related_concepts=["Multi-Column Arithmetic", "ROUND", "Derived Attributes"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-006-pub",
                name="Standard Catalog",
                description="Default 20 product catalog records.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-006-hid1",
                name="Hidden Test Case 1: Clearance Bulk Inventory",
                description="High stock clearance item.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, 'Bulk USB-C Cables (Pack of 5)', 15.50, 1000, 1);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q7: Multi-Expression String Formatting & Cohort Estimation (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-007",
        slug="student-degree-cohort-formatting",
        title="Student Cohort Tagging & Degree Status Formatting",
        topic_id="top-01",
        topic="SELECT & Column Aliasing",
        difficulty="hard",
        problem_description="""Academic affairs needs an identification badge string for all enrolled students.
Write a query to retrieve:
1. `id` as `student_id`.
2. Formatted full name as `display_name` in the format: `'Last, First'` (e.g. `'Danvers, Carol'`).
3. Their university email as `email`.
4. Their estimated undergraduate graduation year (`enrollment_year + 4`) as `estimated_grad_year`.
5. An official badge string as `student_badge` in the exact format:
   `'ID#' || id || ' - ' || UPPER(first_name) || ' [' || enrollment_year || ']'`
   (e.g. `'ID#3 - CAROL [2023]'`).""",
        database_id="db-university",
        relevant_tables=["students"],
        table_schemas=[
            TableSchemaInfo(
                table_name="students",
                description="Undergraduate student roster",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="email", type="VARCHAR(120)"),
                    ColumnSchema(name="enrollment_year", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "students": [
                {"id": 1, "first_name": "Alice", "last_name": "Walker", "email": "alice.w@univ.edu", "enrollment_year": 2021},
                {"id": 2, "first_name": "Bob", "last_name": "Miller", "email": "bob.m@univ.edu", "enrollment_year": 2022},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["student_id", "display_name", "email", "estimated_grad_year", "student_badge"],
            sample_rows=[
                [1, "Walker, Alice", "alice.walker@university.edu", 2025, "ID#1 - ALICE [2021]"],
                [2, "Miller, Bob", "bob.miller@university.edu", 2026, "ID#2 - BOB [2022]"],
            ],
            total_row_count=30,
        ),
        starter_code="-- Format complex student badge string and graduation cohort\nSELECT \nFROM students;\n",
        expected_solution="""SELECT 
    id AS student_id,
    last_name || ', ' || first_name AS display_name,
    email,
    enrollment_year + 4 AS estimated_grad_year,
    'ID#' || id || ' - ' || UPPER(first_name) || ' [' || enrollment_year || ']' AS student_badge
FROM students;""",
        alternative_solution="""SELECT 
    s.id AS student_id,
    CONCAT(s.last_name, ', ', s.first_name) AS display_name,
    s.email,
    (s.enrollment_year + 4) AS estimated_grad_year,
    'ID#' || CAST(s.id AS TEXT) || ' - ' || UPPER(s.first_name) || ' [' || CAST(s.enrollment_year AS TEXT) || ']' AS student_badge
FROM students s;""",
        hints=[
            "Use `last_name || ', ' || first_name` for display_name.",
            "Use `enrollment_year + 4` for estimated_grad_year.",
            "Combine literals and string functions: `'ID#' || id || ' - ' || UPPER(first_name) || ' [' || enrollment_year || ']'`.",
        ],
        detailed_explanation="""Complex projection queries combine scalar mathematical operations, string transformation functions
like `UPPER()`, and multi-segment string concatenation.
Formatting strings directly at the database tier simplifies downstream consumption in rendering clients,
ensuring consistent localization and formatting logic across all consumers.""",
        related_concepts=["UPPER", "String Formatting", "Derived Expressions", "Projection"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-007-pub",
                name="Default Student Body",
                description="30 enrolled university students.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-007-hid1",
                name="Hidden Test Case 1: Transfer Student",
                description="Transfer student admitted in 2024.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO students (id, first_name, last_name, email, major_department_id, enrollment_year, status)
VALUES (999, 'Zack', 'Snyder', 'zack.s@univ.edu', 1, 2024, 'active');""",
            ),
        ],
    ),
]
