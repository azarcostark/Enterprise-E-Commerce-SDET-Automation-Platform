from framework.utilities.log_sanitizer import sanitize

def test_sanitize_masks_password():

    data = {
        "username" : "vipul",
        "password" : "secret123",
        "role" : "admin"
    }

    result = sanitize(data)

    assert result["password"] == "***REDACTED***"
    assert result["username"] == "vipul"
    assert result["role"] == "admin"

    assert data["password"] == "secret123"


def test_sanitize_preserves_original_data():

    data = {
        "username" : "vipul",
        "password" : "secret123",
        "role" : "admin"
    }

    result = sanitize(data)

    assert result["password"] == "***REDACTED***"

    assert data["password"] == "secret123"
    assert data["username"] == "vipul"
    assert data["role"] == "admin"

def test_sanitize_nested_dictionary():

    data = {
        "user" :
        {
            "username" : "vipul",
            "password" : "secret123"
        }
    }

    result = sanitize(data)

    assert result["user"]["password"] == "***REDACTED***"
    assert result["user"]["username"] == "vipul"
    assert data["user"]["password"] == "secret123"

def test_sanitize_case_insensitive_keys():

    data = {
        "Password" : "secret123",
        "ACCESS_TOKEN" : "abc123"
    }

    result = sanitize(data)

    assert result["Password"] == "***REDACTED***"
    assert result["ACCESS_TOKEN"] == "***REDACTED***"

    assert data["Password"] == "secret123"
    assert data["ACCESS_TOKEN"] == "abc123"

def test_sanitize_list_of_dictionaries():

    data = [
    {"username": "vipul", "password": "secret123"},
    {"username": "tester", "password": "pass456"}
]

    result = sanitize(data)

    assert result[0]["password"] == "***REDACTED***"
    assert result[1]["password"] == "***REDACTED***"
    assert result[0]["username"] == "vipul"
    assert result[1]["username"] == "tester"

    assert data[0]["password"] == "secret123"
    assert data[1]["password"] == "pass456"


def test_sanitize_multiple_sensitive_fields():

    data = {
        "username" : "vipul",
        "password" : "secret123",
        "status" : "success",
        "access_token" : "abc123"

    }

    result = sanitize(data)
    assert result["status"] == "success"
    assert result["password"] == "***REDACTED***"
    assert result["username"] == "vipul"
    assert result["access_token"] == "***REDACTED***"

    assert data["password"] == "secret123"
