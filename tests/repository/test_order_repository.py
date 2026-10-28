import pytest

from app.database.connection import get_connection
from app.repositories.product_repository import create_product
from app.repositories.user_repository import create_user
from app.repositories.order_repository import create_order, delete_order



@pytest.fixture
def order_test_data():
    username = "order_test_user"
    password = "testpassword"

    user_id = create_user(username, password)

    product_id_1 = create_product(
        "Order Test Product 1",
        99.99
    )

    product_id_2 = create_product(
        "Order Test Product 2",
        49.99
    )

    created_order_ids = []

    yield {
        "user_id": user_id,
        "product_id_1": product_id_1,
        "product_id_2" : product_id_2,
        "created_order_ids": created_order_ids
    }



    for order_id in created_order_ids:
        delete_order(order_id)

    connection = get_connection()

    try :
        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        connection.execute(
            "DELETE FROM products WHERE id IN (?, ?)",
            (product_id_1, product_id_2)
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
                "unit_price": 99.99
            }
        ]
    )

    order_test_data["created_order_ids"].append(order_id)

    assert isinstance(order_id, int)
    assert order_id > 0

    connection = get_connection()

    order = connection.execute(
        """
        SELECT id, user_id, status
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    order_item = connection.execute(
        """
        SELECT order_id, product_id, quantity, unit_price
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchone()

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
                "product_id" : order_test_data["product_id_1"],
                "quantity" : 2,
                "unit_price" : 99.99
            },
            {
                "product_id" : order_test_data["product_id_2"],
                "quantity" : 3,
                "unit_price" : 49.99
            }
        ]
    )

    order_test_data["created_order_ids"].append(order_id)

    connection = get_connection()

    order_items = connection.execute(
        """
        SELECT order_id, product_id, quantity, unit_price
        FROM order_items
        WHERE order_id = ?
        ORDER BY id
        """,
        (order_id,)
    ).fetchall()

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
                "product_id" : order_test_data["product_id_1"],
                "quantity" : 2,
                "unit_price" : 99.99
            }
        ]
    )

    connection = get_connection()
    delete_order(order_id)

    result = connection.execute(
        """
        SELECT * FROM orders WHERE id = ?
        """,
        (order_id, )
    ).fetchone()

    assert result is None

    result = connection.execute(
        """
        SELECT * FROM order_items WHERE order_id = ?
        """, (order_id,)
    ).fetchone()

    assert result is None

    connection.close()
