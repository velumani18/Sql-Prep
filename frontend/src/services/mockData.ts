import {
  SyntheticDatabase,
  CurriculumModule,
  TopicLesson,
  QuestionDetail,
  UserProfile,
  RecentAttempt
} from '../types';

// ==========================================
// 1. SYNTHETIC RELATIONAL DATABASES
// ==========================================

export const mockDatabases: SyntheticDatabase[] = [
  {
    id: 'db-company',
    name: 'company_db',
    displayName: 'Corporate Workforce & Staff Database',
    description: 'Corporate organizational model containing 60 employees, reporting hierarchies, departments, cross-functional projects, and payroll records.',
    tables: [
      {
        name: 'departments',
        description: 'Company business divisions and annual operational budgets',
        rowCount: 7,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Department code' },
          { name: 'name', type: 'VARCHAR(80)', nullable: false, description: 'Department title' },
          { name: 'budget', type: 'DECIMAL(12,2)', nullable: false, description: 'Annual department budget in USD' },
          { name: 'location', type: 'VARCHAR(100)', nullable: false, description: 'Office campus' },
        ],
        sampleData: [
          { id: 1, name: 'Executive Board', budget: 1500000.00, location: 'San Francisco, CA' },
          { id: 2, name: 'Engineering', budget: 4200000.00, location: 'San Francisco, CA' },
          { id: 3, name: 'Product & Design', budget: 1800000.00, location: 'New York, NY' },
          { id: 4, name: 'Marketing & Growth', budget: 2100000.00, location: 'London, UK' },
          { id: 5, name: 'Sales & Accounts', budget: 3500000.00, location: 'Austin, TX' },
        ]
      },
      {
        name: 'employees',
        description: 'Corporate staff personnel directory and reporting lines',
        rowCount: 60,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Badge number' },
          { name: 'first_name', type: 'VARCHAR(50)', nullable: false, description: 'First name' },
          { name: 'last_name', type: 'VARCHAR(50)', nullable: false, description: 'Last name' },
          { name: 'email', type: 'VARCHAR(120)', nullable: false, description: 'Corporate email' },
          { name: 'department_id', type: 'INTEGER', isForeignKey: true, references: 'departments.id', nullable: true, description: 'Department code' },
          { name: 'manager_id', type: 'INTEGER', isForeignKey: true, references: 'employees.id', nullable: true, description: 'Direct manager badge' },
          { name: 'title', type: 'VARCHAR(100)', nullable: false, description: 'Job title' },
          { name: 'hire_date', type: 'DATE', nullable: false, description: 'Date joined' },
          { name: 'status', type: 'VARCHAR(20)', nullable: false, description: 'Employment status' },
        ],
        sampleData: [
          { id: 1, first_name: 'Evelyn', last_name: 'Vance', email: 'evelyn.vance@company.com', department_id: 1, manager_id: null, title: 'Chief Executive Officer', hire_date: '2018-01-15', status: 'ACTIVE' },
          { id: 2, first_name: 'Marcus', last_name: 'Sterling', email: 'marcus.s@company.com', department_id: 2, manager_id: 1, title: 'VP of Engineering', hire_date: '2018-03-01', status: 'ACTIVE' },
          { id: 3, first_name: 'Nadia', last_name: 'Kowalski', email: 'nadia.k@company.com', department_id: 3, manager_id: 1, title: 'VP of Product', hire_date: '2018-06-15', status: 'ACTIVE' },
          { id: 7, first_name: 'David', last_name: 'Zhao', email: 'david.z@company.com', department_id: 2, manager_id: 2, title: 'Director of Cloud Infra', hire_date: '2019-04-15', status: 'ACTIVE' },
          { id: 54, first_name: 'Jax', last_name: 'Teller', email: 'jax.teller@company.com', department_id: null, manager_id: 1, title: 'Strategic Special Advisor', hire_date: '2021-08-01', status: 'ACTIVE' },
        ]
      },
      {
        name: 'salaries',
        description: 'Employee annual compensation and performance bonuses',
        rowCount: 60,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Record ID' },
          { name: 'employee_id', type: 'INTEGER', isForeignKey: true, references: 'employees.id', nullable: false, description: 'Employee badge' },
          { name: 'base_salary', type: 'DECIMAL(10,2)', nullable: false, description: 'Annual base compensation USD' },
          { name: 'bonus', type: 'DECIMAL(10,2)', nullable: true, description: 'Annual bonus target USD' },
          { name: 'effective_date', type: 'DATE', nullable: false, description: 'Date effective' },
        ],
        sampleData: [
          { id: 1, employee_id: 1, base_salary: 285000.00, bonus: 75000.00, effective_date: '2023-01-01' },
          { id: 2, employee_id: 2, base_salary: 220000.00, bonus: 45000.00, effective_date: '2023-01-01' },
          { id: 3, employee_id: 3, base_salary: 195000.00, bonus: 35000.00, effective_date: '2023-01-01' },
        ]
      },
      {
        name: 'projects',
        description: 'Corporate strategic projects and budgets',
        rowCount: 8,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Project ID' },
          { name: 'name', type: 'VARCHAR(120)', nullable: false, description: 'Project name' },
          { name: 'department_id', type: 'INTEGER', isForeignKey: true, references: 'departments.id', nullable: true, description: 'Funding department' },
          { name: 'start_date', type: 'DATE', nullable: false, description: 'Start date' },
          { name: 'end_date', type: 'DATE', nullable: true, description: 'End date' },
          { name: 'budget', type: 'DECIMAL(12,2)', nullable: true, description: 'Approved budget USD' },
        ],
        sampleData: [
          { id: 101, name: 'NextGen Cloud Migration', department_id: 2, start_date: '2022-01-10', end_date: '2023-03-31', budget: 750000.00 },
          { id: 102, name: 'Zero Trust Architecture Implementation', department_id: 2, start_date: '2022-06-01', end_date: null, budget: 480000.00 },
        ]
      },
      {
        name: 'employee_projects',
        description: 'Cross-functional project staff allocations and roles',
        rowCount: 28,
        columns: [
          { name: 'employee_id', type: 'INTEGER', isPrimaryKey: true, isForeignKey: true, references: 'employees.id', nullable: false, description: 'Employee' },
          { name: 'project_id', type: 'INTEGER', isPrimaryKey: true, isForeignKey: true, references: 'projects.id', nullable: false, description: 'Project' },
          { name: 'role', type: 'VARCHAR(60)', nullable: false, description: 'Assigned role' },
          { name: 'hours_allocated', type: 'INTEGER', nullable: false, description: 'Weekly hours' },
          { name: 'assigned_date', type: 'DATE', nullable: false, description: 'Date assigned' },
        ],
        sampleData: [
          { employee_id: 15, project_id: 101, role: 'Lead Architect', hours_allocated: 35, assigned_date: '2022-01-10' },
          { employee_id: 16, project_id: 101, role: 'DevOps Specialist', hours_allocated: 30, assigned_date: '2022-01-15' },
        ]
      }
    ]
  },
  {
    id: 'db-ecommerce',
    name: 'ecommerce_db',
    displayName: 'Global E-Commerce Database',
    description: 'Relational schema modeling an international online marketplace with customers, categories, orders, line items, and payment gateways.',
    tables: [
      {
        name: 'customers',
        description: 'Registered customer profiles and registration metadata',
        rowCount: 30,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Unique customer identifier' },
          { name: 'first_name', type: 'VARCHAR(50)', nullable: false, description: 'First name' },
          { name: 'last_name', type: 'VARCHAR(50)', nullable: false, description: 'Last name' },
          { name: 'email', type: 'VARCHAR(150)', nullable: false, description: 'Customer primary contact email' },
          { name: 'country', type: 'VARCHAR(50)', nullable: false, description: 'ISO or country name of registration' },
          { name: 'city', type: 'VARCHAR(60)', nullable: false, description: 'City' },
          { name: 'created_at', type: 'DATE', nullable: false, description: 'Account creation date' }
        ],
        sampleData: [
          { id: 101, first_name: 'Sophia', last_name: 'Chen', email: 'sophia.c@example.com', country: 'United States', city: 'San Francisco', created_at: '2022-01-15' },
          { id: 102, first_name: 'Liam', last_name: 'Davies', email: 'liam.d@example.co.uk', country: 'United Kingdom', city: 'London', created_at: '2022-02-01' },
          { id: 201, first_name: 'Brandon', last_name: 'Stark', email: 'brandon.s@example.com', country: 'United States', city: 'Chicago', created_at: '2023-03-01' },
        ]
      },
      {
        name: 'categories',
        description: 'Product merchandising categories',
        rowCount: 6,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Category ID' },
          { name: 'name', type: 'VARCHAR(60)', nullable: false, description: 'Category title' },
          { name: 'description', type: 'TEXT', nullable: true, description: 'Description' },
        ],
        sampleData: [
          { id: 1, name: 'Consumer Electronics', description: 'Smartphones, laptops, and computer peripherals' },
          { id: 2, name: 'Home & Living', description: 'Furniture, decor, and cookware' },
        ]
      },
      {
        name: 'products',
        description: 'Catalogue of items available in the marketplace',
        rowCount: 20,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Unique SKU identifier' },
          { name: 'category_id', type: 'INTEGER', isForeignKey: true, references: 'categories.id', nullable: false, description: 'Category code' },
          { name: 'name', type: 'VARCHAR(150)', nullable: false, description: 'Product marketing title' },
          { name: 'price', type: 'DECIMAL(8,2)', nullable: false, description: 'Unit retail price in USD' },
          { name: 'stock_quantity', type: 'INTEGER', nullable: false, description: 'Current warehouse inventory units' }
        ],
        sampleData: [
          { id: 501, category_id: 1, name: 'Pro Wireless Mechanical Keyboard', price: 149.99, stock_quantity: 85 },
          { id: 502, category_id: 1, name: 'Ergonomic Precision Mouse', price: 79.50, stock_quantity: 120 },
        ]
      },
      {
        name: 'orders',
        description: 'Customer transactions, dates, and order fulfillment status',
        rowCount: 35,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Unique order identifier' },
          { name: 'customer_id', type: 'INTEGER', isForeignKey: true, references: 'customers.id', nullable: false, description: 'Buyer ID' },
          { name: 'order_date', type: 'DATE', nullable: false, description: 'Date transaction was placed' },
          { name: 'total_amount', type: 'DECIMAL(10,2)', nullable: false, description: 'Total charge in USD' },
          { name: 'status', type: 'VARCHAR(20)', nullable: false, description: 'Status: COMPLETED, SHIPPED, PENDING, CANCELLED' }
        ],
        sampleData: [
          { id: 1001, customer_id: 101, order_date: '2023-01-10', total_amount: 648.99, status: 'COMPLETED' },
          { id: 1028, customer_id: 122, order_date: '2023-04-29', total_amount: 499.00, status: 'CANCELLED' },
        ]
      },
      {
        name: 'order_items',
        description: 'Purchased product line items and quantity breakdown',
        rowCount: 45,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Item ID' },
          { name: 'order_id', type: 'INTEGER', isForeignKey: true, references: 'orders.id', nullable: false, description: 'Order ID' },
          { name: 'product_id', type: 'INTEGER', isForeignKey: true, references: 'products.id', nullable: false, description: 'Product SKU' },
          { name: 'quantity', type: 'INTEGER', nullable: false, description: 'Quantity' },
          { name: 'unit_price', type: 'DECIMAL(10,2)', nullable: false, description: 'Unit charge' },
        ],
        sampleData: [
          { id: 1, order_id: 1001, product_id: 503, quantity: 1, unit_price: 499.00 },
          { id: 2, order_id: 1001, product_id: 501, quantity: 1, unit_price: 149.99 },
        ]
      },
      {
        name: 'payments',
        description: 'Payment gateway transactions, methods, and clearance states',
        rowCount: 32,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Payment ID' },
          { name: 'order_id', type: 'INTEGER', isForeignKey: true, references: 'orders.id', nullable: false, description: 'Order ID' },
          { name: 'payment_method', type: 'VARCHAR(30)', nullable: false, description: 'Payment gateway' },
          { name: 'amount', type: 'DECIMAL(10,2)', nullable: false, description: 'Amount in USD' },
          { name: 'payment_status', type: 'VARCHAR(20)', nullable: false, description: 'Status' },
          { name: 'payment_date', type: 'DATE', nullable: true, description: 'Date cleared' },
        ],
        sampleData: [
          { id: 1, order_id: 1001, payment_method: 'CREDIT_CARD', amount: 648.99, payment_status: 'SUCCESSFUL', payment_date: '2023-01-10' },
          { id: 26, order_id: 1026, payment_method: 'CREDIT_CARD', amount: 135.00, payment_status: 'FAILED', payment_date: '2023-04-25' },
        ]
      }
    ]
  },
  {
    id: 'db-university',
    name: 'university_db',
    displayName: 'Academic Registrar & Course Database',
    description: 'Higher education academic schema modeling university departments, professors, course curriculums, student rosters, and letter grade evaluations.',
    tables: [
      {
        name: 'departments',
        description: 'Academic faculties and buildings',
        rowCount: 6,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Dept code' },
          { name: 'name', type: 'VARCHAR(80)', nullable: false, description: 'Faculty name' },
          { name: 'code', type: 'VARCHAR(10)', nullable: false, description: 'Abbreviation' },
          { name: 'building', type: 'VARCHAR(80)', nullable: false, description: 'Building' },
        ],
        sampleData: [
          { id: 1, name: 'Computer Science & Engineering', code: 'CS', building: 'Turing Hall' },
          { id: 2, name: 'Mathematics & Statistics', code: 'MATH', building: 'Euler Science Pavilion' },
        ]
      },
      {
        name: 'professors',
        description: 'Faculty professors and appointments',
        rowCount: 8,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Faculty ID' },
          { name: 'first_name', type: 'VARCHAR(50)', nullable: false, description: 'First name' },
          { name: 'last_name', type: 'VARCHAR(50)', nullable: false, description: 'Last name' },
          { name: 'email', type: 'VARCHAR(120)', nullable: false, description: 'University email' },
          { name: 'department_id', type: 'INTEGER', isForeignKey: true, references: 'departments.id', nullable: false, description: 'Faculty department' },
          { name: 'title', type: 'VARCHAR(60)', nullable: false, description: 'Academic rank' },
          { name: 'hired_year', type: 'INTEGER', nullable: false, description: 'Year appointed' },
        ],
        sampleData: [
          { id: 1, first_name: 'Ada', last_name: 'Lovelace', email: 'ada.lovelace@university.edu', department_id: 1, title: 'Full Professor', hired_year: 2012 },
          { id: 8, first_name: 'Noam', last_name: 'Chomsky', email: 'noam.chomsky@university.edu', department_id: 5, title: 'Full Professor', hired_year: 2005 },
        ]
      },
      {
        name: 'courses',
        description: 'Course catalog, credits, and assigned instructors',
        rowCount: 12,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Course code ID' },
          { name: 'code', type: 'VARCHAR(15)', nullable: false, description: 'Catalog code' },
          { name: 'title', type: 'VARCHAR(120)', nullable: false, description: 'Course title' },
          { name: 'department_id', type: 'INTEGER', isForeignKey: true, references: 'departments.id', nullable: false, description: 'Department' },
          { name: 'professor_id', type: 'INTEGER', isForeignKey: true, references: 'professors.id', nullable: true, description: 'Instructor' },
          { name: 'credits', type: 'INTEGER', nullable: false, description: 'Academic credits' },
        ],
        sampleData: [
          { id: 101, code: 'CS-101', title: 'Introduction to Computer Science & Algorithms', department_id: 1, professor_id: 1, credits: 4 },
          { id: 103, code: 'CS-305', title: 'Relational Database Design & SQL Internals', department_id: 1, professor_id: 2, credits: 4 },
        ]
      },
      {
        name: 'students',
        description: 'Undergraduate and graduate student roster',
        rowCount: 30,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Student ID' },
          { name: 'first_name', type: 'VARCHAR(50)', nullable: false, description: 'First name' },
          { name: 'last_name', type: 'VARCHAR(50)', nullable: false, description: 'Last name' },
          { name: 'email', type: 'VARCHAR(120)', nullable: false, description: 'Student email' },
          { name: 'major_department_id', type: 'INTEGER', isForeignKey: true, references: 'departments.id', nullable: true, description: 'Major' },
          { name: 'enrollment_year', type: 'INTEGER', nullable: false, description: 'Admit year' },
          { name: 'status', type: 'VARCHAR(20)', nullable: false, description: 'Enrollment status' },
        ],
        sampleData: [
          { id: 1001, first_name: 'Alice', last_name: 'Smith', email: 'alice.smith@university.edu', major_department_id: 1, enrollment_year: 2021, status: 'ACTIVE' },
          { id: 2001, first_name: 'Zack', last_name: 'Morris', email: 'zack.m@university.edu', major_department_id: 1, enrollment_year: 2023, status: 'ACTIVE' },
        ]
      },
      {
        name: 'enrollments',
        description: 'Course registrations, terms, and letter grades',
        rowCount: 52,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Enrollment ID' },
          { name: 'student_id', type: 'INTEGER', isForeignKey: true, references: 'students.id', nullable: false, description: 'Student' },
          { name: 'course_id', type: 'INTEGER', isForeignKey: true, references: 'courses.id', nullable: false, description: 'Course' },
          { name: 'semester', type: 'VARCHAR(20)', nullable: false, description: 'Term' },
          { name: 'academic_year', type: 'INTEGER', nullable: false, description: 'Year' },
          { name: 'letter_grade', type: 'VARCHAR(2)', nullable: true, description: 'Letter grade earned' },
        ],
        sampleData: [
          { id: 1, student_id: 1001, course_id: 101, semester: 'Fall', academic_year: 2021, letter_grade: 'A' },
          { id: 48, student_id: 1002, course_id: 104, semester: 'Spring', academic_year: 2023, letter_grade: null },
        ]
      }
    ]
  },
  {
    id: 'db-banking',
    name: 'banking_db',
    displayName: 'Commercial Banking & Loan Services Database',
    description: 'Financial ledger model tracking bank branches, customer credit scores, checking/savings deposit accounts, transaction journals, and loan risk portfolios.',
    tables: [
      {
        name: 'branches',
        description: 'Bank physical branches and regional total assets',
        rowCount: 5,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Branch code ID' },
          { name: 'branch_name', type: 'VARCHAR(80)', nullable: false, description: 'Branch title' },
          { name: 'branch_code', type: 'VARCHAR(10)', nullable: false, description: 'Transit code' },
          { name: 'city', type: 'VARCHAR(60)', nullable: false, description: 'City' },
          { name: 'state', type: 'VARCHAR(30)', nullable: false, description: 'State' },
          { name: 'total_assets', type: 'DECIMAL(15,2)', nullable: false, description: 'Total branch assets USD' },
        ],
        sampleData: [
          { id: 1, branch_name: 'Downtown Financial Center', branch_code: 'BR-NYC-01', city: 'New York', state: 'NY', total_assets: 850000000.00 },
          { id: 2, branch_name: 'Silicon Valley Tech Branch', branch_code: 'BR-SFO-02', city: 'San Francisco', state: 'CA', total_assets: 620000000.00 },
        ]
      },
      {
        name: 'customers',
        description: 'Account owners with credit bureau scores and reported annual incomes',
        rowCount: 25,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Customer ID' },
          { name: 'first_name', type: 'VARCHAR(50)', nullable: false, description: 'First name' },
          { name: 'last_name', type: 'VARCHAR(50)', nullable: false, description: 'Last name' },
          { name: 'email', type: 'VARCHAR(120)', nullable: false, description: 'Contact email' },
          { name: 'credit_score', type: 'INTEGER', nullable: false, description: 'FICO credit score' },
          { name: 'annual_income', type: 'DECIMAL(12,2)', nullable: false, description: 'Annual income USD' },
          { name: 'registered_branch_id', type: 'INTEGER', isForeignKey: true, references: 'branches.id', nullable: false, description: 'Home branch' },
          { name: 'joined_date', type: 'DATE', nullable: false, description: 'Date joined' },
        ],
        sampleData: [
          { id: 101, first_name: 'Alexander', last_name: 'Hamilton', email: 'a.hamilton@financial.org', credit_score: 810, annual_income: 195000.00, registered_branch_id: 1, joined_date: '2019-01-15' },
          { id: 121, first_name: 'Gordon', last_name: 'Gekko', email: 'gordon.gekko@wallst.org', credit_score: 580, annual_income: 250000.00, registered_branch_id: 1, joined_date: '2022-07-01' },
        ]
      },
      {
        name: 'accounts',
        description: 'Checking, savings, money market, and commercial business accounts',
        rowCount: 35,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Account ID' },
          { name: 'customer_id', type: 'INTEGER', isForeignKey: true, references: 'customers.id', nullable: false, description: 'Account holder' },
          { name: 'branch_id', type: 'INTEGER', isForeignKey: true, references: 'branches.id', nullable: false, description: 'Domicile branch' },
          { name: 'account_number', type: 'VARCHAR(20)', nullable: false, description: 'Account number' },
          { name: 'account_type', type: 'VARCHAR(30)', nullable: false, description: 'Account category' },
          { name: 'balance', type: 'DECIMAL(12,2)', nullable: false, description: 'Current ledger balance USD' },
          { name: 'status', type: 'VARCHAR(20)', nullable: false, description: 'Account status' },
          { name: 'opened_date', type: 'DATE', nullable: false, description: 'Date opened' },
        ],
        sampleData: [
          { id: 1001, customer_id: 101, branch_id: 1, account_number: 'CHK-1001-901', account_type: 'CHECKING', balance: 14500.50, status: 'ACTIVE', opened_date: '2019-01-15' },
          { id: 1030, customer_id: 101, branch_id: 1, account_number: 'SAV-1030-930', account_type: 'SAVINGS', balance: 500.00, status: 'DORMANT', opened_date: '2022-11-01' },
        ]
      },
      {
        name: 'transactions',
        description: 'Account activity journal: deposits, withdrawals, fees, and transfers',
        rowCount: 40,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Txn ID' },
          { name: 'account_id', type: 'INTEGER', isForeignKey: true, references: 'accounts.id', nullable: false, description: 'Account' },
          { name: 'transaction_type', type: 'VARCHAR(20)', nullable: false, description: 'Type' },
          { name: 'amount', type: 'DECIMAL(12,2)', nullable: false, description: 'Amount USD' },
          { name: 'balance_after', type: 'DECIMAL(12,2)', nullable: false, description: 'Balance after txn' },
          { name: 'description', type: 'VARCHAR(150)', nullable: true, description: 'Narrative description' },
          { name: 'transaction_date', type: 'DATE', nullable: false, description: 'Date executed' },
        ],
        sampleData: [
          { id: 1, account_id: 1001, transaction_type: 'DEPOSIT', amount: 5000.00, balance_after: 15000.00, description: 'Payroll Direct Deposit', transaction_date: '2023-01-05' },
          { id: 2, account_id: 1001, transaction_type: 'WITHDRAWAL', amount: 850.00, balance_after: 14150.00, description: 'Mortgage Auto Debit', transaction_date: '2023-01-08' },
        ]
      },
      {
        name: 'loans',
        description: 'Credit loan portfolios: mortgages, auto, personal, and business financing',
        rowCount: 15,
        columns: [
          { name: 'id', type: 'INTEGER', isPrimaryKey: true, nullable: false, description: 'Loan contract ID' },
          { name: 'customer_id', type: 'INTEGER', isForeignKey: true, references: 'customers.id', nullable: false, description: 'Borrower' },
          { name: 'branch_id', type: 'INTEGER', isForeignKey: true, references: 'branches.id', nullable: false, description: 'Originating branch' },
          { name: 'loan_type', type: 'VARCHAR(40)', nullable: false, description: 'Credit type' },
          { name: 'principal_amount', type: 'DECIMAL(12,2)', nullable: false, description: 'Principal borrowed USD' },
          { name: 'interest_rate', type: 'DECIMAL(5,2)', nullable: false, description: 'Annual percentage rate APR' },
          { name: 'term_months', type: 'INTEGER', nullable: false, description: 'Term duration in months' },
          { name: 'status', type: 'VARCHAR(20)', nullable: false, description: 'Underwriting status' },
          { name: 'origination_date', type: 'DATE', nullable: false, description: 'Date funded' },
        ],
        sampleData: [
          { id: 501, customer_id: 101, branch_id: 1, loan_type: 'MORTGAGE', principal_amount: 540000.00, interest_rate: 5.25, term_months: 360, status: 'APPROVED', origination_date: '2020-04-15' },
          { id: 515, customer_id: 121, branch_id: 1, loan_type: 'PERSONAL_LOAN', principal_amount: 40000.00, interest_rate: 9.50, term_months: 36, status: 'DEFAULTED', origination_date: '2021-11-01' },
        ]
      }
    ]
  }
];

