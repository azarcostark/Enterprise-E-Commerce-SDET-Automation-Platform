import pytest

from app.database.connection import get_connection
from app.repositories.product_repository import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product)


@pytest.fixture
def clean_products():
    connection = get_connection()

    existing_product_ids = {
        row["id"]
        for row in connection.execute(
            "SELECT id FROM products"
        ).fetchall()
    }

    connection.close()

    yield

    connection = get_connection()

    current_product_ids = {
        row["id"]
        for row in connection.execute(
            "SELECT id FROM products"
        ).fetchall()
    }

    new_product_ids = current_product_ids - existing_product_ids

    for product_id in new_product_ids:
        connection.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )

    connection.commit()
    connection.close()






def test_get_all_products(clean_products):
    product_id = create_product(
        "Repository Test Product", 99.99
    )

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

    rows_deleted = delete_product(product_id)

    assert rows_deleted == 1

    product = get_product_by_id(product_id)

    assert product is None


def test_delete_product_not_found(clean_products):
    rows_deleted = delete_product(9999)

    assert rows_deleted == 0
