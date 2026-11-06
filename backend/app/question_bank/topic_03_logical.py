from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_03_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q15: Wildcard Pattern Matching with LIKE (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-015",
        slug="wireless-tech-products-like",
        title="Wireless Technology Product Search",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="easy",
        problem_description="""Marketing wants to feature all wireless peripheral equipment on the homepage.
Write a query to find all products where `name` contains the substring `'Wireless'`.
Return `id` (as `product_id`), `name` (as `product_name`), and `price`.""",
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
                {"id": 1, "name": "Wireless Ergonomic Mouse", "price": 49.99},
                {"id": 2, "name": "Mechanical RGB Keyboard", "price": 129.99},
                {"id": 5, "name": "Wireless Noise-Canceling Headphones", "price": 299.99},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["product_id", "product_name", "price"],
            sample_rows=[
                [1, "Wireless Ergonomic Mouse", 49.99],
                [5, "Wireless Noise-Canceling Headphones", 299.99],
            ],
            total_row_count=2,
        ),
        starter_code="-- Find products containing 'Wireless'\nSELECT \nFROM products\n",
        expected_solution="""SELECT 
    id AS product_id,
    name AS product_name,
    price
FROM products
WHERE name LIKE '%Wireless%';""",
        alternative_solution="""SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.price
FROM products p
WHERE INSTR(p.name, 'Wireless') > 0;""",
        hints=[
            "Use the `LIKE` operator with surrounding percent signs: `WHERE name LIKE '%Wireless%'`.",
            "Alias `id` as `product_id` and `name` as `product_name`.",
        ],
        detailed_explanation="""The SQL `LIKE` operator performs pattern matching using wildcard characters:
- `%`: Matches zero or more arbitrary characters.
- `_`: Matches exactly one single character.
A pattern with `%` at both ends (`'%Wireless%'`) matches the target substring anywhere within the text column.""",
        related_concepts=["LIKE", "Wildcards", "Substring Matching"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-015-pub",
                name="Default Catalog",
                description="20 products with various tech accessories.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-015-hid1",
                name="Hidden Test Case 1: Additional Wireless Gadget",
                description="New Wireless Charging Stand added to catalog.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, 'Fast Wireless Charging Stand', 39.99, 75, 1);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q16: Discrete Set Membership with IN (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-016",
        slug="strategic-department-personnel",
        title="Strategic Department Personnel Filtering",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="easy",
        problem_description="""Executive leadership is organizing a strategy summit for Engineering (dept 1), Marketing (dept 2), and Finance (dept 4).
Write a query to retrieve all employees belonging to any of these three departments (`department_id IN (1, 2, 4)`).
Return `id` (as `employee_id`), `first_name`, `last_name`, and `department_id`.""",
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
                {"id": 15, "first_name": "Rachel", "department_id": 2},
                {"id": 30, "first_name": "Edward", "department_id": 3},
                {"id": 40, "first_name": "Victor", "department_id": 4},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "first_name", "last_name", "department_id"],
            sample_rows=[
                [1, "Alexander", "Pierce", 1],
                [15, "Rachel", "Green", 2],
                [40, "Victor", "Stone", 4],
            ],
            total_row_count=35,
        ),
        starter_code="-- Find staff in departments 1, 2, or 4\nSELECT \nFROM employees\n",
        expected_solution="""SELECT 
    id AS employee_id,
    first_name,
    last_name,
    department_id
FROM employees
WHERE department_id IN (1, 2, 4);""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.department_id
FROM employees e
WHERE e.department_id = 1 OR e.department_id = 2 OR e.department_id = 4;""",
        hints=[
            "Use the `IN` operator: `WHERE department_id IN (1, 2, 4)`.",
            "This is much cleaner and more readable than chaining multiple `OR` conditions.",
        ],
        detailed_explanation="""The `IN` operator tests whether an expression matches any value in a specified list or subquery.
It is syntactically concise and logically equivalent to chained equality comparisons (`col = 1 OR col = 2 OR col = 4`).
Database optimizers frequently convert `IN (val1, val2)` into binary search lookups or hash lookups.""",
        related_concepts=["IN", "Set Membership", "Disjunctive Equalities"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-016-pub",
                name="Default Employees",
                description="60 corporate employees.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-016-hid1",
                name="Hidden Test Case 1: Additional Marketing Intern",
                description="New hire in department 2.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, title, hire_date, status)
VALUES (999, 'Maya', 'Lin', 'maya.lin@co.com', 2, 'Marketing Associate', '2024-02-01', 'ACTIVE');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q17: Range Filtering with BETWEEN (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-017",
        slug="mid-tier-loan-portfolio-between",
        title="Mid-Tier Commercial Loan Portfolio",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="easy",
        problem_description="""Credit risk management is reviewing intermediate commercial and personal loans.
Write a query to retrieve all loans with a `principal_amount` between $25,000.00 and $75,000.00 inclusive.
Return `id` (as `loan_id`), `loan_type`, `principal_amount`, and `interest_rate`.""",
        database_id="db-banking",
        relevant_tables=["loans"],
        table_schemas=[
            TableSchemaInfo(
                table_name="loans",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="loan_type", type="VARCHAR(40)"),
                    ColumnSchema(name="principal_amount", type="DECIMAL(12,2)"),
                    ColumnSchema(name="interest_rate", type="DECIMAL(5,2)"),
                ],
            )
        ],
        sample_input_data={
            "loans": [
                {"id": 1, "loan_type": "Mortgage", "principal_amount": 350000.00, "interest_rate": 6.50},
                {"id": 2, "loan_type": "Auto", "principal_amount": 28000.00, "interest_rate": 5.25},
                {"id": 3, "loan_type": "Personal", "principal_amount": 50000.00, "interest_rate": 8.10},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["loan_id", "loan_type", "principal_amount", "interest_rate"],
            sample_rows=[
                [2, "Auto", 28000.00, 5.25],
                [3, "Personal", 50000.00, 8.10],
            ],
            total_row_count=5,
        ),
        starter_code="-- Find loans with principal between 25,000 and 75,000\nSELECT \nFROM loans\n",
        expected_solution="""SELECT 
    id AS loan_id,
    loan_type,
    principal_amount,
    interest_rate
FROM loans
WHERE principal_amount BETWEEN 25000.00 AND 75000.00;""",
        alternative_solution="""SELECT 
    l.id AS loan_id,
    l.loan_type,
    l.principal_amount,
    l.interest_rate
FROM loans l
WHERE l.principal_amount >= 25000.00 AND l.principal_amount <= 75000.00;""",
        hints=[
            "Use the `BETWEEN` operator: `WHERE principal_amount BETWEEN 25000.00 AND 75000.00`.",
            "Remember that BETWEEN in SQL is always inclusive of both boundary values.",
        ],
        detailed_explanation="""The `BETWEEN` operator tests whether a value falls within an inclusive range (`col >= low AND col <= high`).
It works seamlessly on numbers, dates, and strings.
Using `BETWEEN` clearly communicates intent and allows the database query engine to construct bounded index seeks.""",
        related_concepts=["BETWEEN", "Inclusive Ranges", "B-Tree Range Seek"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-017-pub",
                name="Default Loans",
                description="15 corporate and retail loans.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-017-hid1",
                name="Hidden Test Case 1: Additional Equipment Loan",
                description="Loan for $45,000.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO loans (id, customer_id, branch_id, loan_type, principal_amount, interest_rate, term_months, status, origination_date)
VALUES (999, 1, 1, 'Commercial Equipment', 45000.00, 6.75, 48, 'active', '2024-01-15');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q18: Compound Conjunction with Precedence (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-018",
        slug="high-value-in-flight-orders",
        title="High-Value In-Flight Orders",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="medium",
        problem_description="""Fulfillment operations needs to expedite high-value orders currently in flight.
Write a query to find all orders where:
1. `status` is EITHER `'completed'` OR `'processing'`.
2. `total_amount > 200.00`.
Return `id` (as `order_id`), `customer_id`, `status`, and `total_amount`.""",
        database_id="db-ecommerce",
        relevant_tables=["orders"],
        table_schemas=[
            TableSchemaInfo(
                table_name="orders",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="customer_id", type="INTEGER"),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                    ColumnSchema(name="total_amount", type="DECIMAL(10,2)"),
                ],
            )
        ],
        sample_input_data={
            "orders": [
                {"id": 1, "customer_id": 1, "status": "completed", "total_amount": 129.99},
                {"id": 2, "customer_id": 2, "status": "completed", "total_amount": 499.98},
                {"id": 3, "customer_id": 3, "status": "processing", "total_amount": 279.99},
                {"id": 5, "customer_id": 4, "status": "cancelled", "total_amount": 599.98},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["order_id", "customer_id", "status", "total_amount"],
            sample_rows=[
                [2, 2, "completed", 499.98],
                [3, 3, "processing", 279.99],
            ],
            total_row_count=12,
        ),
        starter_code="-- High value orders: status IN ('completed', 'processing') AND total_amount > 200\nSELECT \nFROM orders\n",
        expected_solution="""SELECT 
    id AS order_id,
    customer_id,
    status,
    total_amount
FROM orders
WHERE status IN ('completed', 'processing') AND total_amount > 200.00;""",
        alternative_solution="""SELECT 
    o.id AS order_id,
    o.customer_id,
    o.status,
    o.total_amount
FROM orders o
WHERE (o.status = 'completed' OR o.status = 'processing') AND o.total_amount > 200.00;""",
        hints=[
            "Use `status IN ('completed', 'processing')` to group status options cleanly.",
            "Combine with `AND total_amount > 200.00`.",
        ],
        detailed_explanation="""When writing compound filters combining multiple OR branches with an AND condition,
using `status IN ('completed', 'processing')` eliminates ambiguity.
If using `OR`, explicit parentheses `(status = 'A' OR status = 'B') AND amount > 200` are required,
because AND binds tighter than OR.""",
        related_concepts=["IN", "Precedence", "Compound Logic"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-018-pub",
                name="Default Orders",
                description="35 e-commerce orders.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-018-hid1",
                name="Hidden Test Case 1: Cancelled High Value Order",
                description="Cancelled $1,000 order (should be excluded).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO orders (id, customer_id, order_date, total_amount, status)
VALUES (999, 1, '2024-03-01', 1000.00, 'cancelled');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q19: Set Negation & Substring Matching (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-019",
        slug="senior-faculty-tenure-audit",
        title="Senior Faculty Tenure Audit",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="medium",
        problem_description="""The university senate is appointing senior faculty representatives.
Candidates must be tenured or full professors:
1. `title` must NOT contain `'Assistant'` (`title NOT LIKE '%Assistant%'`).
2. `hired_year` must NOT be in the years 2018 or 2020 (`hired_year NOT IN (2018, 2020)`).
Write a query to retrieve `id` (as `professor_id`), `first_name`, `last_name`, `title`, and `hired_year`.""",
        database_id="db-university",
        relevant_tables=["professors"],
        table_schemas=[
            TableSchemaInfo(
                table_name="professors",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="first_name", type="VARCHAR(50)"),
                    ColumnSchema(name="last_name", type="VARCHAR(50)"),
                    ColumnSchema(name="title", type="VARCHAR(60)"),
                    ColumnSchema(name="hired_year", type="INTEGER"),
                ],
            )
        ],
        sample_input_data={
            "professors": [
                {"id": 1, "first_name": "Alan", "title": "Professor", "hired_year": 2012},
                {"id": 2, "first_name": "Grace", "title": "Associate Professor", "hired_year": 2015},
                {"id": 4, "first_name": "Ada", "title": "Assistant Professor", "hired_year": 2020},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["professor_id", "first_name", "last_name", "title", "hired_year"],
            sample_rows=[
                [1, "Alan", "Turing", "Professor", 2012],
                [2, "Grace", "Hopper", "Associate Professor", 2015],
            ],
            total_row_count=5,
        ),
        starter_code="-- NOT LIKE '%Assistant%' AND hired_year NOT IN (2018, 2020)\nSELECT \nFROM professors\n",
        expected_solution="""SELECT 
    id AS professor_id,
    first_name,
    last_name,
    title,
    hired_year
FROM professors
WHERE title NOT LIKE '%Assistant%' AND hired_year NOT IN (2018, 2020);""",
        alternative_solution="""SELECT 
    p.id AS professor_id,
    p.first_name,
    p.last_name,
    p.title,
    p.hired_year
FROM professors p
WHERE NOT (p.title LIKE '%Assistant%') AND p.hired_year != 2018 AND p.hired_year != 2020;""",
        hints=[
            "Use `title NOT LIKE '%Assistant%'` to exclude Assistant Professors.",
            "Use `hired_year NOT IN (2018, 2020)` to exclude specific cohorts.",
        ],
        detailed_explanation="""Negation operators (`NOT LIKE`, `NOT IN`) exclude sets of matching values.
Caution: When using `NOT IN (val1, val2, ...)`, if the target list or subquery contains a single NULL value,
the entire NOT IN expression evaluates to UNKNOWN for all rows in SQL three-valued logic.
When using literal sets `(2018, 2020)`, this risk does not occur.""",
        related_concepts=["NOT LIKE", "NOT IN", "Negation", "Three-Valued Logic"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-019-pub",
                name="Default Faculty",
                description="8 university professors.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-019-hid1",
                name="Hidden Test Case 1: Assistant Professor Hired 2014",
                description="Assistant Professor hired in 2014 (must be excluded due to title).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO professors (id, first_name, last_name, email, department_id, title, hired_year)
VALUES (999, 'Junior', 'Researcher', 'jr@univ.edu', 1, 'Assistant Professor', 2014);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q20: Targeted Transaction Pattern Search (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-020",
        slug="payroll-direct-deposit-detection",
        title="Automated Payroll & Direct Deposit Verification",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="medium",
        problem_description="""Compliance algorithms verify automated wage credit streams into checking accounts.
Write a query to find all transactions where:
1. `description` contains EITHER `'Payroll'` OR `'Direct Deposit'`.
2. `amount >= 1000.00`.
Return `id` (as `transaction_id`), `account_id`, `amount`, and `description`.""",
        database_id="db-banking",
        relevant_tables=["transactions"],
        table_schemas=[
            TableSchemaInfo(
                table_name="transactions",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="account_id", type="INTEGER"),
                    ColumnSchema(name="amount", type="DECIMAL(12,2)"),
                    ColumnSchema(name="description", type="VARCHAR(150)"),
                ],
            )
        ],
        sample_input_data={
            "transactions": [
                {"id": 1, "account_id": 1, "amount": 3500.00, "description": "Bi-weekly Payroll Deposit"},
                {"id": 2, "account_id": 2, "amount": 1200.00, "description": "Direct Deposit Corporate Transfer"},
                {"id": 3, "account_id": 3, "amount": 250.00, "description": "ATM Withdrawal"},
                {"id": 4, "account_id": 4, "amount": 500.00, "description": "Payroll Reimbursement"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["transaction_id", "account_id", "amount", "description"],
            sample_rows=[
                [1, 1, 3500.00, "Monthly Corporate Payroll"],
                [4, 2, 2800.00, "Direct Deposit - Tech Corp"],
            ],
            total_row_count=8,
        ),
        starter_code="-- Find (Payroll OR Direct Deposit) with amount >= 1,000\nSELECT \nFROM transactions\n",
        expected_solution="""SELECT 
    id AS transaction_id,
    account_id,
    amount,
    description
FROM transactions
WHERE (description LIKE '%Payroll%' OR description LIKE '%Direct Deposit%') 
  AND amount >= 1000.00;""",
        alternative_solution="""SELECT 
    t.id AS transaction_id,
    t.account_id,
    t.amount,
    t.description
FROM transactions t
WHERE (INSTR(t.description, 'Payroll') > 0 OR INSTR(t.description, 'Direct Deposit') > 0)
  AND t.amount >= 1000.00;""",
        hints=[
            "Wrap the OR pattern checks in parentheses: `(description LIKE '%Payroll%' OR description LIKE '%Direct Deposit%')`.",
            "Combine with `AND amount >= 1000.00`.",
        ],
        detailed_explanation="""Matching disparate keywords across natural language transaction descriptors requires disjunctive pattern matching.
Parenthesizing `(desc LIKE '%A%' OR desc LIKE '%B%')` ensures that the subsequent `AND amount >= 1000.00` filter applies to both patterns.""",
        related_concepts=["Disjunctive LIKE", "Operator Grouping", "Auditing"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-020-pub",
                name="Default Transactions",
                description="40 banking transactions.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-020-hid1",
                name="Hidden Test Case 1: Small Payroll Transaction",
                description="Payroll transaction under $1,000 (must be excluded).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date)
VALUES (999, 1, 'deposit', 50.00, 8500.00, 'Partial Payroll Adjustment', '2024-03-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q21: Multi-Department Role Pattern Matching (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-021",
        slug="cross-department-technical-staff-audit",
        title="Cross-Department Technical Specialist Identification",
        topic_id="top-03",
        topic="Logical Operators & Pattern Matching",
        difficulty="hard",
        problem_description="""Enterprise architecture is identifying technical specialists outside core Engineering:
1. `title` contains `'Engineer'` OR `'Architect'`.
2. The employee is NOT in the primary Engineering department (`department_id != 1` AND `department_id IS NOT NULL`).
3. The employee reports to a manager (`manager_id IS NOT NULL`).
4. `status = 'ACTIVE'`.
Write a query to retrieve `id` (as `employee_id`), `first_name`, `last_name`, `title`, `department_id`, and `manager_id`.""",
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
                    ColumnSchema(name="department_id", type="INTEGER"),
                    ColumnSchema(name="manager_id", type="INTEGER"),
                    ColumnSchema(name="status", type="VARCHAR(20)"),
                ],
            )
        ],
        sample_input_data={
            "employees": [
                {"id": 3, "first_name": "David", "title": "Staff Engineer", "department_id": 1, "manager_id": 2, "status": "ACTIVE"},
                {"id": 45, "first_name": "Leo", "title": "Data Platform Engineer", "department_id": 5, "manager_id": 10, "status": "ACTIVE"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["employee_id", "first_name", "last_name", "title", "department_id", "manager_id"],
            sample_rows=[
                [45, "Leo", "Fitz", "Data Platform Engineer", 5, 10],
            ],
            total_row_count=3,
        ),
        starter_code="-- Find (Engineer OR Architect) in non-engineering departments with manager\nSELECT \nFROM employees\n",
        expected_solution="""SELECT 
    id AS employee_id,
    first_name,
    last_name,
    title,
    department_id,
    manager_id
FROM employees
WHERE (title LIKE '%Engineer%' OR title LIKE '%Architect%')
  AND department_id != 1
  AND department_id IS NOT NULL
  AND manager_id IS NOT NULL
  AND status = 'ACTIVE';""",
        alternative_solution="""SELECT 
    e.id AS employee_id,
    e.first_name,
    e.last_name,
    e.title,
    e.department_id,
    e.manager_id
FROM employees e
WHERE (e.title LIKE '%Engineer%' OR e.title LIKE '%Architect%')
  AND e.department_id NOT IN (1)
  AND e.manager_id IS NOT NULL
  AND e.status = 'ACTIVE';""",
        hints=[
            "Group titles: `(title LIKE '%Engineer%' OR title LIKE '%Architect%')`.",
            "Remember that `department_id != 1` excludes NULLs in standard SQL, but explicitly testing `department_id IS NOT NULL` is best practice.",
            "Verify `manager_id IS NOT NULL` and `status = 'ACTIVE'`.",
        ],
        detailed_explanation="""Complex business rules require combining disjunctions, inequality filters, and null-checks.
Notice that `department_id != 1` in SQL three-valued logic discards NULL rows, because `NULL != 1` evaluates to UNKNOWN.
Adding `department_id IS NOT NULL` ensures defensive schema design against unexpected null semantics.""",
        related_concepts=["Defensive SQL", "Three-Valued Logic", "Complex Conjunctions"],
        order_matters=False,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-021-pub",
                name="Default Employees",
                description="Full company roster.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-021-hid1",
                name="Hidden Test Case 1: Inactive Architect",
                description="Inactive Solutions Architect (must be excluded).",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO employees (id, first_name, last_name, email, department_id, manager_id, title, hire_date, status)
VALUES (999, 'Inactive', 'Architect', 'inact@co.com', 2, 1, 'Marketing Solutions Architect', '2023-01-01', 'INACTIVE');""",
            ),
        ],
    ),
]
