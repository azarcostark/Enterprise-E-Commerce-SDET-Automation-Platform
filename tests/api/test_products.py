import pytest

from framework.endpoints.product_endpoints import ProductEndpoints
from framework.utilities.schema_validator import validate_schema

from test_data.product_data import (
    get_valid_product,
    UPDATE_PRODUCT,
    DELETE_TEST_PRODUCT,
    INVALID_PRODUCT_CASES
)


def test_get_product(api_client, product_factory):

    create_response = product_factory(
        get_valid_product()
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]
    response = api_client.get(
        ProductEndpoints.by_id(product_id)
    )

    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id

    validate_schema(
        product,
        "schemas/product_schema.json"
    )


def test_get_product_details(api_client, product_factory):

    product_data = get_valid_product()
    create_response = product_factory(
        product_data
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]
    response = api_client.get(
        ProductEndpoints.by_id(product_id)
    )

    assert response.status_code == 200

    product = response.json()
    assert product["id"] == product_id
    assert "name" in product
    assert "price" in product


@pytest.mark.parametrize(
    "product_id, expected_error_code",
    [
        (0, "PRODUCT_NOT_FOUND"),
        (-1, "RESOURCE_NOT_FOUND"),
        (9999, "PRODUCT_NOT_FOUND"),
        (100000, "PRODUCT_NOT_FOUND"),
    ]
)
def test_get_product_not_found(
    api_client,
    product_id,
    expected_error_code
):
    response = api_client.get(
        ProductEndpoints.by_id(product_id)
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == expected_error_code


def test_create_product(product_factory):

    product_data = get_valid_product()

    response = product_factory(
        product_data
    )

    assert response.status_code == 201

    created_product = response.json()

    assert created_product["name"] == product_data["name"]
    assert created_product["price"] == product_data["price"]
    assert "id" in created_product


@pytest.mark.parametrize(
    "product_data",
    INVALID_PRODUCT_CASES,
    ids=[
        "invalid_name_valid_price",
        "valid_name_invalid_price",
        "invalid_name_invalid_price",
        "missing_name_valid_price",
        "valid_name_missing_price"
    ]
)

def test_create_product_invalid_data(
    admin_api_client,
    product_data
):
    response = admin_api_client.post(
        ProductEndpoints.BASE,
        json=product_data
    )

    assert response.status_code == 400

    body = response.json()

    assert body["error"]["code"] == "VALIDATION_FAILED"


def test_update_product(
    admin_api_client,
    product_factory
):

    product_data = get_valid_product()
    create_product = product_factory(
        product_data
    )

    assert create_product.status_code == 201

    product_id = create_product.json()["id"]

    response = admin_api_client.put(
        ProductEndpoints.by_id(product_id),
        json=UPDATE_PRODUCT
    )

    assert response.status_code == 200

    updated_product = response.json()

    assert updated_product["id"] == product_id
    assert updated_product["name"] == UPDATE_PRODUCT["name"]
    assert updated_product["price"] == UPDATE_PRODUCT["price"]


def test_update_product_not_found(admin_api_client):
    response = admin_api_client.put(
        ProductEndpoints.by_id(9999),
        json=UPDATE_PRODUCT
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_delete_product(admin_api_client):
    create_response = admin_api_client.post(
        ProductEndpoints.BASE,
        json=DELETE_TEST_PRODUCT
    )

    assert create_response.status_code == 201

    created_product = create_response.json()
    product_id = created_product["id"]

    delete_response = admin_api_client.delete(
        ProductEndpoints.by_id(product_id)
    )

    assert delete_response.status_code == 204

    get_response = admin_api_client.get(
        ProductEndpoints.by_id(product_id)
    )

    assert get_response.status_code == 404


def test_delete_product_not_found(admin_api_client):
    response = admin_api_client.delete(
        ProductEndpoints.by_id(9999)
    )

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "PRODUCT_NOT_FOUND"
