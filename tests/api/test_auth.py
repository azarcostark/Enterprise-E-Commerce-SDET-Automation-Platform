import pytest


def test_login_success(api_client, user_factory):
    user_factory("test_login_user", "testpassword")

    response = api_client.post(
        "/api/auth/login",
        json={
            "username": "test_login_user",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Login successful"
    assert body["user"]["username"] == "test_login_user"
    assert "id" in body["user"]


def test_login_invalid_password(api_client, user_factory):
    user_factory("test_wrong_password", "testpassword")

    response = api_client.post(
        "/api/auth/login",
        json={
            "username": "test_wrong_password",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_unknown_user(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={
            "username": "doesnotexist",
            "password": "testpassword"
        }
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.parametrize(
    "login_data",
    [
        {},
        {"username": "testuser"},
        {"password": "testpassword"},
    ]
)
def test_login_missing_credentials(api_client, login_data):
    response = api_client.post(
        "/api/auth/login",
        json=login_data
    )

    assert response.status_code == 400

    body = response.json()

    assert body["error"]["code"] == "VALIDATION_FAILED"
