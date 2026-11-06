from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_07_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q43: Categorizing by Value Range with CASE (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-043",
        slug="product-price-tier-classification",
        title="Merchandise Price Tier Categorization",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="easy",
        problem_description="""Marketing assigns merchandise to customer budget tiers based on catalog pricing.
Write a query against `products` to classify each item into a `price_tier`:
- When `price >= 200.00` then `'Premium'`
- When `price >= 50.00` then `'Mid-Range'`
- Else `'Budget'`
Return `id` (as `product_id`), `name` (as `product_name`), `price`, and `price_tier`.""",
        database_id="db-ecommerce",
        relevant_tables=["products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="products",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(150)"),
                    ColumnSchema(name="price", type="DECIMAL(10,2)"),
                ],
            )
        ],
        sample_input_data={
            "products": [
                {"id": 1, "name": "Wireless Mouse", "price": 49.99},
                {"id": 2, "name": "Mechanical Keyboard", "price": 129.99},
                {"id": 4, "name": "4K Monitor", "price": 399.99},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["product_id", "product_name", "price", "price_tier"],
            sample_rows=[
                [1, "Wireless Ergonomic Mouse", 49.99, "Budget"],
                [2, "Mechanical RGB Keyboard", 129.99, "Mid-Range"],
                [4, "Ultra HD 4K Monitor 27-inch", 399.99, "Premium"],
            ],
            total_row_count=20,
        ),
        starter_code="-- Use CASE to classify price into 'Premium', 'Mid-Range', 'Budget'\nSELECT \nFROM products\n",
        expected_solution="""SELECT 
    id AS product_id,
    name AS product_name,
    price,
    CASE 
        WHEN price >= 200.00 THEN 'Premium'
        WHEN price >= 50.00 THEN 'Mid-Range'
        ELSE 'Budget'
    END AS price_tier
FROM products;""",
        alternative_solution="""SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.price,
    CASE 
        WHEN p.price < 50.00 THEN 'Budget'
        WHEN p.price < 200.00 THEN 'Mid-Range'
        ELSE 'Premium'
    END AS price_tier
FROM products p;""",
        hints=[
            "Use a searched `CASE` expression: `CASE WHEN condition THEN result ... ELSE default END`.",
            "Order matters in CASE: conditions are evaluated sequentially from top to bottom.",
        ],
        detailed_explanation="""The SQL `CASE` expression is equivalent to an if-elif-else statement in imperative languages.
It evaluates expressions in sequential order and returns the value of the first `WHEN` clause that matches.
Once a match is found, subsequent clauses are skipped.
If no condition matches, the `ELSE` branch is executed (returning NULL if ELSE is omitted).""",
        related_concepts=["CASE Expression", "Searched CASE", "Conditional Branching"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-043-pub",
                name="Default Products",
                description="20 products across pricing tiers.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-043-hid1",
                name="Hidden Test Case 1: Ultra Luxury Product",
                description="New $1,500 item.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, 'Server Rack Unit', 1499.99, 10, 1);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q44: Fallback Values with COALESCE (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-044",
        slug="employee-department-fallback-coalesce",
        title="Unassigned Department Fallback via COALESCE",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="easy",
        problem_description="""Data warehousing pipelines require non-null integer values for foreign key dimensions.
Write a query against `employees` to retrieve:
1. `id` as `employee_id`.
2. `first_name`.
3. `last_name`.
4. Their department ID, substituting integer `0` whenever `department_id IS NULL`, as `assigned_department` using `COALESCE(department_id, 0)`.""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="department_id", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "first_name": "Alexander", "department_id": 1},
                {"id": 56, "first_name": "Grace", "department_id": None},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "first_name", "last_name", "assigned_department"],
            sample_rows=[
                [1, "Alexander", "Pierce", 1],
                [56, "Grace", "Hopper", 0],
            ],
            total_row_count=60,
        ),
        starter_code="-- Use COALESCE(department_id, 0) as assigned_department\nSELECT \nFROM employees\n",
        expected_solution="""SELECT 
    id AS employee_id,
    first_name,
    last_name,
    COALESCE(department_id, 0) AS assigned_department
FROM employees;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    CASE 
        WHEN e.department_id IS NOT NULL THEN e.department_id 
        ELSE 0 
    END AS assigned_department
FROM employees e;""",
        hints=[
            "Use `COALESCE(department_id, 0)` to replace NULL values with 0.",
            "Alias `id` as `employee_id` and the coalesced column as `assigned_department`.",
        ],
        detailed_explanation="""`COALESCE(val1, val2, ...)` returns the first non-null expression in its argument list.
If all arguments are NULL, it returns NULL.
It is an ANSI SQL standard function and functions identically to `CASE WHEN val1 IS NOT NULL THEN val1 ELSE val2 END`,
providing concise null-coalescing logic essential for data pipelines.""",
        related_concepts=["COALESCE", "NULL Handling", "Default Values"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-044-pub",
                name="Default Employees",
                description="60 employees including unassigned staff.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-044-hid1",
                name="Hidden Test Case 1: Additional Unassigned Staff",
                description="Staff member with NULL department.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Alan', 'Kay', 'alan.kay@co.com', NULL, 'Visionary', '2024-01-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q45: Standardizing Transaction Direction with CASE (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-045",
        slug="standardized-transaction-direction",
        title="Transaction Directional Classification",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="easy",
        problem_description="""Accounting reporting standardizes heterogeneous transaction types into binary ledger flows.
Write a query against `transactions` to map each record's `transaction_type` into `cash_direction`:
- When `transaction_type IN ('deposit', 'transfer_in')` then `'INFLOW'`
- Else `'OUTFLOW'`
Return `id` (as `transaction_id`), `transaction_type`, `amount`, and `cash_direction`.""",
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
                {"id": 3, "transaction_type": "transfer_in", "amount": 1200.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["transaction_id", "transaction_type", "amount", "cash_direction"],
            sample_rows=[
                [1, "deposit", 3500.00, "INFLOW"],
                [2, "withdrawal", 500.00, "OUTFLOW"],
                [3, "transfer_in", 1200.00, "INFLOW"],
            ],
            total_row_count=40,
        ),
        starter_code="-- Map transaction_type to 'INFLOW' or 'OUTFLOW'\nSELECT \nFROM transactions\n",
        expected_solution="""SELECT 
    id AS transaction_id,
    transaction_type,
    amount,
    CASE 
        WHEN transaction_type IN ('deposit', 'transfer_in') THEN 'INFLOW'
        ELSE 'OUTFLOW'
    END AS cash_direction
FROM transactions;""",
        alternative_solution="""SELECT 
    t.id AS transaction_id,
    t.transaction_type,
    t.amount,
    CASE 
        WHEN t.transaction_type = 'deposit' OR t.transaction_type = 'transfer_in' THEN 'INFLOW'
        WHEN t.transaction_type = 'withdrawal' OR t.transaction_type = 'transfer_out' THEN 'OUTFLOW'
        ELSE 'UNKNOWN'
    END AS cash_direction
FROM transactions t;""",
        hints=[
            "Use `CASE WHEN transaction_type IN ('deposit', 'transfer_in') THEN 'INFLOW' ELSE 'OUTFLOW' END`.",
            "Alias the result as `cash_direction`.",
        ],
        detailed_explanation="""Mapping disparate raw system codes into standardized reporting dimensions
is a ubiquitous data engineering responsibility.
Using `IN` inside the `WHEN` predicate consolidates multiple incoming cash flows into a single unified branch.""",
        related_concepts=["CASE", "IN", "Categorical Normalization"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-045-pub",
                name="Default Transactions",
                description="40 transactions in banking ledger.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-045-hid1",
                name="Hidden Test Case 1: Additional Transfer Out",
                description="Transfer out of $1,000 (should map to OUTFLOW).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date)
VALUES (999, 1, 'transfer_out', 1000.00, 7500.00, 'External Wire', '2024-03-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q46: Conditional Executive Bonus Calculation (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-046",
        slug="prospective-holiday-bonus-calculation",
        title="Prospective Holiday Bonus Compensation Modeling",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="medium",
        problem_description="""Executive compensation is modeling year-end holiday bonuses based on organizational seniority:
Join `employees` and `salaries` on `e.id = s.employee_id`.
Calculate a prospective bonus based on the employee's `title`:
- If `title LIKE '%Director%'` OR `title LIKE '%VP%'` then `base_salary * 0.20` (20%)
- Else if `title LIKE '%Manager%'` then `base_salary * 0.15` (15%)
- Else `base_salary * 0.10` (10%)
Round the calculated bonus to 2 decimal places and alias as `holiday_bonus`.
Return `e.id` (as `employee_id`), `e.first_name`, `e.last_name`, `e.title`, `s.base_salary`, and `holiday_bonus`.
Order by `holiday_bonus` descending (`DESC`), then `employee_id` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees", "salaries"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(100)"),
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
                {"id": 1, "first_name": "Alexander", "title": "VP of Engineering"},
                {"id": 2, "first_name": "Sarah", "title": "Engineering Manager"},
                {"id": 3, "first_name": "David", "title": "Software Engineer"},
            ],
            "salaries": [
                {"employee_id": 1, "base_salary": 220000.00},
                {"employee_id": 2, "base_salary": 160000.00},
                {"employee_id": 3, "base_salary": 140000.00},
            ],
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "first_name", "last_name", "title", "base_salary", "holiday_bonus"],
            sample_rows=[
                [1, "Alexander", "Pierce", "VP of Engineering", 220000.00, 44000.00],
                [2, "Sarah", "Connor", "Engineering Manager", 160000.00, 24000.00],
                [3, "David", "Chen", "Staff Software Engineer", 140000.00, 14000.00],
            ],
            total_row_count=60,
        ),
        starter_code="-- Join employees and salaries; calculate holiday_bonus using CASE\nSELECT \nFROM employees e\nJOIN salaries s ON e.id = s.employee_id\n",
        expected_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.title,
    s.base_salary,
    ROUND(
        CASE 
            WHEN e.title LIKE '%Director%' OR e.title LIKE '%VP%' THEN s.base_salary * 0.20
            WHEN e.title LIKE '%Manager%' THEN s.base_salary * 0.15
            ELSE s.base_salary * 0.10
        END, 2
    ) AS holiday_bonus