// ==========================================
// 2. CURRICULUM ROADMAP MODULES
// ==========================================

export const mockCurriculumModules: CurriculumModule[] = [
  {
    id: 'mod-1',
    slug: 'sql-fundamentals',
    title: 'SQL Fundamentals & Data Retrieval',
    description: 'Understand the relational model, master SELECT projections, alias columns, and filter records with WHERE.',
    level: 'beginner',
    icon: 'Database',
    isLocked: false,
    totalTopics: 4,
    completedTopics: 4,
    estimatedHours: 3,
    lessons: [
      { id: 'les-1-1', slug: 'select-and-column-projection', title: 'The Anatomy of SELECT and Column Projections', isCompleted: true, questionsCount: 5 },
      { id: 'les-1-2', slug: 'where-clause-filtering', title: 'Filtering Rows with WHERE and Logical Operators', isCompleted: true, questionsCount: 6 },
      { id: 'les-1-3', slug: 'sorting-and-limiting', title: 'Deterministic Sorting with ORDER BY & LIMIT', isCompleted: true, questionsCount: 5 },
      { id: 'les-1-4', slug: 'null-handling-and-coalesce', title: 'Three-Valued Logic and NULL Handling', isCompleted: true, questionsCount: 5 }
    ]
  },
  {
    id: 'mod-2',
    slug: 'aggregations-and-grouping',
    title: 'Aggregations & Analytical Grouping',
    description: 'Summarize large datasets with COUNT, SUM, AVG, MIN, MAX and segment records with GROUP BY and HAVING.',
    level: 'beginner',
    icon: 'BarChart3',
    isLocked: false,
    totalTopics: 3,
    completedTopics: 2,
    estimatedHours: 4,
    lessons: [
      { id: 'les-2-1', slug: 'aggregate-functions', title: 'Fundamental Aggregate Functions', isCompleted: true, questionsCount: 6 },
      { id: 'les-2-2', slug: 'group-by-foundations', title: 'Grouping Dimensions with GROUP BY', isCompleted: true, questionsCount: 6 },
      { id: 'les-2-3', slug: 'having-vs-where', title: 'Filtering Groups: The Crucial HAVING Clause', isCompleted: false, questionsCount: 7 }
    ]
  },
  {
    id: 'mod-3',
    slug: 'relational-joins',
    title: 'Multi-Table Relational JOINs',
    description: 'Master combining normalized data using INNER JOIN, LEFT OUTER JOIN, RIGHT JOIN, and Self-referencing JOINs.',
    level: 'intermediate',
    icon: 'GitFork',
    isLocked: false,
    prerequisites: ['SQL Fundamentals & Data Retrieval', 'Aggregations & Analytical Grouping'],
    totalTopics: 4,
    completedTopics: 1,
    estimatedHours: 6,
    lessons: [
      { id: 'les-3-1', slug: 'inner-join-essentials', title: 'INNER JOIN: Matching Intersecting Records', isCompleted: true, questionsCount: 7 },
      { id: 'les-3-2', slug: 'left-right-outer-joins', title: 'LEFT & RIGHT OUTER JOIN: Preserving Unmatched Rows', isCompleted: false, questionsCount: 8 },
      { id: 'les-3-3', slug: 'multiple-joins-and-cardinality', title: 'Chaining Multiple JOINs & Preventing Cartesian Bloat', isCompleted: false, questionsCount: 6 },
      { id: 'les-3-4', slug: 'self-joins-and-hierarchies', title: 'Self JOINs: Modeling Trees and Manager Hierarchies', isCompleted: false, questionsCount: 5 }
    ]
  },
  {
    id: 'mod-4',
    slug: 'subqueries-and-ctes',
    title: 'Subqueries & Common Table Expressions',
    description: 'Construct modular, readable analytical pipelines using scalar subqueries, correlated subqueries, and WITH CTEs.',
    level: 'intermediate',
    icon: 'Layers',
    isLocked: false,
    prerequisites: ['Multi-Table Relational JOINs'],
    totalTopics: 3,
    completedTopics: 0,
    estimatedHours: 5,
    lessons: [
      { id: 'les-4-1', slug: 'scalar-and-in-subqueries', title: 'Scalar Subqueries and IN / NOT IN Subqueries', isCompleted: false, questionsCount: 6 },
      { id: 'les-4-2', slug: 'correlated-subqueries-exists', title: 'Correlated Subqueries and the EXISTS Operator', isCompleted: false, questionsCount: 6 },
      { id: 'les-4-3', slug: 'common-table-expressions-cte', title: 'Cleaner Code with Common Table Expressions (WITH)', isCompleted: false, questionsCount: 8 }
    ]
  },
  {
    id: 'mod-5',
    slug: 'window-functions',
    title: 'Window Functions & Ranking',
    description: 'The golden standard of advanced SQL: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, and running cumulative sums.',
    level: 'advanced',
    icon: 'Sparkles',
    isLocked: false,
    prerequisites: ['Subqueries & Common Table Expressions'],
    totalTopics: 3,
    completedTopics: 0,
    estimatedHours: 7,
    lessons: [
      { id: 'les-5-1', slug: 'window-functions-ranking', title: 'ROW_NUMBER(), RANK(), and DENSE_RANK()', isCompleted: false, questionsCount: 8 },
      { id: 'les-5-2', slug: 'value-functions-lag-lead', title: 'Time Series & Comparisons with LAG() and LEAD()', isCompleted: false, questionsCount: 7 },
      { id: 'les-5-3', slug: 'running-totals-and-frames', title: 'Cumulative Rolling Sums and Window Framing (ROWS BETWEEN)', isCompleted: false, questionsCount: 6 }
    ]
  },
  {
    id: 'mod-6',
    slug: 'advanced-optimization-and-schema',
    title: 'Indexing, Execution Plans & Schema Design',
    description: 'Demystify EXPLAIN QUERY PLAN, B-Tree indexes, SARGable queries, and relational normalization forms (1NF-3NF).',
    level: 'advanced',
    icon: 'Cpu',
    isLocked: true,
    prerequisites: ['Window Functions & Ranking'],
    totalTopics: 3,
    completedTopics: 0,
    estimatedHours: 5,
    lessons: [
      { id: 'les-6-1', slug: 'explain-query-plans', title: 'Reading EXPLAIN Plans & Identifying Full Table Scans', isCompleted: false, questionsCount: 5 },
      { id: 'les-6-2', slug: 'indexes-and-sargability', title: 'Index Design and Writing SARGable Predicates', isCompleted: false, questionsCount: 6 },
      { id: 'les-6-3', slug: 'database-normalization', title: 'Normalization Principles: Eliminating Update Anomalies', isCompleted: false, questionsCount: 5 }
    ]
  }
];

