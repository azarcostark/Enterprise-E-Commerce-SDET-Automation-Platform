
import uuid

import pytest

from framework.clients.api_client import APIClient
from app.repositories.user_repository import create_user, delete_user
from app.repositories.order_repository import delete_order


@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000"


@pytest.fixture
def api_client(base_url):
    return APIClient(base_url)


@pytest.fixture
def user_factory():
    created_user_ids = []

    def create_test_user(username, password, role="user"):
        user_id = create_user(username, password, role)
        created_user_ids.append(user_id)
        return user_id

    try:
        yield create_test_user
    finally:
        for user_id in created_user_ids:
            delete_user(user_id)


@pytest.fixture
def order_cleanup(product_factory, user_factory):
    # Keep these dependencies so orders are deleted before
    # their related products and users are cleaned up.
    created_order_ids = []

    def register_order(order_id):
        created_order_ids.append(order_id)

    try:
        yield register_order
    finally:
        for order_id in created_order_ids:
            delete_order(order_id)


@pytest.fixture
def auth_token(api_client, user_factory):
    username = f"product_test_user_{uuid.uuid4().hex}"
    password = "testpassword"

    user_factory(username, password)

    response = api_client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def admin_auth_token(api_client, user_factory):
    username = f"product_test_admin_{uuid.uuid4().hex}"
    password = "testpassword"

    user_factory(username, password, "admin")

    response = api_client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def admin_api_client(base_url, admin_auth_token):
    client = APIClient(base_url)
    client.set_auth_token(admin_auth_token)
    return client


@pytest.fixture
def authenticated_api_client(base_url, auth_token):
    client = APIClient(base_url)
    client.set_auth_token(auth_token)
    return client


@pytest.fixture
def product_factory(admin_api_client):
    created_product_ids = []

    def create_product(product_data):
        response = admin_api_client.post(
            "/api/products",
            json=product_data,
        )

        if response.status_code == 201:
            product_id = response.json()["id"]
            created_product_ids.append(product_id)

        return response

    try:
        yield create_product
    finally:
        for product_id in created_product_ids:
            response = admin_api_client.delete(
                f"/api/products/{product_id}"
            )

            if response.status_code not in (204, 404):
                raise AssertionError(
                    "Product cleanup failed for "
                    f"id={product_id}: "
                    f"HTTP {response.status_code}"
                )


@pytest.fixture
def order_factory():
    from app.repositories.order_repository import (
        create_order,
        delete_order,
    )

    created_order_ids = []

    def create_test_order(user_id, items):
        order_id = create_order(user_id, items)
        created_order_ids.append(order_id)
        return order_id

    try:
        yield create_test_order
    finally:
        for order_id in created_order_ids:
            delete_order(order_id)
