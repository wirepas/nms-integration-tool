# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from .logger import get_logger

logger = get_logger(__name__)

from .cache import Cache
import requests
from requests.auth import HTTPBasicAuth


class ApiClientBuilder:
    def __init__(
            self,
            client,
            hostname,
            cache: Cache,
            api_version="v1",
            client_id=None,
            client_secret=None,
            insecure=False,
            timeout=10.0
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._cache = cache
        self._client = client
        self._auth_url = '/'.join([hostname, 'oauth2', 'token'])
        self._api_url = '/'.join([hostname, 'api', api_version])
        self._insecure = insecure
        self._timeout = float(timeout)

    def _get_token(self):
        auth = HTTPBasicAuth(self._client_id, self._client_secret)
        body = "grant_type=client_credentials&scope=openid"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }

        response = requests.request(
            "POST", self._auth_url, auth=auth, data=body, headers=headers, timeout=self._timeout,
            verify=(not self._insecure)
        )
        logger.debug(f"Authentication response: {response}")
        if not (hasattr(response, 'text') and response.text):
            logger.error("Authentication failed: empty response")
            return None
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            logger.error(
                f"Authentication failed: expected JSON but got non-JSON response "
                f"(HTTP {response.status_code}). Response starts with: {response.text[:200]!r}"
            )
            return None
        logger.debug("Authentication response JSON: " + str(response_json))
        if 'access_token' not in response_json:
            logger.error(
                f"Authentication failed: 'access_token' not found in response: {response_json}"
            )
            return None
        return response_json['access_token']

    def build(self):
        token = None

        if self._client_id is not None and self._client_secret is not None:
            token = self._get_token()
            if token is None:
                raise RuntimeError(
                    "Authentication failed: could not obtain an access token. "
                    "Check credentials and server reachability."
                )

        if token is not None:
            return self._client.AuthenticatedClient(self._api_url, token=token, verify_ssl=(not self._insecure),
                                                    timeout=self._timeout)
        else:
            return self._client.Client(self._api_url, verify_ssl=(not self._insecure), timeout=self._timeout)