FROM employees e
JOIN salaries s ON e.id = s.employee_id
ORDER BY holiday_bonus DESC, employee_id ASC;""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.title,
    s.base_salary,
    ROUND(s.base_salary * (
        CASE 
            WHEN e.title LIKE '%Director%' OR e.title LIKE '%VP%' THEN 0.20
            WHEN e.title LIKE '%Manager%' THEN 0.15
            ELSE 0.10
        END
    ), 2) AS holiday_bonus
FROM employees e
JOIN salaries s ON e.id = s.employee_id
ORDER BY holiday_bonus DESC, employee_id ASC;""",
        hints=[
            "Join employees with salaries on `e.id = s.employee_id`.",
            "Use CASE to determine the multiplier: Directors/VPs (0.20), Managers (0.15), Others (0.10).",
            "Round the result to 2 decimals.",
        ],
        detailed_explanation="""Notice the elegant alternative formulation:
Multiplying `base_salary * (CASE ... END)` factors out the shared base salary column,
using the CASE expression solely to determine the scalar percentage multiplier.
Both approaches are functionally equivalent and computationally efficient.""",
        related_concepts=["Multi-tier CASE", "Join with Expressions", "Compensation Modeling"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-046-pub",
                name="Default Staff",
                description="60 corporate employees and salaries.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-046-hid1",
                name="Hidden Test Case 1: Additional Managing Director",
                description="Director with $250K salary qualifies for 20% bonus ($50,000).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Rachel', 'Zane', 'rachel@co.com', 6, 'Managing Director', '2023-01-01', 'ACTIVE');
INSERT INTO salaries (id, employee_id, base_salary, bonus, effective_date)
VALUES (999, 999, 250000.00, 40000.00, '2023-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q47: Credit Score Tiering & Risk Classification (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-047",
        slug="credit-score-fico-tiering",
        title="Credit Score Regulatory Risk Tiering",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="medium",
        problem_description="""Banking underwriting systems map raw FICO credit scores into standard risk bands:
