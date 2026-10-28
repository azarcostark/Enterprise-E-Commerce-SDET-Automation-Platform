import pytest
import requests
import logging
import json

from framework.clients.api_client import APIClient
from framework.exceptions.api_exceptions import (
    APIConnectionError,
    APITimeoutError
)


def test_api_client_connection_error():
    client = APIClient("http://127.0.0.1:5000")

    def fake_request(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Server unavailable")

    client.session.request = fake_request

    with pytest.raises(APIConnectionError):
        client.get("/api/products/1")


def test_api_client_timeout():
    client = APIClient("http://127.0.0.1:5000")

    def fake_request(*args, **kwargs):
        raise requests.exceptions.Timeout("Request timed out")

    client.session.request = fake_request

    with pytest.raises(APITimeoutError):
        client.get("/api/products/1")

def test_api_client_post_request():
    client = APIClient("http://127.0.0.1:5000")
    captured = {}

    def fake_request(*args, **kwargs):
        captured["method"] = kwargs["method"]
        captured["url"] = kwargs["url"]
        captured["timeout"] = kwargs["timeout"]
        captured["json"] = kwargs["json"]

        return requests.Response()

    client.session.request = fake_request

    test_data = {
        "name": "Test Product",
        "price": 100
    }

    client.post(
        "/api/products",
        json = test_data
    )


    assert captured["method"] == "POST"
    assert captured["url"] == "http://127.0.0.1:5000/api/products"
    assert captured["timeout"] == 10
    assert captured["json"] == test_data


def test_api_client_default_headers():
    client = APIClient("http://127.0.0.1")

    assert client.session.headers["Content-Type"] == "application/json"
    assert client.session.headers["Accept"] == "application/json"


def test_api_client_custom_timeout():
    client = APIClient(
        "http://127.0.0.1:5000",
        timeout=30
    )

    captured = {}

    def fake_request(*args, **kwargs):
        captured["timeout"] = kwargs["timeout"]
        return requests.Response()

    client.session.request = fake_request

    client.get("/api/products")

    assert captured["timeout"] == 30


def test_api_client_patch_request():
    client = APIClient("http://127.0.0.1:5000")

    captured = {}

    def fake_request(*args, **kwargs):
        captured["method"] = kwargs["method"]
        captured["url"] = kwargs["url"]
        captured["json"] = kwargs.get("json")

        return requests.Response()

    client.session.request = fake_request

    test_data = {
        "price": 899.99
    }

    client.patch(
        "/api/products/1",
        json=test_data
    )

    assert captured["method"] == "PATCH"
    assert captured["url"] == "http://127.0.0.1:5000/api/products/1"
    assert captured["json"] == test_data


def test_api_client_delete_request():
    client = APIClient("http://127.0.0.1:5000")

    captured = {}

    def fake_request(*args, **kwargs):
        captured["method"] = kwargs["method"]
        captured["url"] = kwargs["url"]

        return requests.Response()

    client.session.request = fake_request
    client.delete("/api/products/123")

    assert captured["method"] == "DELETE"
    assert captured["url"] == "http://127.0.0.1:5000/api/products/123"


def test_api_client_redacts_password_in_request_logs(caplog):
    client = APIClient("https://127.0.0.1:5000")

    def fake_request(*args, **kwargs):
        return requests.Response()

    client.session.request = fake_request

    test_data = {
        "username": "Vipul",
        "password" : "super-secret-password"
    }

    with caplog.at_level(logging.INFO, logger="APIClient"):
        client.post(
            "/api/auth/login",
            json = test_data
        )

    assert "super-secret-password" not in caplog.text
    assert "***REDACTED***" in caplog.text


def test_api_client_redacts_access_token_in_response_logs(caplog):
    client = APIClient("https://127.0.0.0.1:5000")


    mock_response = requests.Response()

    mock_response.status_code = 200


    response_data = {
    "access_token": "super-secret-token",
    "status": "success"

}
    mock_response._content = json.dumps(response_data).encode("utf-8")


    def fake_request(*args, **kwargs):
        return mock_response

    client.session.request = fake_request

    with caplog.at_level(logging.INFO, logger="APIClient"):
        client.get("/api/auth.login")

    assert "super-secret-token" not in caplog.text
    assert "***REDACTED***" in caplog.text
    assert "success" in caplog.text

def test_api_client_handles_invalid_json_response(caplog):
    client = APIClient("https://127.0.0.1:5000")

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b"This is not valid JSON"

    def fake_request(*args, **kwargs):
        return mock_response

    client.session.request = fake_request

    with caplog.at_level(logging.INFO, logger="APIClient"):
        response = client.get("/api/products")

    assert response.status_code == 200
    assert "[Response body omitted: invalid JSON]" in caplog.text
    assert "This is not valid JSON" not in caplog.text
