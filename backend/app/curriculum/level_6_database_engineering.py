from typing import List
from app.curriculum.models import (
    TopicLesson,
    ClauseExplanation,
    WorkedExample,
    CommonMistake,
    PracticeQuestion,
)

LEVEL_6_LESSONS: List[TopicLesson] = [
    # =========================================================================
    # Topic 1: DDL & Schema Constraints
    # =========================================================================
    TopicLesson(
        id="les-6-1",
        slug="ddl-and-schema-constraints",
        level_number=6,
        level_title="Level 6: Database Engineering & Architecture",
        title="Data Definition Language (DDL) & Schema Constraints",
        order_index=1,
        database_id="db-company",
        database_name="company_db",
        learning_objectives=[
            "Understand the DDL lifecycle: CREATE, ALTER, and DROP table definitions.",
            "Master table and column-level constraints: PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK, and DEFAULT.",
            "Understand referential integrity actions: ON DELETE CASCADE, ON DELETE SET NULL, and RESTRICT.",
            "Learn how to introspect database metadata and schema definitions using sqlite_master / system catalogs.",
        ],
        prerequisites=[
            "Level 1: Fundamentals, Level 2: Aggregations, and Level 3: Joins & Foreign Keys.",
        ],
        detailed_explanation="""Data Definition Language (DDL) comprises the SQL statements that define, modify, and drop database structures such as schemas, tables, columns, indexes, and constraints. Unlike Data Manipulation Language (DML) which operates on row values, DDL shapes the relational schema itself.

Core DDL Operations:
1. `CREATE TABLE`: Defines a new relation, specifying column names, data types, and declarative constraints.
2. `ALTER TABLE`: Modifies an existing table's schema (e.g. adding columns, renaming tables/columns, adding constraints).
3. `DROP TABLE`: Permanently removes a table structure and all stored records from the database catalog.

Declarative Constraints:
Relational databases enforce data integrity at the database layer using declarative constraints:
- `PRIMARY KEY`: Uniquely identifies each row in a relation. Combines NOT NULL and UNIQUE guarantees. Can be single-column or composite.
- `FOREIGN KEY`: Enforces referential integrity by requiring that a value in the child table references an existing key in the parent table.
  - `ON DELETE RESTRICT / NO ACTION`: Prevents deletion of the parent row if child rows reference it.
  - `ON DELETE CASCADE`: Automatically deletes child rows when the referenced parent row is deleted.
  - `ON DELETE SET NULL`: Sets the child table foreign key column to NULL when the parent row is deleted.
- `UNIQUE`: Guarantees that all values in a column or set of columns are distinct (allowing at most one NULL in standard SQL, though SQLite allows multiple NULLs in UNIQUE columns).
- `NOT NULL`: Rejects any attempt to insert or update a row with a NULL value in the specified column.
- `CHECK`: Evaluates a Boolean expression before inserting or modifying a row (e.g. `CHECK (budget > 0)` or `CHECK (salary >= 30000)`).
- `DEFAULT`: Provides a fallback value when an INSERT statement does not specify a value for the column.

System Metadata Introspection:
Relational engines maintain internal system catalogs storing table definitions. In SQLite, table metadata and SQL definitions are queryable via `sqlite_master` (or `sqlite_schema` in modern versions):
```sql
SELECT type, name, tbl_name, sql 
FROM sqlite_master 
WHERE type = 'table' AND name NOT LIKE 'sqlite_%';
```""",
        syntax_reference="""CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    budget DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (budget >= 0)
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department_id INTEGER,
    CONSTRAINT fk_dept FOREIGN KEY (department_id) 
        REFERENCES departments(id) 
        ON DELETE SET NULL
);""",
        clause_breakdown=[
            ClauseExplanation(keyword="PRIMARY KEY", purpose="Designates the unique, non-null identifier for rows in the relation.", notes="Creates a unique index automatically."),
            ClauseExplanation(keyword="FOREIGN KEY", purpose="Links a column to a primary or unique key in another table, enforcing referential integrity.", notes="Configurable with ON DELETE and ON UPDATE actions."),
            ClauseExplanation(keyword="CHECK", purpose="Enforces custom domain validation rules using arbitrary boolean expressions.", notes="Evaluated on every INSERT and UPDATE operation."),
            ClauseExplanation(keyword="UNIQUE", purpose="Ensures all non-null values across specified column(s) are distinct.", notes="Can be applied to single columns or composite column tuples."),
            ClauseExplanation(keyword="DEFAULT", purpose="Specifies a literal or expression to populate when no explicit value is supplied on insert.", notes="e.g. DEFAULT CURRENT_TIMESTAMP or DEFAULT 0.00."),
        ],
        worked_examples=[
            WorkedExample(
                title="Introspecting Database Tables via sqlite_master Catalog",
                explanation="Querying the system catalog to list all user-defined relational tables and their creation DDL statements.",
                sql="""SELECT name, type, sql
FROM sqlite_master
WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
ORDER BY name;""",
                columns=["name", "type", "sql"],
                rows=[
                    ["departments", "table", "CREATE TABLE departments (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    name VARCHAR(100) NOT NULL UNIQUE,\n    code VARCHAR(10) NOT NULL UNIQUE,\n    budget DECIMAL(12, 2) NOT NULL DEFAULT 0.00,\n    location VARCHAR(100)\n)"],
                    ["employee_projects", "table", "CREATE TABLE employee_projects (\n    employee_id INTEGER NOT NULL,\n    project_id INTEGER NOT NULL,\n    assigned_date DATE NOT NULL,\n    hours_allocated DECIMAL(5, 2) DEFAULT 0.00,\n    role VARCHAR(50),\n    PRIMARY KEY (employee_id, project_id),\n    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,\n    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE\n)"],
                    ["employees", "table", "CREATE TABLE employees (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    first_name VARCHAR(50) NOT NULL,\n    last_name VARCHAR(50) NOT NULL,\n    email VARCHAR(100) NOT NULL UNIQUE,\n    department_id INTEGER,\n    manager_id INTEGER,\n    job_title VARCHAR(100) NOT NULL,\n    hire_date DATE NOT NULL,\n    is_active BOOLEAN NOT NULL DEFAULT 1,\n    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,\n    FOREIGN KEY (manager_id) REFERENCES employees(id) ON DELETE SET NULL\n)"],
                    ["managers", "table", "CREATE TABLE managers (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    employee_id INTEGER NOT NULL UNIQUE,\n    department_id INTEGER NOT NULL,\n    management_level VARCHAR(50) NOT NULL,\n    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,\n    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE\n)"],
                    ["projects", "table", "CREATE TABLE projects (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    name VARCHAR(100) NOT NULL,\n    department_id INTEGER NOT NULL,\n    start_date DATE NOT NULL,\n    end_date DATE,\n    budget DECIMAL(12, 2) NOT NULL DEFAULT 0.00,\n    status VARCHAR(20) NOT NULL DEFAULT 'Planned',\n    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE\n)"],
                    ["salaries", "table", "CREATE TABLE salaries (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    employee_id INTEGER NOT NULL UNIQUE,\n    base_salary DECIMAL(10, 2) NOT NULL,\n    bonus DECIMAL(10, 2) DEFAULT 0.00,\n    effective_date DATE NOT NULL,\n    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE\n)"],
                ],
            ),
            WorkedExample(
                title="Auditing Foreign Key Integrity: Finding Employees Without Valid Departments",
                explanation="Referential integrity ensures child records link to valid parents. In real-world schemas, NULL foreign keys may represent unassigned or orphaned entities.",
                sql="""SELECT 
    e.id AS employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    e.job_title,
    e.department_id
FROM employees e
WHERE e.department_id IS NULL;""",
                columns=["employee_id", "employee_name", "job_title", "department_id"],
                rows=[
                    [56, "Grace Hopper", "Chief Research Advisor", None],
                    [57, "Linus Torvalds", "Distinguished Architect", None],
                    [58, "Ada Lovelace", "Senior Algorithmic Consultant", None],
                    [59, "Ken Thompson", "Systems Fellow", None],
                    [60, "Dennis Ritchie", "Language Infrastructure Fellow", None],
                ],
            ),
            WorkedExample(
                title="Detecting Constraint Violation Candidates: Budget Allocation Audits",
                explanation="Before applying a CHECK constraint like (budget > 100000), engineers query existing data to detect any records that would violate the constraint.",
                sql="""SELECT 
    id AS project_id,
    name AS project_name,
    budget,
    status
FROM projects
WHERE budget < 50000.00
ORDER BY budget ASC;""",
                columns=["project_id", "project_name", "budget", "status"],
                rows=[
                    [7, "Internal Wiki Migration", 25000.00, "Completed"],
                    [10, "Developer Tooling Upgrade", 35000.00, "In Progress"],
                    [4, "Employee Portal Redesign", 45000.00, "Completed"],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Forgetting ON DELETE CASCADE when defining foreign keys on dependent child junction tables.",
                explanation="Without ON DELETE CASCADE or ON DELETE SET NULL, deleting a parent row fails with a foreign key constraint violation (FOREIGN KEY constraint failed) if child rows exist.",
                incorrect_sql="""-- Child junction table without cascade
CREATE TABLE employee_projects (
    employee_id INTEGER,
    project_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employees(id) -- Deleting employee will throw foreign key error!
);""",
                corrected_sql="""CREATE TABLE employee_projects (
    employee_id INTEGER,
    project_id INTEGER,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);""",
            ),
            CommonMistake(
                pitfall="Relying on application-level validation instead of database-level constraints.",
                explanation="Validating constraints only in backend code allows corrupt data to enter when batch scripts, manual migrations, or other microservices write directly to the database.",
                incorrect_sql="-- Relying solely on python/backend 'if budget < 0: raise Error'",
                corrected_sql="ALTER TABLE departments ADD CONSTRAINT chk_budget CHECK (budget >= 0);",
            ),
        ],
        real_world_use_cases=[
            "Data migration scripts: Auditing existing schemas and data before enforcing NOT NULL or UNIQUE constraints.",
            "Multi-tenant SaaS architectures: Using composite primary keys (tenant_id, id) to enforce strict isolation.",
            "Database lifecycle tracking: Querying sqlite_master/information_schema in automated CI/CD schema verification pipelines.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="p-6-1",
                slug="audit-unassigned-department-employees",
                title="Audit Employees with Unassigned Departments",
                difficulty="easy",
                prompt="Write a query to return all employees who do not belong to any department (`department_id IS NULL`). Return `id`, `first_name`, `last_name`, and `job_title`, ordered by `id` ASC.",
                starter_sql="-- Find employees without a department assignment\nSELECT \nFROM employees\n",
                solution_sql="""SELECT id, first_name, last_name, job_title
FROM employees
WHERE department_id IS NULL
ORDER BY id ASC;""",
                hints=[
                    "Check for NULL values using 'WHERE department_id IS NULL'.",
                    "Order the results by id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-2",
                slug="identify-duplicate-emails-audit",
                title="Candidate Audit: Check for Duplicate Email Addresses",
                difficulty="medium",
                prompt="Before adding a UNIQUE constraint on a column, engineers must verify there are no duplicate values. Write a query to check if any email appears more than once in `employees`. Return `email` and the occurrence `count`. If no duplicates exist, the result will be empty.",
                starter_sql="-- Audit employees for duplicate emails\nSELECT \nFROM employees\n",
                solution_sql="""SELECT email, COUNT(*) AS count
FROM employees
GROUP BY email
HAVING COUNT(*) > 1;""",
                hints=[
                    "Group by email and filter groups using 'HAVING COUNT(*) > 1'.",
                    "Because our synthetic data is clean and valid, an empty result confirms no violations exist!",
                ],
                order_matters=False,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-3",
                slug="detect-low-budget-projects",
                title="Identify Projects Violating Proposed Minimum Budget",
                difficulty="easy",
                prompt="Management plans to introduce a CHECK constraint requiring all active or in-progress projects to have a budget of at least $60,000. Write a query to find all projects with `status = 'In Progress'` and `budget < 60000.00`. Return `id`, `name`, `budget`, and `status`, sorted by `budget` ASC.",
                starter_sql="-- Find in-progress projects with budget under 60,000\nSELECT \nFROM projects\n",
                solution_sql="""SELECT id, name, budget, status
FROM projects
WHERE status = 'In Progress' AND budget < 60000.00
ORDER BY budget ASC;""",
                hints=[
                    "Filter with 'WHERE status = ''In Progress'' AND budget < 60000.00'.",
                    "Sort by budget ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-4",
                slug="inspect-sqlite-schema-tables",
                title="Catalog Inspection: List All User Tables",
                difficulty="easy",
                prompt="Write a query against `sqlite_master` to retrieve the `name` of all user-created tables (where `type = 'table'` and `name NOT LIKE 'sqlite_%'`). Order the results alphabetically by `name` ASC.",
                starter_sql="-- Inspect sqlite_master for user tables\nSELECT \nFROM sqlite_master\n",
                solution_sql="""SELECT name
FROM sqlite_master
WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
ORDER BY name ASC;""",
                hints=[
                    "Query the 'sqlite_master' catalog.",
                    "Filter with \"type = 'table' AND name NOT LIKE 'sqlite_%'\".",
                    "Order by name ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-5",
                slug="verify-department-budget-non-negative",
                title="Audit Department Budgets Against Non-Negative Check",
                difficulty="medium",
                prompt="Write a query to verify whether all departments adhere to a non-negative budget constraint. Return `name`, `code`, and `budget` for any department where `budget <= 0` or `budget IS NULL`. If all departments have positive budgets, return an empty result.",
                starter_sql="-- Audit department budgets\nSELECT \nFROM departments\n",
                solution_sql="""SELECT name, code, budget
FROM departments
WHERE budget <= 0 OR budget IS NULL;""",
                hints=[
                    "Filter with 'WHERE budget <= 0 OR budget IS NULL'.",
                ],
                order_matters=False,
                check_column_names=True,
            ),
        ],
    ),

    # =========================================================================
    # Topic 2: DML & ACID Transactions
    # =========================================================================
    TopicLesson(
        id="les-6-2",
        slug="dml-and-acid-transactions",
        level_number=6,
        level_title="Level 6: Database Engineering & Architecture",
        title="Data Manipulation Language (DML) & ACID Transactions",
        order_index=2,
        database_id="db-banking",
        database_name="banking_db",
        learning_objectives=[
            "Understand the core DML operations: INSERT, UPDATE, DELETE, and UPSERT (ON CONFLICT).",
            "Master the four pillars of ACID: Atomicity, Consistency, Isolation, and Durability.",
            "Understand transaction control statements: BEGIN TRANSACTION, COMMIT, and ROLLBACK.",
            "Analyze concurrency phenomena: Dirty Reads, Non-Repeatable Reads, and Phantom Reads across SQL Isolation Levels.",
        ],
        prerequisites=[
            "Level 1: Fundamentals, Level 2: Aggregations, and Level 6 Topic 1: DDL & Constraints.",
        ],
        detailed_explanation="""Data Manipulation Language (DML) provides the constructs to modify row-level data stored inside database relations:
- `INSERT INTO`: Adds new tuples to a relation.
- `UPDATE`: Modifies existing column values based on predicate filters.
- `DELETE`: Removes tuples matching predicate criteria.
- `UPSERT` (`INSERT INTO ... ON CONFLICT DO UPDATE`): Atomically inserts a record or updates existing values if a primary key or unique constraint conflict occurs.

The ACID Properties:
A database transaction is an atomic unit of work comprising one or more SQL operations. Relational database engines guarantee data integrity via the four ACID properties:

1. **Atomicity (All-or-Nothing)**:
Every statement in a transaction succeeds, or the entire transaction is rolled back. If a system failure or constraint violation occurs halfway through a multi-step money transfer, no partial writes persist:
```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE id = 101;
UPDATE accounts SET balance = balance + 500 WHERE id = 102;
COMMIT; -- If either update fails, ROLLBACK restores both balances!
```

2. **Consistency (Preserving Invariants)**:
A transaction transitions the database from one valid state to another valid state, satisfying all declared schema constraints, foreign keys, triggers, and business invariants.

3. **Isolation (Concurrent Execution Safety)**:
Transactions executing concurrently appear to execute serially without mutual interference. Without proper isolation, concurrent transactions experience read phenomena:
- **Dirty Read**: Transaction A reads uncommitted changes made by Transaction B. If B aborts and rolls back, A processed phantom data that never existed.
- **Non-Repeatable (Fuzzy) Read**: Transaction A reads a row, Transaction B modifies or deletes that row and commits, then Transaction A rereads the same row and sees different values.
- **Phantom Read**: Transaction A queries a range of rows (e.g. `WHERE balance > 1000`), Transaction B inserts a new row satisfying the predicate and commits, then Transaction A repeats the query and discovers a new "phantom" row.

ANSI SQL Isolation Levels:
| Isolation Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads |
| :--- | :---: | :---: | :---: |
| **READ UNCOMMITTED** | Permitted | Permitted | Permitted |
| **READ COMMITTED** | Prevented | Permitted | Permitted |
| **REPEATABLE READ** | Prevented | Prevented | Permitted |
| **SERIALIZABLE** | Prevented | Prevented | Prevented |

4. **Durability (Fault-Tolerant Persistence)**:
Once a transaction is committed, its modifications survive crashes, power outages, and system restarts, guaranteed via Write-Ahead Logging (WAL).""",
        syntax_reference="""-- Transaction Control
BEGIN TRANSACTION;

-- DML Operations
INSERT INTO transactions (account_id, transaction_type, amount, transaction_date, description)
VALUES (1, 'deposit', 1500.00, CURRENT_DATE, 'Direct payroll deposit');

UPDATE accounts 
SET balance = balance + 1500.00 
WHERE id = 1;

COMMIT; -- or ROLLBACK; on failure

-- Upsert Pattern (SQLite / PostgreSQL)
INSERT INTO customer_stats (customer_id, login_count)
VALUES (42, 1)
ON CONFLICT (customer_id) 
DO UPDATE SET login_count = customer_stats.login_count + 1;""",
        clause_breakdown=[
            ClauseExplanation(keyword="BEGIN TRANSACTION", purpose="Marks the boundary where atomic operations commence.", notes="Subsequent DML statements are isolated until commit or rollback."),
            ClauseExplanation(keyword="COMMIT", purpose="Persists all modifications made during the transaction to permanent storage.", notes="Releases transaction locks."),
            ClauseExplanation(keyword="ROLLBACK", purpose="Aborts the transaction and reverts all changes back to the pre-transaction state.", notes="Essential for error handling and fault recovery."),
            ClauseExplanation(keyword="ON CONFLICT", purpose="Specifies conflict resolution when an INSERT violates a UNIQUE or PRIMARY KEY constraint.", notes="Allows DO UPDATE (upsert) or DO NOTHING."),
        ],
        worked_examples=[
            WorkedExample(
                title="Ledger Consistency Audit: Account Balance vs Recorded Transactions",
                explanation="In banking systems, an account balance must be auditable against the net sum of all historical deposits and withdrawals.",
                sql="""SELECT 
    a.id AS account_id,
    a.account_type,
    a.balance AS current_balance,
    COALESCE(SUM(CASE 
        WHEN t.transaction_type = 'deposit' THEN t.amount 
        WHEN t.transaction_type = 'transfer_in' THEN t.amount 
        WHEN t.transaction_type IN ('withdrawal', 'transfer_out') THEN -t.amount 
        ELSE 0 
    END), 0.00) AS net_transactions
FROM accounts a
LEFT JOIN transactions t ON a.id = t.account_id
WHERE a.id <= 5
GROUP BY a.id, a.account_type, a.balance
ORDER BY a.id ASC;""",
                columns=["account_id", "account_type", "current_balance", "net_transactions"],
                rows=[
                    [1, "Checking", 8450.25, 3450.25],
                    [2, "Savings", 24150.80, 4150.80],
                    [3, "Checking", 1250.00, 250.00],
                    [4, "Savings", 45800.50, 5800.50],
                    [5, "Business", 112400.00, 12400.00],
                ],
            ),
            WorkedExample(
                title="Branch Solvency Ratio: Loan Exposure vs Liquid Account Deposits",
                explanation="A critical consistency and risk metric is calculating each branch's total loan portfolio relative to its total customer deposits.",
                sql="""SELECT 
    b.name AS branch_name,
    b.city,
    COALESCE(SUM(a.balance), 0.00) AS total_deposits,
    (SELECT COALESCE(SUM(l.principal_amount), 0.00) 
     FROM loans l 
     WHERE l.branch_id = b.id AND l.status = 'active') AS active_loans
FROM branches b
LEFT JOIN accounts a ON b.id = a.branch_id
GROUP BY b.id, b.name, b.city
ORDER BY total_deposits DESC;""",
                columns=["branch_name", "city", "total_deposits", "active_loans"],
                rows=[
                    ["Downtown Flagship", "New York", 175251.05, 750000.00],
                    ["Metro West", "Chicago", 157250.75, 450000.00],
                    ["Silicon Hub", "San Francisco", 143800.50, 600000.00],
                    ["South Coast", "Miami", 102450.00, 280000.00],
                    ["Highland Branch", "Denver", 98200.20, 320000.00],
                ],
            ),
            WorkedExample(
                title="Transaction Type Breakdown and Aggregate Volume",
                explanation="Aggregating transaction volume and frequencies across distinct operation types to inspect ledger distributions.",
                sql="""SELECT 
    transaction_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_volume,
    ROUND(AVG(amount), 2) AS average_amount
FROM transactions
GROUP BY transaction_type
ORDER BY total_volume DESC;""",
                columns=["transaction_type", "total_transactions", "total_volume", "average_amount"],
                rows=[
                    ["deposit", 16, 48250.00, 3015.63],
                    ["withdrawal", 14, 21400.00, 1528.57],
                    ["transfer_in", 5, 14500.00, 2900.00],
                    ["transfer_out", 5, 14500.00, 2900.00],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Executing multi-statement financial updates outside an explicit transaction block.",
                explanation="If a debit succeeds but the credit fails due to network timeout or constraints, money vanishes unless wrapped in BEGIN TRANSACTION ... COMMIT.",
                incorrect_sql="""UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- If system crashes here, 100 is lost!
UPDATE accounts SET balance = balance + 100 WHERE id = 2;""",
                corrected_sql="""BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;""",
            ),
            CommonMistake(
                pitfall="Using UPDATE or DELETE without a WHERE clause in production.",
                explanation="Omitting the WHERE predicate updates or deletes every single row in the relation. In mission-critical environments, always test with SELECT first.",
                incorrect_sql="DELETE FROM transactions; -- Deletes all transaction records!",
                corrected_sql="DELETE FROM transactions WHERE account_id = 42 AND transaction_date < '2020-01-01';",
            ),
        ],
        real_world_use_cases=[
            "Financial ledgers: Double-entry bookkeeping where every debit must balance a corresponding credit inside an atomic transaction.",
            "Idempotent API webhooks: Using UPSERT (ON CONFLICT) to safely retry payment webhook deliveries without creating duplicate records.",
            "Data cleanup & compliance: Purging expired or flagged customer records while maintaining audit logs.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="p-6-6",
                slug="high-net-worth-accounts-audit",
                title="Audit High-Balance Accounts for Verification",
                difficulty="easy",
                prompt="Write a query to identify all bank accounts with a `balance >= 50000.00`. Return `id`, `customer_id`, `account_type`, and `balance`, sorted by `balance` DESC.",
                starter_sql="-- Find high balance accounts\nSELECT \nFROM accounts\n",
                solution_sql="""SELECT id, customer_id, account_type, balance
FROM accounts
WHERE balance >= 50000.00
ORDER BY balance DESC;""",
                hints=[
                    "Filter with 'WHERE balance >= 50000.00'.",
                    "Order by balance DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-7",
                slug="unutilized-accounts-audit",
                title="Identify Inactive Accounts Without Any Transactions",
                difficulty="medium",
                prompt="Auditors require a list of all accounts that have NEVER performed any transaction. Use a LEFT JOIN between `accounts` and `transactions` to return `a.id` (as `account_id`), `a.customer_id`, and `a.balance`. Order by `a.id` ASC.",
                starter_sql="-- Find accounts with zero recorded transactions\nSELECT \nFROM accounts a\n",
                solution_sql="""SELECT a.id AS account_id, a.customer_id, a.balance
FROM accounts a
LEFT JOIN transactions t ON a.id = t.account_id
WHERE t.id IS NULL
ORDER BY a.id ASC;""",
                hints=[
                    "Use a LEFT JOIN from accounts to transactions.",
                    "Filter with 'WHERE t.id IS NULL' to find accounts with zero matching transactions.",
                    "Order by a.id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-8",
                slug="customer-total-credit-exposure",
                title="Calculate Total Active Loan Exposure by Customer",
                difficulty="medium",
                prompt="Write a query to calculate the total active loan exposure for each customer who has at least one active loan (`status = 'active'`). Return `c.id` (as `customer_id`), `c.first_name || ' ' || c.last_name` (as `customer_name`), and the sum of `principal_amount` (as `total_loan_amount`). Sort by `total_loan_amount` DESC.",
                starter_sql="-- Calculate active loan exposure per customer\nSELECT \nFROM customers c\n",
                solution_sql="""SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    SUM(l.principal_amount) AS total_loan_amount
FROM customers c
JOIN loans l ON c.id = l.customer_id
WHERE l.status = 'active'
GROUP BY c.id, customer_name
ORDER BY total_loan_amount DESC;""",
                hints=[
                    "Join customers with loans on c.id = l.customer_id.",
                    "Filter by l.status = 'active'.",
                    "Group by c.id, customer_name and order by total_loan_amount DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-9",
                slug="transaction-frequency-per-account",
                title="Transaction Velocity: Top Active Accounts",
                difficulty="easy",
                prompt="Write a query to count the number of transactions per account for accounts that have at least 2 transactions. Return `account_id` and the total `transaction_count`. Order by `transaction_count` DESC, then `account_id` ASC.",
                starter_sql="-- Count transactions per account\nSELECT \nFROM transactions\n",
                solution_sql="""SELECT account_id, COUNT(*) AS transaction_count
FROM transactions
GROUP BY account_id
HAVING COUNT(*) >= 2
ORDER BY transaction_count DESC, account_id ASC;""",
                hints=[
                    "Group by account_id and filter with 'HAVING COUNT(*) >= 2'.",
                    "Order by transaction_count DESC, account_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-10",
                slug="calculate-net-customer-liquidity",
                title="Consolidated Customer Liquidity across All Accounts",
                difficulty="hard",
                prompt="Write a query to compute the total liquidity for every customer who owns more than one account. Return `c.id` AS `customer_id`, `c.first_name || ' ' || c.last_name` AS `customer_name`, `COUNT(a.id)` AS `total_accounts`, and `ROUND(SUM(a.balance), 2)` AS `total_balance`. Order by `total_balance` DESC.",
                starter_sql="-- Calculate consolidated customer liquidity\nSELECT \nFROM customers c\n",
                solution_sql="""SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(a.id) AS total_accounts,
    ROUND(SUM(a.balance), 2) AS total_balance
FROM customers c
JOIN accounts a ON c.id = a.customer_id
GROUP BY c.id, customer_name
HAVING COUNT(a.id) > 1
ORDER BY total_balance DESC;""",
                hints=[
                    "Join customers with accounts.",
                    "Group by c.id and customer_name.",
                    "Filter groups with 'HAVING COUNT(a.id) > 1' to only include multi-account owners.",
                    "Order by total_balance DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
        ],
    ),

    # =========================================================================
    # Topic 3: Relational Normalization & Schema Design
    # =========================================================================
    TopicLesson(
        id="les-6-3",
        slug="relational-normalization-and-design",
        level_number=6,
        level_title="Level 6: Database Engineering & Architecture",
        title="Relational Normalization & Schema Design Integrity",
        order_index=3,
        database_id="db-ecommerce",
        database_name="ecommerce_db",
        learning_objectives=[
            "Understand the theoretical foundations of Relational Normalization and Functional Dependencies.",
            "Distinguish between 1NF, 2NF, 3NF, and Boyce-Codd Normal Form (BCNF).",
            "Identify and prevent the three classic data anomalies: Insertion, Update, and Deletion anomalies.",
            "Analyze practical trade-offs between normalized OLTP schemas and denormalized analytical (OLAP) schemas.",
        ],
        prerequisites=[
            "Level 1: Fundamentals, Level 3: Joins & Keys, and Level 6 Topic 1: DDL & Constraints.",
        ],
        detailed_explanation="""Relational Normalization is a rigorous mathematical process of organizing columns and tables in a relational database to minimize data redundancy and eliminate modification anomalies without losing information.

The Three Classic Modification Anomalies:
Consider an unnormalized table `Orders (order_id, customer_name, customer_city, product_name, price)`:
1. **Insertion Anomaly**: You cannot record a new customer until they place an order, because `order_id` is the primary key and cannot be NULL.
2. **Update Anomaly**: If a customer changes their city, you must update multiple rows across historical orders. If one row is missed, data becomes inconsistent.
3. **Deletion Anomaly**: If a customer cancels their only order, deleting that row also permanently erases the customer's existence and address!

The Normal Forms:
1. **First Normal Form (1NF)**:
   - Each column must contain atomic (indivisible) values (no CSV lists, arrays, or JSON blobs inside a single cell).
   - Each record must be uniquely identifiable (a primary key must exist).
   - No repeating groups or column sequences (e.g. `phone_1`, `phone_2`, `phone_3`).

2. **Second Normal Form (2NF)**:
   - Must be in 1NF.
   - All non-key attributes must be fully functionally dependent on the ENTIRE primary key (no partial key dependencies).
   - In a junction table with composite key `(order_id, product_id)`, storing `product_name` violates 2NF because `product_name` depends only on `product_id`, not on `order_id`!

3. **Third Normal Form (3NF)**:
   - Must be in 2NF.
   - No transitive dependencies: Non-key attributes must depend solely on candidate keys, never on other non-key attributes.
   - Example: In `Employees (id, name, dept_id, dept_name)`, `dept_name` depends on `dept_id`, which depends on `id`. This transitive dependency (`id -> dept_id -> dept_name`) violates 3NF! Moving departments to their own table resolves 3NF.

4. **Boyce-Codd Normal Form (BCNF)**:
   - A stricter version of 3NF: For every non-trivial functional dependency `X -> Y`, `X` must be a superkey.

Normalized (OLTP) vs Denormalized (OLAP):
- **OLTP (Online Transaction Processing)**: Normalized (3NF/BCNF) to guarantee write integrity, fast single-row inserts/updates, and zero redundant storage.
- **OLAP (Online Analytical Processing)**: Denormalized (Star / Snowflake schemas) with pre-aggregated dimension tables to minimize costly multi-table JOINs across billions of rows.""",
        syntax_reference="""-- Normalized 3NF Schema Example:
-- 1. Entity: Customers
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    city VARCHAR(50)
);

-- 2. Entity: Products
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    category_id INTEGER REFERENCES categories(id),
    price DECIMAL(10, 2)
);

-- 3. Header: Orders (Relates Customer to Order event)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date DATE,
    status VARCHAR(20)
);

-- 4. Line Items: OrderItems (Resolves Many-to-Many between Orders and Products)
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) -- Captured at purchase time!
);""",
        clause_breakdown=[
            ClauseExplanation(keyword="Functional Dependency (X -> Y)", purpose="Mathematical assertion that the value of attribute X uniquely determines the value of Y.", notes="e.g. employee_id -> email."),
            ClauseExplanation(keyword="1NF: Atomic Values", purpose="Ensures no multi-valued lists or nested collections exist in a single field.", notes="Requires scalar values per cell."),
            ClauseExplanation(keyword="2NF: Full Dependency", purpose="Eliminates partial dependencies on composite primary keys.", notes="Relevant whenever a composite key is used."),
            ClauseExplanation(keyword="3NF: No Transitive Dependency", purpose="Ensures non-key columns depend only on primary keys, eliminating transitive chains.", notes="'The key, the whole key, and nothing but the key'."),
        ],
        worked_examples=[
            WorkedExample(
                title="Historical Price Drift vs Normalized Product Catalog",
                explanation="In normalized e-commerce schemas, `order_items.unit_price` preserves historical transaction prices, which may diverge from the current `products.price` catalog.",
                sql="""SELECT 
    oi.id AS item_id,
    p.name AS product_name,
    oi.unit_price AS purchased_price,
    p.price AS current_catalog_price,
    ROUND(oi.unit_price - p.price, 2) AS price_difference
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.unit_price != p.price
ORDER BY item_id ASC;""",
                columns=["item_id", "product_name", "purchased_price", "current_catalog_price", "price_difference"],
                rows=[
                    [8, "Wireless Noise-Canceling Headphones", 279.99, 299.99, -20.00],
                    [15, "Ultra HD 4K Monitor 27-inch", 379.99, 399.99, -20.00],
                ],
            ),
            WorkedExample(
                title="Detecting Inventory Stock Depletion across Normalized Categories",
                explanation="Aggregating normalized products joined to categories to evaluate stock health and identify items needing replenishment.",
                sql="""SELECT 
    c.name AS category_name,
    p.name AS product_name,
    p.stock_quantity,
    p.price
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.stock_quantity < 20
ORDER BY p.stock_quantity ASC;""",
                columns=["category_name", "product_name", "stock_quantity", "price"],
                rows=[
                    ["Electronics", "Ultra HD 4K Monitor 27-inch", 12, 399.99],
                    ["Furniture", "Ergonomic Standing Desk", 14, 499.99],
                    ["Appliances", "Espresso Machine Pro", 15, 599.99],
                    ["Electronics", "Mechanical Gaming Keyboard", 18, 129.99],
                ],
            ),
            WorkedExample(
                title="Customer Lifetime Value (LTV) across Normalized Order Tables",
                explanation="Computing multi-table analytical metrics joining customers, orders, and payments to evaluate customer value.",
                sql="""SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    COUNT(DISTINCT o.id) AS total_orders,
    ROUND(COALESCE(SUM(p.amount), 0.00), 2) AS lifetime_spend
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
LEFT JOIN payments p ON o.id = p.order_id AND p.status = 'completed'
GROUP BY c.id, customer_name, c.city
HAVING total_orders > 0
ORDER BY lifetime_spend DESC
LIMIT 5;""",
                columns=["customer_id", "customer_name", "city", "total_orders", "lifetime_spend"],
                rows=[
                    [1, "Alice Smith", "New York", 2, 929.98],
                    [2, "Bob Jones", "Los Angeles", 2, 799.98],
                    [3, "Charlie Brown", "Chicago", 2, 749.98],
                    [4, "Diana Prince", "Houston", 2, 599.98],
                    [5, "Evan Wright", "Phoenix", 2, 459.98],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Storing comma-separated lists of IDs in a single text column (violating 1NF).",
                explanation="Storing '101,102,105' in a single column makes JOINs, indexing, foreign keys, and aggregations virtually impossible without slow string parsing.",
                incorrect_sql="-- Violating 1NF:\nCREATE TABLE orders (id INT, product_ids VARCHAR(255));",
                corrected_sql="-- Proper 1NF with Junction Table:\nCREATE TABLE order_items (order_id INT, product_id INT, PRIMARY KEY (order_id, product_id));",
            ),
            CommonMistake(
                pitfall="Over-denormalizing OLTP tables prematurely.",
                explanation="Copying customer address into every order row seems convenient for querying, but creates massive update anomalies if a customer updates their address.",
                incorrect_sql="-- Duplicate address data across millions of order rows\nCREATE TABLE orders (id INT, customer_id INT, shipping_address TEXT, billing_address TEXT);",
                corrected_sql="-- Keep address in addresses table and reference by foreign key\nCREATE TABLE orders (id INT, customer_id INT, address_id INT REFERENCES addresses(id));",
            ),
        ],
        real_world_use_cases=[
            "Core e-commerce design: Separating order headers from line items to allow variable basket sizes and accurate historical tax/pricing.",
            "Multi-tenant billing systems: Isolating plan tiers and features into normalized lookup tables to allow instant global tier updates.",
            "Data Warehousing: Transforming 3NF transactional models into Star Schemas with Fact and Dimension tables for sub-second analytical reporting.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="p-6-11",
                slug="detect-unpurchased-catalog-products",
                title="Dead Inventory: Identify Products with Zero Orders",
                difficulty="easy",
                prompt="Write a query to identify any catalog products that have never been ordered. Use a LEFT JOIN between `products` and `order_items` to find products where `order_items.id IS NULL`. Return `p.id` AS `product_id`, `p.name` AS `product_name`, and `p.price`. Order by `p.id` ASC.",
                starter_sql="-- Find products that have never been ordered\nSELECT \nFROM products p\n",
                solution_sql="""SELECT p.id AS product_id, p.name AS product_name, p.price
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
WHERE oi.id IS NULL
ORDER BY p.id ASC;""",
                hints=[
                    "Use a LEFT JOIN from products to order_items on p.id = oi.product_id.",
                    "Filter with 'WHERE oi.id IS NULL'.",
                    "Order by p.id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-12",
                slug="revenue-by-product-category",
                title="Category Revenue Distribution Across Normalized Tables",
                difficulty="medium",
                prompt="Write a query to compute the total revenue generated by each product category based on `order_items` (`quantity * unit_price`). Join `categories`, `products`, and `order_items`. Return `c.name` AS `category_name`, and `ROUND(SUM(oi.quantity * oi.unit_price), 2)` AS `total_revenue`. Order by `total_revenue` DESC.",
                starter_sql="-- Calculate total revenue per product category\nSELECT \nFROM categories c\n",
                solution_sql="""SELECT 
    c.name AS category_name,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM categories c
JOIN products p ON c.id = p.category_id
JOIN order_items oi ON p.id = oi.product_id
GROUP BY c.id, c.name
ORDER BY total_revenue DESC;""",
                hints=[
                    "Join categories -> products -> order_items.",
                    "Sum 'oi.quantity * oi.unit_price' and round to 2 decimals.",
                    "Group by c.id, c.name and order by total_revenue DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-13",
                slug="customer-order-frequency-tiers",
                title="Customer Segmentation: Order Count Distribution",
                difficulty="medium",
                prompt="Write a query to find the distribution of customer order frequencies. Return `c.id` AS `customer_id`, `c.first_name || ' ' || c.last_name` AS `customer_name`, and `COUNT(o.id)` AS `order_count`. Include customers with 0 orders using a LEFT JOIN. Order by `order_count` DESC, then `customer_id` ASC.",
                starter_sql="-- Count orders per customer including zeros\nSELECT \nFROM customers c\n",
                solution_sql="""SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, customer_name
ORDER BY order_count DESC, customer_id ASC;""",
                hints=[
                    "Use a LEFT JOIN between customers and orders.",
                    "Use COUNT(o.id) so customers without orders show a count of 0.",
                    "Order by order_count DESC, customer_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-14",
                slug="reconcile-order-total-against-order-items",
                title="Integrity Audit: Verify Order Totals Match Item Sums",
                difficulty="hard",
                prompt="Write a query to verify whether any order's `total_amount` in the `orders` table fails to match the sum of its items in `order_items` (`SUM(quantity * unit_price)`). Return `o.id` AS `order_id`, `o.total_amount`, and `ROUND(SUM(oi.quantity * oi.unit_price), 2)` AS `calculated_total`. Only return orders where `o.total_amount != ROUND(SUM(oi.quantity * oi.unit_price), 2)`.",
                starter_sql="-- Audit orders against order item sums\nSELECT \nFROM orders o\n",
                solution_sql="""SELECT 
    o.id AS order_id,
    o.total_amount,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS calculated_total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.total_amount
HAVING o.total_amount != ROUND(SUM(oi.quantity * oi.unit_price), 2);""",
                hints=[
                    "Join orders with order_items on o.id = oi.order_id.",
                    "Group by o.id and o.total_amount.",
                    "Use HAVING to filter where o.total_amount != ROUND(SUM(oi.quantity * oi.unit_price), 2).",
                    "A clean database will return an empty set, proving data integrity!",
                ],
                order_matters=False,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-15",
                slug="average-basket-size-by-country",
                title="International Sales Metrics: Average Basket by Country",
                difficulty="medium",
                prompt="Write a query to calculate the average order value (total_amount) per customer country. Join `customers` and `orders`. Return `c.country`, `COUNT(o.id)` AS `total_orders`, and `ROUND(AVG(o.total_amount), 2)` AS `avg_order_value`. Order by `avg_order_value` DESC.",
                starter_sql="-- Compute average order value by customer country\nSELECT \nFROM customers c\n",
                solution_sql="""SELECT 
    c.country,
    COUNT(o.id) AS total_orders,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.country
ORDER BY avg_order_value DESC;""",
                hints=[
                    "Join customers and orders.",
                    "Group by c.country.",
                    "Calculate COUNT(o.id) and ROUND(AVG(o.total_amount), 2).",
                    "Order by avg_order_value DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
        ],
    ),

    # =========================================================================
    # Topic 4: Indexing Strategies, SARGability & Query Optimization
    # =========================================================================
    TopicLesson(
        id="les-6-4",
        slug="indexes-and-query-optimization",
        level_number=6,
        level_title="Level 6: Database Engineering & Architecture",
        title="Indexing Strategies, SARGability & Query Optimization",
        order_index=4,
        database_id="db-university",
        database_name="university_db",
        learning_objectives=[
            "Understand physical database storage: B-Tree index structures, pages, and leaf nodes.",
            "Master the difference between Clustered vs Non-Clustered and Single vs Composite Indexes.",
            "Apply the Leftmost Prefix Rule to design multi-column composite indexes.",
            "Write SARGable (Search Argument Able) queries that leverage index lookups rather than full table scans.",
            "Understand query execution plans: Table Scans (SCAN TABLE) vs Index Searches (SEARCH TABLE USING INDEX).",
        ],
        prerequisites=[
            "Level 1: Fundamentals, Level 2: Aggregations, and Level 3: Joins.",
        ],
        detailed_explanation="""In database engineering, writing functionally correct SQL is only half the battle; queries must execute efficiently at scale across millions of rows.

How B-Tree Indexes Work:
Without an index, the database engine must inspect every single page in a table to locate matching rows—a linear operation known as a **Full Table Scan (SCAN TABLE)** ($O(N)$ complexity).
A **B-Tree (Balanced Tree) Index** creates a self-balancing sorted data structure storing column values alongside pointers (RowIDs) to the actual physical table rows. Searching a B-Tree requires traversing from Root to Leaf node, achieving $O(\\log N)$ lookup performance.

Index Varieties:
1. **Clustered Index**: Physically arranges the stored table rows in the order of the indexed key. A table can possess only ONE clustered index (in SQLite, the `INTEGER PRIMARY KEY` acts as the clustered RowID).
2. **Non-Clustered (Secondary) Index**: A separate data structure containing copies of the indexed column(s) plus a pointer to the clustered row.
3. **Composite Index**: An index spanning multiple columns, e.g. `CREATE INDEX idx_student_dept ON students(enrollment_year, major)`.
   - **The Leftmost Prefix Rule**: A composite index on `(A, B, C)` can accelerate queries filtering on:
     - `A`
     - `A AND B`
     - `A AND B AND C`
     - But it CANNOT accelerate a query filtering on `B` alone or `C` alone!
4. **Covering Index**: An index that contains all columns requested by a query. The engine satisfies the query entirely from the B-Tree without looking up the base table (a Zero-Table-Lookup query).

SARGability (Search Argument Able):
A query predicate is **SARGable** if the database engine can directly seek into an index. Wrapping an indexed column inside a function or mathematical expression ruins SARGability, forcing a catastrophic full table scan!

| Non-SARGable Antipattern (Full Table Scan) | SARGable Equivalent (Index Seek) |
| :--- | :--- |
| `WHERE YEAR(enrollment_date) = 2023` | `WHERE enrollment_date >= '2023-01-01' AND enrollment_date < '2024-01-01'` |
| `WHERE UPPER(major) = 'COMPUTER SCIENCE'` | `WHERE major = 'Computer Science' COLLATE NOCASE` |
| `WHERE salary * 1.10 > 100000` | `WHERE salary > 100000 / 1.10` |
| `WHERE name LIKE '%tech'` (Leading wildcard) | `WHERE name LIKE 'tech%'` (Trailing wildcard is SARGable) |""",
        syntax_reference="""-- Create a single-column secondary index
CREATE INDEX idx_students_major ON students(major);

-- Create a multi-column composite index
CREATE INDEX idx_enrollments_student_course ON enrollments(student_id, course_id);

-- Create a unique constraint index
CREATE UNIQUE INDEX idx_professors_email ON professors(email);

-- Query execution plan analysis (in CLI/Management tools)
-- EXPLAIN QUERY PLAN SELECT * FROM students WHERE major = 'Computer Science';""",
        clause_breakdown=[
            ClauseExplanation(keyword="CREATE INDEX", purpose="Builds a B-Tree index on specified column(s) to accelerate search and filter performance.", notes="Slows down INSERT/UPDATE/DELETE as indexes must be maintained."),
            ClauseExplanation(keyword="UNIQUE INDEX", purpose="Enforces uniqueness on indexed columns while building a fast lookup B-Tree.", notes="Automatically created for PRIMARY KEY and UNIQUE columns."),
            ClauseExplanation(keyword="Leftmost Prefix", purpose="Algorithmic requirement that composite index seeks must match column order from left to right.", notes="Index (A, B) cannot seek on B alone."),
            ClauseExplanation(keyword="SARGable", purpose="Query design practice keeping indexed columns bare on one side of comparison operators.", notes="Avoids function calls on indexed fields."),
        ],
        worked_examples=[
            WorkedExample(
                title="SARGable Range Filtering: Enrollment Cohort Analysis",
                explanation="Filtering students by enrollment year using a direct SARGable comparison operator without string or date conversion functions.",
                sql="""SELECT 
    id AS student_id,
    first_name || ' ' || last_name AS student_name,
    major,
    enrollment_year
FROM students
WHERE enrollment_year >= 2023
ORDER BY enrollment_year DESC, student_id ASC;""",
                columns=["student_id", "student_name", "major", "enrollment_year"],
                rows=[
                    [3, "Carol Danvers", "Physics", 2023],
                    [6, "Frank Castle", "Mathematics", 2023],
                    [9, "Ian Malcolm", "Biology", 2023],
                    [12, "Laura Kinney", "Chemistry", 2023],
                    [15, "Oscar Isaac", "Art History", 2023],
                    [18, "Riley Reid", "English Literature", 2023],
                    [21, "Ulysses Grant", "Economics", 2023],
                    [24, "Xavier Charles", "Computer Science", 2023],
                    [27, "Aaron Burr", "Mathematics", 2023],
                    [30, "David Copperfield", "Chemistry", 2023],
                ],
            ),
            WorkedExample(
                title="Optimized Join Aggregation: Professor Course Load Distribution",
                explanation="Efficiently joining professors to courses and counting distinct student enrollments.",
                sql="""SELECT 
    p.id AS professor_id,
    p.first_name || ' ' || p.last_name AS professor_name,
    d.name AS department_name,
    COUNT(DISTINCT c.id) AS courses_taught,
    COUNT(e.id) AS total_enrolled_students
FROM professors p
JOIN departments d ON p.department_id = d.id
LEFT JOIN courses c ON p.id = c.professor_id
LEFT JOIN enrollments e ON c.id = e.course_id
GROUP BY p.id, professor_name, department_name
ORDER BY total_enrolled_students DESC, professor_id ASC;""",
                columns=["professor_id", "professor_name", "department_name", "courses_taught", "total_enrolled_students"],
                rows=[
                    [1, "Alan Turing", "Computer Science", 2, 10],
                    [2, "Grace Hopper", "Computer Science", 2, 9],
                    [5, "Richard Feynman", "Physics", 2, 9],
                    [3, "Carl Friedrich Gauss", "Mathematics", 2, 8],
                    [4, "Ada Lovelace", "Mathematics", 1, 5],
                    [6, "Marie Curie", "Chemistry", 1, 4],
                    [7, "Charles Darwin", "Biology", 1, 4],
                    [8, "Adam Smith", "Economics", 1, 3],
                ],
            ),
            WorkedExample(
                title="Departmental Course Catalog Load and Credit Metrics",
                explanation="Analyzing departmental course offerings and total credit values using index-friendly group aggregations.",
                sql="""SELECT 
    d.name AS department_name,
    COUNT(c.id) AS total_courses,
    SUM(c.credits) AS total_credits,
    ROUND(AVG(c.credits), 1) AS avg_credits_per_course
FROM departments d
LEFT JOIN courses c ON d.id = c.department_id
GROUP BY d.id, d.name
ORDER BY total_courses DESC, department_name ASC;""",
                columns=["department_name", "total_courses", "total_credits", "avg_credits_per_course"],
                rows=[
                    ["Computer Science", 4, 15, 3.8],
                    ["Mathematics", 3, 11, 3.7],
                    ["Physics", 2, 8, 4.0],
                    ["Biology", 1, 4, 4.0],
                    ["Chemistry", 1, 4, 4.0],
                    ["Economics", 1, 3, 3.0],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Over-indexing every column in a table.",
                explanation="Every index adds disk overhead and must be updated on every INSERT, UPDATE, and DELETE. Tables with 15+ indexes suffer massive write degradation.",
                incorrect_sql="-- Creating an index for every individual column blindly\nCREATE INDEX idx_1 ON users(first_name);\nCREATE INDEX idx_2 ON users(last_name);\nCREATE INDEX idx_3 ON users(city);",
                corrected_sql="-- Create composite index matching real query patterns:\nCREATE INDEX idx_users_name_city ON users(last_name, first_name, city);",
            ),
            CommonMistake(
                pitfall="Using wildcard prefix LIKE queries (e.g. LIKE '%term').",
                explanation="A leading wildcard prevents B-Tree index traversal because the engine does not know where in the alphabet to begin searching, forcing a full table scan.",
                incorrect_sql="SELECT * FROM students WHERE email LIKE '%@university.edu'; -- Full Table Scan!",
                corrected_sql="-- If domain filtering is frequent, store domain in separate indexed column or use trailing wildcards\nSELECT * FROM students WHERE email LIKE 'alice%'; -- SARGable index range seek!",
            ),
        ],
        real_world_use_cases=[
            "High-throughput user login lookups: Ensuring email/username lookups utilize unique B-Tree indexes for $O(\\log N)$ sub-millisecond authentication.",
            "Time-series log queries: Using composite indexes `(tenant_id, timestamp DESC)` to retrieve recent events instantly.",
            "E-commerce faceted search: Designing composite indexes matching popular filter sequences (e.g. `category_id, price, rating`).",
        ],
        practice_questions=[
            PracticeQuestion(
                id="p-6-16",
                slug="sargable-academic-year-filter",
                title="SARGable Query Design: Cohort Filtering",
                difficulty="easy",
                prompt="Write a SARGable query to retrieve all students enrolled between 2021 and 2022 inclusive. Return `id`, `first_name`, `last_name`, and `enrollment_year`. Use the `BETWEEN` operator or `>=` and `<=` without any functions on `enrollment_year`. Order by `id` ASC.",
                starter_sql="-- SARGable query for enrollment cohorts 2021-2022\nSELECT \nFROM students\n",
                solution_sql="""SELECT id, first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year BETWEEN 2021 AND 2022
ORDER BY id ASC;""",
                hints=[
                    "Use 'WHERE enrollment_year BETWEEN 2021 AND 2022'.",
                    "Order by id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-17",
                slug="indexed-grade-point-average-gpa",
                title="Student GPA Computation: Multi-Table Analytical Join",
                difficulty="medium",
                prompt="Write a query to calculate the cumulative Grade Point Average (GPA) for each student who has received at least one grade. Join `students`, `enrollments`, and `grades`. Return `s.id` AS `student_id`, `s.first_name || ' ' || s.last_name` AS `student_name`, `s.major`, and `ROUND(AVG(g.numeric_grade), 2)` AS `gpa`. Order by `gpa` DESC, then `student_id` ASC.",
                starter_sql="-- Compute cumulative GPA per student\nSELECT \nFROM students s\n",
                solution_sql="""SELECT 
    s.id AS student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    s.major,
    ROUND(AVG(g.numeric_grade), 2) AS gpa
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN grades g ON e.id = g.enrollment_id
GROUP BY s.id, student_name, s.major
ORDER BY gpa DESC, student_id ASC;""",
                hints=[
                    "Join students -> enrollments -> grades.",
                    "Group by s.id, student_name, s.major.",
                    "Calculate ROUND(AVG(g.numeric_grade), 2) AS gpa.",
                    "Order by gpa DESC, student_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-18",
                slug="courses-exceeding-enrollment-capacity",
                title="Course Popularity: Top Enrolled Courses",
                difficulty="easy",
                prompt="Write a query to identify courses with the highest student enrollment. Join `courses` and `enrollments`. Return `c.id` AS `course_id`, `c.code`, `c.title`, and `COUNT(e.id)` AS `enrolled_students`. Order by `enrolled_students` DESC, then `course_id` ASC.",
                starter_sql="-- Count enrolled students per course\nSELECT \nFROM courses c\n",
                solution_sql="""SELECT 
    c.id AS course_id,
    c.code,
    c.title,
    COUNT(e.id) AS enrolled_students
FROM courses c
JOIN enrollments e ON c.id = e.course_id
GROUP BY c.id, c.code, c.title
ORDER BY enrolled_students DESC, course_id ASC;""",
                hints=[
                    "Join courses with enrollments on c.id = e.course_id.",
                    "Group by c.id, c.code, c.title.",
                    "Order by enrolled_students DESC, course_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-19",
                slug="unassigned-professors-audit",
                title="Resource Allocation Audit: Professors Without Courses",
                difficulty="medium",
                prompt="Write a query to find all professors who are currently NOT assigned to teach any course (`c.id IS NULL`). Use a LEFT JOIN between `professors` and `courses`. Return `p.id` AS `professor_id`, `p.first_name || ' ' || p.last_name` AS `professor_name`, and `p.email`. Order by `professor_id` ASC.",
                starter_sql="-- Find professors without assigned courses\nSELECT \nFROM professors p\n",
                solution_sql="""SELECT 
    p.id AS professor_id,
    p.first_name || ' ' || p.last_name AS professor_name,
    p.email
FROM professors p
LEFT JOIN courses c ON p.id = c.professor_id
WHERE c.id IS NULL
ORDER BY professor_id ASC;""",
                hints=[
                    "LEFT JOIN professors with courses on p.id = c.professor_id.",
                    "Filter with 'WHERE c.id IS NULL'.",
                    "Order by professor_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-20",
                slug="high-credit-stem-courses",
                title="SARGable Multi-Condition Filter: High-Credit STEM Courses",
                difficulty="easy",
                prompt="Write a query to find all courses in the 'Computer Science' or 'Mathematics' departments that grant 4 or more credits (`credits >= 4`). Join `courses` and `departments`. Return `c.id` AS `course_id`, `c.code`, `c.title`, `d.name` AS `department_name`, and `c.credits`. Order by `c.credits` DESC, `course_id` ASC.",
                starter_sql="-- Find 4+ credit STEM courses\nSELECT \nFROM courses c\n",
                solution_sql="""SELECT 
    c.id AS course_id,
    c.code,
    c.title,
    d.name AS department_name,
    c.credits
FROM courses c
JOIN departments d ON c.department_id = d.id
WHERE d.name IN ('Computer Science', 'Mathematics') AND c.credits >= 4
ORDER BY c.credits DESC, course_id ASC;""",
                hints=[
                    "Join courses with departments.",
                    "Filter with \"d.name IN ('Computer Science', 'Mathematics') AND c.credits >= 4\".",
                    "Order by c.credits DESC, course_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
        ],
    ),

    # =========================================================================
    # Topic 5: Database Triggers & Automated Audit Systems
    # =========================================================================
    TopicLesson(
        id="les-6-5",
        slug="database-triggers-and-audit-systems",
        level_number=6,
        level_title="Level 6: Database Engineering & Architecture",
        title="Database Triggers & Automated Audit Systems",
        order_index=5,
        database_id="db-banking",
        database_name="banking_db",
        learning_objectives=[
            "Understand active database rules: CREATE TRIGGER syntax and event triggers.",
            "Differentiate between BEFORE, AFTER, and INSTEAD OF triggers.",
            "Master transition variables: OLD and NEW row tuples across INSERT, UPDATE, and DELETE operations.",
            "Design immutable audit trails and automated change tracking systems.",
            "Analyze performance risks, cascading triggers, and debugging challenges associated with procedural database automation.",
        ],
        prerequisites=[
            "Level 1: Fundamentals, Level 2: Aggregations, and Level 6 Topic 2: DML & Transactions.",
        ],
        detailed_explanation="""A Database Trigger is a procedural program stored within the database catalog that executes automatically (\"fires\") whenever a specific Data Manipulation Language (DML) event occurs on a table or view.

Trigger Execution Timing & Events:
Triggers are defined by three parameters:
1. **Event**: `INSERT`, `UPDATE`, or `DELETE`.
2. **Timing**:
   - `BEFORE`: Fires prior to the operation. Ideal for data sanitization (e.g. converting email to lowercase) or constraint validation that aborts early.
   - `AFTER`: Fires after the operation completes and constraints pass. Ideal for writing audit trails, recalculating cached balances, or notifying dependent systems.
   - `INSTEAD OF`: Fires in place of the operation. Exclusively used on non-updatable relational VIEWS to translate updates back to underlying base tables.
3. **Granularity**:
   - `FOR EACH ROW`: Executes once for every individual row modified by the SQL statement.
   - `FOR EACH STATEMENT`: Executes once per SQL statement, regardless of how many rows were affected.

Transition Variables: OLD and NEW:
Within row-level trigger bodies, special pseudo-records provide access to column states:
- `NEW`: Contains the new values being inserted or updated. Unavailable during `DELETE`.
- `OLD`: Contains the pre-existing values before update or deletion. Unavailable during `INSERT`.

| Operation | `OLD` record available? | `NEW` record available? |
| :--- | :---: | :---: |
| **INSERT** | No | Yes |
| **UPDATE** | Yes (original values) | Yes (modified values) |
| **DELETE** | Yes (deleted values) | No |

Immutable Audit Logging Pattern:
A quintessential trigger engineering pattern is maintaining an audit log for financial or sensitive tables:
```sql
CREATE TRIGGER trg_audit_account_balance_update
AFTER UPDATE OF balance ON accounts
FOR EACH ROW
WHEN OLD.balance <> NEW.balance
BEGIN
    INSERT INTO account_audit_log (
        account_id, 
        old_balance, 
        new_balance, 
        changed_at, 
        action
    ) VALUES (
        OLD.id, 
        OLD.balance, 
        NEW.balance, 
        CURRENT_TIMESTAMP, 
        'UPDATE'
    );
END;
```

Architectural Cautions:
While triggers guarantee that business rules execute regardless of which application service wrote to the database, they have architectural trade-offs:
- **Hidden Logic**: Developers inspecting backend application code cannot see triggers firing in the database.
- **Cascading Performance Cascades**: Trigger A modifying Table B can fire Trigger B modifying Table C, creating unbounded latency spikes or deadlocks.
- **Testing Complexity**: Mocking and isolating triggers in unit tests requires spinning up full database instances.""",
        syntax_reference="""-- Create an audit table
CREATE TABLE account_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    old_balance DECIMAL(12, 2),
    new_balance DECIMAL(12, 2),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create a row-level AFTER UPDATE trigger
CREATE TRIGGER trg_log_balance_change
AFTER UPDATE OF balance ON accounts
FOR EACH ROW
WHEN OLD.balance != NEW.balance
BEGIN
    INSERT INTO account_audit (account_id, old_balance, new_balance)
    VALUES (OLD.id, OLD.balance, NEW.balance);
END;

-- Drop trigger
DROP TRIGGER IF EXISTS trg_log_balance_change;""",
        clause_breakdown=[
            ClauseExplanation(keyword="CREATE TRIGGER", purpose="Defines a new trigger event listener attached to a specific table.", notes="Must specify timing (BEFORE/AFTER) and event (INSERT/UPDATE/DELETE)."),
            ClauseExplanation(keyword="FOR EACH ROW", purpose="Specifies that the trigger action executes for every individual affected tuple.", notes="Standard in SQLite and PostgreSQL for data auditing."),
            ClauseExplanation(keyword="WHEN", purpose="Optional boolean condition that must evaluate to TRUE for the trigger action to fire.", notes="Optimizes performance by skipping unnecessary trigger executions."),
            ClauseExplanation(keyword="OLD / NEW", purpose="Pseudo-records providing access to original vs updated column values.", notes="OLD for pre-change state; NEW for post-change state."),
        ],
        worked_examples=[
            WorkedExample(
                title="Simulating Audit Trails: Tracking High-Value Transactions",
                explanation="In banking systems, transactions exceeding $4,000 trigger compliance monitoring and immediate risk auditing.",
                sql="""SELECT 
    t.id AS transaction_id,
    t.account_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    t.transaction_type,
    t.amount,
    t.transaction_date,
    CASE 
        WHEN t.amount >= 5000.00 THEN 'High Priority Audit'
        WHEN t.amount >= 3000.00 THEN 'Standard Audit'
        ELSE 'Normal'
    END AS compliance_tier
FROM transactions t
JOIN accounts a ON t.account_id = a.id
JOIN customers c ON a.customer_id = c.id
WHERE t.amount >= 3000.00
ORDER BY t.amount DESC;""",
                columns=["transaction_id", "account_id", "customer_name", "transaction_type", "amount", "transaction_date", "compliance_tier"],
                rows=[
                    [34, 15, "Paul Allen", "deposit", 6200.00, "2024-03-01", "High Priority Audit"],
                    [14, 5, "Evan Wright", "deposit", 5400.00, "2024-02-18", "High Priority Audit"],
                    [31, 14, "Olivia Wilde", "deposit", 4800.00, "2024-02-28", "Standard Audit"],
                    [2, 1, "Alice Smith", "deposit", 4500.00, "2024-01-16", "Standard Audit"],
                    [9, 4, "Diana Prince", "deposit", 4200.00, "2024-02-05", "Standard Audit"],
                    [22, 10, "Jack Ryan", "deposit", 3800.00, "2024-02-20", "Standard Audit"],
                    [25, 11, "Karen Page", "deposit", 3500.00, "2024-02-22", "Standard Audit"],
                    [4, 2, "Alice Smith", "deposit", 3200.00, "2024-01-22", "Standard Audit"],
                ],
            ),
            WorkedExample(
                title="Branch Cash Flow Audit: Net Daily Deposits vs Withdrawals",
                explanation="Auditing net cash movements per branch to detect cash reserve anomalies and rebalance vault liquidity.",
                sql="""SELECT 
    b.name AS branch_name,
    ROUND(SUM(CASE WHEN t.transaction_type = 'deposit' THEN t.amount ELSE 0 END), 2) AS total_deposits,
    ROUND(SUM(CASE WHEN t.transaction_type = 'withdrawal' THEN t.amount ELSE 0 END), 2) AS total_withdrawals,
    ROUND(SUM(CASE 
        WHEN t.transaction_type = 'deposit' THEN t.amount 
        WHEN t.transaction_type = 'withdrawal' THEN -t.amount 
        ELSE 0 
    END), 2) AS net_cash_flow
FROM branches b
JOIN accounts a ON b.id = a.branch_id
JOIN transactions t ON a.id = t.account_id
GROUP BY b.id, b.name
ORDER BY net_cash_flow DESC;""",
                columns=["branch_name", "total_deposits", "total_withdrawals", "net_cash_flow"],
                rows=[
                    ["Downtown Flagship", 15200.00, 4800.00, 10400.00],
                    ["Metro West", 11650.00, 5200.00, 6450.00],
                    ["Silicon Hub", 10800.00, 5600.00, 5200.00],
                    ["Highland Branch", 5800.00, 2400.00, 3400.00],
                    ["South Coast", 4800.00, 3400.00, 1400.00],
                ],
            ),
            WorkedExample(
                title="Dormant Account Detection: Identifying Stale Accounts",
                explanation="In banking compliance, accounts with no transactions for an extended duration must be flagged for regulatory dormancy.",
                sql="""SELECT 
    a.id AS account_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    a.account_type,
    a.balance,
    MAX(t.transaction_date) AS latest_transaction_date
FROM accounts a
JOIN customers c ON a.customer_id = c.id
LEFT JOIN transactions t ON a.id = t.account_id
GROUP BY a.id, customer_name, a.account_type, a.balance
ORDER BY latest_transaction_date ASC NULLS FIRST
LIMIT 5;""",
                columns=["account_id", "customer_name", "account_type", "balance", "latest_transaction_date"],
                rows=[
                    [19, "Rachel Green", "Checking", 5200.00, None],
                    [20, "Rachel Green", "Savings", 18500.00, None],
                    [21, "Steve Rogers", "Checking", 4100.00, None],
                    [22, "Steve Rogers", "Savings", 22000.00, None],
                    [23, "Tony Stark", "Business", 250000.00, None],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Modifying the same table inside an AFTER trigger on that table (trigger recursion).",
                explanation="Updating table T inside an AFTER UPDATE ON T trigger will cause the trigger to fire itself recursively until SQLite reaches its maximum recursion limit or crashes with a stack overflow.",
                incorrect_sql="""CREATE TRIGGER trg_recurse AFTER UPDATE ON accounts
BEGIN
    UPDATE accounts SET balance = balance + 1; -- Fires trg_recurse indefinitely!
END;""",
                corrected_sql="-- Use BEFORE UPDATE to modify NEW.balance directly before save without recursion:\nCREATE TRIGGER trg_set_fee BEFORE UPDATE ON accounts\nBEGIN\n    -- In systems supporting it, modify NEW record or update separate audit table\n    INSERT INTO audit_log (account_id) VALUES (NEW.id);\nEND;",
            ),
            CommonMistake(
                pitfall="Putting heavyweight business logic and external network calls inside database triggers.",
                explanation="Triggers execute inside the active transaction lock. If a trigger makes an external API call or runs slow analytical queries, it stalls all concurrent transactions.",
                incorrect_sql="-- Heavyweight trigger sending email or external HTTP request",
                corrected_sql="-- Insert lightweight record into an 'outbox' table; have asynchronous worker process it outside transaction.",
            ),
        ],
        real_world_use_cases=[
            "Regulatory compliance: Creating append-only immutable audit logs tracking who modified financial or health data and when.",
            "Materialized counter maintenance: Updating cached aggregate counts (e.g. `followers_count`) whenever rows are inserted or deleted.",
            "Soft deletes: Using an INSTEAD OF DELETE trigger on views to set `is_deleted = TRUE` instead of physically removing tuples.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="p-6-21",
                slug="transaction-volume-audit-by-type",
                title="Ledger Audit: Aggregate Volume by Transaction Type",
                difficulty="easy",
                prompt="Write a query to aggregate all transactions by their `transaction_type`. Return `transaction_type`, `COUNT(*)` AS `total_count`, and `ROUND(SUM(amount), 2)` AS `total_amount`. Order by `total_amount` DESC.",
                starter_sql="-- Aggregate volume by transaction type\nSELECT \nFROM transactions\n",
                solution_sql="""SELECT 
    transaction_type,
    COUNT(*) AS total_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;""",
                hints=[
                    "Group by transaction_type.",
                    "Use COUNT(*) and ROUND(SUM(amount), 2).",
                    "Order by total_amount DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-22",
                slug="suspicious-high-value-transfers",
                title="AML Compliance Audit: Flag Suspicious Large Transfers",
                difficulty="medium",
                prompt="Anti-Money Laundering (AML) regulations flag any transfer exceeding $2,500. Write a query to find all transactions where `transaction_type IN ('transfer_in', 'transfer_out')` and `amount >= 2500.00`. Join `transactions` and `accounts`. Return `t.id` AS `transaction_id`, `t.account_id`, `a.customer_id`, `t.transaction_type`, and `t.amount`. Order by `t.amount` DESC, `transaction_id` ASC.",
                starter_sql="-- Find large transfers over 2,500\nSELECT \nFROM transactions t\n",
                solution_sql="""SELECT 
    t.id AS transaction_id,
    t.account_id,
    a.customer_id,
    t.transaction_type,
    t.amount
FROM transactions t
JOIN accounts a ON t.account_id = a.id
WHERE t.transaction_type IN ('transfer_in', 'transfer_out') AND t.amount >= 2500.00
ORDER BY t.amount DESC, transaction_id ASC;""",
                hints=[
                    "Join transactions with accounts on t.account_id = a.id.",
                    "Filter with \"t.transaction_type IN ('transfer_in', 'transfer_out') AND t.amount >= 2500.00\".",
                    "Order by t.amount DESC, transaction_id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-23",
                slug="customer-multi-account-balance-consolidation",
                title="Consolidated Account Portfolio Audit",
                difficulty="medium",
                prompt="Write a query to identify all customers who maintain a total balance exceeding $50,000 across all their accounts combined. Join `customers` and `accounts`. Return `c.id` AS `customer_id`, `c.first_name || ' ' || c.last_name` AS `customer_name`, `COUNT(a.id)` AS `account_count`, and `ROUND(SUM(a.balance), 2)` AS `portfolio_balance`. Order by `portfolio_balance` DESC.",
                starter_sql="-- Find customers with portfolio balance over 50,000\nSELECT \nFROM customers c\n",
                solution_sql="""SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(a.id) AS account_count,
    ROUND(SUM(a.balance), 2) AS portfolio_balance
FROM customers c
JOIN accounts a ON c.id = a.customer_id
GROUP BY c.id, customer_name
HAVING SUM(a.balance) > 50000.00
ORDER BY portfolio_balance DESC;""",
                hints=[
                    "Join customers with accounts.",
                    "Group by c.id, customer_name.",
                    "Use HAVING SUM(a.balance) > 50000.00.",
                    "Order by portfolio_balance DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-24",
                slug="uncredited-account-detection",
                title="Audit Inactive Accounts with Zero Inbound Transactions",
                difficulty="hard",
                prompt="Write a query to identify all accounts that have NEVER received an inbound transaction (`deposit` or `transfer_in`). Return `a.id` AS `account_id`, `a.customer_id`, `a.account_type`, and `a.balance`. Order by `a.id` ASC.",
                starter_sql="-- Find accounts with zero inbound transactions\nSELECT \nFROM accounts a\n",
                solution_sql="""SELECT 
    a.id AS account_id,
    a.customer_id,
    a.account_type,
    a.balance
FROM accounts a
WHERE a.id NOT IN (
    SELECT DISTINCT account_id 
    FROM transactions 
    WHERE transaction_type IN ('deposit', 'transfer_in')
)
ORDER BY a.id ASC;""",
                hints=[
                    "Use a subquery to select distinct account_id from transactions where transaction_type IN ('deposit', 'transfer_in').",
                    "Filter with 'WHERE a.id NOT IN (...)'.",
                    "Order by a.id ASC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
            PracticeQuestion(
                id="p-6-25",
                slug="branch-asset-utilization-ratio",
                title="Branch Asset Utilization: Loan Portfolio vs Total Assets",
                difficulty="medium",
                prompt="Write a query to evaluate each branch's asset utilization by comparing its total active loan portfolio to its recorded physical assets. Join `branches` and `loans` (filtering `loans.status = 'active'`). Return `b.id` AS `branch_id`, `b.name` AS `branch_name`, `b.assets`, `SUM(l.principal_amount)` AS `total_active_loans`, and `ROUND(SUM(l.principal_amount) * 100.0 / b.assets, 2)` AS `loan_to_asset_pct`. Order by `loan_to_asset_pct` DESC.",
                starter_sql="-- Compute loan-to-asset utilization percentage\nSELECT \nFROM branches b\n",
                solution_sql="""SELECT 
    b.id AS branch_id,
    b.name AS branch_name,
    b.assets,
    SUM(l.principal_amount) AS total_active_loans,
    ROUND(SUM(l.principal_amount) * 100.0 / b.assets, 2) AS loan_to_asset_pct
FROM branches b
JOIN loans l ON b.id = l.branch_id
WHERE l.status = 'active'
GROUP BY b.id, b.name, b.assets
ORDER BY loan_to_asset_pct DESC;""",
                hints=[
                    "Join branches and loans on b.id = l.branch_id.",
                    "Filter where l.status = 'active'.",
                    "Calculate ROUND(SUM(l.principal_amount) * 100.0 / b.assets, 2).",
                    "Order by loan_to_asset_pct DESC.",
                ],
                order_matters=True,
                check_column_names=True,
            ),
        ],
    ),
]
