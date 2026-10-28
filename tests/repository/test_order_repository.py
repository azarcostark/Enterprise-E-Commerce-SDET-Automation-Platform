
import uuid

import pytest

from app.database.connection import get_connection
from app.repositories.product_repository import create_product
from app.repositories.user_repository import create_user
from app.repositories.order_repository import create_order, delete_order


@pytest.fixture
def order_test_data():
    # Unique username prevents collisions with previous test runs.
    username = f"order_test_{uuid.uuid4().hex}"

    user_id = None
    product_ids = []
    order_ids = []

    try:
        user_id = create_user(username, "testpassword")

        product_id_1 = create_product(
            "Order Test Product 1",
            99.99
        )
        product_ids.append(product_id_1)

        product_id_2 = create_product(
            "Order Test Product 2",
            49.99
        )
        product_ids.append(product_id_2)

        yield {
            "user_id": user_id,
            "product_id_1": product_id_1,
            "product_id_2": product_id_2,
            "created_order_ids": order_ids,
        }

    finally:
        # Delete orders and their items first.
        for order_id in order_ids:
            delete_order(order_id)

        # Then remove the test user and products.
        connection = get_connection()

        try:
            if user_id is not None:
                connection.execute(
                    "DELETE FROM users WHERE id = ?",
                    (user_id,)
                )

            for product_id in product_ids:
                connection.execute(
                    "DELETE FROM products WHERE id = ?",
                    (product_id,)
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()


def test_create_order(order_test_data):
    order_id = create_order(
        order_test_data["user_id"],
        [
            {
                "product_id": order_test_data["product_id_1"],
                "quantity": 2,
                "unit_price": 99.99,
            }
        ],
    )

    order_test_data["created_order_ids"].append(order_id)

    assert isinstance(order_id, int)
    assert order_id > 0

    connection = get_connection()

    try:
        order = connection.execute(
            """
            SELECT id, user_id, status
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        ).fetchone()

        order_item = connection.execute(
            """
            SELECT order_id, product_id, quantity, unit_price
            FROM order_items
            WHERE order_id = ?
            """,
            (order_id,),
        ).fetchone()

    finally:
        connection.close()

    assert order is not None
    assert order["user_id"] == order_test_data["user_id"]
    assert order["status"] == "pending"

    assert order_item is not None
    assert order_item["product_id"] == order_test_data["product_id_1"]
    assert order_item["quantity"] == 2
    assert order_item["unit_price"] == 99.99


def test_create_order_with_multiple_items(order_test_data):
    order_id = create_order(
        order_test_data["user_id"],
        [
            {
                "product_id": order_test_data["product_id_1"],
                "quantity": 2,
                "unit_price": 99.99,
            },
            {
                "product_id": order_test_data["product_id_2"],
                "quantity": 3,
                "unit_price": 49.99,
            },
        ],
    )

    order_test_data["created_order_ids"].append(order_id)

    connection = get_connection()

    try:
        order_items = connection.execute(
            """
            SELECT order_id, product_id, quantity, unit_price
            FROM order_items
            WHERE order_id = ?
            ORDER BY id
            """,
            (order_id,),
        ).fetchall()

    finally:
        connection.close()

    assert len(order_items) == 2

    assert order_items[0]["order_id"] == order_id
    assert order_items[0]["product_id"] == order_test_data["product_id_1"]
    assert order_items[0]["quantity"] == 2
    assert order_items[0]["unit_price"] == 99.99

    assert order_items[1]["order_id"] == order_id
    assert order_items[1]["product_id"] == order_test_data["product_id_2"]
    assert order_items[1]["quantity"] == 3
    assert order_items[1]["unit_price"] == 49.99


def test_delete_order(order_test_data):
    order_id = create_order(
        order_test_data["user_id"],
        [
            {
                "product_id": order_test_data["product_id_1"],
                "quantity": 2,
                "unit_price": 99.99,
            }
        ],
    )

    order_test_data["created_order_ids"].append(order_id)

    delete_order(order_id)

    connection = get_connection()

    try:
        order = connection.execute(
            "SELECT * FROM orders WHERE id = ?",
            (order_id,),
        ).fetchone()

        order_item = connection.execute(
            "SELECT * FROM order_items WHERE order_id = ?",
            (order_id,),
        ).fetchone()

    finally:
        connection.close()

    assert order is None
    assert order_item is None
