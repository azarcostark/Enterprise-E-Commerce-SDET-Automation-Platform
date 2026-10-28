from app.repositories import order_repository
from app.repositories import product_repository

def create_order(user_id, items):
    if not items:
        raise ValueError("Order must contain at least one item.")
    for item in items:
        if item["quantity"]<=0:
            raise ValueError("Quantity must be at least 1.")

        product = product_repository.get_product_by_id(item["product_id"])
        if product is None:
            raise ValueError("The product does not exist.")
        item["unit_price"] = product["price"]

    order_id = order_repository.create_order(user_id, items)

    return order_id
