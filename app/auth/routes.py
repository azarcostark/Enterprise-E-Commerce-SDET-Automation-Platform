from flask import Blueprint, request
from app.services.token_service import generate_access_token
from app.services.auth_service import authenticate_user
from app.errors.handlers import error_response

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix = "/api/auth"
)

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)

    if not data:
        return error_response(
            "VALIDATION_FAILED",
            "Username and password are required.",
            400
        )
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error_response(
            "VALIDATION_FAILED",
            "Username and password are required",
            400
        )

    user = authenticate_user(username, password)

    if user is None:
        return error_response(
            "INVALID_CREDENTIALS",
            "Invalid username or password.",
            401
        )

    access_token = generate_access_token(
        user["id"],
        user["username"],
        user["role"]
    )

    return{
        "message" : "Login successful",
        "access_token": access_token,
        "user": {
            "id" : user ["id"],
            "username" : user["username"]
        }

    }, 200
