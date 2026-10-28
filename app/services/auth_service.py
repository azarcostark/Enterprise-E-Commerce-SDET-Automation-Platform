from werkzeug.security import check_password_hash

from app.repositories.user_repository import get_user_by_username


def authenticate_user(username, password):
    user = get_user_by_username(username)

    if user is None:
        return None

    if not check_password_hash(user["password"], password):
        return None

    return user
