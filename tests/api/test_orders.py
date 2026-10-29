
def test_create_order_item_missing_product_id(authenticated_api_client):
    response = authenticated_api_client.post(
        "/api/orders",
        json={"items": [{"quantity": 1}]},
    )

    assert response.status_code == 400


def test_create_order_item_missing_quantity(
    authenticated_api_client,
    product_factory,
):
    product_response = product_factory(
        {"name": "Validation Test Product", "price": 19.99}
    )
    product_id = product_response.json()["id"]

    response = authenticated_api_client.post(
        "/api/orders",
        json={"items": [{"product_id": product_id}]},
    )

    assert response.status_code == 400


def test_create_order_item_not_an_object(authenticated_api_client):
    response = authenticated_api_client.post(
        "/api/orders",
        json={"items": ["invalid-item"]},
    )

    assert response.status_code == 400
