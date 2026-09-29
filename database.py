import psycopg
import reports
import functions

# =========================================================
# DATABASE CONNECTION
# =========================================================

connection = sqlite3.connect("ecommerce.db")
connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()


# =========================================================
# CREATE TABLES
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT,
    created_at DATE NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    category_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    created_at DATE NOT NULL,

    FOREIGN KEY (category_id)
        REFERENCES categories(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    status TEXT NOT NULL,
    total_amount INTEGER NOT NULL,
    created_at DATE NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price_at_purchase INTEGER NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(id),

    FOREIGN KEY (product_id)
        REFERENCES products(id)
)
""")


# =========================================================
# SAMPLE DATA
# =========================================================

cursor.execute("""
INSERT OR IGNORE INTO users (
    id,
    name,
    email,
    password_hash,
    phone,
    created_at
)
VALUES
    (1, 'amir', 'amir@gmail.com', 'hash1234', '09123455541', '2026-07-28'),
    (2, 'silvana', 'silvana@gmail.com', 'hash1234', '09123785541', '2026-07-14'),
    (3, 'bane', 'bane@gmail.com', 'hash1234', '09113945541', '2026-04-08'),
    (4, 'kane', 'kane@gmail.com', 'hash1234', '09136905541', '2026-06-15'),
    (5, 'sara', 'sara@gmail.com', 'hash1234', '09142295541', '2026-06-03')
""")


cursor.execute("""
INSERT OR IGNORE INTO categories (
    id,
    name,
    description
)
VALUES
    (1, 'Electronics', 'Electronic devices and accessories'),
    (2, 'Computers', 'Computers and computer accessories'),
    (3, 'Toys', 'Toys and entertainment products'),
    (4, 'Luggage', 'Travel bags and luggage'),
    (5, 'Fashion', 'Clothing and fashion products')
""")


cursor.execute("""
INSERT OR IGNORE INTO products (
    id,
    category_id,
    name,
    description,
    price,
    created_at
)
VALUES
    (1, 1, 'Canon Camera', 'Professional digital camera', 2500, '2026-01-19'),
    (2, 1, 'Sony Camera', 'Mirrorless digital camera', 3200, '2026-02-10'),
    (3, 2, 'Razer PC', 'Gaming desktop computer', 4500, '2026-03-29'),
    (4, 2, 'Mechanical Keyboard', 'RGB mechanical keyboard', 150, '2026-04-19'),
    (5, 3, 'Remote Car', 'Remote controlled toy car', 80, '2026-05-06'),
    (6, 3, 'Chess Set', 'Wooden chess set', 60, '2026-05-18'),
    (7, 4, 'Carry On', 'Small travel suitcase', 180, '2026-06-26'),
    (8, 4, 'Travel Backpack', 'Large travel backpack', 120, '2026-07-02'),
    (9, 5, 'Winter Coat', 'Warm winter coat', 200, '2026-07-08'),
    (10, 5, 'Sneakers', 'Casual everyday sneakers', 140, '2026-07-15')
""")


cursor.execute("""
INSERT OR IGNORE INTO orders (
    id,
    user_id,
    status,
    total_amount,
    created_at
)
VALUES
    (1, 1, 'pending', 2650, '2026-08-01'),
    (2, 2, 'processing', 4700, '2026-08-03'),
    (3, 3, 'shipped', 240, '2026-08-05'),
    (4, 4, 'delivered', 260, '2026-08-07'),
    (5, 5, 'cancelled', 3200, '2026-08-09'),
    (6, 1, 'delivered', 530, '2026-08-11'),
    (7, 2, 'processing', 200, '2026-08-13'),
    (8, 3, 'pending', 4580, '2026-08-15')
""")


cursor.execute("""
INSERT OR IGNORE INTO order_items (
    id,
    order_id,
    product_id,
    quantity,
    price_at_purchase
)
VALUES
    (1, 1, 1, 1, 2500),
    (2, 1, 4, 1, 150),
    (3, 2, 3, 1, 4500),
    (4, 2, 4, 1, 150),
    (5, 2, 6, 1, 60),
    (6, 3, 7, 1, 180),
    (7, 3, 8, 1, 120),
    (8, 3, 6, 1, 60),
    (9, 4, 9, 1, 200),
    (10, 4, 10, 1, 140),
    (11, 5, 2, 1, 3200),
    (12, 6, 7, 1, 180),
    (13, 6, 8, 2, 120),
    (14, 6, 6, 2, 60),
    (15, 7, 9, 1, 200),
    (16, 8, 3, 1, 4500),
    (17, 8, 6, 1, 60),
    (18, 8, 5, 1, 80)
""")

connection.commit()

# =========================================================
# CLOSE DATABASE
# =========================================================

connection.close()
