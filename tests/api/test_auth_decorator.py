from flask import Flask
import jwt
from datetime import datetime, timedelta, timezone
from app.auth.decorators import require_auth, require_role
from app.services.token_service import generate_access_token
from config.settings import JWT_SECRET

def create_test_app():
    app = Flask(__name__)

    @app.get("/protected")
    @require_auth
    def protected():
        return {"message": "Access granted"}, 200

    @app.get("/admin")
    @require_auth
    @require_role("admin")
    def admin():
        return {"message" : "Admin access granted"}, 200

    return app


def test_missing_authorization_header():
    app = create_test_app()

    client = app.test_client()

    response = client.get("/protected")

    assert response.status_code == 401

    body = response.json

    assert body["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_invalid_authorization_header():
    app = create_test_app()

    client = app.test_client()

    response = client.get(
        "/protected",
        headers = {
            "Authorization" : "Basic abc123"
        }
    )

    assert response.status_code == 401

    body = response.json

    assert body ["error"]["code"] == "INVALID_AUTH_HEADER"

def test_invalid_bearer_token():
    app = create_test_app()

    client = app.test_client()

    response = client.get(
        "/protected",
        headers = {
            "Authorization" : "Bearer invalid-token"
        }
        )

    assert response.status_code == 401

    body = response.json

    assert body ["error"]["code"] == "INVALID_TOKEN"

def test_valid_bearer_token():
    app = create_test_app()

    client = app.test_client()

    token = generate_access_token(
        10,
        "jwtuser",
        "user"
    )

    response = client.get(
        "/protected",
        headers = {
            "Authorization" : f"Bearer {token}"

        }
    )

    assert response.status_code == 200

    body = response.json

    assert body ["message"] == "Access granted"


def test_user_cannot_access_admin_endpoint():
    app = create_test_app()
    client = app.test_client()

    token = generate_access_token(
        10, "jwtuser", "user"
    )

    response = client.get(
        "/admin",
        headers = {
            "Authorization" : f"Bearer {token}"
        }
    )

    assert response.status_code == 403

    body = response.json

    assert body["error"]["code"] == "FORBIDDEN"


def test_admin_can_access_admin_endpoint():
    app = create_test_app()
    client = app.test_client()

    token = generate_access_token(
        11, "adminuser", "admin"
    )

    response = client.get(
        "/admin",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    body = response.json
    assert body ["message"] == "Admin access granted"

def test_expired_bearer_token():
    app = create_test_app()

    client = app.test_client()

    expired_payload = {
        "sub" : "10",
        "username": "jwtuser",
        "role" : "user",
        "exp" : datetime.now(timezone.utc) - timedelta(minutes=1)
    }

    token = jwt.encode(
        expired_payload,
        JWT_SECRET,
        algorithm = 'HS256'
    )

    response = client.get(
        "/protected",
        headers = {
            "Authorization" : f"Bearer {token}"
        }
    )

    assert response.status_code == 401
    body = response.json
    assert body["error"]["code"] == "INVALID_TOKEN"
