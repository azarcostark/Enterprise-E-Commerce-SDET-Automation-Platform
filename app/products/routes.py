from flask import Blueprint, request

from app.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)

from app.validators.product_validator import validate_product_data
from app.errors.handlers import error_response
from app.auth.decorators import require_auth, require_role


products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/api/products"
)


@products_bp.get("")
def get_products():
    return get_all_products()


@products_bp.get("/<int:product_id>")
def get_product(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        return error_response(
            "PRODUCT_NOT_FOUND",
            "Product not found.",
            404
        )

    return product


@products_bp.post("")
@require_auth
@require_role("admin")
def create_product_endpoint():
    data = request.get_json(silent=True)

    errors = validate_product_data(data)

    if errors:
        return error_response(
            "VALIDATION_FAILED",
            "Product validation failed.",
            400,
            errors
        )

    name = data["name"]
    price = data["price"]

    product_id = create_product(name, price)

    return {
        "id": product_id,
        "name": name,
        "price": price
    }, 201


@products_bp.put("/<int:product_id>")
@require_auth
@require_role("admin")
def update_product_endpoint(product_id):
    data = request.get_json(silent=True)

    errors = validate_product_data(data)

    if errors:
        return error_response(
            "VALIDATION_FAILED",
            "Product validation failed.",
            400,
            errors
        )

    existing_product = get_product_by_id(product_id)

    if existing_product is None:
        return error_response(
            "PRODUCT_NOT_FOUND",
            "Product not found.",
            404
        )

    name = data["name"]
    price = data["price"]

    update_product(product_id, name, price)

    updated_product = get_product_by_id(product_id)

    return updated_product, 200


@products_bp.delete("/<int:product_id>")
@require_auth
@require_role("admin")
def delete_product_endpoint(product_id):
    existing_product = get_product_by_id(product_id)

    if existing_product is None:
        return error_response(
            "PRODUCT_NOT_FOUND",
            "Product not found.",
            404
        )

    delete_product(product_id)

    return "", 204
