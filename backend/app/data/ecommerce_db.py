from app.data.seed_databases import ColumnInfo, TableInfo, SyntheticDatabaseBlueprint

ECOMMERCE_DDL = """
-- ============================================================
-- DATABASE 2: E-COMMERCE DATABASE SCHEMA
-- ============================================================

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    name VARCHAR(100) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
    email VARCHAR(120) NOT NULL UNIQUE,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(60) NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK(price > 0),
    stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0),
    is_active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL CHECK(total_amount >= 0),
    status VARCHAR(20) NOT NULL CHECK(status IN ('COMPLETED', 'SHIPPED', 'PENDING', 'CANCELLED'))
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price > 0)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL UNIQUE REFERENCES orders(id),
    payment_method VARCHAR(30) NOT NULL CHECK(payment_method IN ('CREDIT_CARD', 'PAYPAL', 'BANK_TRANSFER', 'APPLE_PAY')),
    amount DECIMAL(10,2) NOT NULL CHECK(amount > 0),
    payment_status VARCHAR(20) NOT NULL CHECK(payment_status IN ('SUCCESSFUL', 'PENDING', 'FAILED')),
    payment_date DATE
);
"""

ECOMMERCE_DML = """
-- 1. CATEGORIES (6 Categories)
INSERT INTO categories (id, name, description) VALUES
(1, 'Consumer Electronics', 'Smartphones, laptops, monitors, audio devices, and computer peripherals'),
(2, 'Home & Living', 'Furniture, bedding, home decor, cookware, and kitchen appliances'),
(3, 'Apparel & Footwear', 'Men and women designer fashion, athletic shoes, and accessories'),
(4, 'Books & Media', 'Technical literature, computer science books, audiobooks, and graphic novels'),
(5, 'Health & Fitness', 'Gym equipment, supplements, wearable fitness trackers, and yoga mats'),
(6, 'Office Supplies', 'Ergonomic desk accessories, stationery, notebooks, and organizers');

-- 2. CUSTOMERS (30 Customers: some with 3+ orders, some with 1-2, and 6 with ZERO orders for anti-joins!)
INSERT INTO customers (id, first_name, last_name, email, country, city, created_at) VALUES
(101, 'Sophia', 'Chen', 'sophia.c@example.com', 'United States', 'San Francisco', '2022-01-15'),
(102, 'Liam', 'Davies', 'liam.d@example.co.uk', 'United Kingdom', 'London', '2022-02-01'),
(103, 'Elena', 'Rostova', 'elena.r@example.de', 'Germany', 'Berlin', '2022-03-10'),
(104, 'Kenji', 'Sato', 'kenji.s@example.jp', 'Japan', 'Tokyo', '2022-03-25'),
(105, 'Mateo', 'Morales', 'mateo.m@example.es', 'Spain', 'Madrid', '2022-04-05'),
(106, 'Amara', 'Okafor', 'amara.o@example.ng', 'Nigeria', 'Lagos', '2022-05-12'),
(107, 'Lucas', 'Silva', 'lucas.s@example.br', 'Brazil', 'Sao Paulo', '2022-06-01'),
(108, 'Hannah', 'Schmidt', 'hannah.s@example.de', 'Germany', 'Munich', '2022-06-20'),
(109, 'Devon', 'Miles', 'devon.m@example.com', 'United States', 'New York', '2022-07-04'),
(110, 'Amina', 'Yusuf', 'amina.y@example.ae', 'United Arab Emirates', 'Dubai', '2022-07-18'),
(111, 'Oliver', 'Brown', 'oliver.b@example.co.uk', 'United Kingdom', 'Manchester', '2022-08-02'),
(112, 'Priya', 'Sharma', 'priya.s@example.in', 'India', 'Bangalore', '2022-08-15'),
(113, 'Gabriel', 'Mendoza', 'gabriel.m@example.mx', 'Mexico', 'Mexico City', '2022-09-01'),
(114, 'Chloe', 'Dubois', 'chloe.d@example.fr', 'France', 'Paris', '2022-09-22'),
(115, 'Zoe', 'Papadopoulos', 'zoe.p@example.gr', 'Greece', 'Athens', '2022-10-05'),
(116, 'Ethan', 'Hunt', 'ethan.h@example.com', 'United States', 'Austin', '2022-10-20'),
(117, 'Yuki', 'Tanaka', 'yuki.t@example.jp', 'Japan', 'Osaka', '2022-11-01'),
(118, 'Carlos', 'Valdez', 'carlos.v@example.ar', 'Argentina', 'Buenos Aires', '2022-11-15'),
(119, 'Fiona', 'Campbell', 'fiona.c@example.co.uk', 'United Kingdom', 'Edinburgh', '2022-12-01'),
(120, 'Daniel', 'Kim', 'daniel.k@example.kr', 'South Korea', 'Seoul', '2022-12-15'),
(121, 'Ananya', 'Patel', 'ananya.p@example.in', 'India', 'Mumbai', '2023-01-05'),
(122, 'Hugo', 'Larsen', 'hugo.l@example.dk', 'Denmark', 'Copenhagen', '2023-01-20'),
(123, 'Serena', 'Rossi', 'serena.r@example.it', 'Italy', 'Milan', '2023-02-10'),
(124, 'Natasha', 'Ivanova', 'natasha.i@example.com', 'United States', 'Seattle', '2023-02-28'),

-- EDGE CASES: Inactive registered customers with ZERO orders placed!
(201, 'Brandon', 'Stark', 'brandon.s@example.com', 'United States', 'Chicago', '2023-03-01'),
(202, 'Astrid', 'Lindgren', 'astrid.l@example.se', 'Sweden', 'Stockholm', '2023-03-05'),
(203, 'Tariq', 'Ziyad', 'tariq.z@example.eg', 'Egypt', 'Cairo', '2023-03-15'),
(204, 'Mei', 'Ling', 'mei.l@example.cn', 'China', 'Shanghai', '2023-03-20'),
(205, 'Kasper', 'Nielsen', 'kasper.n@example.no', 'Norway', 'Oslo', '2023-04-01'),
(206, 'Daphne', 'Bridgerton', 'daphne.b@example.co.uk', 'United Kingdom', 'Bath', '2023-04-10');

-- 3. PRODUCTS (20 Products across all categories)
INSERT INTO products (id, category_id, name, price, stock_quantity, is_active) VALUES
(501, 1, 'Pro Wireless Mechanical Keyboard', 149.99, 85, 1),
(502, 1, 'Ergonomic Precision Mouse', 79.50, 120, 1),
(503, 1, 'UltraWide 34-Inch Curved Monitor', 499.00, 30, 1),
(504, 1, 'Noise-Cancelling Studio Headphones', 249.00, 65, 1),
(505, 1, 'USB-C Thunderbolt 4 Docking Station', 189.99, 40, 1),
(506, 2, 'Adjustable Standing Desk 60x30', 420.00, 15, 1),
(507, 2, 'Ergonomic Mesh Task Chair', 299.00, 22, 1),
(508, 2, 'Smart LED Desk Lamp with Dimmer', 45.00, 150, 1),
(509, 3, 'Waterproof Breathable Rain Jacket', 120.00, 50, 1),
(510, 3, 'Merino Wool Lightweight Hoodie', 95.00, 80, 1),
(511, 3, 'Trail Running Performance Shoes', 135.00, 45, 1),
(512, 4, 'Designing Data-Intensive Applications', 44.99, 200, 1),
(513, 4, 'Database Internals: A Deep Dive', 52.50, 110, 1),
(514, 4, 'SQL Performance Explained', 39.95, 95, 1),
(515, 5, 'Adjustable Dumbbell Set (5-50 lbs)', 340.00, 18, 1),
(516, 5, 'High-Density Non-Slip Yoga Mat', 35.00, 140, 1),
(517, 5, 'Hydration Insulated Stainless Flask', 28.00, 220, 1),
(518, 6, 'Hardcover Dotted Grid Journal', 18.50, 300, 1),
(519, 6, 'Aluminum Laptop Stand Riser', 32.00, 90, 1),
(520, 1, 'Vintage Mechanical Calculator (Discontinued)', 89.00, 0, 0);

-- 4. ORDERS (35 Orders: multiple items, various statuses, varying amounts)
INSERT INTO orders (id, customer_id, order_date, total_amount, status) VALUES
(1001, 101, '2023-01-10', 648.99, 'COMPLETED'),
(1002, 102, '2023-01-14', 79.50, 'COMPLETED'),
(1003, 103, '2023-01-18', 44.99, 'COMPLETED'),
(1004, 101, '2023-01-25', 189.99, 'COMPLETED'),
(1005, 104, '2023-02-01', 578.50, 'COMPLETED'),
(1006, 105, '2023-02-05', 95.00, 'COMPLETED'),
(1007, 106, '2023-02-12', 375.00, 'COMPLETED'),
(1008, 107, '2023-02-20', 249.00, 'COMPLETED'),
(1009, 108, '2023-02-22', 137.44, 'COMPLETED'),
(1010, 101, '2023-03-01', 340.00, 'COMPLETED'),
(1011, 109, '2023-03-05', 719.00, 'COMPLETED'),
(1012, 110, '2023-03-10', 149.99, 'COMPLETED'),
(1013, 111, '2023-03-15', 82.50, 'COMPLETED'),
(1014, 102, '2023-03-18', 420.00, 'COMPLETED'),
(1015, 112, '2023-03-22', 135.00, 'COMPLETED'),
(1016, 113, '2023-03-25', 299.00, 'COMPLETED'),
(1017, 114, '2023-03-28', 120.00, 'COMPLETED'),
(1018, 103, '2023-04-01', 92.45, 'COMPLETED'),
(1019, 115, '2023-04-05', 249.00, 'COMPLETED'),
(1020, 116, '2023-04-10', 499.00, 'SHIPPED'),
(1021, 117, '2023-04-12', 149.99, 'SHIPPED'),
(1022, 104, '2023-04-15', 79.50, 'SHIPPED'),
(1023, 118, '2023-04-18', 340.00, 'SHIPPED'),
(1024, 119, '2023-04-20', 189.99, 'PENDING'),
(1025, 120, '2023-04-22', 420.00, 'PENDING'),
(1026, 121, '2023-04-25', 135.00, 'PENDING'),
(1027, 101, '2023-04-28', 77.00, 'PENDING'),
-- CANCELLED ORDERS (Edge Cases)
(1028, 122, '2023-04-29', 499.00, 'CANCELLED'),
(1029, 105, '2023-05-01', 149.99, 'CANCELLED'),
(1030, 123, '2023-05-02', 299.00, 'CANCELLED'),
-- Multiple orders by single customers for aggregation queries
(1031, 102, '2023-05-03', 95.00, 'COMPLETED'),
(1032, 104, '2023-05-04', 35.00, 'COMPLETED'),
(1033, 106, '2023-05-05', 44.99, 'COMPLETED'),
(1034, 124, '2023-05-06', 189.99, 'COMPLETED'),
(1035, 101, '2023-05-07', 52.50, 'COMPLETED');

-- 5. ORDER_ITEMS (Detailed line items per order)
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES
(1, 1001, 503, 1, 499.00),
(2, 1001, 501, 1, 149.99),
(3, 1002, 502, 1, 79.50),
(4, 1003, 512, 1, 44.99),
(5, 1004, 505, 1, 189.99),
(6, 1005, 503, 1, 499.00),
(7, 1005, 502, 1, 79.50),
(8, 1006, 510, 1, 95.00),
(9, 1007, 515, 1, 340.00),
(10, 1007, 516, 1, 35.00),
(11, 1008, 504, 1, 249.00),
(12, 1009, 513, 1, 52.50),
(13, 1009, 514, 1, 39.95),
(14, 1009, 518, 2, 22.49),
(15, 1010, 515, 1, 340.00),
(16, 1011, 507, 1, 299.00),
(17, 1011, 506, 1, 420.00),
(18, 1012, 501, 1, 149.99),
(19, 1013, 519, 1, 32.00),
(20, 1013, 517, 1, 28.00),
(21, 1013, 518, 1, 18.50),
(22, 1014, 506, 1, 420.00),
(23, 1015, 511, 1, 135.00),
(24, 1016, 507, 1, 299.00),
(25, 1017, 509, 1, 120.00),
(26, 1018, 513, 1, 52.50),
(27, 1018, 514, 1, 39.95),
(28, 1019, 504, 1, 249.00),
(29, 1020, 503, 1, 499.00),
(30, 1021, 501, 1, 149.99),
(31, 1022, 502, 1, 79.50),
(32, 1023, 515, 1, 340.00),
(33, 1024, 505, 1, 189.99),
(34, 1025, 506, 1, 420.00),
(35, 1026, 511, 1, 135.00),
(36, 1027, 516, 1, 35.00),
(37, 1027, 519, 1, 32.00),
(38, 1028, 503, 1, 499.00),
(39, 1029, 501, 1, 149.99),
(40, 1030, 507, 1, 299.00),
(41, 1031, 510, 1, 95.00),
(42, 1032, 516, 1, 35.00),
(43, 1033, 512, 1, 44.99),
(44, 1034, 505, 1, 189.99),
(45, 1035, 513, 1, 52.50);

-- 6. PAYMENTS (Some orders are paid, pending, failed, or have NO payment record)
INSERT INTO payments (id, order_id, payment_method, amount, payment_status, payment_date) VALUES
(1, 1001, 'CREDIT_CARD', 648.99, 'SUCCESSFUL', '2023-01-10'),
(2, 1002, 'APPLE_PAY', 79.50, 'SUCCESSFUL', '2023-01-14'),
(3, 1003, 'PAYPAL', 44.99, 'SUCCESSFUL', '2023-01-18'),
(4, 1004, 'CREDIT_CARD', 189.99, 'SUCCESSFUL', '2023-01-25'),
(5, 1005, 'BANK_TRANSFER', 578.50, 'SUCCESSFUL', '2023-02-01'),
(6, 1006, 'APPLE_PAY', 95.00, 'SUCCESSFUL', '2023-02-05'),
(7, 1007, 'CREDIT_CARD', 375.00, 'SUCCESSFUL', '2023-02-12'),
(8, 1008, 'PAYPAL', 249.00, 'SUCCESSFUL', '2023-02-20'),
(9, 1009, 'CREDIT_CARD', 137.44, 'SUCCESSFUL', '2023-02-22'),
(10, 1010, 'CREDIT_CARD', 340.00, 'SUCCESSFUL', '2023-03-01'),
(11, 1011, 'BANK_TRANSFER', 719.00, 'SUCCESSFUL', '2023-03-05'),
(12, 1012, 'PAYPAL', 149.99, 'SUCCESSFUL', '2023-03-10'),
(13, 1013, 'APPLE_PAY', 82.50, 'SUCCESSFUL', '2023-03-15'),
(14, 1014, 'CREDIT_CARD', 420.00, 'SUCCESSFUL', '2023-03-18'),
(15, 1015, 'PAYPAL', 135.00, 'SUCCESSFUL', '2023-03-22'),
(16, 1016, 'CREDIT_CARD', 299.00, 'SUCCESSFUL', '2023-03-25'),
(17, 1017, 'APPLE_PAY', 120.00, 'SUCCESSFUL', '2023-03-28'),
(18, 1018, 'CREDIT_CARD', 92.45, 'SUCCESSFUL', '2023-04-01'),
(19, 1019, 'PAYPAL', 249.00, 'SUCCESSFUL', '2023-04-05'),
(20, 1020, 'CREDIT_CARD', 499.00, 'SUCCESSFUL', '2023-04-10'),
(21, 1021, 'APPLE_PAY', 149.99, 'SUCCESSFUL', '2023-04-12'),
(22, 1022, 'CREDIT_CARD', 79.50, 'SUCCESSFUL', '2023-04-15'),
(23, 1023, 'BANK_TRANSFER', 340.00, 'SUCCESSFUL', '2023-04-18'),
-- Pending & Failed payments
(24, 1024, 'CREDIT_CARD', 189.99, 'PENDING', '2023-04-20'),
(25, 1025, 'BANK_TRANSFER', 420.00, 'PENDING', '2023-04-22'),
(26, 1026, 'CREDIT_CARD', 135.00, 'FAILED', '2023-04-25'),
(27, 1028, 'PAYPAL', 499.00, 'FAILED', '2023-04-29'),
(28, 1031, 'CREDIT_CARD', 95.00, 'SUCCESSFUL', '2023-05-03'),
(29, 1032, 'APPLE_PAY', 35.00, 'SUCCESSFUL', '2023-05-04'),
(30, 1033, 'PAYPAL', 44.99, 'SUCCESSFUL', '2023-05-05'),
(31, 1034, 'CREDIT_CARD', 189.99, 'SUCCESSFUL', '2023-05-06'),
(32, 1035, 'APPLE_PAY', 52.50, 'SUCCESSFUL', '2023-05-07');
-- Note: Order 1027, 1029, 1030 have NO payment row (Unpaid/Ghost orders)
"""

