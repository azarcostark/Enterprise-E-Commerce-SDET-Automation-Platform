from app.database.connection import get_connection

def get_all_products():

    connection = get_connection()

    try:
        rows = connection.execute(
            """SELECT id, name, price FROM products"""
        ).fetchall()

    finally:
        connection.close()

    return [dict(row) for row in rows]

def get_product_by_id(product_id):

    connection = get_connection()

    try:

        row = connection.execute(
            "SELECT id, name, price FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

    finally:

        connection.close()

    if row is None:
        return None
    return dict(row)

def create_product(name, price):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO products (name, price)
            VALUES (?, ?)
            """,
            (name, price)
        )

        connection.commit()

        product_id = cursor.lastrowid
    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


    return product_id

def update_product(product_id, name, price):
    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            UPDATE PRODUCTS
            SET name = ?, price = ?
            WHERE id = ?
            """,
            (name, price, product_id)
        )

        connection.commit()

        rows_update = cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return rows_update

def delete_product(product_id):
    connection = get_connection()

    try:

        cursor = connection.execute(
            """DELETE FROM products WHERE id = ?""",
            (product_id,)
        )

        connection.commit()
        rows_deleted = cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return rows_deleted
