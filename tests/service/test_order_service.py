import pytest
from unittest.mock import patch
from app.services import order_service

def test_create_order():

    user_id = 1

    items = [{
            "product_id" : 1,
            "quantity": 2,
            "unit_price" : 99.99
    }

    ]
    with patch("app.services.order_service.product_repository.get_product_by_id") as mock_get_product:
        mock_get_product.return_value = {
             "id" : 1,
             "name" : "Keyboard",
             "price" : 149.99
        }

        with patch("app.services.order_service.order_repository.create_order") as mock_create_order:
            mock_create_order.return_value = 123
            order_id = order_service.create_order(user_id, items)

            assert order_id == 123
            mock_create_order.assert_called_once_with(user_id, items)

            assert items[0]["unit_price"] == 149.99


def test_empty_order():

    user_id = 2
    items = []

    with pytest.raises(ValueError):
        order_service.create_order(user_id, items)



def test_create_order_with_invalid_quantity():

    user_id = 3
    items = [{
        "product_id" : 3,
        "quantity" : -3,
        "unit_price" : 99.99
    }]

    with patch("app.services.order_service.order_repository.create_order") as mock_create_order:
        with pytest.raises(ValueError):
                order_service.create_order(user_id, items)

        mock_create_order.assert_not_called()


def test_create_order_with_nonexistent_product():

    user_id = 4

    items = [
        {
            "product_id": 999,
            "quantity": 2,
            "unit_price": 99.99
        }
    ]

    with patch("app.services.order_service.product_repository.get_product_by_id") as mock_get_product:
        mock_get_product.return_value = None

        with patch("app.services.order_service.order_repository.create_order") as mock_create_order:
            with pytest.raises(ValueError):
                order_service.create_order(user_id, items)

            mock_create_order.assert_not_called()
