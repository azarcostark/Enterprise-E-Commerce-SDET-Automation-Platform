from app.database.connection import get_connection

def create_order(user_id, items):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO orders (user_id)
            VALUES(?)
            """,
            (user_id,)
        )

        order_id = cursor.lastrowid

        for item in items:
            connection.execute(
                """
                INSERT INTO order_items(
                order_id,
                product_id,
                quantity,
                unit_price
                )
                VALUES(?, ?, ?, ?)
                """,


            (
                order_id,
                item["product_id"],
                item["quantity"],
                item["unit_price"]
            )
        )

        connection.commit()

        return order_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def delete_order(order_id):
    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM order_items WHERE order_id = ?

            """,
            (order_id,)
        )

        connection.execute(
            """
            DELETE FROM orders WHERE id = ?
            """,
            (order_id,)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
