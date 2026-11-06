from typing import List
from app.curriculum.models import (
    TopicLesson,
    ClauseExplanation,
    WorkedExample,
    CommonMistake,
    PracticeQuestion,
)

LEVEL_1_LESSONS: List[TopicLesson] = [
    TopicLesson(
        id="les-1-1",
        slug="select-distinct-projection",
        level_number=1,
        level_title="Level 1: SQL Fundamentals",
        title="Column Projections, SELECT, and DISTINCT",
        order_index=1,
        database_id="db-ecommerce",
        database_name="ecommerce_db",
        learning_objectives=[
            "Understand the relational model: relations, tuples, and attributes.",
            "Master column projection using SELECT to retrieve specific fields from a table.",
            "Use DISTINCT to eliminate duplicate row results from tabular outputs.",
            "Define explicit column aliases using the AS keyword for clean reporting.",
        ],
        prerequisites=[
            "None. Designed as the foundational entry point into relational databases.",
        ],
        detailed_explanation="""In the relational database model, data is organized into structured tables (relations) where each horizontal row represents an individual entity instance (tuple) and each vertical column represents a specific attribute.

The SELECT statement forms the fundamental retrieval command in SQL. Unlike procedural programming languages where you write loops to fetch records, SQL is a declarative language: you describe the exact fields and transformation you want, and the database engine determines the most optimal retrieval path.

When executing a SELECT query, the FROM clause is evaluated first to determine the source table. The database engine then projects only the requested columns into memory.

By default, SQL preserves all qualifying rows, even if multiple rows evaluate to the exact same values across projected columns. To eliminate duplicate values and retain only unique combinations, the DISTINCT modifier is placed immediately after SELECT.""",
        syntax_reference="""-- Basic Column Projection
SELECT column_1, column_2, column_3
FROM table_name;

-- Projection with Aliases and Unique Values
SELECT DISTINCT 
    column_name AS alias_name,
    category AS category_label
FROM table_name;""",
        clause_breakdown=[
            ClauseExplanation(keyword="SELECT", purpose="Specifies the list of columns, expressions, or computations to be included in the final tabular output.", notes="Evaluated after FROM, WHERE, and GROUP BY clauses."),
            ClauseExplanation(keyword="DISTINCT", purpose="Forces the query engine to filter out duplicate rows across all projected columns.", notes="Applies to the entire projected row tuple, not individual columns."),
            ClauseExplanation(keyword="AS", purpose="Assigns an explicit label (alias) to a projected column or table expression.", notes="Aliases improve readability and define column names in client API responses."),
            ClauseExplanation(keyword="FROM", purpose="Specifies the target table from which records are to be read.", notes="Always evaluated first in standard query processing."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Projecting Specific Customer Attributes",
                explanation="Extract customer first name, last name, and contact email from the customers table.",
                sql="SELECT first_name, last_name, email FROM customers LIMIT 3;",
                columns=["first_name", "last_name", "email"],
                rows=[
                    ["Sophia", "Chen", "sophia.c@example.com"],
                    ["Liam", "Davies", "liam.d@example.co.uk"],
                    ["Elena", "Rostova", "elena.r@example.de"],
                ],
            ),
            WorkedExample(
                title="Example 2: Discovering Unique Customer Countries",
                explanation="Retrieve all distinct geographic countries where platform customers reside.",
                sql="SELECT DISTINCT country FROM customers ORDER BY country ASC LIMIT 4;",
                columns=["country"],
                rows=[
                    ["Argentina"],
                    ["Brazil"],
                    ["China"],
                    ["Denmark"],
                ],
            ),
            WorkedExample(
                title="Example 3: Column Aliasing for Clean Business Reporting",
                explanation="Project product title and price with clear analytical labels.",
                sql="SELECT name AS product_title, price AS retail_usd FROM products LIMIT 3;",
                columns=["product_title", "retail_usd"],
                rows=[
                    ["Pro Wireless Mechanical Keyboard", 149.99],
                    ["Ergonomic Precision Mouse", 79.50],
                    ["UltraWide 34-Inch Curved Monitor", 499.00],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Using SELECT * in Production Code",
                explanation="Fetching all columns wastes I/O bandwidth, breaks caching, and causes runtime failures if table schemas change.",
                incorrect_sql="SELECT * FROM customers;",
                corrected_sql="SELECT id, first_name, last_name, email FROM customers;",
            ),
            CommonMistake(
                pitfall="Thinking DISTINCT Applies to Only One Column",
                explanation="Writing `SELECT DISTINCT col1, col2` evaluates uniqueness across the combination of BOTH col1 and col2, not just col1.",
                incorrect_sql="SELECT DISTINCT(country), city FROM customers;",
                corrected_sql="SELECT DISTINCT country, city FROM customers;",
            ),
            CommonMistake(
                pitfall="Trailing Comma in SELECT List",
                explanation="Placing a comma after the final column before the FROM clause causes an immediate SQL syntax error.",
                incorrect_sql="SELECT first_name, last_name, FROM customers;",
                corrected_sql="SELECT first_name, last_name FROM customers;",
            ),
        ],
        real_world_use_cases=[
            "Data Pipeline Ingestion: Projecting only required telemetry attributes to minimize network transfer costs.",
            "Dropdown Filters: Fetching distinct category names or unique country lists for frontend UI select inputs.",
            "Compliance Reporting: Exporting sanitized customer rosters omitting sensitive financial columns.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-1-1-1",
                slug="unique-product-categories",
                title="List All Unique Product Category Identifiers",
                difficulty="easy",
                prompt="Write a query to return all unique category_id values present in the products table. Return a single column named category_id ordered ascending.",
                starter_sql="-- Select unique category_id values\nSELECT ",
                solution_sql="SELECT DISTINCT category_id FROM products ORDER BY category_id ASC;",
                hints=["Use the DISTINCT keyword immediately after SELECT.", "Add ORDER BY category_id ASC to sort the output."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-1-2",
                slug="customer-contact-roster",
                title="Format Customer Names with Custom Aliases",
                difficulty="easy",
                prompt="Select first_name as given_name, last_name as family_name, and email from the customers table. Limit the output to the first 5 records ordered by id ASC.",
                starter_sql="SELECT \n    -- Add column aliases using AS\nFROM customers\nORDER BY id ASC\nLIMIT 5;",
                solution_sql="SELECT first_name AS given_name, last_name AS family_name, email FROM customers ORDER BY id ASC LIMIT 5;",
                hints=["Use `AS given_name` after `first_name`.", "Order by id ASC and add LIMIT 5."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-1-3",
                slug="distinct-order-statuses",
                title="Audit Distinct Order Fulfillment Statuses",
                difficulty="easy",
                prompt="Write a query to return all distinct order fulfillment statuses from the orders table. Order the output alphabetically ascending.",
                starter_sql="SELECT \nFROM orders;",
                solution_sql="SELECT DISTINCT status FROM orders ORDER BY status ASC;",
                hints=["Target the `status` column in the `orders` table.", "Use DISTINCT to remove duplicates."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-1-4",
                slug="active-cities-directory",
                title="Unique Country and City Pairs",
                difficulty="medium",
                prompt="Write a query to retrieve all distinct combinations of country and city where customers reside. Sort the result by country ASC, then city ASC.",
                starter_sql="SELECT \nFROM customers;",
                solution_sql="SELECT DISTINCT country, city FROM customers ORDER BY country ASC, city ASC;",
                hints=["Select both country and city following DISTINCT.", "Include both columns in the ORDER BY clause."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-1-5",
                slug="catalog-pricing-preview",
                title="Product Pricing Overview",
                difficulty="easy",
                prompt="Return the name and price of all products from the products table. Alias the name as product_name and price as unit_usd. Order by price DESC and limit to 5 records.",
                starter_sql="SELECT \nFROM products;",
                solution_sql="SELECT name AS product_name, price AS unit_usd FROM products ORDER BY price DESC LIMIT 5;",
                hints=["Use AS for both column aliases.", "Sort using ORDER BY price DESC and LIMIT 5."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-1-2",
        slug="where-filtering-operators",
        level_number=1,
        level_title="Level 1: SQL Fundamentals",
        title="Filtering Rows with WHERE and Logical Operators",
        order_index=2,
        database_id="db-company",
        database_name="company_db",
        learning_objectives=[
            "Understand how the WHERE clause filters rows prior to projection.",
            "Use standard comparison operators (=, !=, <, >, <=, >=).",
            "Combine boolean conditions using AND, OR, and NOT.",
            "Handle operator precedence correctly using parentheses.",
        ],
        prerequisites=[
            "SELECT and Column Projections (Level 1, Lesson 1).",
        ],
        detailed_explanation="""While SELECT controls vertical slicing (which columns to return), the WHERE clause controls horizontal slicing (which rows qualify).

In relational query execution order, the WHERE clause is evaluated immediately after FROM. Every candidate row is tested against a boolean predicate (an expression that evaluates to TRUE, FALSE, or UNKNOWN). Only rows that evaluate strictly to TRUE are passed to the next stage.

Comparison operators allow evaluating numeric ranges, date thresholds, and string equalities:
- Equality: `=` and Inequality: `<>` or `!=`
- Relative comparisons: `<`, `<=`, `>`, `>=`

Multiple predicates can be combined using boolean logic:
- `AND`: True if and only if both conditions are TRUE.
- `OR`: True if either condition is TRUE.
- `NOT`: Inverts the truth value of a condition.

Crucially, in SQL operator precedence, `AND` has higher precedence than `OR`. Writing `A OR B AND C` evaluates as `A OR (B AND C)`. Always use parentheses `(A OR B) AND C` to make business intent explicit.""",
        syntax_reference="""SELECT column_1, column_2
FROM table_name
WHERE condition_1 AND (condition_2 OR condition_3);""",
        clause_breakdown=[
            ClauseExplanation(keyword="WHERE", purpose="Filters rows from the source table based on one or more boolean criteria.", notes="Evaluated row-by-row before GROUP BY or SELECT projections."),
            ClauseExplanation(keyword="AND", purpose="Logical conjunction requiring all connected predicates to be true.", notes="Has higher precedence than OR."),
            ClauseExplanation(keyword="OR", purpose="Logical disjunction requiring at least one connected predicate to be true.", notes="Lower precedence than AND; group with parentheses when mixing."),
            ClauseExplanation(keyword="NOT", purpose="Negates a boolean predicate.", notes="Can be placed before comparisons, IN, BETWEEN, or LIKE."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: High-Earner Department Query",
                explanation="Find all active employees in Engineering (department_id = 2) who hold a Senior or Staff title.",
                sql="SELECT id, first_name, last_name, title FROM employees WHERE department_id = 2 AND status = 'ACTIVE' AND title LIKE 'Senior%' LIMIT 3;",
                columns=["id", "first_name", "last_name", "title"],
                rows=[
                    [15, "Kenji", "Sato", "Senior DevOps Architect"],
                    [21, "Priya", "Sharma", "Senior Database Architect"],
                    [28, "Ethan", "Hunt", "Senior Application Security Specialist"],
                ],
            ),
            WorkedExample(
                title="Example 2: Parentheses & Precedence Filtering",
                explanation="Find employees who are either in Executive Board (dept 1) OR Legal (dept 7), but hired after 2020.",
                sql="SELECT id, first_name, last_name, department_id, hire_date FROM employees WHERE (department_id = 1 OR department_id = 7) AND hire_date >= '2020-01-01' ORDER BY hire_date ASC;",
                columns=["id", "first_name", "last_name", "department_id", "hire_date"],
                rows=[
                    [52, "Elle", "Woods", 7, "2020-06-15"],
                    [53, "Harvey", "Specter", 7, "2021-01-05"],
                ],
            ),
            WorkedExample(
                title="Example 3: Negating Unwanted Categories with NOT",
                explanation="Find all departments that are not in San Francisco and have a budget of at least $1,500,000.",
                sql="SELECT id, name, location, budget FROM departments WHERE NOT location = 'San Francisco, CA' AND budget >= 1500000.00;",
                columns=["id", "name", "location", "budget"],
                rows=[
                    [3, "Product & Design", "New York, NY", 1800000.00],
                    [4, "Marketing & Growth", "London, UK", 2100000.00],
                    [5, "Sales & Accounts", "Austin, TX", 3500000.00],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Operator Precedence Confusion (AND vs OR)",
                explanation="Omitting parentheses when mixing AND with OR leads to unexpected extra rows.",
                incorrect_sql="SELECT * FROM employees WHERE department_id = 2 OR department_id = 3 AND status = 'TERMINATED';",
                corrected_sql="SELECT * FROM employees WHERE (department_id = 2 OR department_id = 3) AND status = 'TERMINATED';",
            ),
            CommonMistake(
                pitfall="Using Column Aliases Inside the WHERE Clause",
                explanation="Column aliases defined in SELECT are not yet available in WHERE because WHERE executes first.",
                incorrect_sql="SELECT base_salary * 12 AS annual_comp FROM salaries WHERE annual_comp > 150000;",
                corrected_sql="SELECT base_salary * 12 AS annual_comp FROM salaries WHERE (base_salary * 12) > 150000;",
            ),
        ],
        real_world_use_cases=[
            "Security Auditing: Isolating administrative staff or accounts with elevated role credentials.",
            "E-Commerce Cart Management: Finding orders abandoned within the past 48 hours for recovery emails.",
            "Financial Risk: Filtering for transactions where amount exceeds $10,000 flagged for compliance review.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-1-2-1",
                slug="active-engineering-staff",
                title="Filter Active Engineering Personnel",
                difficulty="easy",
                prompt="Retrieve first_name, last_name, and title for all employees in department_id = 2 who have status = 'ACTIVE'. Order by last_name ASC.",
                starter_sql="SELECT \nFROM employees\nWHERE \nORDER BY last_name ASC;",
                solution_sql="SELECT first_name, last_name, title FROM employees WHERE department_id = 2 AND status = 'ACTIVE' ORDER BY last_name ASC;",
                hints=["Filter on `department_id = 2` and `status = 'ACTIVE'` using the AND operator."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-2-2",
                slug="high-budget-departments",
                title="Identify High-Budget Operational Units",
                difficulty="easy",
                prompt="Find the name and budget of all departments with a budget strictly greater than 2,000,000.00. Order by budget DESC.",
                starter_sql="SELECT \nFROM departments;",
                solution_sql="SELECT name, budget FROM departments WHERE budget > 2000000.00 ORDER BY budget DESC;",
                hints=["Use `WHERE budget > 2000000.00`.", "Order by budget DESC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-2-3",
                slug="leadership-roster-filter",
                title="Multi-Department Leadership Filter",
                difficulty="medium",
                prompt="Find id, first_name, last_name, and department_id for employees in department 2, 3, or 4 who were hired on or after '2021-01-01'. Order by id ASC.",
                starter_sql="SELECT id, first_name, last_name, department_id\nFROM employees\nWHERE \nORDER BY id ASC;",
                solution_sql="SELECT id, first_name, last_name, department_id FROM employees WHERE (department_id = 2 OR department_id = 3 OR department_id = 4) AND hire_date >= '2021-01-01' ORDER BY id ASC;",
                hints=["Wrap the OR conditions for department_id in parentheses.", "Connect with `AND hire_date >= '2021-01-01'`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-2-4",
                slug="non-active-staff",
                title="Identify Non-Active Employees",
                difficulty="easy",
                prompt="Select id, first_name, last_name, and status for all employees whose status is NOT 'ACTIVE'. Order by id ASC.",
                starter_sql="SELECT \nFROM employees;",
                solution_sql="SELECT id, first_name, last_name, status FROM employees WHERE status != 'ACTIVE' ORDER BY id ASC;",
                hints=["Use either `status != 'ACTIVE'` or `status <> 'ACTIVE'` or `NOT status = 'ACTIVE'`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-2-5",
                slug="executive-hire-filter",
                title="Early Executive Hires",
                difficulty="medium",
                prompt="Find first_name, last_name, title, and hire_date for employees with manager_id = 1 who were hired before '2019-01-01'. Order by hire_date ASC.",
                starter_sql="SELECT \nFROM employees;",
                solution_sql="SELECT first_name, last_name, title, hire_date FROM employees WHERE manager_id = 1 AND hire_date < '2019-01-01' ORDER BY hire_date ASC;",
                hints=["Check `manager_id = 1` and `hire_date < '2019-01-01'`."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-1-3",
        slug="in-between-like-pattern-matching",
        level_number=1,
        level_title="Level 1: SQL Fundamentals",
        title="Pattern Matching & Range Filtering: IN, BETWEEN, LIKE",
        order_index=3,
        database_id="db-ecommerce",
        database_name="ecommerce_db",
        learning_objectives=[
            "Use the IN operator to test membership within discrete value sets.",
            "Use the BETWEEN operator for clean, inclusive range checks on numbers and dates.",
            "Master wildcard pattern matching with LIKE (% and _).",
            "Combine NOT with IN, BETWEEN, and LIKE for exclusion filters.",
        ],
        prerequisites=[
            "WHERE Filtering and Comparison Operators (Level 1, Lesson 2).",
        ],
        detailed_explanation="""Writing multiple chained OR conditions (`status = 'COMPLETED' OR status = 'SHIPPED'`) becomes verbose and error-prone. SQL provides high-level relational predicates for cleaner, more readable filtering.

1. The IN Operator:
Tests whether a column's value matches any element in a discrete list of literals or subquery results.
`WHERE country IN ('United States', 'Canada', 'United Kingdom')`
This is semantically equivalent to chained OR equalities, but allows database optimizers to construct efficient binary searches or hash lookups.

2. The BETWEEN Operator:
Performs an inclusive range evaluation: `WHERE price BETWEEN 50.00 AND 150.00` is equivalent to `WHERE price >= 50.00 AND price <= 150.00`.
Both boundary endpoints are included. BETWEEN works on numbers, ISO dates (`'2023-01-01' AND '2023-06-30'`), and alphabetical strings.

3. The LIKE Operator (Pattern Matching):
Performs string pattern matching using two standard wildcards:
- `%`: Matches zero, one, or multiple arbitrary characters. E.g., `LIKE 'Pro%'` matches 'Pro', 'Product', 'Professional'.
- `_`: Matches exactly one single character. E.g., `LIKE 'CS_01'` matches 'CS-01', 'CS101'.""",
        syntax_reference="""-- Membership Check
SELECT * FROM table_name WHERE status IN ('ACTIVE', 'PENDING');

-- Inclusive Range Check
SELECT * FROM table_name WHERE price BETWEEN 100.00 AND 300.00;

-- Wildcard String Matching
SELECT * FROM table_name WHERE email LIKE '%@company.com';""",
        clause_breakdown=[
            ClauseExplanation(keyword="IN", purpose="Evaluates whether a value matches any item in a comma-separated list of literals.", notes="Can be negated with NOT IN."),
            ClauseExplanation(keyword="BETWEEN", purpose="Evaluates whether a value falls within an inclusive numeric, date, or text range.", notes="Always includes both the start and end boundary values."),
            ClauseExplanation(keyword="LIKE", purpose="Matches string values against patterns containing % (multiple characters) or _ (single character).", notes="Case-sensitivity depends on database collation; in SQLite, LIKE on ASCII text is case-insensitive by default."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Country Membership Filtering with IN",
                explanation="Find all customers located in the United States, United Kingdom, or Germany.",
                sql="SELECT id, first_name, last_name, country FROM customers WHERE country IN ('United States', 'United Kingdom', 'Germany') LIMIT 4;",
                columns=["id", "first_name", "last_name", "country"],
                rows=[
                    [101, "Sophia", "Chen", "United States"],
                    [102, "Liam", "Davies", "United Kingdom"],
                    [103, "Elena", "Rostova", "Germany"],
                    [108, "Hannah", "Schmidt", "Germany"],
                ],
            ),
            WorkedExample(
                title="Example 2: Product Price Range Filtering with BETWEEN",
                explanation="Find all active catalogue products priced between $50.00 and $150.00 inclusive.",
                sql="SELECT id, name, price FROM products WHERE price BETWEEN 50.00 AND 150.00 ORDER BY price ASC LIMIT 4;",
                columns=["id", "name", "price"],
                rows=[
                    [502, "Ergonomic Precision Mouse", 79.50],
                    [510, "Merino Wool Lightweight Hoodie", 95.00],
                    [509, "Waterproof Breathable Rain Jacket", 120.00],
                    [511, "Trail Running Performance Shoes", 135.00],
                ],
            ),
            WorkedExample(
                title="Example 3: Search Substrings with LIKE Wildcards",
                explanation="Find all products whose title contains 'Keyboard' or 'Mouse'.",
                sql="SELECT id, name, price FROM products WHERE name LIKE '%Keyboard%' OR name LIKE '%Mouse%';",
                columns=["id", "name", "price"],
                rows=[
                    [501, "Pro Wireless Mechanical Keyboard", 149.99],
                    [502, "Ergonomic Precision Mouse", 79.50],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Assuming BETWEEN is Exclusive of Endpoints",
                explanation="BETWEEN is strictly inclusive: `BETWEEN 1 AND 5` includes both 1 and 5.",
                incorrect_sql="-- Expecting 100 to be excluded\nSELECT * FROM orders WHERE total_amount BETWEEN 50 AND 100;",
                corrected_sql="SELECT * FROM orders WHERE total_amount >= 50 AND total_amount < 100;",
            ),
            CommonMistake(
                pitfall="Using = with % Wildcards",
                explanation="The `%` character has no special meaning when paired with `=`; pattern matching requires the `LIKE` operator.",
                incorrect_sql="SELECT * FROM customers WHERE email = '%@gmail.com';",
                corrected_sql="SELECT * FROM customers WHERE email LIKE '%@gmail.com';",
            ),
            CommonMistake(
                pitfall="Ordering Boundary Values Incorrectly in BETWEEN",
                explanation="Writing `BETWEEN 100 AND 50` will return 0 rows because SQL checks `col >= 100 AND col <= 50`.",
                incorrect_sql="SELECT * FROM products WHERE price BETWEEN 200 AND 50;",
                corrected_sql="SELECT * FROM products WHERE price BETWEEN 50 AND 200;",
            ),
        ],
        real_world_use_cases=[
            "Search Auto-Complete: Querying user names or product SKUs matching prefix input `WHERE sku LIKE 'ELEC-%'`.",
            "Quarterly Accounting Reports: Querying ledger entries with `WHERE txn_date BETWEEN '2023-01-01' AND '2023-03-31'`.",
            "Geographic Segmentation: Filtering order shipments by regional trade zones with `WHERE country IN ('DE', 'FR', 'IT', 'ES')`.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-1-3-1",
                slug="filter-products-by-categories",
                title="Filter Products Across Target Categories",
                difficulty="easy",
                prompt="Find id, name, and price of all products belonging to category_id 1, 2, or 4. Order by id ASC.",
                starter_sql="SELECT \nFROM products\nWHERE \nORDER BY id ASC;",
                solution_sql="SELECT id, name, price FROM products WHERE category_id IN (1, 2, 4) ORDER BY id ASC;",
                hints=["Use `WHERE category_id IN (1, 2, 4)`.", "Sort using ORDER BY id ASC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-3-2",
                slug="orders-within-date-range",
                title="Identify Orders Placed in February 2023",
                difficulty="easy",
                prompt="Find id, customer_id, and total_amount for all orders placed between '2023-02-01' and '2023-02-28' inclusive. Order by order_date ASC, id ASC.",
                starter_sql="SELECT \nFROM orders;",
                solution_sql="SELECT id, customer_id, total_amount FROM orders WHERE order_date BETWEEN '2023-02-01' AND '2023-02-28' ORDER BY order_date ASC, id ASC;",
                hints=["Use `WHERE order_date BETWEEN '2023-02-01' AND '2023-02-28'`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-3-3",
                slug="search-desk-furniture",
                title="Search Desk Products by Pattern",
                difficulty="medium",
                prompt="Find id, name, and price for all products whose name contains the word 'Desk' (case-insensitive in SQLite). Order by price ASC.",
                starter_sql="SELECT \nFROM products;",
                solution_sql="SELECT id, name, price FROM products WHERE name LIKE '%Desk%' ORDER BY price ASC;",
                hints=["Use `name LIKE '%Desk%'`.", "Order by price ASC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-3-4",
                slug="exclude-statuses-not-in",
                title="Exclude Problematic Order Statuses",
                difficulty="easy",
                prompt="Find id, customer_id, and status for orders whose status is NOT in ('CANCELLED', 'PENDING'). Order by id ASC.",
                starter_sql="SELECT \nFROM orders;",
                solution_sql="SELECT id, customer_id, status FROM orders WHERE status NOT IN ('CANCELLED', 'PENDING') ORDER BY id ASC;",
                hints=["Use `WHERE status NOT IN ('CANCELLED', 'PENDING')`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-3-5",
                slug="domain-email-matching",
                title="Customers with UK Domains",
                difficulty="medium",
                prompt="Select first_name, last_name, and email for all customers whose email ends with '.co.uk'. Order by last_name ASC.",
                starter_sql="SELECT \nFROM customers;",
                solution_sql="SELECT first_name, last_name, email FROM customers WHERE email LIKE '%.co.uk' ORDER BY last_name ASC;",
                hints=["Use `WHERE email LIKE '%.co.uk'`."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-1-4",
        slug="sorting-pagination-null-handling",
        level_number=1,
        level_title="Level 1: SQL Fundamentals",
        title="Deterministic Sorting, Pagination & NULL Handling",
        order_index=4,
        database_id="db-banking",
        database_name="banking_db",
        learning_objectives=[
            "Understand why relational queries are non-deterministic without ORDER BY.",
            "Sort outputs by single or multiple columns in ASC and DESC order.",
            "Implement safe pagination using LIMIT and OFFSET.",
            "Master three-valued logic and NULL checks using IS NULL and IS NOT NULL.",
        ],
        prerequisites=[
            "Pattern Matching & Range Filtering (Level 1, Lesson 3).",
        ],
        detailed_explanation="""In the relational model, tables are unordered multisets of tuples. Without an explicit ORDER BY clause, the database engine makes ZERO guarantees about the return order of rows—subsequent executions of the exact same query may return rows in completely different sequences.

1. Deterministic Sorting:
`ORDER BY column_1 ASC, column_2 DESC`
Sorting evaluates sequentially: it sorts primarily by column_1; for rows that share identical column_1 values, it breaks ties using column_2.

2. Pagination with LIMIT and OFFSET:
- `LIMIT n`: Caps the result set to return at most n records.
- `OFFSET m`: Skips the first m rows before beginning to return results.
Pagination (e.g. Page 2 with 10 items per page) is constructed as: `LIMIT 10 OFFSET 10`.

3. Three-Valued Logic & NULL Handling:
In SQL, NULL represents unknown or missing information. Because NULL is not a concrete value, standard equality operators FAIL:
- `NULL = NULL` evaluates to UNKNOWN, not TRUE!
- `balance = NULL` evaluates to UNKNOWN, filtering out every row!
To check for missing data, SQL requires special unary operators:
- `column_name IS NULL`
- `column_name IS NOT NULL`""",
        syntax_reference="""SELECT column_1, column_2
FROM table_name
WHERE description IS NOT NULL
ORDER BY column_1 DESC, column_2 ASC
LIMIT 10 OFFSET 20;""",
        clause_breakdown=[
            ClauseExplanation(keyword="ORDER BY", purpose="Sorts the query result set by specified expressions.", notes="Executes near the end of query processing, just before LIMIT."),
            ClauseExplanation(keyword="ASC / DESC", purpose="ASC sorts low-to-high / A-to-Z (default). DESC sorts high-to-low / Z-to-A.", notes="Can be configured independently per column."),
            ClauseExplanation(keyword="LIMIT", purpose="Specifies the maximum number of rows to return to the client.", notes="Protects against runaway result sets."),
            ClauseExplanation(keyword="OFFSET", purpose="Specifies the number of rows to skip before returning records.", notes="Commonly paired with LIMIT for web pagination."),
            ClauseExplanation(keyword="IS NULL", purpose="Tests whether a column contains a missing / unassigned value.", notes="Never use = NULL in SQL."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Top Depositors Ranked by Ledger Balance",
                explanation="Find the 5 accounts with the highest ledger balances, breaking ties by account number.",
                sql="SELECT account_number, account_type, balance FROM accounts WHERE status = 'ACTIVE' ORDER BY balance DESC, account_number ASC LIMIT 5;",
                columns=["account_number", "account_type", "balance"],
                rows=[
                    ["SAV-1004-602", "SAVINGS", 210000.00],
                    ["SAV-1008-202", "SAVINGS", 150000.00],
                    ["MM-1002-802", "MONEY_MARKET", 125000.00],
                    ["BUS-1004-603", "BUSINESS_CHECKING", 95000.00],
                    ["SAV-1001-902", "SAVINGS", 85000.00],
                ],
            ),
            WorkedExample(
                title="Example 2: Pagination Window (Page 2)",
                explanation="Retrieve page 2 of customer accounts (records 6 through 10) ordered by id ASC.",
                sql="SELECT id, customer_id, account_number, balance FROM accounts ORDER BY id ASC LIMIT 5 OFFSET 5;",
                columns=["id", "customer_id", "account_number", "balance"],
                rows=[
                    [1006, 104, "CHK-1004-601", 38900.25],
                    [1007, 104, "SAV-1004-602", 210000.00],
                    [1008, 104, "BUS-1004-603", 95000.00],
                    [1009, 105, "CHK-1005-501", 3200.00],
                    [1010, 106, "CHK-1006-401", 12450.00],
                ],
            ),
            WorkedExample(
                title="Example 3: Checking for Missing Data with IS NULL",
                explanation="Find projects in the company database that are currently ongoing (end_date IS NULL).",
                sql="SELECT id, name, start_date, budget FROM projects WHERE end_date IS NULL ORDER BY budget DESC;",
                columns=["id", "name", "start_date", "budget"],
                rows=[
                    [108, "Autonomous Microservices Mesh (R&D)", "2023-04-01", 900000.00],
                    [105, "Enterprise CRM AI Integration", "2022-11-01", 620000.00],
                    [102, "Zero Trust Architecture Implementation", "2022-06-01", 480000.00],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Using = NULL or != NULL",
                explanation="Comparisons against NULL using equality always yield UNKNOWN, which evaluates to false in WHERE clauses.",
                incorrect_sql="SELECT * FROM projects WHERE end_date = NULL;",
                corrected_sql="SELECT * FROM projects WHERE end_date IS NULL;",
            ),
            CommonMistake(
                pitfall="Using LIMIT Without ORDER BY",
                explanation="Using LIMIT without an ORDER BY clause causes non-deterministic results: the database may return a completely different subset of rows on subsequent runs.",
                incorrect_sql="SELECT * FROM transactions LIMIT 10;",
                corrected_sql="SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC LIMIT 10;",
            ),
        ],
        real_world_use_cases=[
            "Infinite Scrolling & API Pagination: Serving paged data chunks to mobile and web user interfaces.",
            "Leaderboards: Ranking top players, highest earners, or bestselling products.",
            "Data Quality Auditing: Scanning for records with missing phone numbers, missing postal codes, or unassigned accounts.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-1-4-1",
                slug="highest-credit-scores",
                title="Top 5 Customers by Credit Score",
                difficulty="easy",
                prompt="Select first_name, last_name, credit_score, and annual_income from customers. Order by credit_score DESC and limit to the top 5.",
                starter_sql="SELECT \nFROM customers\nORDER BY \nLIMIT 5;",
                solution_sql="SELECT first_name, last_name, credit_score, annual_income FROM customers ORDER BY credit_score DESC LIMIT 5;",
                hints=["Sort on `credit_score DESC`.", "Add `LIMIT 5`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-4-2",
                slug="dormant-account-check",
                title="Identify Dormant or Closed Accounts",
                difficulty="easy",
                prompt="Select id, account_number, account_type, and status from accounts where status IN ('DORMANT', 'CLOSED') ORDER BY balance DESC, id ASC.",
                starter_sql="SELECT \nFROM accounts;",
                solution_sql="SELECT id, account_number, account_type, status FROM accounts WHERE status IN ('DORMANT', 'CLOSED') ORDER BY balance DESC, id ASC;",
                hints=["Use `WHERE status IN ('DORMANT', 'CLOSED')`.", "Sort by balance DESC, id ASC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-4-3",
                slug="ongoing-projects-audit",
                title="Audit Open Projects Without End Dates",
                difficulty="medium",
                prompt="Query the projects table for projects where end_date IS NULL. Return id, name, and budget ordered by budget DESC.",
                starter_sql="SELECT \nFROM projects\nWHERE ",
                solution_sql="SELECT id, name, budget FROM projects WHERE end_date IS NULL ORDER BY budget DESC;",
                hints=["Use `WHERE end_date IS NULL`.", "Sort on `budget DESC`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-4-4",
                slug="transaction-pagination-page-3",
                title="Paginate Transactions Page 3",
                difficulty="medium",
                prompt="Return transactions with id, account_id, transaction_type, and amount for page 3 (items 21 through 30, meaning LIMIT 10 OFFSET 20), ordered by id ASC.",
                starter_sql="SELECT \nFROM transactions;",
                solution_sql="SELECT id, account_id, transaction_type, amount FROM transactions ORDER BY id ASC LIMIT 10 OFFSET 20;",
                hints=["Use `LIMIT 10 OFFSET 20`.", "Order by `id ASC`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-1-4-5",
                slug="unassigned-departments-null",
                title="Identify Staff Without Departments",
                difficulty="easy",
                prompt="Query the employees table in company_db for staff where department_id IS NULL. Return id, first_name, last_name, and title ordered by id ASC.",
                starter_sql="SELECT \nFROM employees;",
                solution_sql="SELECT id, first_name, last_name, title FROM employees WHERE department_id IS NULL ORDER BY id ASC;",
                hints=["Filter using `WHERE department_id IS NULL`."],
                order_matters=True,
            ),
        ],
    ),
]
