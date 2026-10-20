import psycopg
from datetime import date


def get_all_products(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, price
        FROM products;
    """)

    products = cursor.fetchall()

    return products


def create_product(connection, name, price):
    cursor = connection.cursor()

    created_at = date.today().isoformat()

    cursor.execute("""
        INSERT INTO products (
            name,
            price,
            created_at
        )
        VALUES (%s, %s, %s)
    """, (
        name,
        price,
        created_at
    ))

    connection.commit()

def delete_product(connection, product_id):
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM products
    WHERE id = %s
    """,(product_id,))
    connection.commit()
    return cursor.rowcount
    
def get_products_by_category(connection, category_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.name,
            c.name
        FROM products p
        JOIN categories c
            ON p.category_id = c.id
        WHERE c.id = %s
    """, (category_id,))

    return cursor.fetchall()


def get_user_orders(connection, user_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE user_id = %s
    """, (user_id,))

    return cursor.fetchall()


def register_user(connection, name, email, password_hash, phone):
    cursor = connection.cursor()

    created_at = date.today().isoformat()

    try:
        cursor.execute("""
            INSERT INTO users (
                name,
                email,
                password_hash,
                phone,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            name,
            email,
            password_hash,
            phone,
            created_at
        ))

        connection.commit()

        print("User registered successfully.")

    except psycopg.IntegrityError:
        connection.rollback()

        print("This email already exists. Please log in instead.")


def get_user_by_email(connection, email):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = %s
    """, (email,))

    return cursor.fetchone()


def update_user_phone(connection, new_phone, user_id):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET phone = %s
        WHERE id = %s
    """, (
        new_phone,
        user_id
    ))

    connection.commit()

    return cursor.rowcount


def delete_user(connection, user_id):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM users
            WHERE id = %s
        """, (user_id,))

        connection.commit()

        return cursor.rowcount

    except psycopg.IntegrityError:
        connection.rollback()

        print("Cannot delete this user because they have related orders.")

        return 0


def create_order(connection, user_id, items):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cursor.fetchone()

    if user is None:
        print("This user does not exist.")
        return None

    total_amount = 0

    for product_id, quantity in items:
        cursor.execute("""
            SELECT name, price
            FROM products
            WHERE id = %s
        """, (product_id,))

        product = cursor.fetchone()

        if product is None:
            print("This product does not exist.")
            return None

        name, price = product

        subtotal = price * quantity
        total_amount += subtotal

    created_at = date.today().isoformat()

    try:
        cursor.execute("""
            INSERT INTO orders (
                user_id,
                status,
                total_amount,
                created_at
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            user_id,
            "pending",
            total_amount,
            created_at
        ))

        order_id = cursor.fetchone()[0]

        for product_id, quantity in items:
            cursor.execute("""
                SELECT price
                FROM products
                WHERE id = %s
            """, (product_id,))

            price = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO order_items (
                    order_id,
                    product_id,
                    quantity,
                    price_at_purchase
                )
                VALUES (%s, %s, %s, %s)
            """, (
                order_id,
                product_id,
                quantity,
                price
            ))

        connection.commit()

        return order_id

    except psycopg.IntegrityError:
        connection.rollback()

        print("Order creation failed.")

        return None