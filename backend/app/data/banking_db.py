from app.data.seed_databases import ColumnInfo, TableInfo, SyntheticDatabaseBlueprint

BANKING_DDL = """
-- ============================================================
-- DATABASE 4: BANKING & FINANCIAL SERVICES DATABASE SCHEMA
-- ============================================================

CREATE TABLE branches (
    id INTEGER PRIMARY KEY,
    branch_name VARCHAR(80) NOT NULL UNIQUE,
    branch_code VARCHAR(10) NOT NULL UNIQUE,
    city VARCHAR(60) NOT NULL,
    state VARCHAR(30) NOT NULL,
    total_assets DECIMAL(15,2) NOT NULL CHECK(total_assets >= 0)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    credit_score INTEGER NOT NULL CHECK(credit_score BETWEEN 300 AND 850),
    annual_income DECIMAL(12,2) NOT NULL CHECK(annual_income >= 0),
    registered_branch_id INTEGER NOT NULL REFERENCES branches(id),
    joined_date DATE NOT NULL
);

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type VARCHAR(30) NOT NULL CHECK(account_type IN ('CHECKING', 'SAVINGS', 'MONEY_MARKET', 'BUSINESS_CHECKING')),
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'DORMANT', 'FROZEN', 'CLOSED')),
    opened_date DATE NOT NULL
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    transaction_type VARCHAR(20) NOT NULL CHECK(transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER_IN', 'TRANSFER_OUT', 'FEE', 'INTEREST')),
    amount DECIMAL(12,2) NOT NULL CHECK(amount > 0),
    balance_after DECIMAL(12,2) NOT NULL,
    description VARCHAR(150),
    transaction_date DATE NOT NULL
);

CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    loan_type VARCHAR(40) NOT NULL CHECK(loan_type IN ('MORTGAGE', 'AUTO_LOAN', 'PERSONAL_LOAN', 'SMALL_BUSINESS')),
    principal_amount DECIMAL(12,2) NOT NULL CHECK(principal_amount > 0),
    interest_rate DECIMAL(5,2) NOT NULL CHECK(interest_rate > 0),
    term_months INTEGER NOT NULL CHECK(term_months > 0),
    status VARCHAR(20) NOT NULL CHECK(status IN ('APPROVED', 'PENDING', 'REJECTED', 'PAID_OFF', 'DEFAULTED')),
    origination_date DATE NOT NULL
);
"""

