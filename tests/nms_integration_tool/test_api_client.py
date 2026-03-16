# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import json
import unittest
from unittest.mock import MagicMock, patch

import requests

from nms_integration_tool.api_client import ApiClientBuilder
from nms_integration_tool.cache import Cache


class ApiClientBuilderTest(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.cache = Cache()
        self.hostname = "https://nms.example.com"

    def test_build_without_credentials_returns_unauthenticated_client(self):
        builder = ApiClientBuilder(client=self.client, hostname=self.hostname, cache=self.cache)
        result = builder.build()

        self.client.Client.assert_called_once_with(
            "https://nms.example.com/api/v1", verify_ssl=True, timeout=10.0
        )
        self.assertEqual(result, self.client.Client.return_value)

    def test_build_with_only_client_id_does_not_authenticate(self):
        builder = ApiClientBuilder(
            client=self.client, hostname=self.hostname, cache=self.cache,
            client_id="cid"  # no secret
        )
        builder.build()

        self.client.Client.assert_called_once()
        self.client.AuthenticatedClient.assert_not_called()

    def test_build_with_credentials_returns_authenticated_client(self):
        mock_resp = MagicMock()
        mock_resp.text = json.dumps({"access_token": "my-token-abc"})
        mock_resp.json.return_value = {"access_token": "my-token-abc"}

        with patch("requests.request", return_value=mock_resp):
            builder = ApiClientBuilder(
                client=self.client, hostname=self.hostname, cache=self.cache,
                client_id="cid", client_secret="sec"
            )
            result = builder.build()

        self.client.AuthenticatedClient.assert_called_once_with(
            "https://nms.example.com/api/v1", token="my-token-abc", verify_ssl=True, timeout=10.0
        )
        self.assertEqual(result, self.client.AuthenticatedClient.return_value)

    def test_api_url_includes_version(self):
        builder = ApiClientBuilder(
            client=self.client, hostname=self.hostname, cache=self.cache, api_version="v2"
        )
        self.assertEqual(builder._api_url, "https://nms.example.com/api/v2")

    def test_auth_url_points_to_oauth2_token(self):
        builder = ApiClientBuilder(client=self.client, hostname=self.hostname, cache=self.cache)
        self.assertEqual(builder._auth_url, "https://nms.example.com/oauth2/token")

    def test_insecure_flag_disables_ssl_on_unauthenticated_client(self):
        builder = ApiClientBuilder(
            client=self.client, hostname=self.hostname, cache=self.cache, insecure=True
        )
        builder.build()

        self.client.Client.assert_called_once_with(
            "https://nms.example.com/api/v1", verify_ssl=False, timeout=10.0
        )

    def test_insecure_flag_disables_ssl_on_authenticated_client(self):
        mock_resp = MagicMock()
        mock_resp.text = json.dumps({"access_token": "tok"})
        mock_resp.json.return_value = {"access_token": "tok"}

        with patch("requests.request", return_value=mock_resp):
            builder = ApiClientBuilder(
                client=self.client, hostname=self.hostname, cache=self.cache,
                client_id="cid", client_secret="sec", insecure=True
            )
            builder.build()

        self.client.AuthenticatedClient.assert_called_once_with(
            "https://nms.example.com/api/v1", token="tok", verify_ssl=False, timeout=10.0
        )

    def test_timeout_string_is_cast_to_float(self):
        builder = ApiClientBuilder(
            client=self.client, hostname=self.hostname, cache=self.cache, timeout="30"
        )
        self.assertIsInstance(builder._timeout, float)
        self.assertEqual(builder._timeout, 30.0)

    def test_build_raises_when_authentication_fails(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.text = "<html>Unauthorized</html>"
        mock_resp.json.side_effect = requests.exceptions.JSONDecodeError("", "", 0)

        with patch("requests.request", return_value=mock_resp):
            builder = ApiClientBuilder(
                client=self.client, hostname=self.hostname, cache=self.cache,
                client_id="cid", client_secret="wrong"
            )
            with self.assertRaises(RuntimeError):
                builder.build()

    def test_custom_timeout_is_passed_to_client(self):
        builder = ApiClientBuilder(
            client=self.client, hostname=self.hostname, cache=self.cache, timeout=60.0
        )
        builder.build()

        self.client.Client.assert_called_once_with(
            "https://nms.example.com/api/v1", verify_ssl=True, timeout=60.0
        )


if __name__ == "__main__":
    unittest.main()
