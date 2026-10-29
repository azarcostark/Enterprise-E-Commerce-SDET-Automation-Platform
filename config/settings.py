import os

JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET environment variable is not configured."
    )

JWT_EXPIRATION_MINUTES = 30
