from flask import jsonify


def error_response(code, message, status_code, details=None):
    response = {
        "error": {
            "code": code,
            "message": message
        }
    }

    if details:
        response["error"]["details"] = details

    return jsonify(response), status_code
