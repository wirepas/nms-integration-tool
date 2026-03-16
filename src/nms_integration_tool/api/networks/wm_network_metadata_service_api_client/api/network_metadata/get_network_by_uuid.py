from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_network_by_uuid_response_200 import GetNetworkByUuidResponse200
from ...types import Response


def _get_kwargs(
    network_uuid: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metadata/networks/{network_uuid}".format(
            network_uuid=quote(str(network_uuid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GetNetworkByUuidResponse200 | str:
    if response.status_code == 200:
        response_200 = GetNetworkByUuidResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = response.text
        return response_401

    if response.status_code == 403:
        response_403 = response.text
        return response_403

    if response.status_code == 404:
        response_404 = response.text
        return response_404

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    response_default = response.text
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | GetNetworkByUuidResponse200 | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | GetNetworkByUuidResponse200 | str]:
    """Obtain information about a network

     Obtain information about a specific network identified by the UUID

    Args:
        network_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetNetworkByUuidResponse200 | str]
    """

    kwargs = _get_kwargs(
        network_uuid=network_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | GetNetworkByUuidResponse200 | str | None:
    """Obtain information about a network

     Obtain information about a specific network identified by the UUID

    Args:
        network_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetNetworkByUuidResponse200 | str
    """

    return sync_detailed(
        network_uuid=network_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | GetNetworkByUuidResponse200 | str]:
    """Obtain information about a network

     Obtain information about a specific network identified by the UUID

    Args:
        network_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetNetworkByUuidResponse200 | str]
    """

    kwargs = _get_kwargs(
        network_uuid=network_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | GetNetworkByUuidResponse200 | str | None:
    """Obtain information about a network

     Obtain information about a specific network identified by the UUID

    Args:
        network_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetNetworkByUuidResponse200 | str
    """

    return (
        await asyncio_detailed(
            network_uuid=network_uuid,
            client=client,
        )
    ).parsed
