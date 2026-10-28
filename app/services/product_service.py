from app.repositories.product_repository import (
    get_all_products as repository_get_all_products,
    get_product_by_id as repository_get_product_by_id,
    create_product as create_product_in_repository,
    update_product as update_product_in_repository,
    delete_product as delete_product_in_repository
)


def get_all_products():
    return repository_get_all_products()


def get_product_by_id(product_id):
    return repository_get_product_by_id(product_id)


def create_product(name, price):
    return create_product_in_repository(name, price)


def update_product(product_id, name, price):
    return update_product_in_repository(product_id, name, price)


def delete_product(product_id):
    return delete_product_in_repository(product_id)
