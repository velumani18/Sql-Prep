from app.data.seed_databases import ColumnInfo, TableInfo, SyntheticDatabaseBlueprint

UNIVERSITY_DDL = """
-- ============================================================
-- DATABASE 3: UNIVERSITY ACADEMIC DATABASE SCHEMA
-- ============================================================

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    building VARCHAR(80) NOT NULL
);

CREATE TABLE professors (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    title VARCHAR(60) NOT NULL CHECK(title IN ('Full Professor', 'Associate Professor', 'Assistant Professor', 'Adjunct Lecturer')),
    hired_year INTEGER NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    code VARCHAR(15) NOT NULL UNIQUE,
    title VARCHAR(120) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id),
    professor_id INTEGER REFERENCES professors(id),
    credits INTEGER NOT NULL CHECK(credits BETWEEN 1 AND 6)
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    major_department_id INTEGER REFERENCES departments(id),
    enrollment_year INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE', 'GRADUATED', 'SUSPENDED'))
);

CREATE TABLE grades (
    letter_grade VARCHAR(2) PRIMARY KEY,
    grade_points DECIMAL(3,2) NOT NULL,
    description VARCHAR(50) NOT NULL
);

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    semester VARCHAR(20) NOT NULL,
    academic_year INTEGER NOT NULL,
    letter_grade VARCHAR(2) REFERENCES grades(letter_grade),
    UNIQUE (student_id, course_id, semester, academic_year)
);
"""

