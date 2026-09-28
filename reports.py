def get_orders_with_users(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            orders.id,
            users.name,
            orders.status,
            orders.total_amount,
            orders.created_at
        FROM orders
        JOIN users
        ON users.id = orders.user_id
    """)

    return cursor.fetchall()

def top_spending_user(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            users.name,
            SUM(orders.total_amount) AS total_spent
        FROM orders
        JOIN users
            ON users.id = orders.user_id
        GROUP BY users.id, users.name
        ORDER BY total_spent DESC
        LIMIT 1
    """)

    return cursor.fetchone()


def best_selling_products(connection):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT 
    products.name,
    SUM(order_items.quantity * order_items.price_at_purchase) AS revenue
    FROM order_items
    JOIN products
    ON order_items.product_id = products.id
    GROUP BY products.id, products.name
    ORDER BY revenue DESC
""")

    return cursor.fetchall()
    
def get_total_revenue(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT SUM(total_amount) AS total_revenue
        FROM orders
""")

    return cursor.fetchone()
def get_users_without_orders(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT users.name
        FROM users
        LEFT JOIN orders
            ON orders.user_id = users.id
        WHERE orders.id IS NULL
    """)

    return cursor.fetchall()