// ==========================================
// 3. TOPIC LESSON DETAIL
// ==========================================

export const mockTopicLesson: TopicLesson = {
  id: 'les-3-2',
  slug: 'left-right-outer-joins',
  moduleId: 'mod-3',
  moduleName: 'Multi-Table Relational JOINs',
  title: 'LEFT & RIGHT OUTER JOIN: Preserving Unmatched Records',
  level: 'intermediate',
  readTimeMinutes: 12,
  orderIndex: 2,
  prevLessonSlug: 'inner-join-essentials',
  nextLessonSlug: 'multiple-joins-and-cardinality',
  conceptSummary: 'Unlike an INNER JOIN which eliminates rows that fail to match on the join condition, an OUTER JOIN guarantees that all rows from one side are retained in the result set, filling unmatched columns with NULL.',
  conceptContent: [
    'In relational databases, data is frequently split across tables to eliminate redundancy. When querying, an INNER JOIN only returns the intersection of both tables.',
    'However, business questions frequently require finding records that have no corresponding counterpart. For example: "Which registered customers have never placed an order?" or "Which products in our catalogue have zero sales this month?"',
    'A LEFT OUTER JOIN (or simply LEFT JOIN) evaluates every record from the left table. If a match exists in the right table according to the ON predicate, the matching attributes are combined. If no match exists, the columns from the right table evaluate to NULL.',
    'A key architectural pattern in SQL analysis is pairing a LEFT JOIN with a `WHERE right_table.id IS NULL` check (often called an Anti-Join pattern). This is one of the most widely asked patterns in SQL technical interviews.'
  ],
  syntaxBlocks: [
    {
      title: 'Standard LEFT OUTER JOIN Syntax',
      description: 'Preserves all records from Table A, matching rows from Table B when possible.',
      syntax: `SELECT \n    table_a.column_1,\n    table_b.column_2\nFROM table_a\nLEFT JOIN table_b \n    ON table_a.foreign_key = table_b.primary_key;`,
      notes: [
        'The keyword OUTER is optional in all modern relational engines (LEFT JOIN is identical to LEFT OUTER JOIN).',
        'Always specify table aliases when tables share column names (e.g., id or created_at) to avoid ambiguous column errors.'
      ]
    },
    {
      title: 'The Anti-Join Pattern (Finding Missing Records)',
      description: 'Filters for rows in Table A that have no related record in Table B.',
      syntax: `SELECT \n    table_a.id,\n    table_a.name\nFROM table_a\nLEFT JOIN table_b \n    ON table_a.id = table_b.a_id\nWHERE table_b.id IS NULL;`,
      notes: [
        'Always check the primary key column of the right table with `IS NULL`, never with `= NULL`.',
        'SQL uses three-valued logic (TRUE, FALSE, UNKNOWN); comparison with `=` on NULL always produces UNKNOWN.'
      ]
    }
  ],
  examples: [
    {
      title: 'Find All Customers and Their Total Order Counts (Including Zero)',
      description: 'Querying customers against orders. Notice customer 105 (Mateo Morales) has never placed an order, so his order count is 0 and last order date is NULL.',
      sql: `SELECT \n    c.id AS customer_id,\n    c.name AS customer_name,\n    COUNT(o.id) AS total_orders\nFROM customers c\nLEFT JOIN orders o \n    ON c.id = o.customer_id\nGROUP BY c.id, c.name\nORDER BY total_orders DESC;`,
      columns: ['customer_id', 'customer_name', 'total_orders'],
      rows: [
        [101, 'Sophia Chen', 3],
        [102, 'Liam Davies', 1],
        [104, 'Kenji Sato', 1],
        [103, 'Elena Rostova', 1],
        [105, 'Mateo Morales', 0]
      ]
    },
    {
      title: 'Anti-Join: Identifying Inactive Registered Customers',
      description: 'Extracting customers who registered on the platform but never completed any checkout transaction.',
      sql: `SELECT \n    c.id,\n    c.name,\n    c.country\nFROM customers c\nLEFT JOIN orders o \n    ON c.id = o.customer_id\nWHERE o.id IS NULL;`,
      columns: ['id', 'name', 'country'],
      rows: [
        [105, 'Mateo Morales', 'Spain']
      ]
    }
  ],
  practiceQuestions: [
    { id: 'q-101', title: 'Customers with Zero Orders (Anti-Join)', slug: 'customers-with-zero-orders', difficulty: 'easy', isSolved: true },
    { id: 'q-102', title: 'Calculate Average Order Value by Country', slug: 'average-order-value-by-country', difficulty: 'medium', isSolved: false },
    { id: 'q-103', title: 'Products Never Ordered by European Customers', slug: 'products-never-ordered-europe', difficulty: 'medium', isSolved: false },
    { id: 'q-104', title: 'Departments Without Active Staff', slug: 'departments-without-staff', difficulty: 'easy', isSolved: false },
    { id: 'q-105', title: 'High-Value Customer Retention Status', slug: 'high-value-customer-retention', difficulty: 'hard', isSolved: false }
  ]
};