BANKING_DML = """
-- 1. BRANCHES (5 Commercial Branches)
INSERT INTO branches (id, branch_name, branch_code, city, state, total_assets) VALUES
(1, 'Downtown Financial Center', 'BR-NYC-01', 'New York', 'NY', 850000000.00),
(2, 'Silicon Valley Tech Branch', 'BR-SFO-02', 'San Francisco', 'CA', 620000000.00),
(3, 'Loop Commercial District', 'BR-CHI-03', 'Chicago', 'IL', 410000000.00),
(4, 'Piedmont Regional Office', 'BR-ATL-04', 'Atlanta', 'GA', 290000000.00),
(5, 'Southwest Capital Hub', 'BR-DFW-05', 'Dallas', 'TX', 340000000.00);

-- 2. CUSTOMERS (25 Customers with varying incomes, credit scores, and branch locations)
INSERT INTO customers (id, first_name, last_name, email, credit_score, annual_income, registered_branch_id, joined_date) VALUES
(101, 'Alexander', 'Hamilton', 'a.hamilton@financial.org', 810, 195000.00, 1, '2019-01-15'),
(102, 'Grace', 'Hopper', 'grace.h@computing.org', 785, 145000.00, 2, '2019-03-20'),
(103, 'Marcus', 'Aurelius', 'm.aurelius@rome.org', 760, 160000.00, 1, '2019-06-10'),
(104, 'Ada', 'Lovelace', 'ada.l@analytical.org', 820, 210000.00, 2, '2019-08-01'),
(105, 'Nikola', 'Tesla', 'nikola.t@wardenclyffe.org', 690, 85000.00, 1, '2020-01-12'),
(106, 'Marie', 'Curie', 'marie.curie@radium.org', 795, 130000.00, 3, '2020-03-05'),
(107, 'Leonardo', 'DaVinci', 'leo.davinci@florence.org', 740, 115000.00, 4, '2020-05-18'),
(108, 'Alan', 'Turing', 'alan.turing@bletchley.org', 805, 175000.00, 2, '2020-07-22'),
(109, 'Hedy', 'Lamarr', 'hedy.l@frequency.org', 775, 150000.00, 2, '2020-09-14'),
(110, 'Galileo', 'Galilei', 'galileo.g@pisa.org', 710, 95000.00, 4, '2020-11-30'),
(111, 'Rosalind', 'Franklin', 'rosalind.f@dna.org', 780, 125000.00, 1, '2021-01-10'),
(112, 'Isaac', 'Newton', 'isaac.newton@cambridge.org', 750, 140000.00, 1, '2021-03-01'),
(113, 'Emmy', 'Noether', 'emmy.noether@symmetry.org', 815, 165000.00, 3, '2021-04-15'),
(114, 'Johannes', 'Kepler', 'j.kepler@astronomy.org', 680, 78000.00, 5, '2021-06-20'),
(115, 'Katherine', 'Johnson', 'k.johnson@mercury.org', 830, 155000.00, 4, '2021-08-10'),
(116, 'Benjamin', 'Franklin', 'ben.franklin@philadelphia.org', 790, 180000.00, 1, '2021-10-05'),
(117, 'Lise', 'Meitner', 'lise.meitner@fission.org', 770, 135000.00, 3, '2021-12-01'),
(118, 'Charles', 'Darwin', 'c.darwin@beagle.org', 735, 110000.00, 5, '2022-01-18'),
(119, 'Srinivasa', 'Ramanujan', 's.ramanujan@infinity.org', 765, 105000.00, 3, '2022-03-25'),
(120, 'Barbara', 'McClintock', 'barbara.m@maize.org', 800, 140000.00, 2, '2022-05-15'),
-- Low credit score / high risk customers for loan evaluation exercises
(121, 'Gordon', 'Gekko', 'gordon.gekko@wallst.org', 580, 250000.00, 1, '2022-07-01'),
(122, 'Jordan', 'Belfort', 'jordan.b@stratton.org', 540, 180000.00, 1, '2022-08-20'),
(123, 'Billy', 'McFarland', 'billy.m@fyrefest.org', 510, 45000.00, 1, '2022-10-10'),
(124, 'Anna', 'Delvey', 'anna.sorokin@delvey.org', 490, 30000.00, 1, '2022-11-05'),
(125, 'Charles', 'Ponzi', 'charles.ponzi@postal.org', 450, 40000.00, 3, '2022-12-15');

-- 3. ACCOUNTS (35 Accounts: multiple accounts per customer, some with zero transactions!)
INSERT INTO accounts (id, customer_id, branch_id, account_number, account_type, balance, status, opened_date) VALUES
(1001, 101, 1, 'CHK-1001-901', 'CHECKING', 14500.50, 'ACTIVE', '2019-01-15'),
(1002, 101, 1, 'SAV-1001-902', 'SAVINGS', 85000.00, 'ACTIVE', '2019-01-20'),
(1003, 102, 2, 'CHK-1002-801', 'CHECKING', 9250.75, 'ACTIVE', '2019-03-20'),
(1004, 102, 2, 'MM-1002-802', 'MONEY_MARKET', 125000.00, 'ACTIVE', '2019-04-01'),
(1005, 103, 1, 'CHK-1003-701', 'CHECKING', 21400.00, 'ACTIVE', '2019-06-10'),
(1006, 104, 2, 'CHK-1004-601', 'CHECKING', 38900.25, 'ACTIVE', '2019-08-01'),
(1007, 104, 2, 'SAV-1004-602', 'SAVINGS', 210000.00, 'ACTIVE', '2019-08-15'),
(1008, 104, 2, 'BUS-1004-603', 'BUSINESS_CHECKING', 95000.00, 'ACTIVE', '2020-02-01'),
(1009, 105, 1, 'CHK-1005-501', 'CHECKING', 3200.00, 'ACTIVE', '2020-01-12'),
(1010, 106, 3, 'CHK-1006-401', 'CHECKING', 12450.00, 'ACTIVE', '2020-03-05'),
(1011, 106, 3, 'SAV-1006-402', 'SAVINGS', 64000.00, 'ACTIVE', '2020-03-10'),
(1012, 107, 4, 'CHK-1007-301', 'CHECKING', 8900.00, 'ACTIVE', '2020-05-18'),
(1013, 108, 2, 'CHK-1008-201', 'CHECKING', 42100.00, 'ACTIVE', '2020-07-22'),
(1014, 108, 2, 'SAV-1008-202', 'SAVINGS', 150000.00, 'ACTIVE', '2020-08-01'),
(1015, 109, 2, 'CHK-1009-101', 'CHECKING', 18750.00, 'ACTIVE', '2020-09-14'),
(1016, 110, 4, 'CHK-1010-001', 'CHECKING', 6400.00, 'ACTIVE', '2020-11-30'),
(1017, 111, 1, 'CHK-1011-911', 'CHECKING', 15300.00, 'ACTIVE', '2021-01-10'),
(1018, 112, 1, 'CHK-1012-912', 'CHECKING', 27600.00, 'ACTIVE', '2021-03-01'),
(1019, 113, 3, 'CHK-1013-913', 'CHECKING', 31200.00, 'ACTIVE', '2021-04-15'),
(1020, 114, 5, 'CHK-1014-914', 'CHECKING', 5100.00, 'ACTIVE', '2021-06-20'),
(1021, 115, 4, 'CHK-1015-915', 'CHECKING', 19800.00, 'ACTIVE', '2021-08-10'),
(1022, 116, 1, 'CHK-1016-916', 'CHECKING', 45000.00, 'ACTIVE', '2021-10-05'),
(1023, 117, 3, 'CHK-1017-917', 'CHECKING', 14200.00, 'ACTIVE', '2021-12-01'),
(1024, 118, 5, 'CHK-1018-918', 'CHECKING', 11300.00, 'ACTIVE', '2022-01-18'),
(1025, 119, 3, 'CHK-1019-919', 'CHECKING', 8400.00, 'ACTIVE', '2022-03-25'),
(1026, 120, 2, 'CHK-1020-920', 'CHECKING', 23500.00, 'ACTIVE', '2022-05-15'),
(1027, 121, 1, 'CHK-1021-921', 'CHECKING', 1500.00, 'FROZEN', '2022-07-01'),
(1028, 122, 1, 'CHK-1022-922', 'CHECKING', 450.00, 'FROZEN', '2022-08-20'),
(1029, 123, 1, 'CHK-1023-923', 'CHECKING', 120.00, 'FROZEN', '2022-10-10'),
-- EDGE CASES: DORMANT / NEW ACCOUNTS WITH ZERO TRANSACTIONS (Anti-join targets!)
(1030, 101, 1, 'SAV-1030-930', 'SAVINGS', 500.00, 'DORMANT', '2022-11-01'),
(1031, 103, 1, 'MM-1031-931', 'MONEY_MARKET', 50000.00, 'ACTIVE', '2023-01-10'),
(1032, 105, 1, 'SAV-1032-932', 'SAVINGS', 250.00, 'DORMANT', '2023-01-15'),
(1033, 124, 1, 'CHK-1033-933', 'CHECKING', 0.00, 'CLOSED', '2022-11-05'),
(1034, 125, 3, 'CHK-1034-934', 'CHECKING', 0.00, 'CLOSED', '2022-12-15'),
(1035, 108, 2, 'MM-1035-935', 'MONEY_MARKET', 75000.00, 'ACTIVE', '2023-02-01');

-- 4. TRANSACTIONS (40 Transactions with various types, dates, amounts)
INSERT INTO transactions (id, account_id, transaction_type, amount, balance_after, description, transaction_date) VALUES
(1, 1001, 'DEPOSIT', 5000.00, 15000.00, 'Payroll Direct Deposit', '2023-01-05'),
(2, 1001, 'WITHDRAWAL', 850.00, 14150.00, 'Mortgage Auto Debit', '2023-01-08'),
(3, 1001, 'TRANSFER_OUT', 1000.00, 13150.00, 'Transfer to Savings 1002', '2023-01-10'),
(4, 1002, 'TRANSFER_IN', 1000.00, 85000.00, 'Transfer from Checking 1001', '2023-01-10'),
(5, 1001, 'FEE', 15.00, 13135.00, 'Out of Network ATM Surcharge', '2023-01-12'),
(6, 1002, 'INTEREST', 285.50, 85285.50, 'Monthly Savings Interest Yield', '2023-01-31'),
(7, 1003, 'DEPOSIT', 6200.00, 11200.00, 'Consulting Wire Transfer', '2023-01-15'),
(8, 1003, 'WITHDRAWAL', 1200.00, 10000.00, 'Branch Cash Withdrawal', '2023-01-18'),
(9, 1004, 'INTEREST', 415.20, 125415.20, 'Money Market Quarterly Yield', '2023-01-31'),
(10, 1005, 'DEPOSIT', 8500.00, 25000.00, 'Investment Dividend Credit', '2023-01-20'),
(11, 1005, 'WITHDRAWAL', 3600.00, 21400.00, 'Property Tax Payment', '2023-01-25'),
(12, 1006, 'DEPOSIT', 12000.00, 45000.00, 'Software Royalty Payment', '2023-02-01'),
(13, 1006, 'TRANSFER_OUT', 5000.00, 40000.00, 'Transfer to High Yield Savings', '2023-02-05'),
(14, 1007, 'TRANSFER_IN', 5000.00, 210000.00, 'Transfer from Checking', '2023-02-05'),
(15, 1008, 'DEPOSIT', 35000.00, 115000.00, 'Client Enterprise Contract Retainer', '2023-02-10'),
(16, 1008, 'WITHDRAWAL', 20000.00, 95000.00, 'Vendor Hardware Procurement', '2023-02-15'),
(17, 1009, 'DEPOSIT', 3200.00, 3200.00, 'Direct Deposit', '2023-02-15'),
(18, 1010, 'DEPOSIT', 4500.00, 14000.00, 'Salary Credit', '2023-02-18'),
(19, 1010, 'WITHDRAWAL', 1550.00, 12450.00, 'Apartment Lease Wire', '2023-02-22'),
(20, 1011, 'INTEREST', 180.00, 64000.00, 'Monthly Savings Interest', '2023-02-28'),
(21, 1012, 'DEPOSIT', 4100.00, 8900.00, 'Biweekly Paycheck', '2023-03-01'),
(22, 1013, 'DEPOSIT', 15000.00, 52000.00, 'Contract Settlement', '2023-03-05'),
(23, 1013, 'WITHDRAWAL', 9900.00, 42100.00, 'Tax Return Disbursement', '2023-03-10'),
(24, 1014, 'INTEREST', 485.00, 150000.00, 'High Yield Savings Interest', '2023-03-31'),
(25, 1015, 'DEPOSIT', 7800.00, 18750.00, 'Royalties Deposit', '2023-03-15'),
(26, 1016, 'WITHDRAWAL', 450.00, 6400.00, 'Utility Auto Pay', '2023-03-20'),
(27, 1017, 'DEPOSIT', 6500.00, 15300.00, 'Research Grant Stipend', '2023-03-25'),
(28, 1018, 'DEPOSIT', 9500.00, 27600.00, 'Consulting Retainer', '2023-04-01'),
(29, 1019, 'DEPOSIT', 11000.00, 31200.00, 'Corporate Dividend', '2023-04-05'),
(30, 1020, 'WITHDRAWAL', 1200.00, 5100.00, 'Car Lease Payment', '2023-04-10'),
(31, 1021, 'DEPOSIT', 8200.00, 19800.00, 'Government Salary Direct Deposit', '2023-04-15'),
(32, 1022, 'DEPOSIT', 18000.00, 45000.00, 'Publishing Advance Royalty', '2023-04-20'),
(33, 1023, 'DEPOSIT', 5400.00, 14200.00, 'Biweekly Salary', '2023-04-25'),
(34, 1024, 'WITHDRAWAL', 2100.00, 11300.00, 'Home Repairs Wire', '2023-04-28'),
(35, 1025, 'DEPOSIT', 3900.00, 8400.00, 'Academic Fellowship Pay', '2023-05-01'),
(36, 1026, 'DEPOSIT', 9200.00, 23500.00, 'Monthly Retainer', '2023-05-05'),
-- Suspicious / overdraft fee transactions on frozen accounts
(37, 1027, 'FEE', 35.00, 1500.00, 'Account Inactivity Legal Freeze Fee', '2023-05-01'),
(38, 1028, 'FEE', 35.00, 450.00, 'Account Inactivity Legal Freeze Fee', '2023-05-01'),
(39, 1029, 'FEE', 35.00, 120.00, 'Account Inactivity Legal Freeze Fee', '2023-05-01'),
(40, 1001, 'DEPOSIT', 5000.00, 14500.50, 'Payroll Direct Deposit', '2023-05-05');

-- 5. LOANS (15 Loan contracts across varying types, amounts, and statuses)
INSERT INTO loans (id, customer_id, branch_id, loan_type, principal_amount, interest_rate, term_months, status, origination_date) VALUES
(501, 101, 1, 'MORTGAGE', 540000.00, 5.25, 360, 'APPROVED', '2020-04-15'),
(502, 102, 2, 'AUTO_LOAN', 42000.00, 4.50, 60, 'PAID_OFF', '2019-06-01'),
(503, 103, 1, 'PERSONAL_LOAN', 25000.00, 7.80, 36, 'PAID_OFF', '2020-02-10'),
(504, 104, 2, 'SMALL_BUSINESS', 250000.00, 6.10, 84, 'APPROVED', '2021-03-15'),
(505, 106, 3, 'MORTGAGE', 380000.00, 4.95, 360, 'APPROVED', '2021-08-01'),
(506, 107, 4, 'AUTO_LOAN', 35000.00, 5.10, 48, 'APPROVED', '2022-01-10'),
(507, 108, 2, 'MORTGAGE', 620000.00, 5.50, 360, 'APPROVED', '2022-04-15'),
(508, 110, 4, 'PERSONAL_LOAN', 18000.00, 8.20, 24, 'APPROVED', '2022-09-01'),
(509, 112, 1, 'AUTO_LOAN', 48000.00, 4.85, 60, 'APPROVED', '2023-01-15'),
-- PENDING LOANS
(510, 115, 4, 'MORTGAGE', 425000.00, 5.75, 360, 'PENDING', '2023-04-10'),
(511, 116, 1, 'SMALL_BUSINESS', 150000.00, 6.50, 60, 'PENDING', '2023-04-25'),
-- REJECTED LOANS (Poor credit score / high risk applicants)
(512, 122, 1, 'PERSONAL_LOAN', 50000.00, 12.50, 36, 'REJECTED', '2023-02-15'),
(513, 124, 1, 'SMALL_BUSINESS', 500000.00, 14.00, 60, 'REJECTED', '2023-03-01'),
(514, 125, 3, 'PERSONAL_LOAN', 35000.00, 15.00, 24, 'REJECTED', '2023-03-20'),
-- DEFAULTED LOAN
(515, 121, 1, 'PERSONAL_LOAN', 40000.00, 9.50, 36, 'DEFAULTED', '2021-11-01');
"""

