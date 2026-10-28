
import pytest

from app.repositories.product_repository import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
)


@pytest.fixture
def clean_products():
    created_product_ids = []

    def track_product(product_id):
        created_product_ids.append(product_id)

    yield track_product

    for product_id in created_product_ids:
        delete_product(product_id)


def test_get_all_products(clean_products):
    product_id = create_product(
        "Repository Test Product", 99.99
    )
    clean_products(product_id)

    products = get_all_products()

    product = next(
        product for product in products
        if product["id"] == product_id
    )

    assert product["name"] == "Repository Test Product"
    assert product["price"] == 99.99


def test_get_product_by_id(clean_products):
    product_id = create_product(
        "Repository Test Product", 99.99
    )
    clean_products(product_id)

    product = get_product_by_id(product_id)

    assert product is not None
    assert product["id"] == product_id
    assert product["name"] == "Repository Test Product"
    assert product["price"] == 99.99


def test_get_product_by_id_not_found(clean_products):
    product = get_product_by_id(9999)

    assert product is None


def test_create_product(clean_products):
    product_id = create_product(
        "Created Product", 149.99
    )
    clean_products(product_id)

    assert isinstance(product_id, int)
    assert product_id > 0

    product = get_product_by_id(product_id)

    assert product is not None
    assert product["name"] == "Created Product"
    assert product["price"] == 149.99


def test_update_product(clean_products):
    product_id = create_product(
        "Original Product", 99.99
    )
    clean_products(product_id)

    rows_updated = update_product(
        product_id,
        "Updated Product", 149.99
    )

    assert rows_updated == 1

    product = get_product_by_id(product_id)

    assert product is not None
    assert product["name"] == "Updated Product"
    assert product["price"] == 149.99


def test_update_product_not_found(clean_products):
    rows_updated = update_product(
        9999, "Updated Product", 149.99
    )

    assert rows_updated == 0


def test_delete_product(clean_products):
    product_id = create_product(
        "Product To Delete", 199.99
    )
    clean_products(product_id)

    rows_deleted = delete_product(product_id)

    assert rows_deleted == 1

    product = get_product_by_id(product_id)

    assert product is None


def test_delete_product_not_found(clean_products):
    rows_deleted = delete_product(9999)

    assert rows_deleted == 0