// ==========================================
// 4. INTERACTIVE PRACTICE QUESTION DETAIL
// ==========================================

export const mockQuestionDetail: QuestionDetail = {
  id: 'q-101',
  slug: 'customers-with-zero-orders',
  title: 'Customers with Zero Purchases',
  difficulty: 'easy',
  topic: 'Multi-Table Relational JOINs',
  topicSlug: 'left-right-outer-joins',
  databaseId: 'db-ecommerce',
  databaseName: 'ecommerce_db',
  acceptanceRate: '78.4%',
  prompt: `An e-commerce marketing team is planning a re-engagement email campaign specifically targeted at users who created an account but have **never placed a single order**.

Write a SQL query to return the **customer_id**, **customer_name**, and **email** of all customers who have zero recorded orders in the \`orders\` table.

Order the final result by \`customer_name\` in **ascending** alphabetical order.`,
  requirements: [
    'Return exactly three columns with aliases: `customer_id`, `customer_name`, `email`.',
    'Include only customers who have no matching rows in the `orders` table.',
    'Order the final output alphabetically by `customer_name` ASC.',
    'Do not hardcode customer IDs; your solution will be validated against multiple synthetic datasets.'
  ],
  starterCode: `-- Find customers with zero orders
-- Available tables: customers, orders
SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.email
FROM customers c
-- Complete your query here:
`,
  officialSolution: {
    sql: `SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.email
FROM customers c
LEFT JOIN orders o 
    ON c.id = o.customer_id
WHERE o.id IS NULL
ORDER BY c.name ASC;`,
    explanation: `We perform a LEFT JOIN between the \`customers\` table (left side) and the \`orders\` table (right side) on the common relational key \`c.id = o.customer_id\`.

Because it is a LEFT JOIN, every customer row is preserved. For customers who have placed orders, the \`o.id\` column contains their order ID. For customers who have never ordered, \`o.id\` evaluates to \`NULL\`.

We filter for these inactive customers using the predicate \`WHERE o.id IS NULL\`. Finally, we sort alphabetically using \`ORDER BY c.name ASC\`.`,
    timeComplexity: 'O(N + M) using Hash / Index Lookup'
  },
  hints: [
    'Think about which type of JOIN preserves all rows from the primary table even when there is no matching record in the secondary table.',
    'Use a LEFT JOIN between `customers` (as the left table) and `orders` (as the right table) on customer_id.',
    'In your WHERE clause, check that the primary key of the orders table `IS NULL`. Remember to never use `= NULL` in SQL.'
  ],
  sampleExpectedOutput: {
    columns: ['customer_id', 'customer_name', 'email'],
    rows: [
      [105, 'Mateo Morales', 'mateo.m@example.es']
    ]
  },
  testCases: [
    {
      id: 'tc-1',
      name: 'Default Test Case (1 Inactive Customer)',
      description: 'Standard dataset with 5 customers, one of whom has placed 0 orders.',
      isHidden: false,
      expectedColumns: ['customer_id', 'customer_name', 'email'],
      expectedRows: [
        [105, 'Mateo Morales', 'mateo.m@example.es']
      ]
    },
    {
      id: 'tc-2',
      name: 'Hidden Edge Case: Multiple Inactive Customers',
      description: 'Dataset containing three newly registered users who have no orders placed.',
      isHidden: true,
      expectedColumns: ['customer_id', 'customer_name', 'email'],
      expectedRows: [
        [106, 'Amara Okafor', 'amara@example.ng'],
        [105, 'Mateo Morales', 'mateo.m@example.es'],
        [107, 'Yuki Tanaka', 'yuki@example.jp']
      ]
    },
    {
      id: 'tc-3',
      name: 'Hidden Edge Case: All Customers Active',
      description: 'Dataset where every single registered customer has at least one completed order.',
      isHidden: true,
      expectedColumns: ['customer_id', 'customer_name', 'email'],
      expectedRows: []
    }
  ]
};

