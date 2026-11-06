from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_05_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q29: Global Metrics Aggregation (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-029",
        slug="department-budget-global-aggregates",
        title="Corporate Budget Overview & Summary Metrics",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="easy",
        problem_description="""Corporate planning needs aggregate budget benchmarks across all departments.
Write a query against `departments` to calculate:
1. Total number of departments as `department_count`.
2. Total combined budget as `total_budget`.
3. Average department budget as `avg_budget`, rounded to 2 decimal places using `ROUND()`.""",
        database_id="db-company",
        relevant_tables=["departments"],
        table_schemas=[
            TableSchemaInfo(
                table_name="departments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(80)"),
                    ColumnSchema(name="budget", type="DECIMAL(12,2)"),
                ],
            )
        ],
        sample_input_data={
            "departments": [
                {"id": 1, "budget": 1200000.00},
                {"id": 2, "budget": 450000.00},
                {"id": 3, "budget": 600000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["department_count", "total_budget", "avg_budget"],
            sample_rows=[
                [7, 3450000.00, 492857.14],
            ],
            total_row_count=1,
        ),
        starter_code="-- Aggregate department_count, total_budget, and avg_budget\nSELECT \nFROM departments;\n",
        expected_solution="""SELECT 
    COUNT(*) AS department_count,
    SUM(budget) AS total_budget,
    ROUND(AVG(budget), 2) AS avg_budget
FROM departments;""",
        alternative_solution="""SELECT 
    COUNT(id) AS department_count,
    SUM(budget) AS total_budget,
    ROUND(CAST(SUM(budget) AS REAL) / COUNT(*), 2) AS avg_budget
FROM departments;""",
        hints=[
            "Use `COUNT(*)` for department_count.",
            "Use `SUM(budget)` for total_budget.",
            "Use `ROUND(AVG(budget), 2)` for avg_budget.",
        ],
        detailed_explanation="""Aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) compute a single summary value
across an entire set of rows.
When used without a `GROUP BY` clause, the entire table forms a single implicit aggregation group,
collapsing all qualifying rows into exactly one result row.""",
        related_concepts=["Aggregate Functions", "COUNT", "SUM", "AVG", "Implicit Group"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-029-pub",
                name="Default Departments",
                description="7 standard corporate departments.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-029-hid1",
                name="Hidden Test Case 1: Additional Department",
                description="New department with $500,000 budget.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO departments (id, name, budget, location)
VALUES (99, 'Security Operations', 500000.00, 'Chicago');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q30: Distinct Count Aggregation (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-030",
        slug="customer-global-diversity-count",
        title="Customer Geographic Diversity Metrics",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="easy",
        problem_description="""International business expansion tracks both total user count and country reach.
Write a query against `customers` to calculate:
1. Total number of registered customers as `total_customers` (`COUNT(*)`).
2. Number of unique countries represented as `unique_countries` using `COUNT(DISTINCT country)`.""",
        database_id="db-ecommerce",
        relevant_tables=["customers"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="country", type="VARCHAR(50)"),
                ],
            )
        ],
        sample_input_data={
            "customers": [
                {"id": 1, "country": "United States"},
                {"id": 2, "country": "United States"},
                {"id": 3, "country": "Canada"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["total_customers", "unique_countries"],
            sample_rows=[
                [30, 5],
            ],
            total_row_count=1,
        ),
        starter_code="-- Count total customers and unique countries\nSELECT \nFROM customers;\n",
        expected_solution="""SELECT 
    COUNT(*) AS total_customers,
    COUNT(DISTINCT country) AS unique_countries
FROM customers;""",
        alternative_solution="""SELECT 
    COUNT(c.id) AS total_customers,
    COUNT(DISTINCT c.country) AS unique_countries
FROM customers c;""",
        hints=[
            "Use `COUNT(*)` for total_customers.",
            "Use `COUNT(DISTINCT country)` for unique_countries.",
        ],
        detailed_explanation="""`COUNT(DISTINCT column)` evaluates uniqueness before counting.
It discards duplicate non-null occurrences of the column value, yielding cardinality.
`COUNT(*)` counts all rows including those with nulls, whereas `COUNT(column)` skips null entries.""",
        related_concepts=["COUNT DISTINCT", "Cardinality", "NULL in Aggregates"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-030-pub",
                name="Default Customers",
                description="30 customers across 5 countries.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-030-hid1",
                name="Hidden Test Case 1: Customer in New Country",
                description="Customer located in Brazil.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO customers (id, first_name, last_name, email, country, city, created_at)
VALUES (999, 'Lucas', 'Silva', 'lucas@sp.br', 'Brazil', 'Sao Paulo', '2024-02-15');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q31: Min & Max Account Balances (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-031",
        slug="extreme-account-balance-boundaries",
        title="Extreme Account Balance Boundaries",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="easy",
        problem_description="""Treasury audit needs to inspect balance boundaries across active accounts.
Write a query against `accounts` (filtering for `status = 'active'`) to calculate:
1. The lowest balance as `min_balance`.
2. The highest balance as `max_balance`.
3. The average balance as `avg_balance` rounded to 2 decimal places.""",
        database_id="db-banking",
        relevant_tables=["accounts"],
        table_schemas=[
            TableSchemaInfo(
                table_name="accounts",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="balance", type="DECIMAL(12,2)"),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                ],
            )
        ],
        sample_input_data={
            "accounts": [
                {"id": 1, "balance": 8450.25, "status": "active"},
                {"id": 2, "balance": 24150.80, "status": "active"},
                {"id": 5, "balance": 112400.00, "status": "active"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["min_balance", "max_balance", "avg_balance"],
            sample_rows=[
                [450.00, 250000.00, 19342.93],
            ],
            total_row_count=1,
        ),
        starter_code="-- Active accounts: MIN(balance), MAX(balance), ROUND(AVG(balance), 2)\nSELECT \nFROM accounts\n",
        expected_solution="""SELECT 
    MIN(balance) AS min_balance,
    MAX(balance) AS max_balance,
    ROUND(AVG(balance), 2) AS avg_balance
FROM accounts
WHERE status = 'active';""",
        alternative_solution="""SELECT 
    MIN(a.balance) AS min_balance,
    MAX(a.balance) AS max_balance,
    ROUND(AVG(a.balance), 2) AS avg_balance
FROM accounts a
WHERE a.status = 'active';""",
        hints=[
            "Filter active accounts using `WHERE status = 'active'`.",
            "Compute `MIN(balance)`, `MAX(balance)`, and `ROUND(AVG(balance), 2)`.",
        ],
        detailed_explanation="""`MIN()` and `MAX()` find extreme values in constant $O(1)$ time if the column is indexed in a B-Tree,
as the engine simply reads the leftmost or rightmost leaf page.
When combined with `WHERE status = 'active'`, only active accounts are factored into the boundary metrics.""",
        related_concepts=["MIN", "MAX", "B-Tree Min/Max Optimization"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-031-pub",
                name="Default Accounts",
                description="35 accounts with balances up to $250K.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-031-hid1",
                name="Hidden Test Case 1: Ultra High Balance Account",
                description="New active account with $1,000,000 balance.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 1, 1, 'MAX-01', 'Private Banking', 1000000.00, 'active', '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q32: Filtered Payroll Aggregation (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-032",
        slug="payroll-summary-analysis",
        title="Comprehensive Payroll Expense Summary",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="medium",
        problem_description="""Total compensation analysis requires an aggregate breakdown of salaries and bonuses.
Write a query against the `salaries` table to calculate:
1. Total base payroll as `total_base_salary` (`SUM(base_salary)`).
2. Average base salary as `avg_base_salary` (`ROUND(AVG(base_salary), 2)`).
3. Total bonus pool as `total_bonuses` (`SUM(bonus)`).
4. Total combined compensation (`SUM(base_salary + bonus)`) as `total_compensation`.""",
        database_id="db-company",
        relevant_tables=["salaries"],
        table_schemas=[
            TableSchemaInfo(
                table_name="salaries",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="employee_id", type="INTEGER", is_foreign_key=True),
                    ColumnSchema(name="base_salary", type="DECIMAL(10,2)"),
                    ColumnSchema(name="bonus", type="DECIMAL(10,2)"),
                ],
            )
        ],
        sample_input_data={
            "salaries": [
                {"id": 1, "base_salary": 220000.00, "bonus": 35000.00},
                {"id": 2, "base_salary": 160000.00, "bonus": 20000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["total_base_salary", "avg_base_salary", "total_bonuses", "total_compensation"],
            sample_rows=[
                [5925000.00, 98750.00, 680000.00, 6605000.00],
            ],
            total_row_count=1,
        ),
        starter_code="-- Sum base_salary, bonus, and base_salary + bonus\nSELECT \nFROM salaries;\n",
        expected_solution="""SELECT 
    SUM(base_salary) AS total_base_salary,
    ROUND(AVG(base_salary), 2) AS avg_base_salary,
    SUM(bonus) AS total_bonuses,
    SUM(base_salary + bonus) AS total_compensation
FROM salaries;""",
        alternative_solution="""SELECT 
    SUM(s.base_salary) AS total_base_salary,
    ROUND(AVG(s.base_salary), 2) AS avg_base_salary,
    SUM(s.bonus) AS total_bonuses,
    (SUM(s.base_salary) + SUM(s.bonus)) AS total_compensation
FROM salaries s;""",
        hints=[
            "Compute `SUM(base_salary)` and `ROUND(AVG(base_salary), 2)`.",
            "Compute `SUM(bonus)`.",
            "For total_compensation, you can sum the arithmetic expression `SUM(base_salary + bonus)`.",
        ],
        detailed_explanation="""Aggregate functions can take arbitrary scalar expressions as arguments (e.g. `SUM(base_salary + bonus)`).
Because mathematical distributive properties hold ($SUM(A + B) = SUM(A) + SUM(B)$),
both formulations produce identical results as long as neither column contains NULLs.
If bonuses could be NULL, `COALESCE(bonus, 0)` would be necessary to prevent NULL propagation.""",
        related_concepts=["Aggregate of Expressions", "SUM", "NULL Resilience"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-032-pub",
                name="Default Salaries",
                description="60 corporate salaries.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-032-hid1",
                name="Hidden Test Case 1: Executive Compensation",
                description="Executive salary $300,000 + $50,000 bonus.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO salaries (id, employee_id, base_salary, bonus, effective_date)
VALUES (999, 999, 300000.00, 50000.00, '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q33: Price Spread & Catalog Breadth (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-033",
        slug="product-price-spread-metrics",
        title="Product Catalog Price Spread & Dispersion",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="medium",
        problem_description="""Merchandising leadership wants to analyze pricing dispersion across active products (`is_active = 1`).
Write a query against `products` to calculate:
1. Total active items as `active_product_count`.
2. Lowest price as `min_price`.
3. Highest price as `max_price`.
4. Difference between highest and lowest price as `price_spread` (`MAX(price) - MIN(price)`).
Round `price_spread` to 2 decimal places.""",
        database_id="db-ecommerce",
        relevant_tables=["products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="products",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="price", type="DECIMAL(10,2)"),
                    ColumnSchema(name="is_active", type="BOOLEAN"),
                ],
            )
        ],
        sample_input_data={
            "products": [
                {"id": 1, "price": 49.99, "is_active": 1},
                {"id": 2, "price": 129.99, "is_active": 1},
                {"id": 4, "price": 399.99, "is_active": 1},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["active_product_count", "min_price", "max_price", "price_spread"],
            sample_rows=[
                [18, 19.99, 599.99, 580.00],
            ],
            total_row_count=1,
        ),
        starter_code="-- Active products: count, min_price, max_price, price_spread\nSELECT \nFROM products\n",
        expected_solution="""SELECT 
    COUNT(*) AS active_product_count,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    ROUND(MAX(price) - MIN(price), 2) AS price_spread
FROM products
WHERE is_active = 1;""",
        alternative_solution="""SELECT 
    COUNT(p.id) AS active_product_count,
    MIN(p.price) AS min_price,
    MAX(p.price) AS max_price,
    ROUND(MAX(p.price) - MIN(p.price), 2) AS price_spread
FROM products p
WHERE p.is_active = TRUE;""",
        hints=[
            "Filter active products: `WHERE is_active = 1`.",
            "Compute `ROUND(MAX(price) - MIN(price), 2) AS price_spread`.",
        ],
        detailed_explanation="""SQL aggregate expressions can be combined using arithmetic operators:
`MAX(price) - MIN(price)` calculates the statistical range of a distribution.
Because aggregate operations execute after the WHERE clause, the min, max, and spread
reflect only active merchandise.""",
        related_concepts=["Range Computation", "Aggregate Arithmetic", "Statistical Dispersion"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-033-pub",
                name="Default Products",
                description="18 active products.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-033-hid1",
                name="Hidden Test Case 1: Ultra Budget Accessory",
                description="Active item priced at $4.99 increases price spread.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, 'Screen Cleaning Cloth', 4.99, 200, 1);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q34: Conditional Sum Aggregation (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-034",
        slug="net-cash-flow-conditional-aggregation",
        title="Ledger Net Cash Flow via Conditional Aggregation",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="medium",
        problem_description="""Treasury liquidity management calculates net ledger cash flow.
Write a query against `transactions` to calculate:
1. Total deposits (`transaction_type = 'deposit'`) as `total_deposits`.
2. Total withdrawals (`transaction_type = 'withdrawal'`) as `total_withdrawals`.
3. Net cash flow (`total_deposits - total_withdrawals`) as `net_cash_flow`.
Use conditional aggregation (`SUM(CASE WHEN ... THEN amount ELSE 0 END)`). Round all metrics to 2 decimal places.""",
        database_id="db-banking",
        relevant_tables=["transactions"],
        table_schemas=[
            TableSchemaInfo(
                table_name="transactions",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="transaction_type", type="VARCHAR(20)"),
                    ColumnSchema(name="amount", type="DECIMAL(12,2)"),
                ],
            )
        ],
        sample_input_data={
            "transactions": [
                {"id": 1, "transaction_type": "deposit", "amount": 3500.00},
                {"id": 2, "transaction_type": "withdrawal", "amount": 500.00},
                {"id": 3, "transaction_type": "deposit", "amount": 1200.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["total_deposits", "total_withdrawals", "net_cash_flow"],
            sample_rows=[
                [48250.00, 21400.00, 26850.00],
            ],
            total_row_count=1,
        ),
        starter_code="-- Conditional aggregation: deposit sum, withdrawal sum, and net\nSELECT \nFROM transactions;\n",
        expected_solution="""SELECT 
    ROUND(SUM(CASE WHEN transaction_type = 'deposit' THEN amount ELSE 0 END), 2) AS total_deposits,
    ROUND(SUM(CASE WHEN transaction_type = 'withdrawal' THEN amount ELSE 0 END), 2) AS total_withdrawals,
    ROUND(SUM(CASE 
        WHEN transaction_type = 'deposit' THEN amount 
        WHEN transaction_type = 'withdrawal' THEN -amount 
        ELSE 0 
    END), 2) AS net_cash_flow
FROM transactions;""",
        alternative_solution="""SELECT 
    ROUND(COALESCE(SUM(CASE WHEN t.transaction_type = 'deposit' THEN t.amount END), 0), 2) AS total_deposits,
    ROUND(COALESCE(SUM(CASE WHEN t.transaction_type = 'withdrawal' THEN t.amount END), 0), 2) AS total_withdrawals,
    ROUND(COALESCE(SUM(CASE WHEN t.transaction_type = 'deposit' THEN t.amount END), 0) - 
          COALESCE(SUM(CASE WHEN t.transaction_type = 'withdrawal' THEN t.amount END), 0), 2) AS net_cash_flow
FROM transactions t;""",
        hints=[
            "Use `SUM(CASE WHEN transaction_type = 'deposit' THEN amount ELSE 0 END)` for total_deposits.",
            "Use `SUM(CASE WHEN transaction_type = 'withdrawal' THEN amount ELSE 0 END)` for total_withdrawals.",
            "For net_cash_flow, sum positive deposits and negative withdrawals, or subtract withdrawals from deposits.",
        ],
        detailed_explanation="""Conditional aggregation is one of the most powerful and versatile patterns in SQL.
By placing a `CASE WHEN` expression inside `SUM()` or `COUNT()`, you selectively aggregate subsets of data
in a single pass over the table, avoiding the need for multiple separate subqueries or expensive joins.""",
        related_concepts=["Conditional Aggregation", "SUM CASE WHEN", "Single-Pass Scanning"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-034-pub",
                name="Default Transactions",
                description="40 transactions in banking ledger.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-034-hid1",
                name="Hidden Test Case 1: Large Deposit",
                description="Deposit of $10,000.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date)
VALUES (999, 1, 'deposit', 10000.00, 25000.00, 'Treasury Inflow', '2024-03-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q35: Multi-Metric Course Catalog Statistics (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-035",
        slug="comprehensive-academic-curriculum-statistics",
        title="Comprehensive Academic Curriculum Catalog Statistics",
        topic_id="top-05",
        topic="Aggregate Functions",
        difficulty="hard",
        problem_description="""Academic accreditation requires an institutional audit of the course catalog.
Write a query against the `courses` table to calculate:
1. Total course offerings as `total_courses` (`COUNT(*)`).
2. Total credit units granted as `total_credit_units` (`SUM(credits)`).
3. Average credits per course as `avg_course_credits`, rounded to 2 decimal places.
4. The credit spread (`MAX(credits) - MIN(credits)`) as `credit_variance_range`.
5. Number of distinct departments actively offering at least one course as `active_departments_count` (`COUNT(DISTINCT department_id)`).
6. Number of courses granting 4 or more credits as `high_credit_courses_count` using conditional counting (`SUM(CASE WHEN credits >= 4 THEN 1 ELSE 0 END)`).""",
        database_id="db-university",
        relevant_tables=["courses"],
        table_schemas=[
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="department_id", type="INTEGER"),
                    ColumnSchema(name="credits", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "courses": [
                {"id": 1, "department_id": 1, "credits": 4},
                {"id": 4, "department_id": 1, "credits": 3},
                {"id": 5, "department_id": 2, "credits": 4},
            ]
        },
        expected_output=ExpectedOutput(
            columns=[
                "total_courses",
                "total_credit_units",
                "avg_course_credits",
                "credit_variance_range",
                "active_departments_count",
                "high_credit_courses_count",
            ],
            sample_rows=[
                [12, 45, 3.75, 1, 6, 9],
            ],
            total_row_count=1,
        ),
        starter_code="-- Compute 6 comprehensive curriculum metrics in a single query\nSELECT \nFROM courses;\n",
        expected_solution="""SELECT 
    COUNT(*) AS total_courses,
    SUM(credits) AS total_credit_units,
    ROUND(AVG(credits), 2) AS avg_course_credits,
    MAX(credits) - MIN(credits) AS credit_variance_range,
    COUNT(DISTINCT department_id) AS active_departments_count,
    SUM(CASE WHEN credits >= 4 THEN 1 ELSE 0 END) AS high_credit_courses_count
FROM courses;""",
        alternative_solution="""SELECT 
    COUNT(c.id) AS total_courses,
    SUM(c.credits) AS total_credit_units,
    ROUND(AVG(CAST(c.credits AS REAL)), 2) AS avg_course_credits,
    MAX(c.credits) - MIN(c.credits) AS credit_variance_range,
    COUNT(DISTINCT c.department_id) AS active_departments_count,
    COUNT(CASE WHEN c.credits >= 4 THEN 1 END) AS high_credit_courses_count
FROM courses c;""",
        hints=[
            "Use `COUNT(*)` for total_courses, `SUM(credits)` for total_credit_units.",
            "Use `ROUND(AVG(credits), 2)` for avg_course_credits.",
            "Use `COUNT(DISTINCT department_id)` for active_departments_count.",
            "Use `SUM(CASE WHEN credits >= 4 THEN 1 ELSE 0 END)` or `COUNT(CASE WHEN credits >= 4 THEN 1 END)`.",
        ],
        detailed_explanation="""Combining counts, distinct counts, sums, arithmetic ranges, and conditional counts in one query
demonstrates the full analytical power of SQL aggregation.
A single scan through the table calculates all six metrics simultaneously in $O(N)$ time,
minimizing database I/O and CPU memory pressure.""",
        related_concepts=["Multi-Metric Aggregation", "COUNT DISTINCT", "Conditional COUNT", "Single Table Scan"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-035-pub",
                name="Default University Courses",
                description="12 catalog courses.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-035-hid1",
                name="Hidden Test Case 1: 5-Credit Graduate Seminar",
                description="5-credit seminar in Department 1 expands range to 2.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO courses (id, code, title, department_id, professor_id, credits)
VALUES (999, 'CS599', 'Advanced Quantum Computing Seminar', 1, 1, 5);""",
            ),
        ],
    ),
]
