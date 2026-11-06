from typing import List
from app.curriculum.models import (
    TopicLesson,
    ClauseExplanation,
    WorkedExample,
    CommonMistake,
    PracticeQuestion,
)

LEVEL_3_LESSONS: List[TopicLesson] = [
    TopicLesson(
        id="les-3-1",
        slug="inner-and-left-outer-joins",
        level_number=3,
        level_title="Level 3: Relational JOINs",
        title="Relational JOINs: INNER JOIN, LEFT JOIN & Anti-Joins",
        order_index=1,
        database_id="db-ecommerce",
        database_name="ecommerce_db",
        learning_objectives=[
            "Understand how Primary Keys (PK) and Foreign Keys (FK) establish relational integrity.",
            "Combine normalized tables using INNER JOIN to extract intersecting records.",
            "Use LEFT OUTER JOIN to preserve all records from the primary table even when secondary matches are absent.",
            "Implement the Anti-Join pattern (LEFT JOIN + WHERE IS NULL) to isolate orphan or inactive records.",
        ],
        prerequisites=[
            "Level 1: SQL Fundamentals and Level 2: Aggregations.",
        ],
        detailed_explanation="""Relational databases split data across specialized, normalized tables to eliminate redundancy. To query across these entities, SQL provides the `JOIN` operation.

1. The Relational Backbone: Primary & Foreign Keys:
- Primary Key (PK): A column or set of columns uniquely identifying every row in a table (e.g. `customers.id`).
- Foreign Key (FK): A column in a child table pointing to the PK of a parent table (e.g. `orders.customer_id REFERENCES customers.id`).

2. INNER JOIN:
Returns only rows that satisfy the join condition (`ON`) in BOTH tables. If a customer has no orders, they are completely excluded from an INNER JOIN between customers and orders.

3. LEFT OUTER JOIN:
Guarantees that ALL rows from the left-hand table are retained in the output. If a matching row exists in the right-hand table, its attributes are populated. If no matching row exists, the right-hand columns evaluate to NULL.

4. The Anti-Join Pattern:
One of the most frequently tested patterns in technical SQL interviews. By performing a LEFT JOIN and adding `WHERE right_table.id IS NULL`, you instantly isolate records that have NO counterpart in the secondary table (e.g. customers who have never bought anything, products with zero orders).""",
        syntax_reference="""-- Standard INNER JOIN
SELECT c.name, o.id AS order_id, o.total_amount
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;

-- Anti-Join Pattern (Missing Records)
SELECT c.id, c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;""",
        clause_breakdown=[
            ClauseExplanation(keyword="INNER JOIN", purpose="Produces the intersection of two tables based on matching predicates.", notes="Rows without a match on both sides are discarded."),
            ClauseExplanation(keyword="LEFT JOIN", purpose="Preserves all rows from the left table, padding missing right-table columns with NULL.", notes="The keyword OUTER is optional."),
            ClauseExplanation(keyword="ON", purpose="Specifies the join condition linking primary and foreign keys.", notes="Evaluated during table matching prior to the WHERE clause."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Customer Order History (INNER JOIN)",
                explanation="Extract completed orders along with customer contact names and order dates.",
                sql="SELECT c.first_name, c.last_name, o.id AS order_id, o.order_date, o.total_amount FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE o.status = 'COMPLETED' ORDER BY o.order_date DESC LIMIT 3;",
                columns=["first_name", "last_name", "order_id", "order_date", "total_amount"],
                rows=[
                    ["Sophia", "Chen", 1035, "2023-05-07", 52.50],
                    ["Natasha", "Ivanova", 1034, "2023-05-06", 189.99],
                    ["Amara", "Okafor", 1033, "2023-05-05", 44.99],
                ],
            ),
            WorkedExample(
                title="Example 2: All Customers & Order Counts (LEFT JOIN)",
                explanation="Count total orders per customer, including customers with zero orders.",
                sql="SELECT c.id, c.first_name, c.last_name, COUNT(o.id) AS total_orders FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name ORDER BY total_orders DESC, c.id ASC LIMIT 4;",
                columns=["id", "first_name", "last_name", "total_orders"],
                rows=[
                    [101, "Sophia", "Chen", 5],
                    [102, "Liam", "Davies", 3],
                    [104, "Kenji", "Sato", 3],
                    [103, "Elena", "Rostova", 2],
                ],
            ),
            WorkedExample(
                title="Example 3: Anti-Join (Customers Who Never Purchased)",
                explanation="Find all registered customer profiles who have never placed an order.",
                sql="SELECT c.id, c.first_name, c.last_name, c.email FROM customers c LEFT JOIN orders o ON c.id = o.customer_id WHERE o.id IS NULL ORDER BY c.id ASC LIMIT 4;",
                columns=["id", "first_name", "last_name", "email"],
                rows=[
                    [201, "Brandon", "Stark", "brandon.s@example.com"],
                    [202, "Astrid", "Lindgren", "astrid.l@example.se"],
                    [203, "Tariq", "Ziyad", "tariq.z@example.eg"],
                    [204, "Mei", "Ling", "mei.l@example.cn"],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Using COUNT(*) Instead of COUNT(column) in a LEFT JOIN",
                explanation="`COUNT(*)` counts the row created by the LEFT JOIN (which is 1 row with NULLs), incorrectly reporting that an inactive user has 1 order! Use `COUNT(orders.id)` to return 0.",
                incorrect_sql="SELECT c.id, COUNT(*) FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id;",
                corrected_sql="SELECT c.id, COUNT(o.id) FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id;",
            ),
            CommonMistake(
                pitfall="Accidentally Converting a LEFT JOIN into an INNER JOIN via WHERE",
                explanation="Placing a filter on the right table like `WHERE o.status = 'COMPLETED'` discards the NULL rows generated by the LEFT JOIN, converting it into an INNER JOIN.",
                incorrect_sql="SELECT c.id FROM customers c LEFT JOIN orders o ON c.id = o.customer_id WHERE o.status = 'COMPLETED';",
                corrected_sql="SELECT c.id FROM customers c LEFT JOIN orders o ON c.id = o.customer_id AND o.status = 'COMPLETED';",
            ),
        ],
        real_world_use_cases=[
            "Marketing Campaigns: Extracting churned users or inactive signups for win-back promotions.",
            "Catalog Management: Discovering products that have generated zero sales for clearance discounts.",
            "Data Pipeline Validation: Identifying orphan records where foreign keys fail to resolve.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-3-1-1",
                slug="customer-order-spending",
                title="Total Customer Lifetime Spending",
                difficulty="medium",
                prompt="Write a query to calculate total lifetime spending for each customer who has placed completed orders. Join customers c and orders o on customer_id where status = 'COMPLETED'. Return customer_id, first_name, last_name, and total_spent (sum of total_amount rounded to 2 decimal places). Order by total_spent DESC, customer_id ASC LIMIT 5.",
                starter_sql="SELECT c.id AS customer_id, c.first_name, c.last_name, ROUND(SUM(o.total_amount), 2) AS total_spent\nFROM customers c\nINNER JOIN orders o ON c.id = o.customer_id\nWHERE o.status = 'COMPLETED'\nGROUP BY c.id, c.first_name, c.last_name\nORDER BY total_spent DESC, customer_id ASC\nLIMIT 5;",
                solution_sql="SELECT c.id AS customer_id, c.first_name, c.last_name, ROUND(SUM(o.total_amount), 2) AS total_spent FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE o.status = 'COMPLETED' GROUP BY c.id, c.first_name, c.last_name ORDER BY total_spent DESC, customer_id ASC LIMIT 5;",
                hints=["Join on `c.id = o.customer_id`.", "Group by customer attributes and filter on `o.status = 'COMPLETED'`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-1-2",
                slug="products-with-zero-sales",
                title="Find Catalogue Products with Zero Sales",
                difficulty="medium",
                prompt="In ecommerce_db, find all products that have never been ordered (do not appear in order_items). Return product id, name, and price ordered by id ASC.",
                starter_sql="SELECT p.id, p.name, p.price\nFROM products p\nLEFT JOIN order_items oi ON p.id = oi.product_id\nWHERE oi.id IS NULL\nORDER BY p.id ASC;",
                solution_sql="SELECT p.id, p.name, p.price FROM products p LEFT JOIN order_items oi ON p.id = oi.product_id WHERE oi.id IS NULL ORDER BY p.id ASC;",
                hints=["Perform a LEFT JOIN between products p and order_items oi.", "Filter with `WHERE oi.id IS NULL`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-1-3",
                slug="orders-with-product-categories",
                title="Order Details with Category Names",
                difficulty="medium",
                prompt="Join order_items oi, products p on oi.product_id = p.id, and categories c on p.category_id = c.id. Return oi.order_id, p.name AS product_name, c.name AS category_name, and oi.quantity. Order by oi.order_id ASC, p.name ASC LIMIT 5.",
                starter_sql="SELECT oi.order_id, p.name AS product_name, c.name AS category_name, oi.quantity\nFROM order_items oi\nJOIN products p ON oi.product_id = p.id\nJOIN categories c ON p.category_id = c.id\nORDER BY oi.order_id ASC, product_name ASC\nLIMIT 5;",
                solution_sql="SELECT oi.order_id, p.name AS product_name, c.name AS category_name, oi.quantity FROM order_items oi JOIN products p ON oi.product_id = p.id JOIN categories c ON p.category_id = c.id ORDER BY oi.order_id ASC, product_name ASC LIMIT 5;",
                hints=["Chain two joins: order_items -> products -> categories.", "Use consistent table aliases."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-1-4",
                slug="count-orders-per-customer-all",
                title="Customer Order Count (Including Inactive)",
                difficulty="easy",
                prompt="Select c.id, c.first_name, c.last_name, and COUNT(o.id) AS order_count from customers c LEFT JOIN orders o on c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name HAVING order_count = 0 ORDER BY c.id ASC LIMIT 5.",
                starter_sql="SELECT c.id, c.first_name, c.last_name, COUNT(o.id) AS order_count\nFROM customers c\nLEFT JOIN orders o ON c.id = o.customer_id\nGROUP BY c.id, c.first_name, c.last_name\nHAVING order_count = 0\nORDER BY c.id ASC\nLIMIT 5;",
                solution_sql="SELECT c.id, c.first_name, c.last_name, COUNT(o.id) AS order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name HAVING order_count = 0 ORDER BY c.id ASC LIMIT 5;",
                hints=["Use `LEFT JOIN` and `COUNT(o.id)`.", "Filter for `order_count = 0` in HAVING."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-1-5",
                slug="payment-method-revenue-breakdown",
                title="Revenue by Payment Gateway Method",
                difficulty="medium",
                prompt="Join orders o and payments p on o.id = p.order_id. Calculate the sum of p.amount (rounded to 2 decimal places as total_cleared) and the count of transactions as txn_count for each payment_method where payment_status = 'SUCCESSFUL'. Order by total_cleared DESC.",
                starter_sql="SELECT p.payment_method, ROUND(SUM(p.amount), 2) AS total_cleared, COUNT(*) AS txn_count\nFROM payments p\nWHERE p.payment_status = 'SUCCESSFUL'\nGROUP BY p.payment_method\nORDER BY total_cleared DESC;",
                solution_sql="SELECT p.payment_method, ROUND(SUM(p.amount), 2) AS total_cleared, COUNT(*) AS txn_count FROM payments p WHERE p.payment_status = 'SUCCESSFUL' GROUP BY p.payment_method ORDER BY total_cleared DESC;",
                hints=["Group by `p.payment_method`.", "Filter with `WHERE p.payment_status = 'SUCCESSFUL'`."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-3-2",
        slug="self-joins-cross-joins-unions",
        level_number=3,
        level_title="Level 3: Relational JOINs",
        title="SELF JOINs, CROSS JOINs, and Set Operations (UNION)",
        order_index=2,
        database_id="db-company",
        database_name="company_db",
        learning_objectives=[
            "Model organizational hierarchies and tree structures using SELF JOINs.",
            "Generate Cartesian products using CROSS JOIN for grid generation.",
            "Combine independent result sets using UNION and UNION ALL.",
            "Understand the performance difference between UNION (deduplicating sort) and UNION ALL (fast append).",
        ],
        prerequisites=[
            "INNER & LEFT JOINs (Level 3, Lesson 1).",
        ],
        detailed_explanation="""Beyond standard parent-child table joins, relational systems provide powerful mechanisms to join a table to itself and perform mathematical set unions.

1. SELF JOIN:
A SELF JOIN is a regular join in which a table is joined with itself. It is primarily used to query hierarchical data stored in a single table, such as employee-to-manager relationships or category parent-child trees:
```sql
SELECT 
    e.first_name AS employee,
    m.first_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```
Different aliases (`e` for employee and `m` for manager) are mandatory to treat the single table as two distinct entities.

2. CROSS JOIN:
Produces the Cartesian product of two tables—combining every row of Table A with every row of Table B (size: `len(A) * len(B)`). Useful for generating complete matrix combinations (e.g. all branches × all months).

3. Set Operations: UNION vs. UNION ALL:
Combines rows from two queries with matching column counts and data types:
- `UNION`: Appends rows and removes all duplicate rows across sets (requires a sort or hash table).
- `UNION ALL`: Appends rows directly without checking for duplicates (significantly faster; use whenever duplicates are impossible or acceptable).""",
        syntax_reference="""-- Self-Join for Hierarchies
SELECT e.first_name AS employee, m.first_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Set Union
SELECT column_1, column_2 FROM table_a
UNION ALL
SELECT column_1, column_2 FROM table_b;""",
        clause_breakdown=[
            ClauseExplanation(keyword="SELF JOIN", purpose="Joins a table to itself using separate table aliases.", notes="Essential for parent-child hierarchies."),
            ClauseExplanation(keyword="CROSS JOIN", purpose="Produces every possible combination of rows between two tables.", notes="Avoid on large tables without strict WHERE filters."),
            ClauseExplanation(keyword="UNION", purpose="Appends two result sets and removes duplicate rows.", notes="Both queries must project the exact same number of compatible columns."),
            ClauseExplanation(keyword="UNION ALL", purpose="Appends two result sets preserving all duplicate rows.", notes="Significantly faster than UNION because it skips the deduplication sort."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Employee to Direct Manager Mapping (SELF JOIN)",
                explanation="Find each active employee and the full name of their direct manager. Preserves the CEO using a LEFT JOIN.",
                sql="SELECT e.id AS emp_id, e.first_name || ' ' || e.last_name AS employee_name, COALESCE(m.first_name || ' ' || m.last_name, 'None (Top Executive)') AS manager_name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id WHERE e.status = 'ACTIVE' ORDER BY e.id ASC LIMIT 5;",
                columns=["emp_id", "employee_name", "manager_name"],
                rows=[
                    [1, "Evelyn Vance", "None (Top Executive)"],
                    [2, "Marcus Sterling", "Evelyn Vance"],
                    [3, "Nadia Kowalski", "Evelyn Vance"],
                    [4, "Julian Mercer", "Evelyn Vance"],
                    [5, "Victoria Stone", "Evelyn Vance"],
                ],
            ),
            WorkedExample(
                title="Example 2: Peers Sharing the Same Manager (SELF JOIN)",
                explanation="Find pairs of distinct employees who report to the same manager in department 7.",
                sql="SELECT e1.first_name AS emp_1, e2.first_name AS emp_2, e1.manager_id FROM employees e1 JOIN employees e2 ON e1.manager_id = e2.manager_id AND e1.id < e2.id WHERE e1.department_id = 7 AND e1.manager_id IS NOT NULL;",
                columns=["emp_1", "emp_2", "manager_id"],
                rows=[
                    ["Elle", "Harvey", 51],
                ],
            ),
            WorkedExample(
                title="Example 3: Unified Activity Ledger (UNION ALL)",
                explanation="Combine active employee names and consultant names into a single unified directory.",
                sql="SELECT first_name, last_name, 'Internal Staff' AS affiliation FROM employees WHERE department_id IS NOT NULL AND status = 'ACTIVE' UNION ALL SELECT first_name, last_name, 'External Contractor' AS affiliation FROM employees WHERE manager_id IS NULL AND id > 50 LIMIT 4;",
                columns=["first_name", "last_name", "affiliation"],
                rows=[
                    ["Evelyn", "Vance", "Internal Staff"],
                    ["Marcus", "Sterling", "Internal Staff"],
                    ["Nadia", "Kowalski", "Internal Staff"],
                    ["Julian", "Mercer", "Internal Staff"],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Using UNION When UNION ALL is Sufficient",
                explanation="UNION forces the database to sort and hash the entire combined dataset to remove duplicates, causing severe performance penalties on large tables.",
                incorrect_sql="SELECT id FROM orders_2022 UNION SELECT id FROM orders_2023;",
                corrected_sql="SELECT id FROM orders_2022 UNION ALL SELECT id FROM orders_2023;",
            ),
            CommonMistake(
                pitfall="Self-Join Duplicate Pairings (e1.id != e2.id)",
                explanation="Using `!=` returns both (Alice, Bob) and (Bob, Alice). Use `e1.id < e2.id` to prevent duplicate mirror pairs.",
                incorrect_sql="JOIN employees e2 ON e1.manager_id = e2.manager_id AND e1.id != e2.id",
                corrected_sql="JOIN employees e2 ON e1.manager_id = e2.manager_id AND e1.id < e2.id",
            ),
        ],
        real_world_use_cases=[
            "HR Org Charts: Visualizing management chains and direct reports.",
            "Cross-Product Grids: Generating test matrices (e.g. all store locations × all dates in year).",
            "Consolidated Ledgers: Merging archived historical transactions with real-time operational tables.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-3-2-1",
                slug="managers-and-their-headcounts",
                title="Count Direct Reports per Manager",
                difficulty="medium",
                prompt="Using a self-join or join on employees, find each manager's id and full name (first_name || ' ' || last_name AS manager_name), and count their direct reports as report_count. Filter for managers who have at least 3 direct reports. Order by report_count DESC, m.id ASC.",
                starter_sql="SELECT m.id AS manager_id, m.first_name || ' ' || m.last_name AS manager_name, COUNT(e.id) AS report_count\nFROM employees e\nJOIN employees m ON e.manager_id = m.id\nGROUP BY m.id, manager_name\nHAVING report_count >= 3\nORDER BY report_count DESC, m.id ASC;",
                solution_sql="SELECT m.id AS manager_id, m.first_name || ' ' || m.last_name AS manager_name, COUNT(e.id) AS report_count FROM employees e JOIN employees m ON e.manager_id = m.id GROUP BY m.id, manager_name HAVING report_count >= 3 ORDER BY report_count DESC, m.id ASC;",
                hints=["Join `employees e` to `employees m` on `e.manager_id = m.id`.", "Group by manager id and filter in HAVING."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-2-2",
                slug="union-customer-and-employee-contacts",
                title="Union Directory of Names",
                difficulty="easy",
                prompt="Combine first_name and email from company_db employees with first_name and email from ecommerce_db customers using UNION. Order by email ASC LIMIT 5.",
                starter_sql="SELECT first_name, email FROM employees\nUNION\nSELECT first_name, email FROM customers\nORDER BY email ASC\nLIMIT 5;",
                solution_sql="SELECT first_name, email FROM employees UNION SELECT first_name, email FROM customers ORDER BY email ASC LIMIT 5;",
                hints=["Select matching columns: first_name, email.", "Use UNION and ORDER BY email ASC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-2-3",
                slug="employees-hired-same-day",
                title="Identify Employees Hired on the Same Day",
                difficulty="hard",
                prompt="Find pairs of distinct employees in company_db who share the exact same hire_date. Return e1.first_name AS emp1_name, e2.first_name AS emp2_name, and e1.hire_date. Ensure e1.id < e2.id to avoid duplicate pairings. Order by e1.hire_date ASC, emp1_name ASC LIMIT 5.",
                starter_sql="SELECT e1.first_name AS emp1_name, e2.first_name AS emp2_name, e1.hire_date\nFROM employees e1\nJOIN employees e2 ON e1.hire_date = e2.hire_date AND e1.id < e2.id\nORDER BY e1.hire_date ASC, emp1_name ASC\nLIMIT 5;",
                solution_sql="SELECT e1.first_name AS emp1_name, e2.first_name AS emp2_name, e1.hire_date FROM employees e1 JOIN employees e2 ON e1.hire_date = e2.hire_date AND e1.id < e2.id ORDER BY e1.hire_date ASC, emp1_name ASC LIMIT 5;",
                hints=["Join on `e1.hire_date = e2.hire_date`.", "Add condition `e1.id < e2.id`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-2-4",
                slug="all-departments-all-branches-cross",
                title="Cartesian Combinations of Locations",
                difficulty="easy",
                prompt="In company_db, perform a CROSS JOIN between departments d and projects p where d.id = 1. Return d.name AS dept_name and p.name AS project_name. Order by project_name ASC LIMIT 4.",
                starter_sql="SELECT d.name AS dept_name, p.name AS project_name\nFROM departments d\nCROSS JOIN projects p\nWHERE d.id = 1\nORDER BY project_name ASC\nLIMIT 4;",
                solution_sql="SELECT d.name AS dept_name, p.name AS project_name FROM departments d CROSS JOIN projects p WHERE d.id = 1 ORDER BY project_name ASC LIMIT 4;",
                hints=["Use `CROSS JOIN projects p`.", "Filter `WHERE d.id = 1`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-3-2-5",
                slug="employees-reporting-to-vp-engineering",
                title="Direct Reports of Marcus Sterling",
                difficulty="medium",
                prompt="Find first_name, last_name, and title of all employees who report directly to Marcus Sterling (manager_id = 2) in company_db. Order by last_name ASC.",
                starter_sql="SELECT first_name, last_name, title\nFROM employees\nWHERE manager_id = 2\nORDER BY last_name ASC;",
                solution_sql="SELECT first_name, last_name, title FROM employees WHERE manager_id = 2 ORDER BY last_name ASC;",
                hints=["Filter for `manager_id = 2`.", "Sort on `last_name ASC`."],
                order_matters=True,
            ),
        ],
    ),
]
