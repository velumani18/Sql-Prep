from app.data.seed_databases import ColumnInfo, TableInfo, SyntheticDatabaseBlueprint
from app.data.generate_datasets import generate_company_sql

COMPANY_DDL, COMPANY_DML = generate_company_sql()

COMPANY_DATABASE = SyntheticDatabaseBlueprint(
    id="db-company",
    name="company_db",
    display_name="Enterprise Corporate & Staff Database",
    description="Corporate workforce structure containing 60 employees, reporting hierarchies, departments, cross-functional projects, and payroll records.",
    init_ddl=COMPANY_DDL,
    seed_dml=COMPANY_DML,
    tables=[
        TableInfo(
            name="departments",
            description="Company business divisions and annual operational budgets",
            row_count=7,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="name", type="VARCHAR(80)", nullable=False),
                ColumnInfo(name="budget", type="DECIMAL(12,2)", nullable=False),
                ColumnInfo(name="location", type="VARCHAR(100)", nullable=False),
            ],
        ),
        TableInfo(
            name="employees",
            description="Personnel directory including executives, leads, ICs, contractors, and reporting lines",
            row_count=60,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="first_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="last_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="email", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="department_id", type="INTEGER", is_foreign_key=True, references="departments.id", nullable=True),
                ColumnInfo(name="manager_id", type="INTEGER", is_foreign_key=True, references="employees.id", nullable=True),
                ColumnInfo(name="title", type="VARCHAR(100)", nullable=False),
                ColumnInfo(name="hire_date", type="DATE", nullable=False),
                ColumnInfo(name="status", type="VARCHAR(20)", nullable=False),
            ],
        ),
        TableInfo(
            name="managers",
            description="Official management appointments and management tier assignments",
            row_count=14,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="employee_id", type="INTEGER", is_foreign_key=True, references="employees.id", nullable=False),
                ColumnInfo(name="department_id", type="INTEGER", is_foreign_key=True, references="departments.id", nullable=True),
                ColumnInfo(name="management_level", type="VARCHAR(30)", nullable=False),
            ],
        ),
        TableInfo(
            name="salaries",
            description="Employee annual compensation, performance bonuses, and effective dates",
            row_count=60,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="employee_id", type="INTEGER", is_foreign_key=True, references="employees.id", nullable=False),
                ColumnInfo(name="base_salary", type="DECIMAL(10,2)", nullable=False),
                ColumnInfo(name="bonus", type="DECIMAL(10,2)", nullable=True),
                ColumnInfo(name="effective_date", type="DATE", nullable=False),
            ],
        ),
        TableInfo(
            name="projects",
            description="Strategic business initiatives, project schedules, and budgets",
            row_count=8,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="name", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="department_id", type="INTEGER", is_foreign_key=True, references="departments.id", nullable=True),
                ColumnInfo(name="start_date", type="DATE", nullable=False),
                ColumnInfo(name="end_date", type="DATE", nullable=True),
                ColumnInfo(name="budget", type="DECIMAL(12,2)", nullable=True),
            ],
        ),
        TableInfo(
            name="employee_projects",
            description="Cross-functional project staff allocations and roles",
            row_count=28,
            columns=[
                ColumnInfo(name="employee_id", type="INTEGER", is_primary_key=True, is_foreign_key=True, references="employees.id", nullable=False),
                ColumnInfo(name="project_id", type="INTEGER", is_primary_key=True, is_foreign_key=True, references="projects.id", nullable=False),
                ColumnInfo(name="role", type="VARCHAR(60)", nullable=False),
                ColumnInfo(name="hours_allocated", type="INTEGER", nullable=False),
                ColumnInfo(name="assigned_date", type="DATE", nullable=False),
            ],
        ),
    ],
)