ECOMMERCE_DATABASE = SyntheticDatabaseBlueprint(
    id="db-ecommerce",
    name="ecommerce_db",
    display_name="Global E-Commerce & Marketplace Database",
    description="Multi-tier retail relational database modeling customers across 15 countries, product categories, transactions, multi-item checkouts, and payment gateways.",
    init_ddl=ECOMMERCE_DDL,
    seed_dml=ECOMMERCE_DML,
    tables=[
        TableInfo(
            name="categories",
            description="Product merchandising categories",
            row_count=6,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="name", type="VARCHAR(60)", nullable=False),
                ColumnInfo(name="description", type="TEXT", nullable=True),
            ],
        ),
        TableInfo(
            name="customers",
            description="Registered user profiles with international registration locations",
            row_count=30,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="first_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="last_name", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="name", type="VARCHAR(100)", nullable=False),
                ColumnInfo(name="email", type="VARCHAR(120)", nullable=False),
                ColumnInfo(name="country", type="VARCHAR(50)", nullable=False),
                ColumnInfo(name="city", type="VARCHAR(60)", nullable=False),
                ColumnInfo(name="created_at", type="DATE", nullable=False),
            ],
        ),
        TableInfo(
            name="products",
            description="Item catalog with categories, retail prices, and inventory units",
            row_count=20,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="category_id", type="INTEGER", is_foreign_key=True, references="categories.id", nullable=False),
                ColumnInfo(name="name", type="VARCHAR(150)", nullable=False),
                ColumnInfo(name="price", type="DECIMAL(10,2)", nullable=False),
                ColumnInfo(name="stock_quantity", type="INTEGER", nullable=False),
                ColumnInfo(name="is_active", type="BOOLEAN", nullable=False),
            ],
        ),
        TableInfo(
            name="orders",
            description="Purchases, total charges, order dates, and fulfillment statuses",
            row_count=35,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="customer_id", type="INTEGER", is_foreign_key=True, references="customers.id", nullable=False),
                ColumnInfo(name="order_date", type="DATE", nullable=False),
                ColumnInfo(name="total_amount", type="DECIMAL(10,2)", nullable=False),
                ColumnInfo(name="status", type="VARCHAR(20)", nullable=False),
            ],
        ),
        TableInfo(
            name="order_items",
            description="Line items for placed orders, quantities, and purchased prices",
            row_count=45,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="order_id", type="INTEGER", is_foreign_key=True, references="orders.id", nullable=False),
                ColumnInfo(name="product_id", type="INTEGER", is_foreign_key=True, references="products.id", nullable=False),
                ColumnInfo(name="quantity", type="INTEGER", nullable=False),
                ColumnInfo(name="unit_price", type="DECIMAL(10,2)", nullable=False),
            ],
        ),
        TableInfo(
            name="payments",
            description="Payment gateway records, payment methods, and clearance statuses",
            row_count=32,
            columns=[
                ColumnInfo(name="id", type="INTEGER", is_primary_key=True, nullable=False),
                ColumnInfo(name="order_id", type="INTEGER", is_foreign_key=True, references="orders.id", nullable=False),
                ColumnInfo(name="payment_method", type="VARCHAR(30)", nullable=False),
                ColumnInfo(name="amount", type="DECIMAL(10,2)", nullable=False),
                ColumnInfo(name="payment_status", type="VARCHAR(20)", nullable=False),
                ColumnInfo(name="payment_date", type="DATE", nullable=True),
            ],
        ),
    ],
)
