
from functools import wraps

import jwt
from flask import request

from config.settings import JWT_SECRET
from app.errors.handlers import error_response


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        parts = auth_header.split()

        if not parts:
            return error_response(
                "AUTHENTICATION_REQUIRED",
                "Authorization header is required.",
                401
            )

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return error_response(
                "INVALID_AUTH_HEADER",
                "Authorization header must use Bearer token.",
                401
            )

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"],
                options={
                    "require": ["exp", "sub", "username", "role"]
                }
            )

            if (
                not isinstance(payload["sub"], str)
                or not payload["sub"]
                or not isinstance(payload["username"], str)
                or not payload["username"]
                or payload["role"] not in ("user", "admin")
            ):
                raise jwt.InvalidTokenError(
                    "Required token claims are invalid."
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
