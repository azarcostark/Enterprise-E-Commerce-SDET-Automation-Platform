from flask import request, jsonify, Blueprint
from app.services import order_service
from app.auth.decorators import require_auth
from app.errors.handlers import error_response


orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/api/orders", methods=["POST"])
@require_auth
def create_order():

    data = request.json

    items = data.get("items")

    if items is None:
        return error_response(
            "VALIDATION_FAILED",
            "The 'items' field is required.",
            400
        )

    user_id = int(request.user["sub"])

    try:

        order_id = order_service.create_order(user_id, items)

        return jsonify(
            {
                "id" : order_id
            }
        ), 201

    except ValueError as error:

        return error_response(
            "VALIDATION_FAILED",
            str(error),
            400
        )