Write a query against `customers` to map each customer's `credit_score` into `credit_tier`:
- When `credit_score >= 800` then `'Exceptional'`
- When `credit_score >= 740` then `'Very Good'`
- When `credit_score >= 670` then `'Good'`
- When `credit_score >= 580` then `'Fair'`
- Else `'Poor'`
Return `id` (as `customer_id`), `first_name`, `last_name`, `credit_score`, and `credit_tier`.
Order by `credit_score` descending (`DESC`), then `customer_id` ascending (`ASC`).""",
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
                ],
            )
        ],
        sample_input_data={
            "customers": [
                {"id": 4, "first_name": "Diana", "credit_score": 810},
                {"id": 1, "first_name": "Alice", "credit_score": 750},
                {"id": 2, "first_name": "Bob", "credit_score": 680},
                {"id": 8, "first_name": "Henry", "credit_score": 620},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["customer_id", "first_name", "last_name", "credit_score", "credit_tier"],
            sample_rows=[
                [4, "Diana", "Prince", 810, "Exceptional"],
                [1, "Alice", "Smith", 750, "Very Good"],
                [2, "Bob", "Jones", 680, "Good"],
            ],
            total_row_count=25,
        ),
        starter_code="-- Map credit_score to FICO tiers using CASE\nSELECT \nFROM customers\n",
        expected_solution="""SELECT 
    id AS customer_id,
    first_name,
    last_name,
    credit_score,
    CASE 
        WHEN credit_score >= 800 THEN 'Exceptional'
        WHEN credit_score >= 740 THEN 'Very Good'
        WHEN credit_score >= 670 THEN 'Good'
        WHEN credit_score >= 580 THEN 'Fair'
        ELSE 'Poor'
    END AS credit_tier
