from functools import wraps

import jwt
from flask import request

from config.settings import JWT_SECRET
from app.errors.handlers import error_response


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return error_response(
                "AUTHENTICATION_REQUIRED",
                "Authorization header is required.",
                401
            )

        if not auth_header.startswith("Bearer "):
            return error_response(
                "INVALID_AUTH_HEADER",
                "Authorization header must use Bearer token.",
                401
            )

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            return error_response(
                "INVALID_TOKEN",
                "Invalid or expired token.",
                401
            )

        request.user = payload

        return f(*args, **kwargs)

    return decorated_function

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = request.user.get("role")

            if user_role != required_role:
                return error_response(
                    "FORBIDDEN",
                    "You do not have the permission to perform this action.",
                    403
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator
