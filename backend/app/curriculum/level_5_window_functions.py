from typing import List
from app.curriculum.models import (
    TopicLesson,
    ClauseExplanation,
    WorkedExample,
    CommonMistake,
    PracticeQuestion,
)

LEVEL_5_LESSONS: List[TopicLesson] = [
    TopicLesson(
        id="les-5-1",
        slug="window-ranking-functions",
        level_number=5,
        level_title="Level 5: Window Functions & Analytics",
        title="Ranking Functions: ROW_NUMBER(), RANK(), and DENSE_RANK()",
        order_index=1,
        database_id="db-company",
        database_name="company_db",
        learning_objectives=[
            "Understand the fundamental architecture of Window Functions.",
            "Compare how GROUP BY collapses rows while Window Functions retain row identity.",
            "Master PARTITION BY to segment calculations across dimensional windows.",
            "Distinguish between ROW_NUMBER(), RANK(), and DENSE_RANK() when resolving ties.",
        ],
        prerequisites=[
            "Level 2: Aggregations & Grouping and Level 4: CTEs.",
        ],
        detailed_explanation="""Traditional `GROUP BY` queries aggregate rows by collapsing them into a single summary row per group bucket. In contrast, Window Functions perform calculations across a set of table rows that are related to the current row, while retaining the individual identity of every single row in the result set!

The `OVER()` clause defines the window (partition and ordering) across which the function operates:
- `PARTITION BY`: Divides the rows into logical partitions (similar to GROUP BY, but without collapsing).
- `ORDER BY`: Defines the logical sequence within each partition.

The Three Core Ranking Functions:
When ranking entities (e.g. salaries: $100K, $90K, $90K, $80K):
1. `ROW_NUMBER()`: Always assigns a unique, strictly sequential integer (1, 2, 3, 4). Even if values tie, row numbers never duplicate.
2. `RANK()`: Assigns identical ranks to tied values, but SKIPS subsequent ranks to preserve overall count (1, 2, 2, 4). Notice rank 3 is skipped!
3. `DENSE_RANK()`: Assigns identical ranks to tied values, but NEVER skips subsequent ranks (1, 2, 2, 3).

Top-N Pattern:
Because window functions execute after WHERE clauses, filtering by rank (e.g. finding the Top 3 earners per department) requires wrapping the window query in a CTE or subquery:
```sql
WITH RankedStaff AS (
    SELECT 
        e.department_id,
        e.first_name,
        s.base_salary,
        DENSE_RANK() OVER (
            PARTITION BY e.department_id 
            ORDER BY s.base_salary DESC
        ) AS salary_rank
    FROM employees e
    JOIN salaries s ON e.id = s.employee_id
)
SELECT * FROM RankedStaff WHERE salary_rank <= 3;
```""",
        syntax_reference="""SELECT 
    department_id,
    first_name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rnk
FROM employees;""",
        clause_breakdown=[
            ClauseExplanation(keyword="OVER()", purpose="Designates the function as a window function and defines its operational frame.", notes="Mandatory for all window functions."),
            ClauseExplanation(keyword="PARTITION BY", purpose="Splits the dataset into independent calculation windows.", notes="If omitted, the entire result set is treated as a single partition."),
            ClauseExplanation(keyword="ROW_NUMBER()", purpose="Generates sequential integer ranks (1, 2, 3, 4...) without duplicate handling.", notes="Non-deterministic for tied values unless tie-breakers are provided."),
            ClauseExplanation(keyword="RANK()", purpose="Assigns duplicate ranks to ties and skips subsequent numbers (1, 2, 2, 4).", notes="Standard Olympic medal ranking."),
            ClauseExplanation(keyword="DENSE_RANK()", purpose="Assigns duplicate ranks to ties without skipping subsequent numbers (1, 2, 2, 3).", notes="Preferred for salary bands and tier rankings."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Top 3 Earners in Engineering (DENSE_RANK)",
                explanation="Rank engineering employees by salary and retrieve the top 3 salary tiers using a CTE.",
                sql="WITH RankedEngineering AS (SELECT e.id, e.first_name, e.last_name, s.base_salary, DENSE_RANK() OVER (ORDER BY s.base_salary DESC) AS salary_rank FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id = 2) SELECT id, first_name, last_name, base_salary, salary_rank FROM RankedEngineering WHERE salary_rank <= 3 ORDER BY salary_rank ASC, id ASC LIMIT 5;",
                columns=["id", "first_name", "last_name", "base_salary", "salary_rank"],
                rows=[
                    [2, "Marcus", "Sterling", 220000.00, 1],
                    [8, "Elena", "Rostova", 190000.00, 2],
                    [7, "David", "Zhao", 185000.00, 3],
                ],
            ),
            WorkedExample(
                title="Example 2: Comparing ROW_NUMBER, RANK, and DENSE_RANK on Ties",
                explanation="Examine how the three ranking functions resolve identical salaries of $145,000.",
                sql="SELECT e.id, e.first_name, e.last_name, s.base_salary, ROW_NUMBER() OVER (ORDER BY s.base_salary DESC) AS row_n, RANK() OVER (ORDER BY s.base_salary DESC) AS rnk, DENSE_RANK() OVER (ORDER BY s.base_salary DESC) AS dense_rnk FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE s.base_salary = 145000.00 ORDER BY e.id ASC LIMIT 4;",
                columns=["id", "first_name", "last_name", "base_salary", "row_n", "rnk", "dense_rnk"],
                rows=[
                    [12, "Hannah", "Abbott", 145000.00, 1, 1, 1],
                    [44, "Natasha", "Romanoff", 145000.00, 2, 1, 1],
                ],
            ),
            WorkedExample(
                title="Example 3: Partitioned Departmental Headcount Windows",
                explanation="Rank employees by hire_date within each department to identify seniority order.",
                sql="SELECT e.id, e.department_id, e.first_name, e.hire_date, ROW_NUMBER() OVER (PARTITION BY e.department_id ORDER BY e.hire_date ASC) AS seniority_order FROM employees e WHERE e.department_id IN (1, 6) ORDER BY e.department_id ASC, seniority_order ASC;",
                columns=["id", "department_id", "first_name", "hire_date", "seniority_order"],
                rows=[
                    [1, 1, "Evelyn", "2018-01-15", 1],
                    [6, 6, "Arthur", "2018-04-12", 1],
                    [47, 6, "Pam", "2019-05-20", 2],
                    [48, 6, "Toby", "2019-09-15", 3],
                    [50, 6, "Stanley", "2020-01-10", 4],
                    [49, 6, "Kelly", "2021-02-01", 5],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Using Window Functions Inside the WHERE Clause",
                explanation="Window functions execute AFTER the WHERE and GROUP BY clauses. Trying to filter with `WHERE ROW_NUMBER() OVER (...) = 1` causes a syntax error. Wrap in a CTE instead.",
                incorrect_sql="SELECT id FROM employees WHERE ROW_NUMBER() OVER (ORDER BY hire_date) = 1;",
                corrected_sql="WITH Ranked AS (SELECT id, ROW_NUMBER() OVER (ORDER BY hire_date) AS rn FROM employees) SELECT id FROM Ranked WHERE rn = 1;",
            ),
            CommonMistake(
                pitfall="Confusing RANK with DENSE_RANK on Gaps",
                explanation="Using RANK for 'Top 3' when ties exist will skip ranks, potentially excluding candidates (e.g. ranks 1, 2, 2, 4 means 4 is excluded even if it's the 3rd highest distinct salary).",
                incorrect_sql="-- May skip 3rd salary tier on ties\nWHERE RANK() OVER (...) <= 3",
                corrected_sql="-- Preserves distinct top 3 tiers\nWHERE DENSE_RANK() OVER (...) <= 3",
            ),
        ],
        real_world_use_cases=[
            "LeetCode #185: Department Top 3 Salaries (The most famous SQL interview problem).",
            "E-Commerce: Identifying the top 5 bestselling products in each category.",
            "Customer Support: Assigning tickets to the next available agent using round-robin row numbering.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-5-1-1",
                slug="dense-rank-department-salaries",
                title="Top 2 Earners Per Department (DENSE_RANK)",
                difficulty="hard",
                prompt="Using a CTE and DENSE_RANK(), find the top 2 highest-paid employees in departments 1, 3, and 5. Return department_id, first_name, last_name, base_salary, and rank as salary_rank. Filter where department_id IN (1, 3, 5) and salary_rank <= 2. Order by department_id ASC, salary_rank ASC, last_name ASC.",
                starter_sql="WITH Ranked AS (\n    SELECT e.department_id, e.first_name, e.last_name, s.base_salary,\n           DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY s.base_salary DESC) AS salary_rank\n    FROM employees e\n    JOIN salaries s ON e.id = s.employee_id\n    WHERE e.department_id IN (1, 3, 5)\n)\nSELECT department_id, first_name, last_name, base_salary, salary_rank\nFROM Ranked\nWHERE salary_rank <= 2\nORDER BY department_id ASC, salary_rank ASC, last_name ASC;",
                solution_sql="WITH Ranked AS (SELECT e.department_id, e.first_name, e.last_name, s.base_salary, DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY s.base_salary DESC) AS salary_rank FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id IN (1, 3, 5)) SELECT department_id, first_name, last_name, base_salary, salary_rank FROM Ranked WHERE salary_rank <= 2 ORDER BY department_id ASC, salary_rank ASC, last_name ASC;",
                hints=["Partition by `e.department_id` and order by `s.base_salary DESC` inside DENSE_RANK().", "Filter `salary_rank <= 2` in the outer query."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-1-2",
                slug="senior-hire-per-department",
                title="First Hired Employee in Each Department",
                difficulty="medium",
                prompt="Using ROW_NUMBER() partitioned by department_id and ordered by hire_date ASC, find the first employee hired in each department. Filter out NULL department_ids. Return department_id, id AS employee_id, first_name, and hire_date ordered by department_id ASC.",
                starter_sql="WITH Hires AS (\n    SELECT department_id, id, first_name, hire_date,\n           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY hire_date ASC) AS rn\n    FROM employees\n    WHERE department_id IS NOT NULL\n)\nSELECT department_id, id AS employee_id, first_name, hire_date\nFROM Hires\nWHERE rn = 1\nORDER BY department_id ASC;",
                solution_sql="WITH Hires AS (SELECT department_id, id, first_name, hire_date, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY hire_date ASC) AS rn FROM employees WHERE department_id IS NOT NULL) SELECT department_id, id AS employee_id, first_name, hire_date FROM Hires WHERE rn = 1 ORDER BY department_id ASC;",
                hints=["Partition by `department_id` and order by `hire_date ASC`.", "Filter `rn = 1` in the outer query."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-1-3",
                slug="global-salary-ranking-row-number",
                title="Global Company Salary Ranking",
                difficulty="easy",
                prompt="Assign a global row number to all employees ordered by base_salary DESC, id ASC. Return e.id, e.first_name, s.base_salary, and row_number as global_rank. Limit to the top 5.",
                starter_sql="SELECT e.id, e.first_name, s.base_salary,\n       ROW_NUMBER() OVER (ORDER BY s.base_salary DESC, e.id ASC) AS global_rank\nFROM employees e\nJOIN salaries s ON e.id = s.employee_id\nORDER BY global_rank ASC\nLIMIT 5;",
                solution_sql="SELECT e.id, e.first_name, s.base_salary, ROW_NUMBER() OVER (ORDER BY s.base_salary DESC, e.id ASC) AS global_rank FROM employees e JOIN salaries s ON e.id = s.employee_id ORDER BY global_rank ASC LIMIT 5;",
                hints=["Use `ROW_NUMBER() OVER (ORDER BY s.base_salary DESC, e.id ASC)`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-1-4",
                slug="customer-order-sequence-number",
                title="Number Customer Orders Chronologically",
                difficulty="medium",
                prompt="In ecommerce_db, assign a sequential order_seq (1, 2, 3...) to each order placed by customer_id = 101, ordered by order_date ASC, id ASC. Return id AS order_id, order_date, total_amount, and order_seq.",
                starter_sql="SELECT id AS order_id, order_date, total_amount,\n       ROW_NUMBER() OVER (ORDER BY order_date ASC, id ASC) AS order_seq\nFROM orders\nWHERE customer_id = 101\nORDER BY order_seq ASC;",
                solution_sql="SELECT id AS order_id, order_date, total_amount, ROW_NUMBER() OVER (ORDER BY order_date ASC, id ASC) AS order_seq FROM orders WHERE customer_id = 101 ORDER BY order_seq ASC;",
                hints=["Filter for `customer_id = 101`.", "Order by `order_date ASC, id ASC` in the OVER clause."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-1-5",
                slug="rank-branches-by-assets",
                title="Rank Branches by Asset Size",
                difficulty="easy",
                prompt="In banking_db, rank all branches in descending order of total_assets using RANK(). Return branch_name, total_assets, and asset_rank. Order by asset_rank ASC.",
                starter_sql="SELECT branch_name, total_assets,\n       RANK() OVER (ORDER BY total_assets DESC) AS asset_rank\nFROM branches\nORDER BY asset_rank ASC;",
                solution_sql="SELECT branch_name, total_assets, RANK() OVER (ORDER BY total_assets DESC) AS asset_rank FROM branches ORDER BY asset_rank ASC;",
                hints=["Use `RANK() OVER (ORDER BY total_assets DESC)`."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-5-2",
        slug="lag-lead-running-totals",
        level_number=5,
        level_title="Level 5: Window Functions & Analytics",
        title="Time Series & Framing: LAG, LEAD, Running Totals",
        order_index=2,
        database_id="db-banking",
        database_name="banking_db",
        learning_objectives=[
            "Access adjacent preceding and following rows without self-joins using LAG and LEAD.",
            "Compute Period-over-Period (MoM/YoY) percentage changes.",
            "Calculate cumulative running totals using window frames.",
            "Master ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.",
        ],
        prerequisites=[
            "Ranking Window Functions (Level 5, Lesson 1).",
        ],
        detailed_explanation="""In analytical reporting, business queries frequently require comparing the current row's value to the row that immediately preceded it (e.g. Month-over-Month revenue delta) or calculating a continuous cumulative sum over time.

1. The LAG() and LEAD() Functions:
- `LAG(column, offset, default)`: Accesses data from a previous row in the partition (offset defaults to 1).
- `LEAD(column, offset, default)`: Accesses data from a subsequent following row in the partition.

2. Window Framing & Cumulative Running Sums:
When calculating running totals, SQL allows defining the window frame:
`SUM(amount) OVER (PARTITION BY account_id ORDER BY transaction_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`
- `UNBOUNDED PRECEDING`: Starts from the very first row of the partition.
- `CURRENT ROW`: Ends at the current evaluated row.
As the engine scans forward, each row outputs the cumulative sum of all transactions up to that exact point in time!

3. Moving Averages:
By adjusting the frame boundaries, moving averages (e.g. 7-day or 3-row moving average) are easily calculated:
`AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`""",
        syntax_reference="""-- Prior Value Comparison
SELECT 
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date ASC) AS prior_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date ASC) AS period_delta
FROM daily_sales;

-- Cumulative Running Total
SELECT 
    account_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY account_id 
        ORDER BY transaction_date ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_balance
FROM transactions;""",
        clause_breakdown=[
            ClauseExplanation(keyword="LAG()", purpose="Retrieves a column value from N rows prior within the ordered window partition.", notes="Returns NULL if prior row does not exist, unless a default value is passed."),
            ClauseExplanation(keyword="LEAD()", purpose="Retrieves a column value from N rows ahead within the ordered window partition.", notes="Essential for lead-time and event interval calculations."),
            ClauseExplanation(keyword="ROWS BETWEEN", purpose="Explicitly defines the physical sliding frame of rows to include in the calculation.", notes="Default frame with ORDER BY is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW."),
            ClauseExplanation(keyword="UNBOUNDED PRECEDING", purpose="Designates the very beginning of the partition as the frame starting boundary.", notes="Core component of cumulative sums."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Delta Between Consecutive Transactions (LAG)",
                explanation="Examine account 1001 transaction amounts and compute the difference from the previous transaction.",
                sql="SELECT id, transaction_type, amount, LAG(amount, 1, 0.00) OVER (ORDER BY transaction_date ASC, id ASC) AS prev_amount, ROUND(amount - LAG(amount, 1, amount) OVER (ORDER BY transaction_date ASC, id ASC), 2) AS amount_diff FROM transactions WHERE account_id = 1001 ORDER BY transaction_date ASC, id ASC LIMIT 4;",
                columns=["id", "transaction_type", "amount", "prev_amount", "amount_diff"],
                rows=[
                    [1, "DEPOSIT", 5000.00, 0.00, 0.00],
                    [2, "WITHDRAWAL", 850.00, 5000.00, -4150.00],
                    [3, "TRANSFER_OUT", 1000.00, 850.00, 150.00],
                    [5, "FEE", 15.00, 1000.00, -985.00],
                ],
            ),
            WorkedExample(
                title="Example 2: Cumulative Deposit Running Total (ROWS BETWEEN)",
                explanation="Calculate the continuous running sum of deposits across the bank over time.",
                sql="SELECT id, transaction_date, amount, SUM(amount) OVER (ORDER BY transaction_date ASC, id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_deposit_total FROM transactions WHERE transaction_type = 'DEPOSIT' ORDER BY transaction_date ASC, id ASC LIMIT 4;",
                columns=["id", "transaction_date", "amount", "running_deposit_total"],
                rows=[
                    [1, "2023-01-05", 5000.00, 5000.00],
                    [7, "2023-01-15", 6200.00, 11200.00],
                    [10, "2023-01-20", 8500.00, 19700.00],
                    [12, "2023-02-01", 12000.00, 31700.00],
                ],
            ),
            WorkedExample(
                title="Example 3: 3-Row Rolling Moving Average",
                explanation="Compute a 3-row moving average (current row plus two preceding rows) of deposit amounts.",
                sql="SELECT id, transaction_date, amount, ROUND(AVG(amount) OVER (ORDER BY transaction_date ASC, id ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3_txns FROM transactions WHERE transaction_type = 'DEPOSIT' ORDER BY transaction_date ASC, id ASC LIMIT 4;",
                columns=["id", "transaction_date", "amount", "moving_avg_3_txns"],
                rows=[
                    [1, "2023-01-05", 5000.00, 5000.00],
                    [7, "2023-01-15", 6200.00, 5600.00],
                    [10, "2023-01-20", 8500.00, 6566.67],
                    [12, "2023-02-01", 12000.00, 8900.00],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Default Window Frame with ORDER BY (RANGE vs ROWS)",
                explanation="Without `ROWS BETWEEN`, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. If rows tie on date, RANGE aggregates all tied rows simultaneously, creating duplicate running sums!",
                incorrect_sql="SUM(amount) OVER (ORDER BY transaction_date)",
                corrected_sql="SUM(amount) OVER (ORDER BY transaction_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
            ),
            CommonMistake(
                pitfall="Forgetting Tie-Breakers in ORDER BY for LAG",
                explanation="If duplicate timestamps exist in a table, `LAG()` order is non-deterministic unless a secondary unique tie-breaker column (e.g. `id ASC`) is included in ORDER BY.",
                incorrect_sql="LAG(amount) OVER (ORDER BY transaction_date)",
                corrected_sql="LAG(amount) OVER (ORDER BY transaction_date ASC, id ASC)",
            ),
        ],
        real_world_use_cases=[
            "Financial Ledger Auditing: Calculating continuous running balances and detecting accounting discrepancies.",
            "E-Commerce Time-to-Next-Order: Measuring churn velocity using `LEAD(order_date) - order_date`.",
            "Stock Market Trading Systems: Calculating 50-day and 200-day Simple Moving Averages (SMA).",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-5-2-1",
                slug="cumulative-revenue-growth",
                title="Cumulative Revenue Running Total",
                difficulty="medium",
                prompt="In ecommerce_db, calculate a cumulative running total of revenue for completed orders. Select id AS order_id, order_date, total_amount, and running_revenue using SUM(total_amount) OVER (ORDER BY order_date ASC, id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) for orders WHERE status = 'COMPLETED'. Order by order_date ASC, id ASC LIMIT 5.",
                starter_sql="SELECT id AS order_id, order_date, total_amount,\n       ROUND(SUM(total_amount) OVER (ORDER BY order_date ASC, id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_revenue\nFROM orders\nWHERE status = 'COMPLETED'\nORDER BY order_date ASC, id ASC\nLIMIT 5;",
                solution_sql="SELECT id AS order_id, order_date, total_amount, ROUND(SUM(total_amount) OVER (ORDER BY order_date ASC, id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_revenue FROM orders WHERE status = 'COMPLETED' ORDER BY order_date ASC, id ASC LIMIT 5;",
                hints=["Use `SUM(total_amount) OVER (...)` with `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-2-2",
                slug="prior-order-comparison-lag",
                title="Compare Current Order to Prior Order (LAG)",
                difficulty="medium",
                prompt="For customer_id = 101 in ecommerce_db, select id AS order_id, order_date, total_amount, and prev_order_amount using LAG(total_amount, 1, 0.00) OVER (ORDER BY order_date ASC, id ASC). Order by order_date ASC, id ASC.",
                starter_sql="SELECT id AS order_id, order_date, total_amount,\n       LAG(total_amount, 1, 0.00) OVER (ORDER BY order_date ASC, id ASC) AS prev_order_amount\nFROM orders\nWHERE customer_id = 101\nORDER BY order_date ASC, id ASC;",
                solution_sql="SELECT id AS order_id, order_date, total_amount, LAG(total_amount, 1, 0.00) OVER (ORDER BY order_date ASC, id ASC) AS prev_order_amount FROM orders WHERE customer_id = 101 ORDER BY order_date ASC, id ASC;",
                hints=["Use `LAG(total_amount, 1, 0.00)`.", "Filter for `customer_id = 101`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-2-3",
                slug="next-transaction-lead",
                title="Inspect Following Transaction with LEAD",
                difficulty="easy",
                prompt="In banking_db, select id AS txn_id, account_id, amount, and next_amount using LEAD(amount, 1) OVER (ORDER BY id ASC) from transactions WHERE account_id = 1001 ORDER BY id ASC LIMIT 4.",
                starter_sql="SELECT id AS txn_id, account_id, amount,\n       LEAD(amount, 1) OVER (ORDER BY id ASC) AS next_amount\nFROM transactions\nWHERE account_id = 1001\nORDER BY id ASC\nLIMIT 4;",
                solution_sql="SELECT id AS txn_id, account_id, amount, LEAD(amount, 1) OVER (ORDER BY id ASC) AS next_amount FROM transactions WHERE account_id = 1001 ORDER BY id ASC LIMIT 4;",
                hints=["Use `LEAD(amount, 1) OVER (ORDER BY id ASC)`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-2-4",
                slug="running-account-transaction-balance",
                title="Continuous Balance Calculation",
                difficulty="hard",
                prompt="In banking_db for account_id = 1001, calculate running_net by summing the signed amount (if transaction_type = 'DEPOSIT' then amount else -amount) over the window ordered by transaction_date ASC, id ASC. Return id, transaction_type, amount, and running_net. Order by id ASC LIMIT 5.",
                starter_sql="SELECT id, transaction_type, amount,\n       SUM(CASE WHEN transaction_type = 'DEPOSIT' THEN amount ELSE -amount END) OVER (\n           ORDER BY transaction_date ASC, id ASC\n           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n       ) AS running_net\nFROM transactions\nWHERE account_id = 1001\nORDER BY id ASC\nLIMIT 5;",
                solution_sql="SELECT id, transaction_type, amount, SUM(CASE WHEN transaction_type = 'DEPOSIT' THEN amount ELSE -amount END) OVER (ORDER BY transaction_date ASC, id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_net FROM transactions WHERE account_id = 1001 ORDER BY id ASC LIMIT 5;",
                hints=["Use a CASE expression inside SUM: `CASE WHEN transaction_type = 'DEPOSIT' THEN amount ELSE -amount END`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-5-2-5",
                slug="three-order-moving-average",
                title="3-Order Moving Average Spending",
                difficulty="medium",
                prompt="In ecommerce_db, compute a 3-order moving average of total_amount (current row plus two preceding rows) for completed orders, rounded to 2 decimal places as moving_avg. Return id AS order_id, order_date, total_amount, and moving_avg ordered by id ASC LIMIT 5.",
                starter_sql="SELECT id AS order_id, order_date, total_amount,\n       ROUND(AVG(total_amount) OVER (\n           ORDER BY id ASC\n           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n       ), 2) AS moving_avg\nFROM orders\nWHERE status = 'COMPLETED'\nORDER BY id ASC\nLIMIT 5;",
                solution_sql="SELECT id AS order_id, order_date, total_amount, ROUND(AVG(total_amount) OVER (ORDER BY id ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg FROM orders WHERE status = 'COMPLETED' ORDER BY id ASC LIMIT 5;",
                hints=["Use `AVG(total_amount) OVER (...)` with `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`."],
                order_matters=True,
            ),
        ],
    ),
]