FROM customers
ORDER BY credit_score DESC, customer_id ASC;""",
        alternative_solution="""SELECT 
    c.id AS customer_id,
    c.first_name,
    c.last_name,
    c.credit_score,
    CASE 
        WHEN c.credit_score BETWEEN 800 AND 850 THEN 'Exceptional'
        WHEN c.credit_score BETWEEN 740 AND 799 THEN 'Very Good'
        WHEN c.credit_score BETWEEN 670 AND 739 THEN 'Good'
        WHEN c.credit_score BETWEEN 580 AND 669 THEN 'Fair'
        ELSE 'Poor'
    END AS credit_tier
FROM customers c
ORDER BY c.credit_score DESC, c.id ASC;""",
        hints=[
            "Structure the CASE statement with descending thresholds (800, 740, 670, 580).",
            "Order by `credit_score DESC, customer_id ASC`.",
        ],
        detailed_explanation="""When categorizing a continuous numeric dimension into discrete bins,
arranging thresholds monotonically (e.g. >= 800, >= 740, >= 670) simplifies the logic,
because each subsequent WHEN condition implicitly guarantees that the value was strictly less than the previous threshold.""",
        related_concepts=["Numeric Discretization", "FICO Tiering", "Monotonic CASE Clauses"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-047-pub",
                name="Default Banking Customers",
                description="25 customers across FICO credit bands.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-047-hid1",
                name="Hidden Test Case 1: Subprime Customer",
                description="Customer with credit_score 520 (maps to Poor).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO customers (id, first_name, last_name, email, credit_score, annual_income, registered_branch_id, joined_date)
VALUES (999, 'Poor', 'Credit', 'poor@bank.com', 520, 35000.00, 1, '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q48: Pivoting Metrics with Conditional Aggregation (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-048",
        slug="customer-order-status-matrix-pivot",
        title="Customer Order Status Fulfillment Matrix",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="medium",
        problem_description="""Account managers want a matrix of order completion rates per customer.
