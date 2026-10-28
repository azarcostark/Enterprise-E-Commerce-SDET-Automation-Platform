import jwt
from datetime import datetime, timedelta, timezone

from config.settings import JWT_SECRET, JWT_EXPIRATION_MINUTES


def generate_access_token(user_id, username, role):
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm="HS256"
    )