UNIVERSITY_DML = """
-- 1. GRADES REFERENCE TABLE
INSERT INTO grades (letter_grade, grade_points, description) VALUES
('A+', 4.00, 'Distinguished High Honors'),
('A',  4.00, 'Excellent Mastery'),
('A-', 3.70, 'Very Good'),
('B+', 3.30, 'Good'),
('B',  3.00, 'Above Average'),
('B-', 2.70, 'Average Competency'),
('C+', 2.30, 'Satisfactory'),
('C',  2.00, 'Marginal Pass'),
('D',  1.00, 'Minimum Passing Grade'),
('F',  0.00, 'Failing Mark');

-- 2. DEPARTMENTS
INSERT INTO departments (id, name, code, building) VALUES
(1, 'Computer Science & Engineering', 'CS', 'Turing Hall'),
(2, 'Mathematics & Statistics', 'MATH', 'Euler Science Pavilion'),
(3, 'Physics & Astronomy', 'PHYS', 'Newton Laboratories'),
(4, 'Economics & Finance', 'ECON', 'Adam Smith Building'),
(5, 'Philosophy & Ethics', 'PHIL', 'Aristotle Center'),
(6, 'Biology & Life Sciences', 'BIO', 'Darwin Natural Sciences');

-- 3. PROFESSORS (8 Professors: some teaching 2-3 courses, one on sabbatical with 0 courses!)
INSERT INTO professors (id, first_name, last_name, email, department_id, title, hired_year) VALUES
(1, 'Ada', 'Lovelace', 'ada.lovelace@university.edu', 1, 'Full Professor', 2012),
(2, 'Donald', 'Knuth', 'donald.knuth@university.edu', 1, 'Full Professor', 2008),
(3, 'Grace', 'Hopper', 'grace.hopper@university.edu', 1, 'Associate Professor', 2016),
(4, 'Carl', 'Gauss', 'carl.gauss@university.edu', 2, 'Full Professor', 2010),
(5, 'Katherine', 'Johnson', 'katherine.j@university.edu', 2, 'Associate Professor', 2015),
(6, 'Richard', 'Feynman', 'richard.feynman@university.edu', 3, 'Full Professor', 2011),
(7, 'Elinor', 'Ostrom', 'elinor.ostrom@university.edu', 4, 'Full Professor', 2014),
-- EDGE CASE: Professor on Sabbatical Research (Teaches 0 courses!)
(8, 'Noam', 'Chomsky', 'noam.chomsky@university.edu', 5, 'Full Professor', 2005);

-- 4. COURSES (12 Courses: some popular, 2 niche courses with ZERO student enrollments!)
INSERT INTO courses (id, code, title, department_id, professor_id, credits) VALUES
(101, 'CS-101', 'Introduction to Computer Science & Algorithms', 1, 1, 4),
(102, 'CS-201', 'Data Structures & System Software', 1, 1, 4),
(103, 'CS-305', 'Relational Database Design & SQL Internals', 1, 2, 4),
(104, 'CS-402', 'Compilers, Parsing & Virtual Machines', 1, 3, 4),
(105, 'MATH-110', 'Calculus I: Differential Analysis', 2, 4, 4),
(106, 'MATH-220', 'Linear Algebra & Matrix Decompositions', 2, 4, 3),
(107, 'MATH-310', 'Probability, Stochastics & Statistical Inference', 2, 5, 3),
(108, 'PHYS-101', 'Classical Mechanics & Wave Dynamics', 3, 6, 4),
(109, 'PHYS-301', 'Quantum Electrodynamics & Particle Physics', 3, 6, 4),
(110, 'ECON-101', 'Principles of Microeconomics & Game Theory', 4, 7, 3),
-- EDGE CASES: Courses with ZERO student enrollments!
(111, 'CS-599', 'Advanced Topics in Quantum Computing Cryptography', 1, 2, 4),
(112, 'MATH-500', 'Non-Euclidean Geometries & Topology Seminar', 2, 4, 3);

-- 5. STUDENTS (30 Students: some taking multiple courses, 5 newly admitted with ZERO enrollments!)
INSERT INTO students (id, first_name, last_name, email, major_department_id, enrollment_year, status) VALUES
(1001, 'Alice', 'Smith', 'alice.smith@university.edu', 1, 2021, 'ACTIVE'),
(1002, 'Bob', 'Jones', 'bob.jones@university.edu', 1, 2021, 'ACTIVE'),
(1003, 'Charlie', 'Brown', 'charlie.b@university.edu', 1, 2022, 'ACTIVE'),
(1004, 'Diana', 'Prince', 'diana.p@university.edu', 2, 2021, 'ACTIVE'),
(1005, 'Evan', 'Wright', 'evan.w@university.edu', 2, 2022, 'ACTIVE'),
(1006, 'Fiona', 'Gallagher', 'fiona.g@university.edu', 3, 2020, 'ACTIVE'),
(1007, 'George', 'Miller', 'george.m@university.edu', 4, 2021, 'ACTIVE'),
(1008, 'Hannah', 'Abbott', 'hannah.a@university.edu', 1, 2022, 'ACTIVE'),
(1009, 'Ian', 'Malcolm', 'ian.m@university.edu', 3, 2021, 'ACTIVE'),
(1010, 'Julia', 'Roberts', 'julia.r@university.edu', 4, 2022, 'ACTIVE'),
(1011, 'Kevin', 'Flynn', 'kevin.f@university.edu', 1, 2020, 'GRADUATED'),
(1012, 'Laura', 'Croft', 'laura.c@university.edu', 1, 2021, 'ACTIVE'),
(1013, 'Miles', 'Morales', 'miles.m@university.edu', 1, 2022, 'ACTIVE'),
(1014, 'Nora', 'Valkyrie', 'nora.v@university.edu', 2, 2021, 'ACTIVE'),
(1015, 'Oscar', 'Wilde', 'oscar.w@university.edu', 5, 2021, 'ACTIVE'),
(1016, 'Peter', 'Parker', 'peter.p@university.edu', 3, 2021, 'ACTIVE'),
(1017, 'Quinn', 'Fabray', 'quinn.f@university.edu', 4, 2022, 'ACTIVE'),
(1018, 'Riley', 'Matthews', 'riley.m@university.edu', 1, 2022, 'ACTIVE'),
(1019, 'Sam', 'Winchester', 'sam.w@university.edu', 5, 2020, 'ACTIVE'),
(1020, 'Tara', 'Maclay', 'tara.m@university.edu', 2, 2021, 'ACTIVE'),
(1021, 'Uma', 'Thurman', 'uma.t@university.edu', 4, 2021, 'ACTIVE'),
(1022, 'Victor', 'Stone', 'victor.s@university.edu', 1, 2021, 'ACTIVE'),
(1023, 'Wanda', 'Maximoff', 'wanda.m@university.edu', 3, 2021, 'ACTIVE'),
(1024, 'Xavier', 'Thornton', 'xavier.t@university.edu', 1, 2022, 'ACTIVE'),
(1025, 'Yara', 'Greyjoy', 'yara.g@university.edu', 2, 2022, 'ACTIVE'),

-- EDGE CASES: Newly admitted freshmen with ZERO enrollments (Anti-join targets!)
(2001, 'Zack', 'Morris', 'zack.m@university.edu', 1, 2023, 'ACTIVE'),
(2002, 'Betty', 'Cooper', 'betty.c@university.edu', 4, 2023, 'ACTIVE'),
(2003, 'Clark', 'Kent', 'clark.k@university.edu', 5, 2023, 'ACTIVE'),
(2004, 'Daisy', 'Johnson', 'daisy.j@university.edu', 1, 2023, 'ACTIVE'),
(2005, 'Bruce', 'Wayne', 'bruce.w@university.edu', 4, 2023, 'ACTIVE');

-- 6. ENROLLMENTS (Completed courses have letter grades; in-progress courses have NULL grade!)
INSERT INTO enrollments (id, student_id, course_id, semester, academic_year, letter_grade) VALUES
-- CS-101 Enrollments
(1, 1001, 101, 'Fall', 2021, 'A'),
(2, 1002, 101, 'Fall', 2021, 'B+'),
(3, 1003, 101, 'Fall', 2022, 'A-'),
(4, 1008, 101, 'Fall', 2022, 'A'),
(5, 1011, 101, 'Fall', 2020, 'A+'),
(6, 1012, 101, 'Fall', 2021, 'B'),
(7, 1013, 101, 'Fall', 2022, 'A'),
(8, 1018, 101, 'Fall', 2022, 'B-'),
(9, 1022, 101, 'Fall', 2021, 'A'),
(10, 1024, 101, 'Fall', 2022, 'C+'),

-- CS-102 Enrollments
(11, 1001, 102, 'Spring', 2022, 'A'),
(12, 1002, 102, 'Spring', 2022, 'B'),
(13, 1011, 102, 'Spring', 2021, 'A'),
(14, 1012, 102, 'Spring', 2022, 'A-'),
(15, 1022, 102, 'Spring', 2022, 'B+'),

-- CS-305 (Databases & SQL)
(16, 1001, 103, 'Fall', 2022, 'A+'),
(17, 1002, 103, 'Fall', 2022, 'A-'),
(18, 1011, 103, 'Fall', 2021, 'A'),
(19, 1012, 103, 'Fall', 2022, 'B+'),
(20, 1004, 103, 'Fall', 2022, 'A'),
(21, 1022, 103, 'Fall', 2022, 'A'),

-- CS-402 (Compilers)
(22, 1001, 104, 'Spring', 2023, 'A'),
(23, 1011, 104, 'Spring', 2022, 'A-'),

-- MATH-110 (Calculus)
(24, 1001, 105, 'Fall', 2021, 'A-'),
(25, 1004, 105, 'Fall', 2021, 'A+'),
(26, 1005, 105, 'Fall', 2022, 'B'),
(27, 1014, 105, 'Fall', 2021, 'A'),
(28, 1020, 105, 'Fall', 2021, 'A-'),
(29, 1025, 105, 'Fall', 2022, 'B+'),

-- MATH-220 (Linear Algebra)
(30, 1004, 106, 'Spring', 2022, 'A'),
(31, 1005, 106, 'Spring', 2023, 'B+'),
(32, 1014, 106, 'Spring', 2022, 'A'),
(33, 1020, 106, 'Spring', 2022, 'B'),

-- MATH-310 (Probability & Stats)
(34, 1004, 107, 'Fall', 2022, 'A'),
(35, 1007, 107, 'Fall', 2022, 'B+'),
(36, 1014, 107, 'Fall', 2022, 'A-'),

-- PHYS-101 (Mechanics)
(37, 1006, 108, 'Fall', 2020, 'A'),
(38, 1009, 108, 'Fall', 2021, 'B+'),
(39, 1016, 108, 'Fall', 2021, 'A+'),
(40, 1023, 108, 'Fall', 2021, 'A'),

-- PHYS-301 (Quantum)
(41, 1006, 109, 'Spring', 2022, 'A'),
(42, 1016, 109, 'Spring', 2022, 'A'),
(43, 1023, 109, 'Spring', 2022, 'B+'),

-- ECON-101 (Microeconomics)
(44, 1007, 110, 'Fall', 2021, 'A'),
(45, 1010, 110, 'Fall', 2022, 'A-'),
(46, 1017, 110, 'Fall', 2022, 'B'),
(47, 1021, 110, 'Fall', 2021, 'A'),

-- EDGE CASES: In-Progress Enrollments (Grade is NULL!)
(48, 1002, 104, 'Spring', 2023, NULL),
(49, 1003, 102, 'Spring', 2023, NULL),
(50, 1008, 103, 'Spring', 2023, NULL),
(51, 1013, 103, 'Spring', 2023, NULL),
(52, 1018, 105, 'Spring', 2023, NULL);
"""

