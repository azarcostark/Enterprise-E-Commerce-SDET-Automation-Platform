from app.database.connection import get_connection
def test_create_order(authenticated_api_client, product_factory, order_cleanup):

    product_data = {
        "name" : "Test Keyboard",
        "price" : 149.99
    }

    product_response = product_factory(product_data)

    product_id = product_response.json()["id"]

    order_data = {
        "items" : [ {
            "product_id" : product_id,
            "quantity" : 2
        }
        ]
    }

    order_response = authenticated_api_client.post(
        "/api/orders",
        json=order_data
    )

    assert order_response.status_code == 201

    assert "id" in order_response.json()

    order_id = order_response.json()["id"]
    order_cleanup(order_id)
    assert isinstance(order_id, int)

    connection = get_connection()

    cursor = connection.execute(
     """
        SELECT * FROM  order_items Where order_id = ?

    """,
        (order_id, )
    )


    row = cursor.fetchone()

    assert row["quantity"] == 2
    assert row["product_id"] == product_id

    connection.close()

def test_create_order_empty_items(authenticated_api_client):

    order_data = {
        "items" : []
    }

    order_response = authenticated_api_client.post(
        "/api/orders",
        json = order_data
    )

    assert order_response.status_code == 400

    assert order_response.json()["error"]["code"] == "VALIDATION_FAILED"
    assert order_response.json()["error"]["message"] == "Order must contain at least one item."


def test_create_order_invalid_quantity(authenticated_api_client, product_factory):

    product_data = {
         "name" : "Test Keyboard",
            "price" : 149.99
        }

    product_response = product_factory(product_data)

    product_id = product_response.json()["id"]

    order_data = {
        "items" : [ {
            "product_id" : product_id,
            "quantity" : -2
        }
        ]
    }

    order_response = authenticated_api_client.post(
        "/api/orders",
        json=order_data
    )

    assert order_response.status_code == 400

    assert order_response.json()["error"]["code"] == "VALIDATION_FAILED"
    assert order_response.json()["error"]["message"] == "Quantity must be at least 1."

def test_create_order_nonexistent_product_id(authenticated_api_client):

    order_data = {
        "items" : [
            {
                "product_id" : 9999,
                "quantity" : 1
            }
        ]
    }

    order_response = authenticated_api_client.post(
        "/api/orders",
        json=order_data
    )

    assert order_response.status_code == 400
    assert order_response.json()["error"]["code"] == "VALIDATION_FAILED"
    assert order_response.json()["error"]["message"] == "The product does not exist."


def test_create_order_missing_items(authenticated_api_client):

    order_data = {}

    order_response = authenticated_api_client.post(
        "/api/orders",
        json=order_data
    )

    assert order_response.status_code == 400
    assert order_response.json()["error"]["code"] == "VALIDATION_FAILED"
    assert order_response.json()["error"]["message"] == "The 'items' field is required."
