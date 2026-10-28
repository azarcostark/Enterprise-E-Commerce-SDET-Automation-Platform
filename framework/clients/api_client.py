
import requests

from framework.exceptions.api_exceptions import (
    APIConnectionError,
    APITimeoutError
)
from framework.utilities.log_sanitizer import sanitize
from framework.utilities.logger import get_logger


class APIClient:

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        self.logger = get_logger("APIClient")

    def _get_safe_response_body(self, response):
        try:
            return sanitize(response.json())
        except ValueError:
            return "[Response body omitted: invalid JSON]"

    def set_auth_token(self, token):
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"

        # Sanitize the request body before logging it.
        self.logger.info(
            "REQUEST | %s %s | body=%s",
            method,
            url,
            sanitize(kwargs.get("json"))
        )

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )

        except requests.exceptions.Timeout as error:
            self.logger.error(
                "TIMEOUT | %s %s | timeout=%ss",
                method,
                url,
                self.timeout
            )

            raise APITimeoutError(
                f"API request timed out after {self.timeout} seconds: "
                f"{method} {url}"
            ) from error

        except requests.exceptions.ConnectionError as error:
            self.logger.error(
                "CONNECTION ERROR | %s %s",
                method,
                url
            )

            raise APIConnectionError(
                f"Unable to connect to API: {method} {url}"
            ) from error

        # Parse and sanitize the response before logging it.
        self.logger.info(
            "RESPONSE | %s | %s | body=%s",
            response.status_code,
            url,
            self._get_safe_response_body(response)
        )

        return response

    def get(self, endpoint):
        return self.request(
            "GET",
            endpoint
        )

    def post(self, endpoint, json=None):
        return self.request(
            "POST",
            endpoint,
            json=json
        )

    def put(self, endpoint, json=None):
        return self.request(
            "PUT",
            endpoint,
            json=json
        )

    def patch(self, endpoint, json=None):
        return self.request(
            "PATCH",
            endpoint,
            json=json
        )

    def delete(self, endpoint):
        return self.request(
            "DELETE",
            endpoint
        )