// ==========================================
// 5. INTERVIEW PRACTICE QUESTIONS POOL
// ==========================================

export interface InterviewQuestionItem {
  id: string;
  slug: string;
  title: string;
  difficulty: 'easy' | 'medium' | 'hard';
  topic: string;
  databaseName: string;
  acceptanceRate: string;
  isSolved: boolean;
  companies: string[];
}

export const mockInterviewQuestions: InterviewQuestionItem[] = [
  {
    id: 'iq-1',
    slug: 'customers-with-zero-orders',
    title: 'Customers with Zero Purchases',
    difficulty: 'easy',
    topic: 'Relational Joins',
    databaseName: 'ecommerce_db',
    acceptanceRate: '78.4%',
    isSolved: true,
    companies: ['Amazon', 'Shopify', 'eBay']
  },
  {
    id: 'iq-2',
    slug: 'second-highest-salary',
    title: 'Second Highest Compensation by Division',
    difficulty: 'medium',
    topic: 'Window Functions',
    databaseName: 'hr_analytics_db',
    acceptanceRate: '54.2%',
    isSolved: false,
    companies: ['Google', 'Meta', 'Netflix']
  },
  {
    id: 'iq-3',
    slug: 'department-top-3-earners',
    title: 'Top 3 Highest Earners Per Department',
    difficulty: 'hard',
    topic: 'Window Functions',
    databaseName: 'hr_analytics_db',
    acceptanceRate: '41.8%',
    isSolved: false,
    companies: ['Stripe', 'Uber', 'Apple']
  },
  {
    id: 'iq-4',
    slug: 'cumulative-monthly-revenue',
    title: 'Cumulative Running Revenue & Month-over-Month Growth',
    difficulty: 'hard',
    topic: 'Window Functions',
    databaseName: 'ecommerce_db',
    acceptanceRate: '36.5%',
    isSolved: false,
    companies: ['Airbnb', 'DoorDash', 'Coinbase']
  },
  {
    id: 'iq-5',
    slug: 'average-order-value-by-country',
    title: 'Average Order Value & Outlier Filtering',
    difficulty: 'medium',
    topic: 'Aggregations',
    databaseName: 'ecommerce_db',
    acceptanceRate: '62.1%',
    isSolved: false,
    companies: ['Amazon', 'Walmart']
  },
  {
    id: 'iq-6',
    slug: 'consecutive-login-days',
    title: 'Identify Active Users with 3 Consecutive Days',
    difficulty: 'hard',
    topic: 'Subqueries & CTEs',
    databaseName: 'ecommerce_db',
    acceptanceRate: '32.9%',
    isSolved: false,
    companies: ['Twitter / X', 'LinkedIn', 'ByteDance']
  },
  {
    id: 'iq-7',
    slug: 'department-salary-budget-ratio',
    title: 'Department Salary as Percentage of Total Payroll',
    difficulty: 'medium',
    topic: 'Aggregations',
    databaseName: 'hr_analytics_db',
    acceptanceRate: '68.0%',
    isSolved: true,
    companies: ['Bloomberg', 'Goldman Sachs']
  },
  {
    id: 'iq-8',
    slug: 'products-never-ordered-europe',
    title: 'Catalogue Products Never Purchased in Europe',
    difficulty: 'medium',
    topic: 'Relational Joins',
    databaseName: 'ecommerce_db',
    acceptanceRate: '58.3%',
    isSolved: false,
    companies: ['Spotify', 'Zalando']
  }
];

