
from app.repositories import order_repository
from app.repositories import product_repository


def create_order(user_id, items):
    if not isinstance(items, list) or not items:
        raise ValueError("Order must contain at least one item.")

    validated_items = []

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each order item must be an object.")

        if "product_id" not in item:
            raise ValueError("The 'product_id' field is required.")

        if "quantity" not in item:
            raise ValueError("The 'quantity' field is required.")

        product_id = item["product_id"]
        quantity = item["quantity"]

        # Reject booleans, strings, floats, zero, and negative quantities.
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be at least 1.")

        # Product IDs must be positive integers, not booleans or strings.
        if type(product_id) is not int or product_id <= 0:
            raise ValueError("A valid product ID is required.")

        product = product_repository.get_product_by_id(product_id)

        if product is None:
            raise ValueError("The product does not exist.")

        validated_items.append(
            {
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": product["price"],
            }
        )

    return order_repository.create_order(user_id, validated_items)
