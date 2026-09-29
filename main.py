import psycopg
import functions
import reports
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

while True:
    print("\nMenu:")
    print("1. View all products by category")
    print("2. View all orders for a user")
    print("3. Register new user")
    print("4. Find user by email address")
    print("5. Change selected user phone number")
    print("6. Delete user")
    print("7. View admin reports")
    print("8. Exit")

    choice = input("Enter your choice (1-8): ")

    if choice == "1":
        category_id = input("Enter category ID: ")

        products = functions.get_products_by_category(
            connection,
            category_id
        )

        for product_name, category_name in products:
            print(
                f"Product: {product_name} | "
                f"Category: {category_name}"
            )

    elif choice == "2":
        user_id = input("Enter user ID: ")

        orders = functions.get_user_orders(
            connection,
            user_id
        )

        for order_id, uid, status, total, created_at in orders:
            print(
                f"Order ID: {order_id} | "
                f"Status: {status} | "
                f"Total: ${total} | "
                f"Date: {created_at}"
            )

    elif choice == "3":
        name = input("Name: ")
        email = input("Email: ")
        password_hash = input("Password: ")
        phone = input("Phone: ")

        functions.register_user(
            connection,
            name,
            email,
            password_hash,
            phone
        )

    elif choice == "4":
        email = input("Enter the email address: ")

        wanted_user = functions.get_user_by_email(
            connection,
            email
        )

        if wanted_user:
            print(wanted_user)
        else:
            print("User not found.")

    elif choice == "5":
        user = input("Enter user ID: ")
        new_number = input("Enter new phone number: ")

        updated_rows = functions.update_user_phone(
            connection,
            new_number,
            user
        )

        if updated_rows == 0:
            print("User not found.")
        else:
            print(f"Number changed to {new_number}")

    elif choice == "6":
        user = input("Enter user ID: ")

        deleted_rows = functions.delete_user(
            connection,
            user
        )

        if deleted_rows == 0:
            print("User was not deleted.")
        else:
            print(f"User {user} was deleted successfully.")
    elif choice == "7":
        print("\nAdmin Reports:")
        print("1. Orders with users")
        print("2. Top spending user")
        print("3. Best selling products")
        print("4. Total revenue")
        print("5. Users without orders")

        report_choice = input("Choose report: ")

        if report_choice == "1":
            result = reports.get_orders_with_users(connection)

            for report in result:
                print(report)

        elif report_choice == "2":
            print(reports.top_spending_user(connection))

        elif report_choice == "3":
            result = reports.best_selling_products(connection)

            for report in result:
                print(report)

        elif report_choice == "4":
            print(reports.get_total_revenue(connection))

        elif report_choice == "5":
            result = reports.get_users_without_orders(connection)

            for report in result:
                print(report)

    elif choice == "8":
        print("Exiting application. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1-8.")