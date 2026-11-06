from typing import List
from app.curriculum.models import (
    TopicLesson,
    ClauseExplanation,
    WorkedExample,
    CommonMistake,
    PracticeQuestion,
)

LEVEL_4_LESSONS: List[TopicLesson] = [
    TopicLesson(
        id="les-4-1",
        slug="subqueries-and-exists",
        level_number=4,
        level_title="Level 4: Advanced SQL & CTEs",
        title="Scalar Subqueries, Correlated Subqueries & EXISTS",
        order_index=1,
        database_id="db-university",
        database_name="university_db",
        learning_objectives=[
            "Distinguish between scalar, column, and table subqueries.",
            "Understand correlated subqueries and their row-by-row execution mechanics.",
            "Master EXISTS and NOT EXISTS for short-circuit existential checks.",
            "Compare the performance characteristics of EXISTS vs IN with NULLs.",
        ],
        prerequisites=[
            "Level 3: Relational JOINs (INNER and LEFT JOINs).",
        ],
        detailed_explanation="""A subquery (or nested query) is a SELECT statement enclosed in parentheses within an outer query. Subqueries allow you to compute intermediate values dynamically without hardcoding magic numbers.

1. Subquery Classifications:
- Scalar Subquery: Returns exactly one value (one row, one column). Can be used anywhere a literal expression is valid: `WHERE price > (SELECT AVG(price) FROM products)`.
- Multi-Row Subquery: Returns a single column containing multiple rows. Evaluated using membership operators: `WHERE id IN (SELECT student_id FROM enrollments)`.
- Table Subquery: Returns multiple rows and multiple columns, treated as an inline derived table in the FROM clause.

2. Correlated Subqueries:
A standard subquery executes once independently. In contrast, a correlated subquery references columns from the outer query. The database engine re-evaluates the inner subquery for each candidate row evaluated by the outer query:
```sql
SELECT s.first_name, s.salary
FROM salaries s
WHERE s.base_salary > (
    SELECT AVG(s2.base_salary) 
    FROM employees e2
    JOIN salaries s2 ON e2.id = s2.employee_id
    WHERE e2.department_id = s.department_id
);
```

3. The EXISTS Operator:
Tests for the presence of qualifying rows in a subquery: `WHERE EXISTS (SELECT 1 FROM ...)`.
Unlike `IN`, which fetches all values into memory, `EXISTS` short-circuits: the moment the database engine encounters the very first matching row, it immediately returns TRUE without scanning the remainder of the table.""",
        syntax_reference="""-- Scalar Subquery Comparison
SELECT title, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- Existential Check with EXISTS
SELECT s.id, s.first_name, s.last_name
FROM students s
WHERE EXISTS (
    SELECT 1 
    FROM enrollments e 
    WHERE e.student_id = s.id AND e.course_id = 101
);""",
        clause_breakdown=[
            ClauseExplanation(keyword="EXISTS", purpose="Returns TRUE if the enclosed subquery returns at least one row, FALSE otherwise.", notes="Employs short-circuit evaluation for maximum performance."),
            ClauseExplanation(keyword="NOT EXISTS", purpose="Returns TRUE if the enclosed subquery returns zero rows.", notes="Immune to NULL pitfalls that plague NOT IN."),
            ClauseExplanation(keyword="Correlated Subquery", purpose="A subquery that references attributes from an outer query scope.", notes="Evaluates dynamically per outer tuple."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Students Enrolled in Database Internals (EXISTS)",
                explanation="Find student names who are enrolled in CS-305 (Relational Database Design) using an EXISTS check.",
                sql="SELECT s.id, s.first_name, s.last_name, s.email FROM students s WHERE EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.id AND e.course_id = 103) ORDER BY s.id ASC LIMIT 4;",
                columns=["id", "first_name", "last_name", "email"],
                rows=[
                    [1001, "Alice", "Smith", "alice.smith@university.edu"],
                    [1002, "Bob", "Jones", "bob.jones@university.edu"],
                    [1004, "Diana", "Prince", "diana.p@university.edu"],
                    [1008, "Hannah", "Abbott", "hannah.a@university.edu"],
                ],
            ),
            WorkedExample(
                title="Example 2: Unenrolled Freshmen (NOT EXISTS)",
                explanation="Identify students who have zero recorded course registrations across all semesters.",
                sql="SELECT s.id, s.first_name, s.last_name, s.enrollment_year FROM students s WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.id) ORDER BY s.id ASC LIMIT 4;",
                columns=["id", "first_name", "last_name", "enrollment_year"],
                rows=[
                    [2001, "Zack", "Morris", 2023],
                    [2002, "Betty", "Cooper", 2023],
                    [2003, "Clark", "Kent", 2023],
                    [2004, "Daisy", "Johnson", 2023],
                ],
            ),
            WorkedExample(
                title="Example 3: Scalar Subquery Filtering (Above-Average Pricing)",
                explanation="Find courses that award strictly more academic credits than the overall average credits across the university.",
                sql="SELECT code, title, credits FROM courses WHERE credits > (SELECT AVG(credits) FROM courses) ORDER BY code ASC LIMIT 4;",
                columns=["code", "title", "credits"],
                rows=[
                    ["CS-101", "Introduction to Computer Science & Algorithms", 4],
                    ["CS-102", "Data Structures & System Software", 4],
                    ["CS-305", "Relational Database Design & SQL Internals", 4],
                    ["CS-402", "Compilers, Parsing & Virtual Machines", 4],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="The Lethal NOT IN with NULL Pitfall",
                explanation="If the subquery inside `NOT IN` returns even a single NULL value, the entire expression evaluates to UNKNOWN, returning zero rows! Always use `NOT EXISTS` instead.",
                incorrect_sql="SELECT * FROM students WHERE id NOT IN (SELECT student_id FROM enrollments);",
                corrected_sql="SELECT * FROM students s WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.id);",
            ),
            CommonMistake(
                pitfall="Scalar Subquery Returning Multiple Rows",
                explanation="Using `=` with a subquery that yields more than 1 row produces a fatal runtime error: 'subquery returned more than 1 row'.",
                incorrect_sql="SELECT * FROM courses WHERE department_id = (SELECT id FROM departments WHERE building LIKE '%Hall%');",
                corrected_sql="SELECT * FROM courses WHERE department_id IN (SELECT id FROM departments WHERE building LIKE '%Hall%');",
            ),
        ],
        real_world_use_cases=[
            "Access Control Auditing: Identifying user accounts with zero recorded logins or missing permission groups.",
            "Dynamic Thresholding: Comparing individual transactional values against daily rolling benchmark averages.",
            "Inventory Stock Alerts: Isolating items whose current warehouse stock falls below the regional reorder threshold.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-4-1-1",
                slug="courses-with-no-students-not-exists",
                title="Find Abandoned Courses with Zero Enrollments",
                difficulty="medium",
                prompt="Using NOT EXISTS, find all courses in university_db that have zero students enrolled in the enrollments table. Return course code, title, and credits ordered by code ASC.",
                starter_sql="SELECT c.code, c.title, c.credits\nFROM courses c\nWHERE NOT EXISTS (\n    -- Write subquery\n)\nORDER BY c.code ASC;",
                solution_sql="SELECT c.code, c.title, c.credits FROM courses c WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.course_id = c.id) ORDER BY c.code ASC;",
                hints=["Check `WHERE e.course_id = c.id` in the subquery.", "Use `NOT EXISTS`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-1-2",
                slug="students-above-average-enrollment-count",
                title="Students Enrolled in at Least 3 Courses",
                difficulty="medium",
                prompt="From students s in university_db, find id, first_name, and last_name of students who have at least 3 enrollments using a subquery with IN or an EXISTS clause. Order by s.id ASC LIMIT 5.",
                starter_sql="SELECT s.id, s.first_name, s.last_name\nFROM students s\nWHERE s.id IN (\n    SELECT student_id FROM enrollments GROUP BY student_id HAVING COUNT(*) >= 3\n)\nORDER BY s.id ASC\nLIMIT 5;",
                solution_sql="SELECT s.id, s.first_name, s.last_name FROM students s WHERE s.id IN (SELECT student_id FROM enrollments GROUP BY student_id HAVING COUNT(*) >= 3) ORDER BY s.id ASC LIMIT 5;",
                hints=["Use `WHERE s.id IN (SELECT student_id FROM enrollments GROUP BY student_id HAVING COUNT(*) >= 3)`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-1-3",
                slug="salaries-above-department-average-correlated",
                title="Employees Earning More Than Department Average",
                difficulty="hard",
                prompt="In company_db, find employee_id and base_salary for employees whose base_salary exceeds the average base_salary of their own department. Filter out NULL departments. Order by base_salary DESC, employee_id ASC LIMIT 5.",
                starter_sql="SELECT e.id AS employee_id, s.base_salary\nFROM employees e\nJOIN salaries s ON e.id = s.employee_id\nWHERE e.department_id IS NOT NULL\n  AND s.base_salary > (\n      SELECT AVG(s2.base_salary)\n      FROM employees e2\n      JOIN salaries s2 ON e2.id = s2.employee_id\n      WHERE e2.department_id = e.department_id\n  )\nORDER BY s.base_salary DESC, employee_id ASC\nLIMIT 5;",
                solution_sql="SELECT e.id AS employee_id, s.base_salary FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id IS NOT NULL AND s.base_salary > (SELECT AVG(s2.base_salary) FROM employees e2 JOIN salaries s2 ON e2.id = s2.employee_id WHERE e2.department_id = e.department_id) ORDER BY s.base_salary DESC, employee_id ASC LIMIT 5;",
                hints=["Correlate `e2.department_id = e.department_id` inside the subquery."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-1-4",
                slug="professors-teaching-multiple-courses",
                title="Professors Teaching 2 or More Courses",
                difficulty="easy",
                prompt="Find id, first_name, and last_name of professors who teach 2 or more courses in university_db. Use a subquery with IN. Order by id ASC.",
                starter_sql="SELECT id, first_name, last_name\nFROM professors\nWHERE id IN (\n    SELECT professor_id FROM courses WHERE professor_id IS NOT NULL GROUP BY professor_id HAVING COUNT(*) >= 2\n)\nORDER BY id ASC;",
                solution_sql="SELECT id, first_name, last_name FROM professors WHERE id IN (SELECT professor_id FROM courses WHERE professor_id IS NOT NULL GROUP BY professor_id HAVING COUNT(*) >= 2) ORDER BY id ASC;",
                hints=["Group by `professor_id` in the subquery with `HAVING COUNT(*) >= 2`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-1-5",
                slug="customers-with-large-orders-exists",
                title="Customers with Orders Over $500 (EXISTS)",
                difficulty="medium",
                prompt="In ecommerce_db, return id, first_name, and email for customers who have at least one completed order with total_amount >= 500.00 using an EXISTS clause. Order by id ASC.",
                starter_sql="SELECT c.id, c.first_name, c.email\nFROM customers c\nWHERE EXISTS (\n    -- Subquery checking orders\n)\nORDER BY c.id ASC;",
                solution_sql="SELECT c.id, c.first_name, c.email FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status = 'COMPLETED' AND o.total_amount >= 500.00) ORDER BY c.id ASC;",
                hints=["Check `o.customer_id = c.id`, `o.status = 'COMPLETED'`, and `o.total_amount >= 500.00` in EXISTS."],
                order_matters=True,
            ),
        ],
    ),
    TopicLesson(
        id="les-4-2",
        slug="common-table-expressions-cte",
        level_number=4,
        level_title="Level 4: Advanced SQL & CTEs",
        title="Common Table Expressions (WITH CTEs) & Recursive Queries",
        order_index=2,
        database_id="db-company",
        database_name="company_db",
        learning_objectives=[
            "Construct modular, readable analytical pipelines using Common Table Expressions (WITH).",
            "Chain multiple CTEs in a single query.",
            "Master Recursive CTEs for traversing tree hierarchies and generating sequences.",
            "Understand when the database optimizer materializes or inlines CTE expressions.",
        ],
        prerequisites=[
            "Subqueries and Correlated Queries (Level 4, Lesson 1).",
        ],
        detailed_explanation="""Complex SQL queries with deeply nested subqueries quickly become unreadable and difficult to maintain. Common Table Expressions (CTEs), defined using the `WITH` clause, allow you to break complex data transformations into clean, named, modular steps.

1. Standard CTEs:
A CTE defines a temporary named result set that exists only during the execution of a single query:
```sql
WITH HighEarners AS (
    SELECT employee_id, base_salary
    FROM salaries
    WHERE base_salary >= 180000
)
SELECT e.first_name, e.last_name, h.base_salary
FROM employees e
JOIN HighEarners h ON e.id = h.employee_id;
```
Multiple CTEs can be chained together by separating them with commas.

2. Recursive CTEs:
A Recursive CTE is a powerful SQL construct capable of self-referencing to traverse graph data structures, org-chart hierarchies, and bill-of-materials trees.
A Recursive CTE contains two distinct parts joined by `UNION ALL`:
- Anchor Member: The base query that initiates the recursion (e.g. finding the CEO where `manager_id IS NULL`).
- Recursive Member: The query that references the CTE itself, executing iteratively until no new rows are produced.

Recursive CTEs are the gold standard for calculating organizational depth levels, bill-of-materials rollups, and pathfinding.""",
        syntax_reference="""-- Chained CTEs
WITH StepOne AS (
    SELECT id, name FROM departments WHERE budget > 1000000
),
StepTwo AS (
    SELECT e.id, e.first_name, s.name AS dept_name
    FROM employees e
    JOIN StepOne s ON e.department_id = s.id
)
SELECT * FROM StepTwo;

-- Recursive CTE for Hierarchies
WITH RECURSIVE OrgHierarchy AS (
    -- Anchor Member
    SELECT id, first_name, manager_id, 1 AS depth_level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    -- Recursive Member
    SELECT e.id, e.first_name, e.manager_id, o.depth_level + 1
    FROM employees e
    JOIN OrgHierarchy o ON e.manager_id = o.id
)
SELECT * FROM OrgHierarchy;""",
        clause_breakdown=[
            ClauseExplanation(keyword="WITH", purpose="Introduces one or more Common Table Expressions (CTEs).", notes="Placed at the very beginning of the statement before the outer SELECT."),
            ClauseExplanation(keyword="RECURSIVE", purpose="Notifies the query optimizer that the CTE will self-reference to execute recursive loops.", notes="Required in SQLite, PostgreSQL, and MySQL for recursive CTEs."),
            ClauseExplanation(keyword="UNION ALL", purpose="Combines the anchor query result with the recursive iteration results.", notes="Essential for recursion termination."),
        ],
        worked_examples=[
            WorkedExample(
                title="Example 1: Department Spend & Headcount Analysis (Chained CTEs)",
                explanation="Calculate total compensation and headcount per department, then filter for departments spending > $500K.",
                sql="WITH DeptMetrics AS (SELECT e.department_id, COUNT(e.id) AS headcount, SUM(s.base_salary) AS total_payroll FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id IS NOT NULL GROUP BY e.department_id) SELECT d.name AS department_name, m.headcount, m.total_payroll FROM departments d JOIN DeptMetrics m ON d.id = m.department_id WHERE m.total_payroll > 500000.00 ORDER BY m.total_payroll DESC LIMIT 3;",
                columns=["department_name", "headcount", "total_payroll"],
                rows=[
                    ["Engineering", 17, 2576000.00],
                    ["Product & Design", 5, 785000.00],
                    ["Sales & Accounts", 5, 723000.00],
                ],
            ),
            WorkedExample(
                title="Example 2: Organizational Hierarchy Traversal (Recursive CTE)",
                explanation="Traverse the management chain starting from CEO Evelyn Vance (depth 1) down to Directors (depth 3).",
                sql="WITH RECURSIVE OrgChart AS (SELECT id, first_name || ' ' || last_name AS name, title, manager_id, 1 AS hierarchy_level FROM employees WHERE id = 1 UNION ALL SELECT e.id, e.first_name || ' ' || e.last_name, e.title, e.manager_id, o.hierarchy_level + 1 FROM employees e JOIN OrgChart o ON e.manager_id = o.id) SELECT id, name, title, hierarchy_level FROM OrgChart WHERE hierarchy_level <= 3 ORDER BY hierarchy_level ASC, id ASC LIMIT 6;",
                columns=["id", "name", "title", "hierarchy_level"],
                rows=[
                    [1, "Evelyn Vance", "Chief Executive Officer", 1],
                    [2, "Marcus Sterling", "VP of Engineering", 2],
                    [3, "Nadia Kowalski", "VP of Product", 2],
                    [4, "Julian Mercer", "VP of Marketing", 2],
                    [5, "Victoria Stone", "VP of Global Sales", 2],
                    [6, "Arthur Pendleton", "Chief People Officer", 2],
                ],
            ),
            WorkedExample(
                title="Example 3: Generating Number Sequences with Recursive CTE",
                explanation="Generate a calendar sequence of integers from 1 to 5 dynamically without an underlying physical table.",
                sql="WITH RECURSIVE NumberSeq(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM NumberSeq WHERE n < 5) SELECT n, n * 10 AS multiplier FROM NumberSeq;",
                columns=["n", "multiplier"],
                rows=[
                    [1, 10],
                    [2, 20],
                    [3, 30],
                    [4, 40],
                    [5, 50],
                ],
            ),
        ],
        common_mistakes=[
            CommonMistake(
                pitfall="Infinite Recursion in Recursive CTEs",
                explanation="Omitting the terminating condition in the recursive member (e.g. `WHERE n < 100`) causes an infinite loop until aborted by execution timeouts.",
                incorrect_sql="WITH RECURSIVE bad(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM bad) SELECT * FROM bad;",
                corrected_sql="WITH RECURSIVE safe(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM safe WHERE x < 10) SELECT * FROM safe;",
            ),
            CommonMistake(
                pitfall="Using Multiple WITH Keywords",
                explanation="Multiple CTEs are separated by commas; writing `WITH cte1 AS (...) WITH cte2 AS (...)` causes a syntax error.",
                incorrect_sql="WITH a AS (SELECT 1) WITH b AS (SELECT 2) SELECT * FROM a, b;",
                corrected_sql="WITH a AS (SELECT 1), b AS (SELECT 2) SELECT * FROM a, b;",
            ),
        ],
        real_world_use_cases=[
            "Org Chart Visualizations: Generating reporting chain breadcrumbs (e.g. CEO > VP > Director > Manager).",
            "Bill of Materials: Exploding nested assembly components in manufacturing manufacturing software.",
            "Multi-Touch Attribution: Chaining sequential customer conversion touchpoint events.",
        ],
        practice_questions=[
            PracticeQuestion(
                id="q-4-2-1",
                slug="cte-department-salary-outliers",
                title="Department Payroll Summaries with CTE",
                difficulty="medium",
                prompt="Using a CTE named DeptStats, calculate department_id, COUNT(*) AS emp_count, and AVG(s.base_salary) AS avg_sal from employees e JOIN salaries s on e.id = s.employee_id WHERE e.department_id IS NOT NULL GROUP BY e.department_id. In the outer query, select department_id, emp_count, and ROUND(avg_sal, 2) AS avg_sal where emp_count >= 5 ORDER BY avg_sal DESC.",
                starter_sql="WITH DeptStats AS (\n    -- Calculate stats\n)\nSELECT department_id, emp_count, ROUND(avg_sal, 2) AS avg_sal\nFROM DeptStats\nWHERE emp_count >= 5\nORDER BY avg_sal DESC;",
                solution_sql="WITH DeptStats AS (SELECT e.department_id, COUNT(*) AS emp_count, AVG(s.base_salary) AS avg_sal FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id IS NOT NULL GROUP BY e.department_id) SELECT department_id, emp_count, ROUND(avg_sal, 2) AS avg_sal FROM DeptStats WHERE emp_count >= 5 ORDER BY avg_sal DESC;",
                hints=["Construct the CTE with GROUP BY `e.department_id`.", "Filter `emp_count >= 5` in the outer query."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-2-2",
                slug="recursive-org-chain-depth",
                title="Calculate Employee Depth Level in Org Tree",
                difficulty="hard",
                prompt="Using a Recursive CTE named OrgTree, start with employee id = 1 (depth = 1). Traverse downwards to find all employees reporting to them directly or indirectly. Return id, first_name, manager_id, and depth. Order by depth ASC, id ASC LIMIT 7.",
                starter_sql="WITH RECURSIVE OrgTree AS (\n    SELECT id, first_name, manager_id, 1 AS depth\n    FROM employees WHERE id = 1\n    UNION ALL\n    SELECT e.id, e.first_name, e.manager_id, o.depth + 1\n    FROM employees e\n    JOIN OrgTree o ON e.manager_id = o.id\n)\nSELECT id, first_name, manager_id, depth FROM OrgTree ORDER BY depth ASC, id ASC LIMIT 7;",
                solution_sql="WITH RECURSIVE OrgTree AS (SELECT id, first_name, manager_id, 1 AS depth FROM employees WHERE id = 1 UNION ALL SELECT e.id, e.first_name, e.manager_id, o.depth + 1 FROM employees e JOIN OrgTree o ON e.manager_id = o.id) SELECT id, first_name, manager_id, depth FROM OrgTree ORDER BY depth ASC, id ASC LIMIT 7;",
                hints=["Anchor member: `WHERE id = 1`.", "Recursive member joins `e.manager_id = o.id`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-2-3",
                slug="generate-date-series-cte",
                title="Generate Consecutive Integers 1 to 5",
                difficulty="easy",
                prompt="Using a Recursive CTE named Counter, generate integer values from 1 to 5 in a column named num. Order by num ASC.",
                starter_sql="WITH RECURSIVE Counter(num) AS (\n    SELECT 1\n    UNION ALL\n    SELECT num + 1 FROM Counter WHERE num < 5\n)\nSELECT num FROM Counter ORDER BY num ASC;",
                solution_sql="WITH RECURSIVE Counter(num) AS (SELECT 1 UNION ALL SELECT num + 1 FROM Counter WHERE num < 5) SELECT num FROM Counter ORDER BY num ASC;",
                hints=["Anchor with `SELECT 1`.", "Increment with `SELECT num + 1 WHERE num < 5`."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-2-4",
                slug="top-earner-per-department-cte",
                title="Isolate Maximum Salary per Department",
                difficulty="hard",
                prompt="Using a CTE named MaxSalaries, find department_id and MAX(base_salary) AS max_sal from employees e JOIN salaries s on e.id = s.employee_id WHERE e.department_id IS NOT NULL GROUP BY e.department_id. Join back in the outer query to return e.department_id, e.first_name, e.last_name, and s.base_salary. Order by e.department_id ASC LIMIT 5.",
                starter_sql="WITH MaxSalaries AS (\n    SELECT e.department_id, MAX(s.base_salary) AS max_sal\n    FROM employees e JOIN salaries s ON e.id = s.employee_id\n    WHERE e.department_id IS NOT NULL GROUP BY e.department_id\n)\nSELECT e.department_id, e.first_name, e.last_name, s.base_salary\nFROM employees e\nJOIN salaries s ON e.id = s.employee_id\nJOIN MaxSalaries m ON e.department_id = m.department_id AND s.base_salary = m.max_sal\nORDER BY e.department_id ASC\nLIMIT 5;",
                solution_sql="WITH MaxSalaries AS (SELECT e.department_id, MAX(s.base_salary) AS max_sal FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE e.department_id IS NOT NULL GROUP BY e.department_id) SELECT e.department_id, e.first_name, e.last_name, s.base_salary FROM employees e JOIN salaries s ON e.id = s.employee_id JOIN MaxSalaries m ON e.department_id = m.department_id AND s.base_salary = m.max_sal ORDER BY e.department_id ASC LIMIT 5;",
                hints=["Join back to employees and salaries on both department_id and base_salary = max_sal."],
                order_matters=True,
            ),
            PracticeQuestion(
                id="q-4-2-5",
                slug="chained-ctes-customer-segmentation",
                title="Chained CTEs for Order Totals",
                difficulty="medium",
                prompt="In ecommerce_db, create two CTEs: TotalSpend (customer_id, SUM(total_amount) AS spend from orders WHERE status = 'COMPLETED' GROUP BY customer_id) and BigSpenders (SELECT customer_id, spend FROM TotalSpend WHERE spend >= 500.00). In the outer query, join customers c to BigSpenders b to return c.id, c.first_name, and b.spend ORDER BY b.spend DESC.",
                starter_sql="WITH TotalSpend AS (\n    SELECT customer_id, SUM(total_amount) AS spend\n    FROM orders WHERE status = 'COMPLETED'\n    GROUP BY customer_id\n),\nBigSpenders AS (\n    SELECT customer_id, spend FROM TotalSpend WHERE spend >= 500.00\n)\nSELECT c.id, c.first_name, b.spend\nFROM customers c\nJOIN BigSpenders b ON c.id = b.customer_id\nORDER BY b.spend DESC;",
                solution_sql="WITH TotalSpend AS (SELECT customer_id, SUM(total_amount) AS spend FROM orders WHERE status = 'COMPLETED' GROUP BY customer_id), BigSpenders AS (SELECT customer_id, spend FROM TotalSpend WHERE spend >= 500.00) SELECT c.id, c.first_name, b.spend FROM customers c JOIN BigSpenders b ON c.id = b.customer_id ORDER BY b.spend DESC;",
                hints=["Chain TotalSpend followed by comma and BigSpenders.", "Join BigSpenders in the outer query."],
                order_matters=True,
            ),
        ],
    ),
]
