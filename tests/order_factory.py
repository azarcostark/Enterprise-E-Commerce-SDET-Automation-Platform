from app.database.connection import get_connection

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