Write a query against `orders` to aggregate records by `customer_id`:
1. `customer_id`.
2. Total completed orders as `completed_count` (`SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)`).
3. Total cancelled orders as `cancelled_count` (`SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)`).
4. Total orders placed as `total_orders` (`COUNT(*)`).
Group by `customer_id` and order by `total_orders` descending (`DESC`), then `customer_id` ascending (`ASC`).""",
        database_id="db-ecommerce",
        relevant_tables=["orders"],
        table_schemas=[
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER"),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                ],
            )
        ],
        sample_input_data={
            "orders": [
                {"id": 1, "customer_id": 1, "status": "completed"},
                {"id": 2, "customer_id": 1, "status": "completed"},
                {"id": 5, "customer_id": 4, "status": "cancelled"},
                {"id": 6, "customer_id": 4, "status": "completed"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["customer_id", "completed_count", "cancelled_count", "total_orders"],
            sample_rows=[
                [1, 2, 0, 2],
                [2, 2, 0, 2],
                [3, 1, 0, 2],
                [4, 1, 1, 2],
            ],
            total_row_count=20,
        ),
        starter_code="-- Pivot status counts per customer using conditional SUM(CASE ...)\nSELECT \nFROM orders\n",
        expected_solution="""SELECT 
    customer_id,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_count,
    COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC, customer_id ASC;""",
        alternative_solution="""SELECT 
    o.customer_id,
    COUNT(CASE WHEN o.status = 'completed' THEN 1 END) AS completed_count,
    COUNT(CASE WHEN o.status = 'cancelled' THEN 1 END) AS cancelled_count,
    COUNT(o.id) AS total_orders
FROM orders o
GROUP BY o.customer_id
ORDER BY total_orders DESC, o.customer_id ASC;""",
        hints=[
            "Use `SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)` or `COUNT(CASE WHEN status = 'completed' THEN 1 END)`.",
            "Group by `customer_id` and order by `total_orders DESC, customer_id ASC`.",
        ],
        detailed_explanation="""This technique transforms vertical row status values into horizontal summary columns (pivoting).
Notice that `COUNT(CASE WHEN status = 'completed' THEN 1 END)` works because when the condition is false,
the CASE expression implicitly returns NULL, and `COUNT()` ignores NULLs!
This elegant pattern avoids expensive table self-joins.""",
        related_concepts=["Pivoting", "Cross-Tabulation", "Conditional COUNT"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-048-pub",
                name="Default Orders",
                description="35 orders across 20 customers.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-048-hid1",
                name="Hidden Test Case 1: Additional Cancelled Order",
                description="Customer 1 cancels an order.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO orders (id, customer_id, order_date, total_amount, status)
VALUES (999, 1, '2024-03-01', 75.00, 'cancelled');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q49: GPA Grade Point Transformation (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-049",
        slug="academic-grade-point-average-gpa-case",
        title="Cumulative Grade Point Average (GPA) Computation via CASE",
        topic_id="top-07",
        topic="CASE Expressions, COALESCE & Conditional Logic",
        difficulty="hard",
        problem_description="""Registrar systems compute cumulative Grade Point Average (GPA) from letter grades.
