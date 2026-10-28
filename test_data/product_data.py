def get_valid_product():
    return {
        "name": "Automation Test Product",
        "price": 149.99
    }


INVALID_PRODUCT = {
    "name": "",
    "price": -100
}


UPDATE_PRODUCT = {
    "name": "Updated Automation Product",
    "price": 199.99
}


DELETE_TEST_PRODUCT = {
    "name": "Product To Delete",
    "price": 50.00
}


INVALID_PRODUCT_CASES = [
    {
        "name": "",
        "price": 100
    },
    {
        "name": "Test Product",
        "price": -10
    },
    {
        "name": "",
        "price": -100
    },
    {
        "price": 100
    },
    {
        "name": "Test Product"
    }
]
