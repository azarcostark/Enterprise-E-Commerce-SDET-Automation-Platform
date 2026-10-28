def validate_product_data(data):
    errors = {}

    if not isinstance(data, dict):
        return {"body": "Request body must be a JSON object."}

    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        errors["name"] = "Name is required and must be a non-empty string."

    if price is None:
        errors["price"] = "Price is required."
    elif not isinstance(price, (int, float)):
        errors["price"] = "Price must be a number."
    elif price <= 0:
        errors["price"] = "Price must be greater than 0."

    return errors
