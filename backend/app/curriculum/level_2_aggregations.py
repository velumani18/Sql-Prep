from typing import List
from app.curriculum.models import (
    TopicLesson,
    ClauseExplanation,
    WorkedExample,
    CommonMistake,
    PracticeQuestion,
)

LEVEL_2_LESSONS: List[TopicLesson] = [
    TopicLesson(
        id="les-2-1",
        slug="aggregate-functions-foundations",
        level_number=2,
        level_title="Level 2: Aggregations & Grouping",
        title="Aggregate Functions: COUNT, SUM, AVG, MIN, MAX",
        order_index=1,
        database_id="db-ecommerce",
        database_name="ecommerce_db",
        learning_objectives=[
            "Understand how aggregate functions collapse multiple rows into a single scalar summary.",
            "Master the difference between COUNT(*) and COUNT(column_name) regarding NULLs.",
            "Use SUM and AVG for quantitative numeric aggregations.",
            "Extract boundaries with MIN and MAX across numbers, dates, and text strings.",
        ],
        prerequisites=[
            "Level 1: SQL Fundamentals (SELECT, WHERE, NULL handling).",
        ],
        detailed_explanation="""Scalar SQL operations process rows individually. In contrast, aggregate functions summarize collections of rows across an entire table or partitioned group, collapsing many rows into a single summary scalar value.

The core standard aggregate functions are:
- `COUNT(*)`: Returns the total count of rows in the candidate set, regardless of whether any cell contains NULL.
- `COUNT(column)`: Returns the count of rows where the specified column is NOT NULL.
- `COUNT(DISTINCT column)`: Returns the count of unique non-null values.
- `SUM(column)`: Calculates the mathematical sum of all non-null values in a numeric column.
- `AVG(column)`: Calculates the arithmetic mean (`SUM(col) / COUNT(col)`), completely ignoring NULL values.
- `MIN(column)`: Evaluates the lowest value in a column (supports numbers, dates, and alphabetical strings).
- `MAX(column)`: Evaluates the highest value in a column.

A critical rule in SQL: You cannot select regular non-aggregated columns alongside aggregate functions unless those columns are explicitly included in a `GROUP BY` clause.""",
        syntax_reference="""SELECT 
    COUNT(*) AS total_rows,
    COUNT(column_name) AS non_null_count,
    SUM(numeric_col) AS total_sum,
    AVG(numeric_col) AS average_val,
    MIN(numeric_col) AS minimum_val,
    MAX(numeric_col) AS maximum_val
FROM table_name
WHERE status = 'ACTIVE';""",
        clause_breakdown=[
            ClauseExplanation(keyword="COUNT(*)", purpose="Counts all qualifying rows in the candidate set including rows with NULLs.", notes="Highly optimized in database engines using table indexes."),
            ClauseExplanation(keyword="COUNT(column)", purpose="Counts only rows where the specified column is NOT NULL.", notes="Useful for measuring completion rates and missing data."),
            ClauseExplanation(keyword="SUM()", purpose="Calculates the total sum of numeric values.", notes="Ignores NULLs; returns NULL if all input values are NULL."),
            ClauseExplanation(keyword="AVG()", purpose="Calculates the arithmetic mean.", notes="Divides by non-null row count, NOT total row count."),
            ClauseExplanation(keyword="MIN() / MAX()", purpose="Finds extreme boundary values.", notes="Works seamlessly on timestamps and dates as well as numbers."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: E-Commerce Transaction Volume & Metrics",
                explanation="Calculate overall sales volume, total revenue, average order value, and order amount extremes.",
                sql="SELECT COUNT(*) AS total_orders, SUM(total_amount) AS gross_revenue, ROUND(AVG(total_amount), 2) AS avg_order_val, MIN(total_amount) AS smallest_order, MAX(total_amount) AS largest_order FROM orders WHERE status = 'COMPLETED';",
                columns=["total_orders", "gross_revenue", "avg_order_val", "smallest_order", "largest_order"],
                rows=[
                    [27, 6554.43, 242.76, 35.00, 719.00],
                ],
            ),
            WorkedExample(
                title="Example 2: NULL Sensitivity in COUNT",
                explanation="Demonstrate how COUNT(payment_date) ignores unpaid orders while COUNT(*) counts all rows.",
                sql="SELECT COUNT(*) AS total_records, COUNT(payment_date) AS cleared_payments, COUNT(*) - COUNT(payment_date) AS pending_or_null FROM payments;",
                columns=["total_records", "cleared_payments", "pending_or_null"],
                rows=[
                    [32, 32, 0],
                ],
            ),
            WorkedExample(
                title="Example 3: Counting Unique Entities with DISTINCT",
                explanation="Determine how many distinct customers have completed at least one order.",
                sql="SELECT COUNT(DISTINCT customer_id) AS unique_purchasing_customers FROM orders WHERE status = 'COMPLETED';",
                columns=["unique_purchasing_customers"],
                rows=[
                    [20],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Mixing Aggregates with Non-Aggregated Columns Without GROUP BY",
                explanation="Selecting an unaggregated column like `SELECT name, MAX(price) FROM products` is invalid in ANSI SQL because the engine cannot know which product's name to pick.",
                incorrect_sql="SELECT name, MAX(price) FROM products;",
                corrected_sql="SELECT MAX(price) FROM products; -- Or use subqueries/window functions for top item",
            ),
            CommonMistake(
                pitfall="Misunderstanding How AVG Handles NULLs",
                explanation="AVG does not treat NULL as zero; it ignores NULL completely. If a column has values [10, 0, NULL], AVG is 5.0 (10 / 2), not 3.33.",
                incorrect_sql="-- Assuming NULL counts as 0 in AVG\nSELECT AVG(bonus) FROM salaries;",
                corrected_sql="SELECT AVG(COALESCE(bonus, 0)) FROM salaries;",
            ),
        ],
        real_world_use_cases=[
            "Executive Dashboards: KPI metrics (Total Gross Merchandise Value, Daily Active Users, Average Order Value).",
            "Data Quality Monitoring: Calculating completeness ratios via `(COUNT(email) * 100.0) / COUNT(*)`.",
            "Financial Reconciliation: Verifying ledger debit balances equal credit balances.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-2-1-1",
                slug="active-product-inventory-metrics",
                title="Calculate Product Inventory Aggregates",
                difficulty="easy",
                prompt="Write a query to calculate the total number of products as total_products, total stock units as total_inventory, and maximum price as max_price from the products table where is_active = 1.",
                starter_sql="SELECT \nFROM products\nWHERE is_active = 1;",
                solution_sql="SELECT COUNT(*) AS total_products, SUM(stock_quantity) AS total_inventory, MAX(price) AS max_price FROM products WHERE is_active = 1;",
                hints=["Use COUNT(*), SUM(stock_quantity), and MAX(price)."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-1-2",
                slug="completed-order-revenue",
                title="Total Revenue from Completed Transactions",
                difficulty="easy",
                prompt="Calculate the sum of total_amount as total_revenue and the rounded average total_amount as avg_revenue (rounded to 2 decimal places) for orders with status = 'COMPLETED'.",
                starter_sql="SELECT \nFROM orders;",
                solution_sql="SELECT ROUND(SUM(total_amount), 2) AS total_revenue, ROUND(AVG(total_amount), 2) AS avg_revenue FROM orders WHERE status = 'COMPLETED';",
                hints=["Filter using `WHERE status = 'COMPLETED'`.", "Use `ROUND(SUM(total_amount), 2)`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-1-3",
                slug="count-distinct-buying-countries",
                title="Count Purchasing Customer Countries",
                difficulty="medium",
                prompt="Count the number of distinct countries among registered customers in the customers table. Return a single column named unique_countries.",
                starter_sql="SELECT \nFROM customers;",
                solution_sql="SELECT COUNT(DISTINCT country) AS unique_countries FROM customers;",
                hints=["Use `COUNT(DISTINCT country)`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-1-4",
                slug="price-spread-analysis",
                title="Calculate Product Price Spread",
                difficulty="medium",
                prompt="Find the difference between the maximum price and minimum price of all active products in the products table. Return as price_spread.",
                starter_sql="SELECT \nFROM products;",
                solution_sql="SELECT MAX(price) - MIN(price) AS price_spread FROM products WHERE is_active = 1;",
                hints=["Subtract MIN(price) from MAX(price)."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-1-5",
                slug="earliest-and-latest-orders",
                title="Determine Order Time Boundaries",
                difficulty="easy",
                prompt="Find the earliest order date as first_order_date and latest order date as latest_order_date from the orders table.",
                starter_sql="SELECT \nFROM orders;",
                solution_sql="SELECT MIN(order_date) AS first_order_date, MAX(order_date) AS latest_order_date FROM orders;",
                hints=["Use `MIN(order_date)` and `MAX(order_date)`."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-2-2",
        slug="group-by-having-clauses",
        level_number=2,
        level_title="Level 2: Aggregations & Grouping",
        title="Grouping Dimensions with GROUP BY and HAVING",
        order_index=2,
        database_id="db-company",
        database_name="company_db",
        learning_objectives=[
            "Understand the conceptual mechanics of GROUP BY in partitioning rows into buckets.",
            "Select dimension columns alongside aggregated metrics.",
            "Master the crucial distinction between WHERE (pre-aggregation filter) and HAVING (post-aggregation filter).",
            "Group by multiple columns simultaneously.",
        ],
        prerequisites=[
            "Aggregate Functions Foundations (Level 2, Lesson 1).",
        ],
        detailed_explanation="""While aggregate functions alone collapse all table rows into a single scalar result, real-world reporting requires summarizing data across specific dimensional categories—such as total revenue by country, employee count by department, or average loan size by branch.

The `GROUP BY` clause groups rows sharing identical values in specified columns into independent buckets. The aggregate functions then compute metrics separately for each individual bucket.

The Single-Rule Constraint of GROUP BY:
Every column that appears in the SELECT clause MUST either:
1. Be listed explicitly in the GROUP BY clause (a grouping dimension), OR
2. Be wrapped inside an aggregate function (e.g., `SUM()`, `AVG()`, `COUNT()`).

WHERE vs. HAVING (The Most Common Interview Question):
- `WHERE`: Evaluates before grouping occurs. It filters individual rows from the source table. It CANNOT evaluate aggregate functions because aggregates do not yet exist!
- `HAVING`: Evaluates after grouping occurs. It filters the resulting group buckets based on aggregate calculations (e.g. `HAVING COUNT(*) > 5` or `HAVING AVG(salary) >= 100000`).""",
        syntax_reference="""SELECT 
    dimension_col_1,
    dimension_col_2,
    COUNT(*) AS row_count,
    AVG(metric_col) AS avg_metric
FROM table_name
WHERE individual_row_filter = 1
GROUP BY dimension_col_1, dimension_col_2
HAVING COUNT(*) >= 3
ORDER BY avg_metric DESC;""",
        clause_breakdown=[
            ClauseExplanation(keyword="GROUP BY", purpose="Splits candidate rows into distinct group buckets based on identical values in the specified dimension columns.", notes="Evaluated after FROM and WHERE, but before HAVING, SELECT, and ORDER BY."),
            ClauseExplanation(keyword="HAVING", purpose="Filters the aggregated groups produced by GROUP BY.", notes="Can evaluate aggregate expressions like SUM, COUNT, AVG."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Headcount & Average Compensation by Department",
                explanation="Calculate total active employee headcount and average base salary for each department.",
                sql="SELECT e.department_id, COUNT(*) AS headcount, ROUND(AVG(s.base_salary), 2) AS avg_salary FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.status = 'ACTIVE' AND e.department_id IS NOT NULL GROUP BY e.department_id ORDER BY avg_salary DESC LIMIT 4;",
                columns=["department_id", "headcount", "avg_salary"],
                rows=[
                    [1, 1, 285000.00],
                    [2, 17, 151529.41],
                    [5, 5, 144600.00],
                    [7, 3, 190000.00],
                ],
            ),
            WorkedExample(
                title="Example 2: Filtering Group Buckets with HAVING",
                explanation="Find departments that employ strictly more than 4 active staff members.",
                sql="SELECT department_id, COUNT(*) AS active_headcount FROM employees WHERE status = 'ACTIVE' AND department_id IS NOT NULL GROUP BY department_id HAVING COUNT(*) > 4 ORDER BY active_headcount DESC;",
                columns=["department_id", "active_headcount"],
                rows=[
                    [2, 17],
                    [5, 5],
                    [3, 5],
                    [4, 5],
                ],
            ),
            WorkedExample(
                title="Example 3: Multi-Column Dimensional Grouping",
                explanation="Calculate project staff allocations grouped by department_id and management_level.",
                sql="SELECT department_id, management_level, COUNT(*) AS manager_count FROM managers WHERE department_id IS NOT NULL GROUP BY department_id, management_level ORDER BY department_id ASC, management_level ASC LIMIT 5;",
                columns=["department_id", "management_level", "manager_count"],
                rows=[
                    [1, "EXECUTIVE", 1],
                    [2, "DIRECTOR", 2],
                    [2, "EXECUTIVE", 1],
                    [2, "TEAM_LEAD", 1],
                    [3, "EXECUTIVE", 1],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Using WHERE to Filter on Aggregate Functions",
                explanation="Writing `WHERE COUNT(*) > 5` causes a syntax error because WHERE executes before the aggregates are computed. Aggregate filters MUST go in HAVING.",
                incorrect_sql="SELECT department_id, COUNT(*) FROM employees WHERE COUNT(*) > 5 GROUP BY department_id;",
                corrected_sql="SELECT department_id, COUNT(*) FROM employees GROUP BY department_id HAVING COUNT(*) > 5;",
            ),
            CommonMistake(
                pitfall="Selecting Columns Not Included in GROUP BY",
                explanation="Selecting columns that are neither grouped nor aggregated violates relational principles and triggers errors in standard SQL.",
                incorrect_sql="SELECT department_id, first_name, COUNT(*) FROM employees GROUP BY department_id;",
                corrected_sql="SELECT department_id, COUNT(*) FROM employees GROUP BY department_id;",
            ),
        ],
        real_world_use_cases=[
            "SaaS Revenue Reporting: Monthly Recurring Revenue (MRR) grouped by subscription plan tier.",
            "Logistics: Identifying fulfillment hubs that processed more than 1,000 packages today.",
            "Customer Retention: Pinpointing buyer cohorts who completed 3 or more repeat purchases.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-2-2-1",
                slug="customer-orders-count-having",
                title="Frequent Buyers with 3+ Orders",
                difficulty="medium",
                prompt="From the orders table in ecommerce_db, group by customer_id to find customers who placed at least 3 orders. Return customer_id and total_orders ordered by total_orders DESC, customer_id ASC.",
                starter_sql="SELECT customer_id, COUNT(*) AS total_orders\nFROM orders\nGROUP BY \nHAVING \nORDER BY total_orders DESC, customer_id ASC;",
                solution_sql="SELECT customer_id, COUNT(*) AS total_orders FROM orders GROUP BY customer_id HAVING COUNT(*) >= 3 ORDER BY total_orders DESC, customer_id ASC;",
                hints=["Group by `customer_id`.", "Filter with `HAVING COUNT(*) >= 3`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-2-2",
                slug="total-budget-by-location",
                title="Department Budget Allocation by Location",
                difficulty="easy",
                prompt="From the departments table in company_db, calculate the total budget per city location. Return location and total_budget ordered by total_budget DESC.",
                starter_sql="SELECT location, SUM(budget) AS total_budget\nFROM departments\nGROUP BY \nORDER BY total_budget DESC;",
                solution_sql="SELECT location, SUM(budget) AS total_budget FROM departments GROUP BY location ORDER BY total_budget DESC;",
                hints=["Group by location.", "Order by total_budget DESC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-2-3",
                slug="products-per-category-threshold",
                title="Categories with at Least 3 Products",
                difficulty="easy",
                prompt="In ecommerce_db, find category_id values that contain at least 3 products in the products table. Return category_id and product_count ordered by category_id ASC.",
                starter_sql="SELECT category_id, COUNT(*) AS product_count\nFROM products\nGROUP BY category_id\nHAVING \nORDER BY category_id ASC;",
                solution_sql="SELECT category_id, COUNT(*) AS product_count FROM products GROUP BY category_id HAVING COUNT(*) >= 3 ORDER BY category_id ASC;",
                hints=["Use `HAVING COUNT(*) >= 3`.", "Order by category_id ASC."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-2-4",
                slug="department-average-salaries",
                title="Departments with Average Salary Above $150K",
                difficulty="hard",
                prompt="From employees e and salaries s in company_db, find department_id and average base_salary (rounded to 2 decimal places as avg_sal) for departments where the average base_salary exceeds 150,000. Filter out NULL department_ids. Order by avg_sal DESC.",
                starter_sql="SELECT \nFROM employees e\nJOIN salaries s ON e.id = s.employee_id\nWHERE e.department_id IS NOT NULL\nGROUP BY e.department_id\nHAVING \nORDER BY avg_sal DESC;",
                solution_sql="SELECT e.department_id, ROUND(AVG(s.base_salary), 2) AS avg_sal FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id IS NOT NULL GROUP BY e.department_id HAVING AVG(s.base_salary) > 150000 ORDER BY avg_sal DESC;",
                hints=["Filter in WHERE for `department_id IS NOT NULL`.", "Filter in HAVING using `AVG(s.base_salary) > 150000`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-2-5",
                slug="order-status-breakdown",
                title="Breakdown of Orders by Status",
                difficulty="easy",
                prompt="In ecommerce_db, group orders by status to return status, the count of orders as order_count, and total amount as total_sum. Order by order_count DESC.",
                starter_sql="SELECT status, COUNT(*) AS order_count, SUM(total_amount) AS total_sum\nFROM orders\nGROUP BY status\nORDER BY order_count DESC;",
                solution_sql="SELECT status, COUNT(*) AS order_count, SUM(total_amount) AS total_sum FROM orders GROUP BY status ORDER BY order_count DESC;",
                hints=["Group by status.", "Use COUNT(*) and SUM(total_amount)."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-2-3",
        slug="case-when-conditional-aggregation",
        level_number=2,
        level_title="Level 2: Aggregations & Grouping",
        title="Conditional Logic with CASE WHEN & COALESCE",
        order_index=3,
        database_id="db-banking",
        database_name="banking_db",
        learning_objectives=[
            "Implement branching conditional logic inside queries using CASE WHEN ... THEN ... ELSE ... END.",
            "Use COALESCE to provide fallback default values for NULL fields.",
            "Master conditional aggregation (pivoting rows into columns using SUM(CASE WHEN ...)).",
            "Categorize numeric values into discrete business buckets.",
        ],
        prerequisites=[
            "Aggregate Functions & Grouping (Level 2, Lessons 1 and 2).",
        ],
        detailed_explanation="""SQL is a declarative language, but real-world data transformation demands if-then-else procedural logic. In SQL, this is achieved using the `CASE` expression.

The CASE Expression:
Can be used in SELECT, WHERE, GROUP BY, and ORDER BY clauses:
```sql
CASE 
    WHEN score >= 800 THEN 'Excellent'
    WHEN score >= 700 THEN 'Good'
    WHEN score >= 600 THEN 'Fair'
    ELSE 'Poor'
END AS credit_tier
```
The database evaluates conditions top-to-bottom and returns the result of the first matching branch. If no condition matches and no ELSE is provided, it returns NULL.

Conditional Aggregation (Pivoting):
A cornerstone analytical technique is combining aggregate functions with CASE statements. For example, instead of running separate queries for completed, pending, and cancelled orders, a single query can aggregate them into distinct columns:
```sql
SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_count,
SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_count
```

The COALESCE Function:
`COALESCE(val_1, val_2, val_3, ...)` evaluates a list of arguments and returns the FIRST non-null value. It is the gold standard for providing safe default values (e.g. `COALESCE(bonus, 0)`).""",
        syntax_reference="""-- Standard CASE Expression
SELECT 
    name,
    CASE 
        WHEN balance >= 100000 THEN 'Platinum'
        WHEN balance >= 25000 THEN 'Gold'
        ELSE 'Silver'
    END AS tier_status
FROM accounts;

-- Conditional Aggregation
SELECT 
    branch_id,
    COUNT(*) AS total_accounts,
    SUM(CASE WHEN account_type = 'CHECKING' THEN 1 ELSE 0 END) AS checking_count,
    SUM(CASE WHEN account_type = 'SAVINGS' THEN 1 ELSE 0 END) AS savings_count
FROM accounts
GROUP BY branch_id;""",
        clause_breakdown=[
            ClauseExplanation(keyword="CASE", purpose="Initiates conditional evaluation logic.", notes="Always closed with the END keyword."),
            ClauseExplanation(keyword="WHEN ... THEN", purpose="Defines the predicate condition and the value to yield if true.", notes="Evaluated sequentially from top to bottom."),
            ClauseExplanation(keyword="ELSE", purpose="Provides the fallback default value if none of the WHEN predicates match.", notes="If omitted and no condition matches, yields NULL."),
            ClauseExplanation(keyword="COALESCE", purpose="Returns the first non-null argument from a list.", notes="Compact shorthand for a simple CASE checking IS NOT NULL."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Classifying Customer Credit Tiers",
                explanation="Segment customers into Credit Tiers based on their FICO bureau credit score.",
                sql="SELECT first_name, last_name, credit_score, CASE WHEN credit_score >= 800 THEN 'Tier 1 - Super Prime' WHEN credit_score >= 740 THEN 'Tier 2 - Prime' WHEN credit_score >= 670 THEN 'Tier 3 - Near Prime' ELSE 'Tier 4 - Subprime' END AS credit_tier FROM customers ORDER BY credit_score DESC LIMIT 4;",
                columns=["first_name", "last_name", "credit_score", "credit_tier"],
                rows=[
                    ["Katherine", "Johnson", 830, "Tier 1 - Super Prime"],
                    ["Ada", "Lovelace", 820, "Tier 1 - Super Prime"],
                    ["Emmy", "Noether", 815, "Tier 1 - Super Prime"],
                    ["Alexander", "Hamilton", 810, "Tier 1 - Super Prime"],
                ],
            ),
            WorkedExample(
                title="Example 2: Conditional Aggregation (Pivoting Account Types)",
                explanation="Aggregate total active accounts per branch into separate checking and savings columns in a single scan.",
                sql="SELECT branch_id, COUNT(*) AS total_accounts, SUM(CASE WHEN account_type = 'CHECKING' THEN 1 ELSE 0 END) AS checking_accs, SUM(CASE WHEN account_type = 'SAVINGS' THEN 1 ELSE 0 END) AS savings_accs, SUM(CASE WHEN account_type = 'MONEY_MARKET' THEN 1 ELSE 0 END) AS mm_accs FROM accounts WHERE status = 'ACTIVE' GROUP BY branch_id ORDER BY branch_id ASC;",
                columns=["branch_id", "total_accounts", "checking_accs", "savings_accs", "mm_accs"],
                rows=[
                    [1, 7, 5, 1, 1],
                    [2, 9, 4, 2, 2],
                    [3, 5, 4, 1, 0],
                    [4, 3, 3, 0, 0],
                    [5, 2, 2, 0, 0],
                ],
            ),
            WorkedExample(
                title="Example 3: COALESCE for NULL Fallbacks",
                explanation="Ensure that employees without assigned bonuses evaluate cleanly to 0.00 rather than NULL in total comp calculations.",
                sql="SELECT employee_id, base_salary, COALESCE(bonus, 0.00) AS safe_bonus, base_salary + COALESCE(bonus, 0.00) AS total_compensation FROM salaries WHERE bonus = 0.00 OR bonus IS NULL LIMIT 3;",
                columns=["employee_id", "base_salary", "safe_bonus", "total_compensation"],
                rows=[
                    [27, 52000.00, 0.00, 52000.00],
                    [57, 150000.00, 0.00, 150000.00],
                    [58, 140000.00, 0.00, 140000.00],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Forgetting the END Keyword in CASE Expressions",
                explanation="Every CASE block must terminate with END. Omitting it produces an immediate syntax error.",
                incorrect_sql="SELECT CASE WHEN balance > 0 THEN 'Positive' ELSE 'Zero' AS status FROM accounts;",
                corrected_sql="SELECT CASE WHEN balance > 0 THEN 'Positive' ELSE 'Zero' END AS status FROM accounts;",
            ),
            CommonMistake(
                pitfall="Using COUNT instead of SUM in Conditional Aggregation",
                explanation="`COUNT(CASE WHEN col = 'X' THEN 0 END)` still counts the 0 because 0 is not NULL! Use `SUM()` when returning 1/0, or omit the ELSE so COUNT ignores NULL.",
                incorrect_sql="SELECT COUNT(CASE WHEN status = 'FROZEN' THEN 0 END) FROM accounts;",
                corrected_sql="SELECT SUM(CASE WHEN status = 'FROZEN' THEN 1 ELSE 0 END) FROM accounts;",
            ),
        ],
        real_world_use_cases=[
            "Data Warehousing ETL: Pivoting transactional events into wide feature tables for machine learning.",
            "Financial Risk Models: Flagging accounts into risk classifications (Low, Medium, High).",
            "Conversion Funnel Reporting: Calculating drop-off rates across checkout stages in a single query.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-2-3-1",
                slug="categorize-account-balances",
                title="Classify Account Balances into Tiers",
                difficulty="easy",
                prompt="In banking_db, select account_number, balance, and balance_category from accounts where status = 'ACTIVE'. Category rules: balance >= 100000 is 'High', balance >= 10000 is 'Medium', else 'Low'. Order by balance DESC.",
                starter_sql="SELECT account_number, balance,\n    CASE \n        -- Add conditions\n    END AS balance_category\nFROM accounts\nWHERE status = 'ACTIVE'\nORDER BY balance DESC;",
                solution_sql="SELECT account_number, balance, CASE WHEN balance >= 100000 THEN 'High' WHEN balance >= 10000 THEN 'Medium' ELSE 'Low' END AS balance_category FROM accounts WHERE status = 'ACTIVE' ORDER BY balance DESC;",
                hints=["Use `CASE WHEN balance >= 100000 THEN 'High' ... END`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-3-2",
                slug="conditional-loan-portfolio-breakdown",
                title="Pivoted Loan Status Breakdown per Branch",
                difficulty="medium",
                prompt="From the loans table in banking_db, group by branch_id to count: total_loans, approved_loans (status = 'APPROVED'), and rejected_loans (status = 'REJECTED'). Order by branch_id ASC.",
                starter_sql="SELECT branch_id, COUNT(*) AS total_loans,\n    -- Add conditional SUMs\nFROM loans\nGROUP BY branch_id\nORDER BY branch_id ASC;",
                solution_sql="SELECT branch_id, COUNT(*) AS total_loans, SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) AS approved_loans, SUM(CASE WHEN status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected_loans FROM loans GROUP BY branch_id ORDER BY branch_id ASC;",
                hints=["Use `SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END)`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-3-3",
                slug="coalesce-safe-bonuses",
                title="Safe Bonus Display with COALESCE",
                difficulty="easy",
                prompt="In company_db, select employee_id, base_salary, and safe_bonus using COALESCE(bonus, 0.00) from the salaries table. Order by safe_bonus ASC, employee_id ASC LIMIT 5.",
                starter_sql="SELECT employee_id, base_salary, \nFROM salaries\nORDER BY safe_bonus ASC, employee_id ASC\nLIMIT 5;",
                solution_sql="SELECT employee_id, base_salary, COALESCE(bonus, 0.00) AS safe_bonus FROM salaries ORDER BY safe_bonus ASC, employee_id ASC LIMIT 5;",
                hints=["Use `COALESCE(bonus, 0.00) AS safe_bonus`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-3-4",
                slug="active-vs-dormant-ratio",
                title="Calculate Active Account Percentage",
                difficulty="medium",
                prompt="From accounts in banking_db, calculate the overall total_accounts, and the percentage of accounts that are active as active_pct (active count divided by total count multiplied by 100.0, rounded to 1 decimal place).",
                starter_sql="SELECT \nFROM accounts;",
                solution_sql="SELECT COUNT(*) AS total_accounts, ROUND(SUM(CASE WHEN status = 'ACTIVE' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 1) AS active_pct FROM accounts;",
                hints=["Use conditional sum for active accounts.", "Multiply by 100.0 and divide by COUNT(*)."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-2-3-5",
                slug="deposit-vs-withdrawal-totals",
                title="Separate Deposit and Withdrawal Volumes",
                difficulty="medium",
                prompt="From transactions in banking_db, calculate total_deposits (SUM of amount where transaction_type = 'DEPOSIT') and total_withdrawals (SUM of amount where transaction_type = 'WITHDRAWAL').",
                starter_sql="SELECT \nFROM transactions;",
                solution_sql="SELECT SUM(CASE WHEN transaction_type = 'DEPOSIT' THEN amount ELSE 0 END) AS total_deposits, SUM(CASE WHEN transaction_type = 'WITHDRAWAL' THEN amount ELSE 0 END) AS total_withdrawals FROM transactions;",
                hints=["Use `CASE WHEN transaction_type = 'DEPOSIT' THEN amount ELSE 0 END` inside SUM."],
                order_matters=True,
            ),
        ],
    ),
]
