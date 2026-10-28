from werkzeug.security import generate_password_hash

from app.database.connection import get_connection


def get_user_by_username(username):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, username, password, role
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def create_user(username, password, role="user"):

    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:

        cursor = connection.execute(
        """
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, role)
        )

        connection.commit()

        user_id = cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return user_id



def delete_user(user_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """DELETE FROM users WHERE id = ?""",
            (user_id,)
        )

        connection.commit()
        rows_deleted = cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return rows_deleted
