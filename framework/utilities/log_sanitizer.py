from copy import deepcopy

SENSITIVE_FIELDS = {
    "token",
    "access_token",
    "password",
    "authorization"
}


def sanitize(data):
    safe_data = deepcopy(data)

    if isinstance(safe_data, dict):
        for key, value in safe_data.items():
            if key.lower() in SENSITIVE_FIELDS:
                safe_data[key] = "***REDACTED***"
            else:
                safe_data[key] = sanitize(value)

        return safe_data

    elif isinstance(safe_data, list):
        sanitized_items = []

        for item in safe_data:
            sanitized_items.append(sanitize(item))

        return sanitized_items

    return safe_data