BANKING_DATABASE = SyntheticDatabaseBlueprint(
    id="db-banking",
    name="banking_db",
    display_name="Commercial Banking & Credit Services Database",
    description="Financial core banking model tracking regional branches, customer credit scores, multitype deposit accounts, transactional journals, and loan risk portfolios.",
    init_ddl=BANKING_DDL,
    seed_dml=BANKING_DML,
    tables=[
        TableInfo(
            name="branches",
            description="Bank physical branch locations and asset totals",
            row_count=5,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="branch_name", type="VARCHAR(80)", nullable=False),
                ColumnInfo(name="branch_code", type="VARCHAR(10)", nullable=False),
                ColumnInfo(name="city", type="VARCHAR(60)", nullable=False),
                ColumnInfo(name="state", type="VARCHAR(30)", nullable=False),
                ColumnInfo(name="total_assets", type="DECIMAL(15,2)", nullable=False),
            ],
        ),
        TableInfo(
            name="customers",
            description="Banking customers with credit bureau scores and reported annual incomes",
            row_count=25,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="first_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="last_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="email", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="credit_score", type="INTEGER", nullable=False),
                ColumnInfo(name="annual_income", type="DECIMAL(12,2)", nullable=False),
                ColumnInfo(name="registered_branch_id", type="INTEGER", is_foreign_key=True, references="branches.id", nullable=False),
                ColumnInfo(name="joined_date", type="DATE", nullable=False),
            ],
        ),
        TableInfo(
            name="accounts",
            description="Checking, savings, money market, and commercial business accounts",
            row_count=35,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="customer_id", type="INTEGER", is_foreign_key=True, references="customers.id", nullable=False),
                ColumnInfo(name="branch_id", type="INTEGER", is_foreign_key=True, references="branches.id", nullable=False),
                ColumnInfo(name="account_number", type="VARCHAR(20)", nullable=False),
                ColumnInfo(name="account_type", type="VARCHAR(30)", nullable=False),
                ColumnInfo(name="balance", type="DECIMAL(12,2)", nullable=False),
                ColumnInfo(name="status", type="VARCHAR(20)", nullable=False),
                ColumnInfo(name="opened_date", type="DATE", nullable=False),
            ],
        ),
        TableInfo(
            name="transactions",
            description="Deposits, withdrawals, fees, interest payments, and transfers",
            row_count=40,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="account_id", type="INTEGER", is_foreign_key=True, references="accounts.id", nullable=False),
                ColumnInfo(name="transaction_type", type="VARCHAR(20)", nullable=False),
                ColumnInfo(name="amount", type="DECIMAL(12,2)", nullable=False),
                ColumnInfo(name="balance_after", type="DECIMAL(12,2)", nullable=False),
                ColumnInfo(name="description", type="VARCHAR(150)", nullable=True),
                ColumnInfo(name="transaction_date", type="DATE", nullable=False),
            ],
        ),
        TableInfo(
            name="loans",
            description="Mortgages, auto loans, personal, and small business credit applications",
            row_count=15,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="customer_id", type="INTEGER", is_foreign_key=True, references="customers.id", nullable=False),
                ColumnInfo(name="branch_id", type="INTEGER", is_foreign_key=True, references="branches.id", nullable=False),
                ColumnInfo(name="loan_type", type="VARCHAR(40)", nullable=False),
                ColumnInfo(name="principal_amount", type="DECIMAL(12,2)", nullable=False),
                ColumnInfo(name="interest_rate", type="DECIMAL(5,2)", nullable=False),
                ColumnInfo(name="term_months", type="INTEGER", nullable=False),
                ColumnInfo(name="status", type="VARCHAR(20)", nullable=False),
                ColumnInfo(name="origination_date", type="DATE", nullable=False),
            ],
        ),
    ],
)

