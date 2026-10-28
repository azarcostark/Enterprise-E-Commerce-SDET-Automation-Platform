from app.database.connection import get_connection
from app.product_data import PRODUCTS


def seed_products():
    connection = get_connection()

    for product in PRODUCTS:
        connection.execute(
            """
            INSERT INTO products (name, price)
            VALUES (?, ?)
            """,
            (product["name"], product["price"])
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    seed_products()
    print("Products seeded successfully.")
