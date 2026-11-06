"""
Deterministic synthetic dataset generator for SQL learning platform.
Generates 4 realistic databases:
1. company_db (Employees, Departments, Projects, EmployeeProjects, Salaries, Managers)
2. ecommerce_db (Customers, Categories, Products, Orders, OrderItems, Payments)
3. university_db (Students, Departments, Professors, Courses, Enrollments, Grades)
4. banking_db (Branches, Customers, Accounts, Transactions, Loans)
"""

import sqlite3

def generate_company_sql():
    ddl = """
-- ============================================================
-- DATABASE 1: COMPANY DATABASE SCHEMA
-- ============================================================

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    budget DECIMAL(12,2) NOT NULL CHECK(budget >= 0),
    location VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    department_id INTEGER REFERENCES departments(id),
    manager_id INTEGER REFERENCES employees(id),
    title VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'ON_LEAVE', 'TERMINATED'))
);

CREATE TABLE managers (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL UNIQUE REFERENCES employees(id),
    department_id INTEGER REFERENCES departments(id),
    management_level VARCHAR(30) NOT NULL CHECK(management_level IN ('EXECUTIVE', 'DIRECTOR', 'TEAM_LEAD'))
);

CREATE TABLE salaries (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    base_salary DECIMAL(10,2) NOT NULL CHECK(base_salary > 0),
    bonus DECIMAL(10,2) DEFAULT 0.00 CHECK(bonus >= 0),
    effective_date DATE NOT NULL
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(12,2) CHECK(budget >= 0)
);

CREATE TABLE employee_projects (
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    project_id INTEGER NOT NULL REFERENCES projects(id),
    role VARCHAR(60) NOT NULL,
    hours_allocated INTEGER NOT NULL CHECK(hours_allocated > 0),
    assigned_date DATE NOT NULL,
    PRIMARY KEY (employee_id, project_id)
);
"""

    dml = """
-- 1. DEPARTMENTS
INSERT INTO departments (id, name, budget, location) VALUES
(1, 'Executive Board', 1500000.00, 'San Francisco, CA'),
(2, 'Engineering', 4200000.00, 'San Francisco, CA'),
(3, 'Product & Design', 1800000.00, 'New York, NY'),
(4, 'Marketing & Growth', 2100000.00, 'London, UK'),
(5, 'Sales & Accounts', 3500000.00, 'Austin, TX'),
(6, 'Human Resources', 950000.00, 'San Francisco, CA'),
(7, 'Legal & Compliance', 800000.00, 'Washington, DC');

-- 2. EMPLOYEES (60 Employees: CEO, VPs, Directors, Leads, ICs, Contractors/Floaters)
INSERT INTO employees (id, first_name, last_name, email, department_id, manager_id, title, hire_date, status) VALUES
-- C-Level Executives (manager_id is NULL for CEO)
(1, 'Evelyn', 'Vance', 'evelyn.vance@company.com', 1, NULL, 'Chief Executive Officer', '2018-01-15', 'ACTIVE'),
(2, 'Marcus', 'Sterling', 'marcus.s@company.com', 2, 1, 'VP of Engineering', '2018-03-01', 'ACTIVE'),
(3, 'Nadia', 'Kowalski', 'nadia.k@company.com', 3, 1, 'VP of Product', '2018-06-15', 'ACTIVE'),
(4, 'Julian', 'Mercer', 'julian.m@company.com', 4, 1, 'VP of Marketing', '2019-01-10', 'ACTIVE'),
(5, 'Victoria', 'Stone', 'victoria.s@company.com', 5, 1, 'VP of Global Sales', '2019-02-01', 'ACTIVE'),
(6, 'Arthur', 'Pendleton', 'arthur.p@company.com', 6, 1, 'Chief People Officer', '2018-04-12', 'ACTIVE'),

-- Engineering Directors and Managers (Reporting to Marcus #2)
(7, 'David', 'Zhao', 'david.z@company.com', 2, 2, 'Director of Cloud Infra', '2019-04-15', 'ACTIVE'),
(8, 'Elena', 'Rostova', 'elena.r@company.com', 2, 2, 'Director of Core Platform', '2019-07-01', 'ACTIVE'),
(9, 'Tariq', 'Al-Mansoor', 'tariq.m@company.com', 2, 2, 'Security Engineering Lead', '2020-01-15', 'ACTIVE'),

-- Product & Design Leads (Reporting to Nadia #3)
(10, 'Chloe', 'Dupont', 'chloe.d@company.com', 3, 3, 'Lead Product Designer', '2019-08-20', 'ACTIVE'),
(11, 'Liam', 'OConnor', 'liam.oc@company.com', 3, 3, 'Principal Product Manager', '2020-02-10', 'ACTIVE'),

-- Marketing & Sales Leads (Reporting to #4 and #5)
(12, 'Hannah', 'Abbott', 'hannah.a@company.com', 4, 4, 'Performance Marketing Lead', '2020-05-01', 'ACTIVE'),
(13, 'Siddharth', 'Nair', 'sid.nair@company.com', 5, 5, 'Enterprise Sales Director', '2019-11-15', 'ACTIVE'),
(14, 'Isabella', 'Torres', 'isabella.t@company.com', 5, 5, 'Regional Sales Director - EMEA', '2020-03-01', 'ACTIVE'),

-- Engineering ICs (Reporting to David #7)
(15, 'Kenji', 'Sato', 'kenji.s@company.com', 2, 7, 'Senior DevOps Architect', '2020-06-01', 'ACTIVE'),
(16, 'Devon', 'Miles', 'devon.m@company.com', 2, 7, 'Site Reliability Engineer', '2021-01-15', 'ACTIVE'),
(17, 'Amina', 'Yusuf', 'amina.y@company.com', 2, 7, 'Cloud Infrastructure Engineer', '2021-04-10', 'ACTIVE'),
(18, 'Lucas', 'Silva', 'lucas.s@company.com', 2, 7, 'Kubernetes Systems Admin', '2021-09-01', 'ACTIVE'),
(19, 'Zoe', 'Kappas', 'zoe.k@company.com', 2, 7, 'Junior Cloud Engineer', '2022-02-15', 'ACTIVE'),

-- Engineering ICs (Reporting to Elena #8)
(20, 'Nathan', 'Drake', 'nathan.d@company.com', 2, 8, 'Principal Backend Engineer', '2019-09-01', 'ACTIVE'),
(21, 'Priya', 'Sharma', 'priya.s@company.com', 2, 8, 'Senior Database Architect', '2020-03-15', 'ACTIVE'),
(22, 'Gabriel', 'Mendoza', 'gabriel.m@company.com', 2, 8, 'Staff Software Engineer', '2020-08-01', 'ACTIVE'),
(23, 'Emily', 'Watson', 'emily.w@company.com', 2, 8, 'Backend Engineer', '2021-03-01', 'ACTIVE'),
(24, 'Kaito', 'Takahashi', 'kaito.t@company.com', 2, 8, 'Full Stack Developer', '2021-06-15', 'ACTIVE'),
(25, 'Leila', 'Benali', 'leila.b@company.com', 2, 8, 'Frontend Engineer', '2021-11-01', 'ACTIVE'),
(26, 'Oliver', 'Schmidt', 'oliver.s@company.com', 2, 8, 'Junior Backend Engineer', '2022-03-01', 'ACTIVE'),
(27, 'Maya', 'Lin', 'maya.l@company.com', 2, 8, 'Software Engineering Intern', '2022-06-01', 'ACTIVE'),

-- Security Team (Reporting to Tariq #9)
(28, 'Ethan', 'Hunt', 'ethan.h@company.com', 2, 9, 'Senior Application Security Specialist', '2020-07-15', 'ACTIVE'),
(29, 'Sara', 'Lindqvist', 'sara.l@company.com', 2, 9, 'Penetration Tester', '2021-02-20', 'ACTIVE'),
(30, 'Chen', 'Wei', 'chen.w@company.com', 2, 9, 'Security Operations Analyst', '2021-08-15', 'ACTIVE'),

-- Product & UX Team (Reporting to Chloe #10 and Liam #11)
(31, 'Rachel', 'Green', 'rachel.g@company.com', 3, 10, 'Senior UX Researcher', '2020-09-01', 'ACTIVE'),
(32, 'Carlos', 'Santana', 'carlos.s@company.com', 3, 10, 'Visual UI Designer', '2021-01-10', 'ACTIVE'),
(33, 'Fiona', 'Gallagher', 'fiona.g@company.com', 3, 10, 'Design Systems Specialist', '2021-07-01', 'ACTIVE'),
(34, 'Omar', 'Farooq', 'omar.f@company.com', 3, 11, 'Senior Technical Product Manager', '2020-10-15', 'ACTIVE'),
(35, 'Ananya', 'Deshmukh', 'ananya.d@company.com', 3, 11, 'Associate Product Manager', '2021-05-01', 'ACTIVE'),

-- Marketing Team (Reporting to Hannah #12)
(36, 'Benjamin', 'Franklin', 'ben.f@company.com', 4, 12, 'SEO & Content Strategist', '2020-08-15', 'ACTIVE'),
(37, 'Lucia', 'Moretti', 'lucia.m@company.com', 4, 12, 'Brand Communications Manager', '2021-03-10', 'ACTIVE'),
(38, 'Daniel', 'Craig', 'daniel.c@company.com', 4, 12, 'Growth Marketing Specialist', '2021-09-15', 'ACTIVE'),
(39, 'Sora', 'Kim', 'sora.k@company.com', 4, 12, 'Social Media Coordinator', '2022-01-20', 'ACTIVE'),
(40, 'Hugo', 'Weaving', 'hugo.w@company.com', 4, 12, 'Event Marketing Producer', '2022-04-01', 'ON_LEAVE'),

-- Sales Team (Reporting to Siddharth #13 and Isabella #14)
(41, 'George', 'Clark', 'george.c@company.com', 5, 13, 'Senior Enterprise Account Exec', '2020-04-01', 'ACTIVE'),
(42, 'Serena', 'VanDerWoodsen', 'serena.v@company.com', 5, 13, 'Key Account Manager', '2020-11-01', 'ACTIVE'),
(43, 'Tobias', 'Fünke', 'tobias.f@company.com', 5, 13, 'Sales Development Rep', '2021-06-01', 'ACTIVE'),
(44, 'Natasha', 'Romanoff', 'natasha.r@company.com', 5, 14, 'EMEA Strategic Accounts Lead', '2020-12-01', 'ACTIVE'),
(45, 'Jean-Luc', 'Picard', 'jean.luc@company.com', 5, 14, 'Account Executive - France', '2021-04-15', 'ACTIVE'),
(46, 'Astrid', 'Hofferson', 'astrid.h@company.com', 5, 14, 'Account Executive - Nordics', '2021-10-01', 'ACTIVE'),

-- HR Team (Reporting to Arthur #6)
(47, 'Pam', 'Beesly', 'pam.b@company.com', 6, 6, 'HR Business Partner', '2019-05-20', 'ACTIVE'),
(48, 'Toby', 'Flenderson', 'toby.f@company.com', 6, 6, 'Employee Relations Manager', '2019-09-15', 'ACTIVE'),
(49, 'Kelly', 'Kapoor', 'kelly.k@company.com', 6, 6, 'Talent Acquisition Recruiter', '2021-02-01', 'ACTIVE'),
(50, 'Stanley', 'Hudson', 'stanley.h@company.com', 6, 6, 'Payroll & Benefits Administrator', '2020-01-10', 'ACTIVE'),

-- Legal & Compliance Team (Reporting to Evelyn #1)
(51, 'Atticus', 'Finch', 'atticus.f@company.com', 7, 1, 'General Counsel', '2018-09-01', 'ACTIVE'),
(52, 'Elle', 'Woods', 'elle.w@company.com', 7, 51, 'Senior Corporate Attorney', '2020-06-15', 'ACTIVE'),
(53, 'Harvey', 'Specter', 'harvey.s@company.com', 7, 51, 'Litigation & Compliance Counsel', '2021-01-05', 'ACTIVE'),

-- EDGE CASES: Floating Employees WITHOUT Departments (department_id IS NULL)
(54, 'Jax', 'Teller', 'jax.teller@company.com', NULL, 1, 'Strategic Special Advisor', '2021-08-01', 'ACTIVE'),
(55, 'Dominic', 'Toretto', 'dom.t@company.com', NULL, 1, 'Chief Security Architect Consultant', '2022-01-15', 'ACTIVE'),
(56, 'Walter', 'White', 'walter.w@company.com', NULL, 2, 'Research Fellow - AI Chemistry', '2022-05-10', 'ACTIVE'),

-- EDGE CASES: Independent Contractors WITHOUT Managers (manager_id IS NULL)
(57, 'Lisbeth', 'Salander', 'lisbeth.s@contractor.com', 2, NULL, 'External Cryptography Auditor', '2022-03-01', 'ACTIVE'),
(58, 'Sherlock', 'Holmes', 'sherlock.h@contractor.com', 7, NULL, 'External Forensic Investigator', '2022-04-15', 'ACTIVE'),

-- EDGE CASES: Terminated Employees
(59, 'Gordon', 'Gekko', 'gordon.g@company.com', 5, 5, 'Former Senior Trader', '2019-01-15', 'TERMINATED'),
(60, 'Gavin', 'Belson', 'gavin.b@company.com', 2, 2, 'Former Systems Lead', '2019-03-01', 'TERMINATED');

-- 3. MANAGERS TABLE
INSERT INTO managers (id, employee_id, department_id, management_level) VALUES
(1, 1, 1, 'EXECUTIVE'),
(2, 2, 2, 'EXECUTIVE'),
(3, 3, 3, 'EXECUTIVE'),
(4, 4, 4, 'EXECUTIVE'),
(5, 5, 5, 'EXECUTIVE'),
(6, 6, 6, 'EXECUTIVE'),
(7, 7, 2, 'DIRECTOR'),
(8, 8, 2, 'DIRECTOR'),
(9, 13, 5, 'DIRECTOR'),
(10, 14, 5, 'DIRECTOR'),
(11, 9, 2, 'TEAM_LEAD'),
(12, 10, 3, 'TEAM_LEAD'),
(13, 11, 3, 'TEAM_LEAD'),
(14, 12, 4, 'TEAM_LEAD');

-- 4. SALARIES TABLE
INSERT INTO salaries (id, employee_id, base_salary, bonus, effective_date) VALUES
(1, 1, 285000.00, 75000.00, '2023-01-01'),
(2, 2, 220000.00, 45000.00, '2023-01-01'),
(3, 3, 195000.00, 35000.00, '2023-01-01'),
(4, 4, 185000.00, 30000.00, '2023-01-01'),
(5, 5, 205000.00, 50000.00, '2023-01-01'),
(6, 6, 175000.00, 25000.00, '2023-01-01'),
(7, 7, 185000.00, 25000.00, '2023-01-01'),
(8, 8, 190000.00, 28000.00, '2023-01-01'),
(9, 9, 160000.00, 20000.00, '2023-01-01'),
(10, 10, 155000.00, 18000.00, '2023-01-01'),
(11, 11, 170000.00, 22000.00, '2023-01-01'),
(12, 12, 145000.00, 15000.00, '2023-01-01'),
(13, 13, 175000.00, 40000.00, '2023-01-01'),
(14, 14, 168000.00, 38000.00, '2023-01-01'),
(15, 15, 155000.00, 15000.00, '2023-01-01'),
(16, 16, 135000.00, 12000.00, '2023-01-01'),
(17, 17, 128000.00, 10000.00, '2023-01-01'),
(18, 18, 122000.00, 8000.00, '2023-01-01'),
(19, 19, 85000.00, 5000.00, '2023-01-01'),
(20, 20, 180000.00, 24000.00, '2023-01-01'),
(21, 21, 175000.00, 22000.00, '2023-01-01'),
(22, 22, 165000.00, 18000.00, '2023-01-01'),
(23, 23, 135000.00, 12000.00, '2023-01-01'),
(24, 24, 130000.00, 10000.00, '2023-01-01'),
(25, 25, 125000.00, 10000.00, '2023-01-01'),
(26, 26, 95000.00, 6000.00, '2023-01-01'),
(27, 27, 52000.00, 0.00, '2023-01-01'),
(28, 28, 150000.00, 18000.00, '2023-01-01'),
(29, 29, 132000.00, 12000.00, '2023-01-01'),
(30, 30, 110000.00, 8000.00, '2023-01-01'),
(31, 31, 140000.00, 14000.00, '2023-01-01'),
(32, 32, 120000.00, 10000.00, '2023-01-01'),
(33, 33, 125000.00, 10000.00, '2023-01-01'),
(34, 34, 155000.00, 18000.00, '2023-01-01'),
(35, 35, 105000.00, 8000.00, '2023-01-01'),
(36, 36, 115000.00, 10000.00, '2023-01-01'),
(37, 37, 120000.00, 12000.00, '2023-01-01'),
(38, 38, 110000.00, 10000.00, '2023-01-01'),
(39, 39, 78000.00, 4000.00, '2023-01-01'),
(40, 40, 92000.00, 5000.00, '2023-01-01'),
(41, 41, 140000.00, 55000.00, '2023-01-01'),
(42, 42, 125000.00, 45000.00, '2023-01-01'),
(43, 43, 75000.00, 15000.00, '2023-01-01'),
(44, 44, 145000.00, 50000.00, '2023-01-01'),
(45, 45, 115000.00, 35000.00, '2023-01-01'),
(46, 46, 110000.00, 30000.00, '2023-01-01'),
(47, 47, 115000.00, 10000.00, '2023-01-01'),
(48, 48, 110000.00, 8000.00, '2023-01-01'),
(49, 49, 95000.00, 12000.00, '2023-01-01'),
(50, 50, 98000.00, 7000.00, '2023-01-01'),
(51, 51, 230000.00, 40000.00, '2023-01-01'),
(52, 52, 175000.00, 25000.00, '2023-01-01'),
(53, 53, 165000.00, 22000.00, '2023-01-01'),
(54, 54, 160000.00, 20000.00, '2023-01-01'),
(55, 55, 190000.00, 30000.00, '2023-01-01'),
(56, 56, 170000.00, 15000.00, '2023-01-01'),
(57, 57, 150000.00, 0.00, '2023-01-01'),
(58, 58, 140000.00, 0.00, '2023-01-01'),
(59, 59, 180000.00, 0.00, '2022-01-01'),
(60, 60, 170000.00, 0.00, '2022-01-01');

-- 5. PROJECTS
INSERT INTO projects (id, name, department_id, start_date, end_date, budget) VALUES
(101, 'NextGen Cloud Migration', 2, '2022-01-10', '2023-03-31', 750000.00),
(102, 'Zero Trust Architecture Implementation', 2, '2022-06-01', NULL, 480000.00),
(103, 'Mobile App Redesign 3.0', 3, '2022-09-15', '2023-05-30', 320000.00),
(104, 'Global Brand Refresh Campaign', 4, '2023-01-05', '2023-06-30', 550000.00),
(105, 'Enterprise CRM AI Integration', 5, '2022-11-01', NULL, 620000.00),
(106, 'Automated Payroll & Benefits Modernization', 6, '2023-02-01', '2023-08-31', 190000.00),
(107, 'SOC2 Type II Annual Audit', 7, '2023-03-01', '2023-09-30', 150000.00),
(108, 'Autonomous Microservices Mesh (R&D)', 2, '2023-04-01', NULL, 900000.00);

-- 6. EMPLOYEE_PROJECTS (Cross-functional assignments, some employees on multiple projects)
INSERT INTO employee_projects (employee_id, project_id, role, hours_allocated, assigned_date) VALUES
(7, 101, 'Technical Director', 15, '2022-01-10'),
(15, 101, 'Lead Architect', 35, '2022-01-10'),
(16, 101, 'DevOps Specialist', 30, '2022-01-15'),
(17, 101, 'Infrastructure Engineer', 40, '2022-02-01'),
(9, 102, 'Security Lead', 25, '2022-06-01'),
(28, 102, 'AppSec Specialist', 35, '2022-06-01'),
(29, 102, 'Penetration Tester', 30, '2022-06-15'),
(57, 102, 'External Cryptographer', 20, '2022-07-01'),
(10, 103, 'Design Director', 20, '2022-09-15'),
(31, 103, 'UX Researcher', 35, '2022-09-15'),
(32, 103, 'UI Designer', 40, '2022-10-01'),
(25, 103, 'Frontend Engineer', 30, '2022-10-15'),
(12, 104, 'Campaign Director', 25, '2023-01-05'),
(36, 104, 'Content Specialist', 35, '2023-01-05'),
(37, 104, 'Brand Communications', 30, '2023-01-10'),
(13, 105, 'Executive Sponsor', 10, '2022-11-01'),
(41, 105, 'Lead Account Exec', 25, '2022-11-01'),
(21, 105, 'Data Architect', 20, '2022-11-15'),
(50, 106, 'System Administrator', 35, '2023-02-01'),
(47, 106, 'HR Business Partner', 20, '2023-02-01'),
(51, 107, 'Legal Oversight', 15, '2023-03-01'),
(53, 107, 'Compliance Counsel', 35, '2023-03-01'),
(8, 108, 'R&D Lead', 20, '2023-04-01'),
(20, 108, 'Principal Backend Engineer', 35, '2023-04-01'),
(22, 108, 'Staff Systems Engineer', 35, '2023-04-01'),
-- Employees assigned to multiple projects (e.g. employee 15, 21, 28)
(15, 108, 'Cloud Advisory', 10, '2023-04-01'),
(21, 101, 'Database Migration Lead', 20, '2022-02-01'),
(28, 101, 'Security Reviewer', 10, '2022-03-01');
"""
    return ddl, dml

# Quick self-test in SQLite
if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    c_ddl, c_dml = generate_company_sql()
    conn.executescript(c_ddl)
    conn.executescript(c_dml)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM employees;")
    print("Company Employees Count:", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM departments;")
    print("Departments Count:", cur.fetchone()[0])
    conn.close()