// ==========================================
// 6. USER PROFILE & STATS
// ==========================================

export const mockUserProfile: UserProfile = {
  id: 'usr-9001',
  name: 'Alex Rivera',
  username: 'alex_sql',
  email: 'alex.rivera@example.com',
  avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=250',
  xpPoints: 1840,
  currentStreak: 5,
  maxStreak: 14,
  solvedCount: {
    easy: 12,
    medium: 7,
    hard: 2,
    total: 21
  }
};

export const mockRecentAttempts: RecentAttempt[] = [
  {
    id: 'att-1',
    questionId: 'q-101',
    questionTitle: 'Customers with Zero Purchases',
    questionSlug: 'customers-with-zero-orders',
    difficulty: 'easy',
    status: 'solved',
    timestamp: 'Today, 2:45 PM',
    executionTimeMs: 18
  },
  {
    id: 'att-2',
    questionId: 'iq-7',
    questionTitle: 'Department Salary as Percentage of Total Payroll',
    questionSlug: 'department-salary-budget-ratio',
    difficulty: 'medium',
    status: 'solved',
    timestamp: 'Yesterday, 8:12 PM',
    executionTimeMs: 24
  },
  {
    id: 'att-3',
    questionId: 'iq-2',
    questionTitle: 'Second Highest Compensation by Division',
    questionSlug: 'second-highest-salary',
    difficulty: 'medium',
    status: 'attempted',
    timestamp: '2 days ago',
    executionTimeMs: 42
  }
];

