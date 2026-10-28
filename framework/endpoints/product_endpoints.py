class ProductEndpoints:
    BASE = "/api/products"

    @staticmethod
    def by_id(product_id):
        return f"{ProductEndpoints.BASE}/{product_id}"
