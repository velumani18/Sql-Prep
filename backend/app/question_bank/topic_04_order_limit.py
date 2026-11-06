from typing import List
from app.engine.types import TestCase
from app.question_bank.models import (
    BankQuestion,
    ColumnSchema,
    TableSchemaInfo,
    ExpectedOutput,
)

TOPIC_04_QUESTIONS: List[BankQuestion] = [
    # -------------------------------------------------------------------------
    # Q22: Top-N Highest Values (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-022",
        slug="top-five-department-budgets",
        title="Top Five Department Budgets",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="easy",
        problem_description="""Corporate leadership requires a leaderboard of the 5 highest-budget departments.
Write a query to retrieve `name` and `budget` from `departments`, ordered by `budget` in descending order.
Limit the result to exactly 5 records.""",
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
                {"name": "Engineering", "budget": 1200000.00},
                {"name": "Sales", "budget": 600000.00},
                {"name": "Product", "budget": 500000.00},
                {"name": "Marketing", "budget": 450000.00},
                {"name": "Operations", "budget": 350000.00},
                {"name": "Human Resources", "budget": 250000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["name", "budget"],
            sample_rows=[
                ["Engineering", 1200000.00],
                ["Sales", 600000.00],
                ["Product", 500000.00],
                ["Marketing", 450000.00],
                ["Finance", 300000.00],
            ],
            total_row_count=5,
        ),
        starter_code="-- Top 5 departments by budget DESC\nSELECT \nFROM departments\n",
        expected_solution="""SELECT name, budget
FROM departments
ORDER BY budget DESC
LIMIT 5;""",
        alternative_solution="""SELECT d.name, d.budget
FROM departments d
ORDER BY d.budget DESC
FETCH FIRST 5 ROWS ONLY;""",
        hints=[
            "Use `ORDER BY budget DESC` to place highest amounts first.",
            "Use `LIMIT 5` to restrict the output to 5 rows.",
        ],
        detailed_explanation="""The `ORDER BY` clause determines the physical sequence of rows returned.
When combined with `LIMIT N`, modern relational engines can employ a bounded Top-N Heap Sort algorithm,
requiring only $O(N \\log K)$ memory without sorting the entire dataset.""",
        related_concepts=["ORDER BY", "LIMIT", "Top-N Sort", "DESC"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-022-pub",
                name="Default Departments",
                description="7 standard departments.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-022-hid1",
                name="Hidden Test Case 1: Massive Infrastructure Budget",
                description="Infrastructure department with $5M budget takes #1 spot.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO departments (id, name, budget, location)
VALUES (99, 'Global Infrastructure', 5000000.00, 'Virginia');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q23: Multi-Column Sorting Hierarchy (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-023",
        slug="product-category-pricing-hierarchy",
        title="Product Catalog Categorical Price Sorting",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="easy",
        problem_description="""Online storefront merchandising needs products sorted in a clean hierarchical layout:
First by `category_id` in ascending order (`ASC`), and within each category, by `price` in descending order (`DESC`).
Return `id` (as `product_id`), `name` (as `product_name`), `category_id`, and `price`.""",
        database_id="db-ecommerce",
        relevant_tables=["products"],
        table_schemas=[
            TableSchemaInfo(
                table_name="products",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="name", type="VARCHAR(150)"),
                    ColumnSchema(name="category_id", type="INTEGER"),
                    ColumnSchema(name="price", type="DECIMAL(10,2)"),
                ],
            )
        ],
        sample_input_data={
            "products": [
                {"id": 1, "name": "Mouse", "category_id": 1, "price": 49.99},
                {"id": 2, "name": "Keyboard", "category_id": 1, "price": 129.99},
                {"id": 6, "name": "Coffee Maker", "category_id": 2, "price": 89.99},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["product_id", "product_name", "category_id", "price"],
            sample_rows=[
                [4, "Ultra HD 4K Monitor 27-inch", 1, 399.99],
                [5, "Wireless Noise-Canceling Headphones", 1, 299.99],
                [2, "Mechanical RGB Keyboard", 1, 129.99],
                [1, "Wireless Ergonomic Mouse", 1, 49.99],
                [3, "USB-C Multi-Port Hub", 1, 39.99],
            ],
            total_row_count=20,
        ),
        starter_code="-- Sort by category_id ASC, then price DESC\nSELECT \nFROM products\n",
        expected_solution="""SELECT 
    id AS product_id,
    name AS product_name,
    category_id,
    price
FROM products
ORDER BY category_id ASC, price DESC;""",
        alternative_solution="""SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.category_id,
    p.price
FROM products p
ORDER BY 3 ASC, 4 DESC;""",
        hints=[
            "Specify multiple columns in the ORDER BY clause: `ORDER BY category_id ASC, price DESC`.",
            "Verify column aliases match `product_id` and `product_name`.",
        ],
        detailed_explanation="""SQL allows multi-column sorting. The query engine first sorts by the primary column (`category_id`).
Whenever rows have identical values for the primary column, it breaks ties using the secondary column (`price DESC`).
A composite index on `(category_id ASC, price DESC)` can satisfy this sort order with zero additional sorting cost.""",
        related_concepts=["Multi-Column Sort", "Hierarchical Ordering", "Composite Index Sorting"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-023-pub",
                name="Default Products",
                description="20 products across categories.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-023-hid1",
                name="Hidden Test Case 1: Luxury Audio Product",
                description="New $999 item in Category 1.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, 'Audiophile Reference Headphones', 999.99, 10, 1);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q24: Smallest Balance Pagination (Easy)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-024",
        slug="lowest-balance-accounts",
        title="Lowest Active Balance Accounts",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="easy",
        problem_description="""Account managers want to proactively contact customers with low but positive account balances.
Write a query to retrieve the 5 accounts with the lowest non-zero balances (`balance > 0`).
Order by `balance` in ascending order (`ASC`).
Return `id` (as `account_id`), `account_type`, and `balance`.""",
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
                {"id": 3, "account_type": "Checking", "balance": 1250.00},
                {"id": 7, "account_type": "Checking", "balance": 850.50},
                {"id": 10, "account_type": "Savings", "balance": 450.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["account_id", "account_type", "balance"],
            sample_rows=[
                [10, "Savings", 450.00],
                [7, "Checking", 850.50],
                [3, "Checking", 1250.00],
            ],
            total_row_count=5,
        ),
        starter_code="-- Lowest 5 accounts with balance > 0\nSELECT \nFROM accounts\n",
        expected_solution="""SELECT 
    id AS account_id,
    account_type,
    balance
FROM accounts
WHERE balance > 0
ORDER BY balance ASC
LIMIT 5;""",
        alternative_solution="""SELECT 
    a.id AS account_id,
    a.account_type,
    a.balance
FROM accounts a
WHERE a.balance > 0.00
ORDER BY a.balance
LIMIT 5 OFFSET 0;""",
        hints=[
            "Filter positive balances: `WHERE balance > 0`.",
            "Order from lowest to highest: `ORDER BY balance ASC`.",
            "Limit output: `LIMIT 5`.",
        ],
        detailed_explanation="""Ascending order (`ASC`) is the default sorting direction in SQL if neither `ASC` nor `DESC` is specified.
Filtering before sorting (`WHERE balance > 0`) is vital because the WHERE filter narrows the dataset
before the sorting step executes.""",
        related_concepts=["ASC", "LIMIT", "Filtering before Sorting"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-024-pub",
                name="Default Accounts",
                description="35 banking accounts.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-024-hid1",
                name="Hidden Test Case 1: Minimum Balance Account",
                description="Account with $5.00 balance.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date)
VALUES (999, 1, 1, 'MIN-001', 'Checking', 5.00, 'active', '2024-01-01');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q25: Second-Highest Value with OFFSET (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-025",
        slug="second-highest-department-budget",
        title="Second Highest Department Budget",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="medium",
        problem_description="""A classic SQL interview question:
Find the department with the 2nd highest budget.
Use `ORDER BY` and `LIMIT` with `OFFSET` to return the second-place department.
Return `name` and `budget`.""",
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
                {"name": "Engineering", "budget": 1200000.00},
                {"name": "Sales", "budget": 600000.00},
                {"name": "Product", "budget": 500000.00},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["name", "budget"],
            sample_rows=[
                ["Sales", 600000.00],
            ],
            total_row_count=1,
        ),
        starter_code="-- Second highest budget using LIMIT and OFFSET\nSELECT \nFROM departments\n",
        expected_solution="""SELECT name, budget
FROM departments
ORDER BY budget DESC
LIMIT 1 OFFSET 1;""",
        alternative_solution="""SELECT name, budget
FROM departments
WHERE budget = (
    SELECT MAX(budget)
    FROM departments
    WHERE budget < (SELECT MAX(budget) FROM departments)
);""",
        hints=[
            "Order by budget in descending order: `ORDER BY budget DESC`.",
            "Skip the first row and take the next row: `LIMIT 1 OFFSET 1`.",
        ],
        detailed_explanation="""The `OFFSET M` clause skips the first $M$ rows of the sorted result set,
and `LIMIT N` takes the next $N$ rows.
Therefore, `ORDER BY budget DESC LIMIT 1 OFFSET 1` skips the single highest budget and returns the second highest.
While convenient, for production datasets with potential duplicate ties, window functions (`DENSE_RANK()`) are often preferred.""",
        related_concepts=["OFFSET", "LIMIT OFFSET", "Nth Highest Value", "Top-N Patterns"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-025-pub",
                name="Default Departments",
                description="Engineering is 1st ($1.2M), Sales is 2nd ($600K).",
                is_hidden=False,
            ),
            TestCase(
                id="tc-025-hid1",
                name="Hidden Test Case 1: New #1 Budget",
                description="New $2M department pushes Engineering to 2nd place.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO departments (id, name, budget, location)
VALUES (99, 'Quantum Labs', 2000000.00, 'Cambridge');""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q26: Deterministic Secondary Sorting (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-026",
        slug="faculty-roster-hierarchical-seniority",
        title="Faculty Roster Hierarchical Seniority Sorting",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="medium",
        problem_description="""The academic catalog orders faculty by rank and seniority:
1. `title` in alphabetical order (`ASC`).
2. For professors sharing the same title, order by `hired_year` in ascending order (`ASC`) (earliest hires first).
3. To break any remaining ties, sort by `id` ASC.
Return `id` (as `professor_id`), `first_name`, `last_name`, `title`, and `hired_year`.""",
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
                {"id": 4, "first_name": "Ada", "title": "Assistant Professor", "hired_year": 2020},
                {"id": 2, "first_name": "Grace", "title": "Associate Professor", "hired_year": 2015},
                {"id": 1, "first_name": "Alan", "title": "Professor", "hired_year": 2012},
                {"id": 3, "first_name": "Carl", "title": "Professor", "hired_year": 2010},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["professor_id", "first_name", "last_name", "title", "hired_year"],
            sample_rows=[
                [4, "Ada", "Lovelace", "Assistant Professor", 2020],
                [2, "Grace", "Hopper", "Associate Professor", 2015],
                [3, "Carl Friedrich", "Gauss", "Professor", 2010],
                [1, "Alan", "Turing", "Professor", 2012],
            ],
            total_row_count=8,
        ),
        starter_code="-- Deterministic multi-tier sort: title ASC, hired_year ASC, id ASC\nSELECT \nFROM professors\n",
        expected_solution="""SELECT 
    id AS professor_id,
    first_name,
    last_name,
    title,
    hired_year
FROM professors
ORDER BY title ASC, hired_year ASC, id ASC;""",
        alternative_solution="""SELECT 
    p.id AS professor_id,
    p.first_name,
    p.last_name,
    p.title,
    p.hired_year
FROM professors p
ORDER BY p.title, p.hired_year, p.id;""",
        hints=[
            "List all three sorting keys in order: `ORDER BY title ASC, hired_year ASC, id ASC`.",
            "Alias `id` as `professor_id`.",
        ],
        detailed_explanation="""Deterministic ordering is vital when presenting paginated user interfaces.
If a query lacks a unique tie-breaker (such as primary key `id ASC`), the database engine is free to return
tied rows in arbitrary order between query runs, causing rows to disappear or duplicate across pages.""",
        related_concepts=["Deterministic Sorting", "Tie-Breaking", "Stable Results"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-026-pub",
                name="Default Faculty",
                description="8 professors sorted by rank, year, id.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-026-hid1",
                name="Hidden Test Case 1: Peer Professor",
                description="Professor hired in same year 2010.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO professors (id, first_name, last_name, email, department_id, title, hired_year)
VALUES (999, 'Bernhard', 'Riemann', 'riemann@univ.edu', 2, 'Professor', 2010);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q27: Pagination Page 2 Simulation (Medium)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-027",
        slug="ecommerce-catalog-pagination-page-two",
        title="E-Commerce Catalog Pagination (Page 2)",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="medium",
        problem_description="""Web API endpoints serve product listings using page-based pagination.
Assume a page size of 5 products per page.
Write a query to retrieve **Page 2** (items 6 through 10) of the product catalog.
Order products by `price` descending (`DESC`), and break ties by `id` ascending (`ASC`).
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
                {"id": 4, "name": "Ultra HD Monitor", "price": 399.99},
                {"id": 5, "name": "Headphones", "price": 299.99},
                {"id": 2, "name": "Keyboard", "price": 129.99},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["product_id", "product_name", "price"],
            sample_rows=[
                [5, "Wireless Noise-Canceling Headphones", 299.99],
                [10, "Smart Home Security Camera", 179.99],
                [2, "Mechanical RGB Keyboard", 129.99],
                [7, "Air Purifier HEPA Filter", 119.99],
                [6, "Drip Coffee Maker", 89.99],
            ],
            total_row_count=5,
        ),
        starter_code="-- Page 2: Limit 5, Offset 5 ordered by price DESC, id ASC\nSELECT \nFROM products\n",
        expected_solution="""SELECT 
    id AS product_id,
    name AS product_name,
    price
FROM products
ORDER BY price DESC, id ASC
LIMIT 5 OFFSET 5;""",
        alternative_solution="""SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.price
FROM products p
ORDER BY p.price DESC, p.id ASC
LIMIT 5, 5;""",
        hints=[
            "For Page 2 with page size 5, the offset is `(page - 1) * pageSize = (2 - 1) * 5 = 5`.",
            "Write `LIMIT 5 OFFSET 5`.",
            "Order by `price DESC, id ASC`.",
        ],
        detailed_explanation="""In standard page-based pagination architectures:
`LIMIT = page_size` and `OFFSET = (page_number - 1) * page_size`.
For Page 2 with 5 items per page: `LIMIT 5 OFFSET 5`.
For large production tables ($N > 1,000,000$), offset-based pagination can become slow because the engine must still scan and discard the initial 5 rows; keyset pagination (`WHERE id < last_seen_id`) is used for extreme scale.""",
        related_concepts=["Pagination Formula", "LIMIT OFFSET", "Keyset Pagination Alternatives"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-027-pub",
                name="Default Products",
                description="20 products, page 2 items 6-10.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-027-hid1",
                name="Hidden Test Case 1: High Priced TV Insert",
                description="New $2,000 product alters page boundaries.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO products (id, category_id, name, price, stock_quantity, is_active)
VALUES (999, 1, '85-inch OLED Cinema Display', 2499.99, 5, 1);""",
            ),
        ],
    ),

    # -------------------------------------------------------------------------
    # Q28: Deterministic Tie-Breaking Financial Auditing (Hard)
    # -------------------------------------------------------------------------
    BankQuestion(
        id="q-028",
        slug="highest-value-transactions-tie-break",
        title="Highest-Value Transaction Audit with Deterministic Tie-Breaking",
        topic_id="top-04",
        topic="ORDER BY, LIMIT, and Pagination",
        difficulty="hard",
        problem_description="""Banking anti-fraud systems audit the top 3 largest transactions in the ledger.
To guarantee audit repeatability across distributed replicas, sorting must be strictly deterministic:
1. `amount` descending (`DESC`).
2. If amounts are equal, by `transaction_date` descending (`DESC`).
3. If dates are also equal, by `id` ascending (`ASC`).
Retrieve the top 3 matching transactions.
Return `id` (as `transaction_id`), `account_id`, `amount`, `transaction_date`, and `description`.""",
        database_id="db-banking",
        relevant_tables=["transactions"],
        table_schemas=[
            TableSchemaInfo(
                table_name="transactions",
                columns=[
                    ColumnSchema(name="id", type="INTEGER", is_primary_key=True),
                    ColumnSchema(name="account_id", type="INTEGER"),
                    ColumnSchema(name="amount", type="DECIMAL(12,2)"),
                    ColumnSchema(name="transaction_date", type="DATE"),
                    ColumnSchema(name="description", type="VARCHAR(150)"),
                ],
            )
        ],
        sample_input_data={
            "transactions": [
                {"id": 34, "account_id": 15, "amount": 6200.00, "transaction_date": "2024-03-01"},
                {"id": 14, "account_id": 5, "amount": 5400.00, "transaction_date": "2024-02-18"},
                {"id": 31, "account_id": 14, "amount": 4800.00, "transaction_date": "2024-02-28"},
            ]
        },
        expected_output=ExpectedOutput(
            columns=["transaction_id", "account_id", "amount", "transaction_date", "description"],
            sample_rows=[
                [34, 15, 6200.00, "2024-03-01", "Investment Liquidation Transfer"],
                [14, 5, 5400.00, "2024-02-18", "Commercial Invoice Settlement"],
                [31, 14, 4800.00, "2024-02-28", "Treasury Bond Interest"],
            ],
            total_row_count=3,
        ),
        starter_code="-- Top 3 transactions: amount DESC, transaction_date DESC, id ASC\nSELECT \nFROM transactions\n",
        expected_solution="""SELECT 
    id AS transaction_id,
    account_id,
    amount,
    transaction_date,
    description
FROM transactions
ORDER BY amount DESC, transaction_date DESC, id ASC
LIMIT 3;""",
        alternative_solution="""SELECT 
    t.id AS transaction_id,
    t.account_id,
    t.amount,
    t.transaction_date,
    t.description
FROM transactions t
ORDER BY t.amount DESC, t.transaction_date DESC, t.id ASC
LIMIT 3 OFFSET 0;""",
        hints=[
            "Combine all three sorting conditions: `ORDER BY amount DESC, transaction_date DESC, id ASC`.",
            "Limit to 3 rows.",
        ],
        detailed_explanation="""In financial systems, regulatory audits require exact reproducibility.
Without the tie-breaker `id ASC`, if two transactions have identical amounts and dates,
the database could order them non-deterministically based on internal disk page layout or concurrency states.
Adding the unique primary key as the final tie-breaker guarantees a canonical total ordering.""",
        related_concepts=["Canonical Total Ordering", "Auditing", "Deterministic Pagination"],
        order_matters=True,
        check_column_names=True,
        test_cases=[
            TestCase(
                id="tc-028-pub",
                name="Default Transactions",
                description="40 transactions in ledger.",
                is_hidden=False,
            ),
            TestCase(
                id="tc-028-hid1",
                name="Hidden Test Case 1: Tied High Value Transaction",
                description="Transaction tied at $6,200 but earlier date.",
                is_hidden=True,
                custom_seed_dml="""INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date)
VALUES (999, 1, 'deposit', 6200.00, 20000.00, 'Legacy Wire', '2024-01-01');""",
            ),
        ],
    ),
]