UNIVERSITY_DATABASE = SyntheticDatabaseBlueprint(
    id="db-university",
    name="university_db",
    display_name="Higher Education Academic & Registrar Database",
    description="Collegiate educational data model containing academic departments, professors, course curriculums, student rosters, enrollments, and letter grade evaluations.",
    init_ddl=UNIVERSITY_DDL,
    seed_dml=UNIVERSITY_DML,
    tables=[
        TableInfo(
            name="departments",
            description="Academic faculties and campus buildings",
            row_count=6,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="name", type="VARCHAR(80)", nullable=False),
                ColumnInfo(name="code", type="VARCHAR(10)", nullable=False),
                ColumnInfo(name="building", type="VARCHAR(80)", nullable=False),
            ],
        ),
        TableInfo(
            name="professors",
            description="Faculty teaching staff, ranks, and department appointments",
            row_count=8,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="first_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="last_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="email", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="department_id", type="INTEGER", is_foreign_key=True, references="departments.id", nullable=False),
                ColumnInfo(name="title", type="VARCHAR(60)", nullable=False),
                ColumnInfo(name="hired_year", type="INTEGER", nullable=False),
            ],
        ),
        TableInfo(
            name="courses",
            description="Course catalog, assigned instructors, and credit units",
            row_count=12,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="code", type="VARCHAR(15)", nullable=False),
                ColumnInfo(name="title", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="department_id", type="INTEGER", is_foreign_key=True, references="departments.id", nullable=False),
                ColumnInfo(name="professor_id", type="INTEGER", is_foreign_key=True, references="professors.id", nullable=True),
                ColumnInfo(name="credits", type="INTEGER", nullable=False),
            ],
        ),
        TableInfo(
            name="students",
            description="Undergraduate and graduate student roster",
            row_count=30,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="first_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="last_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="email", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="major_department_id", type="INTEGER", is_foreign_key=True, references="departments.id", nullable=True),
                ColumnInfo(name="enrollment_year", type="INTEGER", nullable=False),
                ColumnInfo(name="status", type="VARCHAR(20)", nullable=False),
            ],
        ),
        TableInfo(
            name="grades",
            description="Official grading system and GPA scale points",
            row_count=10,
            columns=[
                ColumnInfo(name="letter_grade", type="VARCHAR(2)", is_primary_key=True, nullable=False),
                ColumnInfo(name="grade_points", type="DECIMAL(3,2)", nullable=False),
                ColumnInfo(name="description", type="VARCHAR(50)", nullable=False),
            ],
        ),
        TableInfo(
            name="enrollments",
            description="Course registrations, semesters, and earned student grades",
            row_count=52,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="student_id", type="INTEGER", is_foreign_key=True, references="students.id", nullable=False),
                ColumnInfo(name="course_id", type="INTEGER", is_foreign_key=True, references="courses.id", nullable=False),
                ColumnInfo(name="semester", type="VARCHAR(20)", nullable=False),
                ColumnInfo(name="academic_year", type="INTEGER", nullable=False),
                ColumnInfo(name="letter_grade", type="VARCHAR(2)", is_foreign_key=True, references="grades.letter_grade", nullable=True),
            ],
        ),
    ],
)