Write a query against `enrollments` to convert each enrollment's `letter_grade` into numeric grade points using `CASE`:
- `'A'` -> `4.0`
- `'B'` -> `3.0`
- `'C'` -> `2.0`
- `'D'` -> `1.0`
- `'F'` -> `0.0`
Filter for completed enrollments where `letter_grade IS NOT NULL`.
Group by `student_id` and calculate:
1. `student_id`.
2. Total graded courses as `graded_courses` (`COUNT(*)`).
3. The average grade points as `gpa` (`ROUND(AVG(...), 2)`).
Filter to only include students who have completed at least 2 graded courses (`HAVING COUNT(*) >= 2`).
Order by `gpa` descending (`DESC`), then `student_id` ascending (`ASC`).""",
        database_id="db-university",
        relevant_tables=["enrollments"],
        table_schemas=[
            TableSchemaInfo(
                table_name="enrollments",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="student_id", type="INTEGER"),
                    ColumnSchema(name="course_id", type="INTEGER"),
                    ColumnSchema(name="letter_grade", type="VARCHAR(2)"),
                ],
            )
        ],
        sample_input_data={
            "enrollments": [
                {"id": 1, "student_id": 1, "letter_grade": "A"},
                {"id": 2, "student_id": 1, "letter_grade": "B"},
                {"id": 3, "student_id": 2, "letter_grade": "A"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["student_id", "graded_courses", "gpa"],
            sample_rows=[
                [1, 2, 3.50],
                [3, 2, 3.50],
                [2, 2, 3.00],
            ],
            total_row_count=20,
        ),
        starter_code="-- Map letter_grade to grade points (4.0, 3.0, 2.0, 1.0, 0.0) and compute GPA\nSELECT \nFROM enrollments\n",
        expected_solution="""SELECT 
    student_id,
    COUNT(*) AS graded_courses,
    ROUND(AVG(
        CASE letter_grade
            WHEN 'A' THEN 4.0
            WHEN 'B' THEN 3.0
            WHEN 'C' THEN 2.0
            WHEN 'D' THEN 1.0
            WHEN 'F' THEN 0.0
            ELSE 0.0
        END
    ), 2) AS gpa
FROM enrollments
WHERE letter_grade IS NOT NULL
GROUP BY student_id
HAVING COUNT(*) >= 2
ORDER BY gpa DESC, student_id ASC;""",
        alternative_solution="""SELECT 
    e.student_id,
    COUNT(e.id) AS graded_courses,
    ROUND(AVG(
        CASE 
            WHEN e.letter_grade = 'A' THEN 4.0
            WHEN e.letter_grade = 'B' THEN 3.0
            WHEN e.letter_grade = 'C' THEN 2.0
            WHEN e.letter_grade = 'D' THEN 1.0
            ELSE 0.0
        END
    ), 2) AS gpa
FROM enrollments e
WHERE e.letter_grade IS NOT NULL
GROUP BY e.student_id
HAVING COUNT(e.id) >= 2
ORDER BY gpa DESC, e.student_id ASC;""",
        hints=[
            "Use a simple CASE: `CASE letter_grade WHEN 'A' THEN 4.0 ... END`.",
            "Wrap the CASE expression inside `AVG(...)`, then `ROUND(..., 2)`.",
            "Group by `student_id` and filter with `HAVING COUNT(*) >= 2`.",
            "Order by `gpa DESC, student_id ASC`.",
        ],
        detailed_explanation="""This problem demonstrates nesting a `CASE` expression inside an aggregate function `AVG()`.
The engine evaluates the scalar CASE mapping for each individual row, producing a stream of numeric grade points,
and then computes the arithmetic mean for each student group.
The `HAVING COUNT(*) >= 2` filter ensures that GPA rankings reflect meaningful course loads.""",
        related_concepts=["Nested CASE in AVG", "GPA Calculation", "Simple CASE vs Searched CASE"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-049-pub",
                name="Default Enrollments",
                description="52 enrollments across students.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-049-hid1",
                name="Hidden Test Case 1: Straight-A Student",
                description="Student with two straight A grades takes top rank with 4.00.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO enrollments (id, student_id, course_id, semester, academic_year, letter_grade) VALUES
(998, 25, 1, 'Fall', 2023, 'A'),
(999, 25, 2, 'Spring', 2024, 'A');""",
            ),
        ],
    ),
]
