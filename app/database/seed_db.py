
from app.database.connection import get_connection


SEED_PRODUCTS = [
    {"name": "Wireless Mouse", "price": 24.99},
    {"name": "Mechanical Keyboard", "price": 79.99},
    {"name": "USB-C Hub", "price": 39.99},
]


def seed_products():
    connection = get_connection()

    try:
        for product in SEED_PRODUCTS:
            connection.execute(
                """
                INSERT INTO products (name, price)
                VALUES (?, ?)
                """,
                (product["name"], product["price"])
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    seed_products()
    print("Products seeded successfully.")
