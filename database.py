import sqlite3

connection = sqlite3.connect("ecommerce.db")

cursor = connection.cursor()
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE categories (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
description TEXT NOT NULL
)
""")

cursor.execute("""

""")


connection.commit()

print("Database connected")

connection.close()