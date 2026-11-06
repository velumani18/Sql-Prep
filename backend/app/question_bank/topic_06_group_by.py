from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_06_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q36: Employee Headcount per Department (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-036",
        slug="department-headcount-distribution",
        title="Department Headcount Distribution",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="easy",
        problem_description="""Human resources needs a staffing distribution breakdown across all active departments.
Write a query against `employees` to count the number of employees in each department.
Filter out unassigned employees (`WHERE department_id IS NOT NULL`).
Group by `department_id` and return `department_id` and `COUNT(*)` as `headcount`.
Order by `headcount` in descending order (`DESC`), then by `department_id` ascending (`ASC`).""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="department_id", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "department_id": 1},
                {"id": 2, "department_id": 1},
                {"id": 15, "department_id": 2},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["department_id", "headcount"],
            sample_rows=[
                [1, 15],
                [3, 10],
                [2, 8],
                [4, 8],
                [5, 6],
                [6, 4],
                [7, 4],
            ],
            total_row_count=7,
        ),
        starter_code="-- Group employees by department_id and count headcount\nSELECT \nFROM employees\n",
        expected_solution="""SELECT 
    department_id,
    COUNT(*) AS headcount
FROM employees
WHERE department_id IS NOT NULL
GROUP BY department_id
ORDER BY headcount DESC, department_id ASC;""",
        alternative_solution="""SELECT 
    e.department_id,
    COUNT(e.id) AS headcount
FROM employees e
WHERE e.department_id IS NOT NULL
GROUP BY e.department_id
ORDER BY 2 DESC, 1 ASC;""",
        hints=[
            "Filter unassigned employees: `WHERE department_id IS NOT NULL`.",
            "Group by department: `GROUP BY department_id`.",
            "Order by `headcount DESC, department_id ASC`.",
        ],
        detailed_explanation="""The `GROUP BY` clause divides rows into summary buckets based on distinct values of the grouping key.
Each bucket produces exactly one summary row in the result set.
Ordering by `headcount DESC, department_id ASC` guarantees a deterministic sequence from largest to smallest division.""",
        related_concepts=["GROUP BY", "Aggregate Bucket", "Deterministic Ordering"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-036-pub",
                name="Default Company Staff",
                description="55 department-assigned employees across 7 departments.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-036-hid1",
                name="Hidden Test Case 1: Additional Legal Hire",
                description="New hire in department 6.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Frank', 'Nitti', 'frank@co.com', 6, 'Associate Counsel', '2024-03-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q37: Order Volume and Value by Status (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-037",
        slug="ecommerce-order-status-breakdown",
        title="Order Status Volume and Revenue Distribution",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="easy",
        problem_description="""Fulfillment operations tracks processing pipelines and completed revenue.
Write a query against `orders` to aggregate:
1. `status`.
2. Total count of orders as `order_count` (`COUNT(*)`).
3. Sum of total_amount as `total_revenue`, rounded to 2 decimal places.
Group by `status` and order by `total_revenue` in descending order (`DESC`).""",
        database_id="db-ecommerce",
        relevant_tables=["orders"],
        table_schemas=[
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                    ColumnSchema(name="total_amount", type="DECIMAL(10,2)"),
                ],
            )
        ],
        sample_input_data={
            "orders": [
                {"id": 1, "status": "completed", "total_amount": 129.99},
                {"id": 2, "status": "completed", "total_amount": 499.98},
                {"id": 3, "status": "processing", "total_amount": 279.99},
                {"id": 5, "status": "cancelled", "total_amount": 599.98},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["status", "order_count", "total_revenue"],
            sample_rows=[
                ["completed", 20, 8459.60],
                ["processing", 10, 3120.45],
                ["cancelled", 5, 1450.00],
            ],
            total_row_count=3,
        ),
        starter_code="-- Group orders by status: count and total_revenue\nSELECT \nFROM orders\n",
        expected_solution="""SELECT 
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;""",
        alternative_solution="""SELECT 
    o.status,
    COUNT(o.id) AS order_count,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
GROUP BY o.status
ORDER BY 3 DESC;""",
        hints=[
            "Group by status: `GROUP BY status`.",
            "Compute `COUNT(*)` and `ROUND(SUM(total_amount), 2)`.",
            "Order by `total_revenue DESC`.",
        ],
        detailed_explanation="""Grouping by categorical status columns reveals operational bottlenecks and pipeline volume.
When calculating revenue sums, wrapping `SUM(total_amount)` inside `ROUND(..., 2)` ensures
currency formatting and eliminates floating-point artifacts.""",
        related_concepts=["GROUP BY", "SUM", "Categorical Breakdown"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-037-pub",
                name="Default Orders",
                description="35 orders across 3 statuses.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-037-hid1",
                name="Hidden Test Case 1: Additional Processing Order",
                description="New $500 processing order.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO orders (id, customer_id, order_date, total_amount, status)
VALUES (999, 1, '2024-03-01', 500.00, 'processing');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q38: Portfolio Segmentation by Account Type (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-038",
        slug="banking-account-type-portfolio",
        title="Deposit Portfolio Segmentation by Account Type",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="easy",
        problem_description="""Retail banking executives analyze deposit balances by product category.
Write a query against `accounts` to aggregate:
1. `account_type`.
2. Total number of accounts as `account_count`.
3. Average balance as `avg_balance`, rounded to 2 decimal places.
Group by `account_type` and order by `avg_balance` in descending order (`DESC`).""",
        database_id="db-banking",
        relevant_tables=["accounts"],
        table_schemas=[
            TableSchemaInfo(
                table_name="accounts",
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
                {"id": 5, "account_type": "Business", "balance": 112400.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["account_type", "account_count", "avg_balance"],
            sample_rows=[
                ["Business", 5, 85600.00],
                ["Savings", 15, 22400.50],
                ["Checking", 15, 6250.75],
            ],
            total_row_count=3,
        ),
        starter_code="-- Group accounts by account_type: count and avg_balance\nSELECT \nFROM accounts\n",
        expected_solution="""SELECT 
    account_type,
    COUNT(*) AS account_count,
    ROUND(AVG(balance), 2) AS avg_balance
FROM accounts
GROUP BY account_type
ORDER BY avg_balance DESC;""",
        alternative_solution="""SELECT 
    a.account_type,
    COUNT(a.id) AS account_count,
    ROUND(AVG(a.balance), 2) AS avg_balance
FROM accounts a
GROUP BY a.account_type
ORDER BY 3 DESC;""",
        hints=[
            "Group by account_type: `GROUP BY account_type`.",
            "Use `COUNT(*)` for account_count and `ROUND(AVG(balance), 2)` for avg_balance.",
            "Order by `avg_balance DESC`.",
        ],
        detailed_explanation="""Categorical aggregation segments financial metrics across lines of business.
Grouping automatically partitions the dataset by distinct `account_type` values,
calculating the count and average balance independently for each tier.""",
        related_concepts=["GROUP BY", "AVG", "Financial Portfolio Analysis"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-038-pub",
                name="Default Accounts",
                description="35 accounts across Checking, Savings, Business.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-038-hid1",
                name="Hidden Test Case 1: Extra Checking Account",
                description="New checking account with $10,000 balance.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 1, 1, 'CHK-TEST', 'Checking', 10000.00, 'active', '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q39: Filtering Aggregated Groups with HAVING (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-039",
        slug="departments-with-large-headcounts-having",
        title="Filtering Department Headcounts with HAVING",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="medium",
        problem_description="""Organizational restructuring focuses on large divisions.
Write a query against `employees` to find all departments that have strictly more than 6 employees (`headcount > 6`).
Filter out unassigned staff (`WHERE department_id IS NOT NULL`).
Group by `department_id`, apply the group filter with `HAVING`, and return `department_id` and `COUNT(*)` as `headcount`.
Order by `headcount` in descending order (`DESC`), then `department_id` ASC.""",
        database_id="db-company",
        relevant_tables=["employees"],
        table_schemas=[
            TableSchemaInfo(
                table_name="employees",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="department_id", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 1, "department_id": 1},
                {"id": 15, "department_id": 2},
                {"id": 50, "department_id": 6},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["department_id", "headcount"],
            sample_rows=[
                [1, 15],
                [3, 10],
                [2, 8],
                [4, 8],
            ],
            total_row_count=4,
        ),
        starter_code="-- Find departments with COUNT(*) > 6 using HAVING\nSELECT \nFROM employees\n",
        expected_solution="""SELECT 
    department_id,
    COUNT(*) AS headcount
FROM employees
WHERE department_id IS NOT NULL
GROUP BY department_id
HAVING COUNT(*) > 6
ORDER BY headcount DESC, department_id ASC;""",
        alternative_solution="""SELECT 
    e.department_id,
    COUNT(e.id) AS headcount
FROM employees e
WHERE e.department_id IS NOT NULL
GROUP BY e.department_id
HAVING COUNT(e.id) >= 7
ORDER BY headcount DESC, e.department_id ASC;""",
        hints=[
            "Use `WHERE department_id IS NOT NULL` before grouping.",
            "Use `GROUP BY department_id`.",
            "Use `HAVING COUNT(*) > 6` to filter aggregated group rows.",
        ],
        detailed_explanation="""Understanding the distinction between WHERE and HAVING is a cornerstone of SQL mastery:
- `WHERE`: Filters individual rows BEFORE aggregation.
- `HAVING`: Filters aggregated summary groups AFTER aggregation.
Attempting to filter `WHERE COUNT(*) > 6` causes a syntax error because aggregate values do not yet exist during WHERE execution.""",
        related_concepts=["HAVING vs WHERE", "Aggregate Filtering", "Execution Order"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-039-pub",
                name="Default Company Staff",
                description="Departments 1, 3, 2, 4 have > 6 staff.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-039-hid1",
                name="Hidden Test Case 1: Department 5 Expansion",
                description="Two hires in department 5 push it to 8 staff.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status) VALUES
(998, 'H1', 'L1', 'h1@co.com', 5, 'Specialist', '2024-03-01', 'ACTIVE'),
(999, 'H2', 'L2', 'h2@co.com', 5, 'Specialist', '2024-03-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q40: Multi-Column Grouping by Country and City (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-040",
        slug="customer-multi-column-location-clusters",
        title="Customer Multi-Column Geographic Clusters",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="medium",
        problem_description="""Marketing wants to identify metropolitan customer clusters.
Write a query against `customers` to group records by both `country` and `city`.
Calculate the number of customers in each city as `customer_count` (`COUNT(*)`).
Filter to include only cities that have at least 2 customers (`HAVING COUNT(*) >= 2`).
Order by `customer_count` descending (`DESC`), then `country` ascending (`ASC`), then `city` ascending (`ASC`).
Return `country`, `city`, and `customer_count`.""",
        database_id="db-ecommerce",
        relevant_tables=["customers"],
        table_schemas=[
            TableSchemaInfo(
                table_name="customers",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="country", type="VARCHAR(50)"),
                    ColumnSchema(name="city", type="VARCHAR(60)"),
                ],
            )
        ],
        sample_input_data={
            "customers": [
                {"id": 1, "country": "United States", "city": "New York"},
                {"id": 6, "country": "United States", "city": "New York"},
                {"id": 2, "country": "United States", "city": "Los Angeles"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["country", "city", "customer_count"],
            sample_rows=[
                ["United States", "New York", 3],
                ["Canada", "Toronto", 2],
                ["United Kingdom", "London", 2],
            ],
            total_row_count=5,
        ),
        starter_code="-- Multi-column group: country, city with COUNT(*) >= 2\nSELECT \nFROM customers\n",
        expected_solution="""SELECT 
    country,
    city,
    COUNT(*) AS customer_count
FROM customers
GROUP BY country, city
HAVING COUNT(*) >= 2
ORDER BY customer_count DESC, country ASC, city ASC;""",
        alternative_solution="""SELECT 
    c.country,
    c.city,
    COUNT(c.id) AS customer_count
FROM customers c
GROUP BY c.country, c.city
HAVING COUNT(c.id) > 1
ORDER BY customer_count DESC, c.country ASC, c.city ASC;""",
        hints=[
            "Specify both columns in the GROUP BY clause: `GROUP BY country, city`.",
            "Use `HAVING COUNT(*) >= 2` to filter for clusters with 2 or more customers.",
            "Order by `customer_count DESC, country ASC, city ASC`.",
        ],
        detailed_explanation="""Multi-column grouping creates a distinct bucket for every unique combination of `(country, city)`.
This allows hierarchical demographic aggregation.
The `HAVING COUNT(*) >= 2` clause prunes solitary individual records, leaving only meaningful customer clusters.""",
        related_concepts=["Multi-Column Grouping", "HAVING", "Geographic Clusters"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-040-pub",
                name="Default Customers",
                description="30 global customers.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-040-hid1",
                name="Hidden Test Case 1: Additional London Customer",
                description="New customer in London increases cluster size to 3.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO customers (id, first_name, last_name, email, country, city, created_at)
VALUES (999, 'Arthur', 'Dent', 'arthur@hitchhiker.uk', 'United Kingdom', 'London', '2024-03-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q41: Professor Course Load with HAVING (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-041",
        slug="faculty-course-load-threshold",
        title="Faculty Teaching Load & Credit Volume",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="medium",
        problem_description="""Academic affairs tracks faculty teaching allocations.
Write a query against `courses` to analyze teaching loads for assigned professors (`WHERE professor_id IS NOT NULL`).
Group by `professor_id` and find all professors assigned to teach 2 or more courses (`HAVING COUNT(*) >= 2`).
Return `professor_id`, total courses taught as `courses_taught` (`COUNT(*)`), and total credits as `total_credits_taught` (`SUM(credits)`).
Order by `courses_taught` descending (`DESC`), then `professor_id` ascending (`ASC`).""",
        database_id="db-university",
        relevant_tables=["courses"],
        table_schemas=[
            TableSchemaInfo(
                table_name="courses",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="professor_id", type="INTEGER"),
                    ColumnSchema(name="credits", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "courses": [
                {"id": 1, "professor_id": 1, "credits": 4},
                {"id": 2, "professor_id": 1, "credits": 4},
                {"id": 3, "professor_id": 2, "credits": 4},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["professor_id", "courses_taught", "total_credits_taught"],
            sample_rows=[
                [1, 2, 8],
                [2, 2, 7],
                [3, 2, 8],
                [5, 2, 8],
            ],
            total_row_count=4,
        ),
        starter_code="-- Group courses by professor_id with COUNT(*) >= 2\nSELECT \nFROM courses\n",
        expected_solution="""SELECT 
    professor_id,
    COUNT(*) AS courses_taught,
    SUM(credits) AS total_credits_taught
FROM courses
WHERE professor_id IS NOT NULL
GROUP BY professor_id
HAVING COUNT(*) >= 2
ORDER BY courses_taught DESC, professor_id ASC;""",
        alternative_solution="""SELECT 
    c.professor_id,
    COUNT(c.id) AS courses_taught,
    SUM(c.credits) AS total_credits_taught
FROM courses c
WHERE c.professor_id IS NOT NULL
GROUP BY c.professor_id
HAVING COUNT(c.id) > 1
ORDER BY 2 DESC, 1 ASC;""",
        hints=[
            "Filter out null assignments: `WHERE professor_id IS NOT NULL`.",
            "Group by `professor_id`.",
            "Filter for professors teaching at least 2 courses using `HAVING COUNT(*) >= 2`.",
        ],
        detailed_explanation="""Aggregating child foreign key records (`courses.professor_id`) allows capacity audits
without necessarily joining to parent dimension tables.
`HAVING COUNT(*) >= 2` isolates heavily loaded instructors, calculating both their class frequency and aggregate credit load.""",
        related_concepts=["Foreign Key Grouping", "HAVING", "Workload Audits"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-041-pub",
                name="Default Courses",
                description="Professors 1, 2, 3, 5 teach 2 courses each.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-041-hid1",
                name="Hidden Test Case 1: Third Course for Professor 1",
                description="Professor 1 assigned 3rd course.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO courses (id, code, title, department_id, professor_id, credits)
VALUES (999, 'CS499', 'Capstone Project', 1, 1, 4);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q42: High-Volume Account Alert with HAVING (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-042",
        slug="high-volume-velocity-account-alert",
        title="High-Velocity Account Risk Audit with Dual HAVING Conditions",
        topic_id="top-06",
        topic="GROUP BY & HAVING",
        difficulty="hard",
        problem_description="""Anti-money laundering compliance flags accounts exhibiting high velocity and high average transaction value:
Write a query against `transactions` to identify accounts where:
1. The account has at least 3 transactions recorded (`COUNT(*) >= 3`).
2. The average transaction amount is at least $1,500.00 (`AVG(amount) >= 1500.00`).
Group by `account_id` and return:
- `account_id`
- Total transaction count as `tx_count` (`COUNT(*)`)
- Total transaction volume as `total_volume` (`ROUND(SUM(amount), 2)`)
- Average transaction size as `avg_amount` (`ROUND(AVG(amount), 2)`)
Order by `total_volume` in descending order (`DESC`), then `account_id` ascending (`ASC`).""",
        database_id="db-banking",
        relevant_tables=["transactions"],
        table_schemas=[
            TableSchemaInfo(
                table_name="transactions",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="account_id", type="INTEGER"),
                    ColumnSchema(name="amount", type="DECIMAL(12,2)"),
                ],
            )
        ],
        sample_input_data={
            "transactions": [
                {"id": 1, "account_id": 1, "amount": 3500.00},
                {"id": 2, "account_id": 1, "amount": 4500.00},
                {"id": 3, "account_id": 1, "amount": 250.00},
                {"id": 10, "account_id": 5, "amount": 5400.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["account_id", "tx_count", "total_volume", "avg_amount"],
            sample_rows=[
                [1, 4, 9450.25, 2362.56],
                [4, 3, 7800.50, 2600.17],
            ],
            total_row_count=2,
        ),
        starter_code="-- Dual HAVING criteria: COUNT(*) >= 3 AND AVG(amount) >= 1500\nSELECT \nFROM transactions\n",
        expected_solution="""SELECT 
    account_id,
    COUNT(*) AS tx_count,
    ROUND(SUM(amount), 2) AS total_volume,
    ROUND(AVG(amount), 2) AS avg_amount
FROM transactions
GROUP BY account_id
HAVING COUNT(*) >= 3 AND AVG(amount) >= 1500.00
ORDER BY total_volume DESC, account_id ASC;""",
        alternative_solution="""SELECT 
    t.account_id,
    COUNT(t.id) AS tx_count,
    ROUND(SUM(t.amount), 2) AS total_volume,
    ROUND(AVG(t.amount), 2) AS avg_amount
FROM transactions t
GROUP BY t.account_id
HAVING COUNT(t.id) > 2 AND AVG(t.amount) >= 1500
ORDER BY total_volume DESC, t.account_id ASC;""",
        hints=[
            "Group by `account_id`.",
            "Combine group filters using `HAVING COUNT(*) >= 3 AND AVG(amount) >= 1500.00`.",
            "Order by `total_volume DESC, account_id ASC`.",
        ],
        detailed_explanation="""HAVING clauses can evaluate multiple compound aggregate conditions connected with `AND` and `OR`.
Filtering on both transaction frequency (`COUNT(*) >= 3`) and intensity (`AVG(amount) >= 1500.00`)
isolates institutional or high-risk accounts from micro-retail accounts,
performing the entire multi-dimensional filter in a single post-aggregation phase.""",
        related_concepts=["Compound HAVING", "Risk Segmentation", "Post-Aggregation Filtering"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-042-pub",
                name="Default Transactions",
                description="40 transactions in ledger.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-042-hid1",
                name="Hidden Test Case 1: Account 2 Third Transaction",
                description="Account 2 qualifies with 3rd large transaction.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date)
VALUES (999, 2, 'deposit', 5000.00, 30000.00, 'Commercial Transfer', '2024-03-01');""",
            ),
        ],
    ),
]
