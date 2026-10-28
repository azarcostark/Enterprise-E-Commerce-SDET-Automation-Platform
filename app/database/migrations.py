from app.database.connection import get_connection

def add_user_role_column():
    connection = get_connection()

    connection.execute(
        """ALTER TABLE users
        ADD COLUMN role TEXT NOT NULL DEFAULT 'user'
        """
    )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    add_user_role_column()
    print("User role column added successfully.")
