from flask import Flask
from app.products import products_bp
from app.orders import orders_bp
from app.errors.handlers import error_response
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    @app.errorhandler(404)
    def handle_not_found(error):
        return error_response(
            "RESOURCE_NOT_FOUND",
            "The requested resource was not found.",
            404
        )

    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(auth_bp)

    return app
