from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.gateway import Gateway
from ...models.gateway_info import GatewayInfo
from ...types import Response


def _get_kwargs(
    gateway_uuid: UUID,
    *,
    body: GatewayInfo,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/metadata/gateways/{gateway_uuid}".format(
            gateway_uuid=quote(str(gateway_uuid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorResponse | Gateway | str:
    if response.status_code == 200:
        response_200 = Gateway.from_dict(response.json())

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
) -> Response[ErrorResponse | Gateway | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: GatewayInfo,
) -> Response[ErrorResponse | Gateway | str]:
    """Partially/patch update the gateway

     Update the given fields in a specific gateway identified by UUID. Note that the static information
    defined during the
    gateway configuration / provisioning phase cannot be updated.

    **NOTE:** The item given in the body may not be a complete gateway object, thus only those fields
    that are given are updated.

    Args:
        gateway_uuid (UUID):
        body (GatewayInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Gateway | str]
    """

    kwargs = _get_kwargs(
        gateway_uuid=gateway_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: GatewayInfo,
) -> ErrorResponse | Gateway | str | None:
    """Partially/patch update the gateway

     Update the given fields in a specific gateway identified by UUID. Note that the static information
    defined during the
    gateway configuration / provisioning phase cannot be updated.

    **NOTE:** The item given in the body may not be a complete gateway object, thus only those fields
    that are given are updated.

    Args:
        gateway_uuid (UUID):
        body (GatewayInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Gateway | str
    """

    return sync_detailed(
        gateway_uuid=gateway_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: GatewayInfo,
) -> Response[ErrorResponse | Gateway | str]:
    """Partially/patch update the gateway

     Update the given fields in a specific gateway identified by UUID. Note that the static information
    defined during the
    gateway configuration / provisioning phase cannot be updated.

    **NOTE:** The item given in the body may not be a complete gateway object, thus only those fields
    that are given are updated.

    Args:
        gateway_uuid (UUID):
        body (GatewayInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Gateway | str]
    """

    kwargs = _get_kwargs(
        gateway_uuid=gateway_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: GatewayInfo,
) -> ErrorResponse | Gateway | str | None:
    """Partially/patch update the gateway

     Update the given fields in a specific gateway identified by UUID. Note that the static information
    defined during the
    gateway configuration / provisioning phase cannot be updated.

    **NOTE:** The item given in the body may not be a complete gateway object, thus only those fields
    that are given are updated.

    Args:
        gateway_uuid (UUID):
        body (GatewayInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Gateway | str
    """

    return (
        await asyncio_detailed(
            gateway_uuid=gateway_uuid,
            client=client,
            body=body,
        )
    ).parsed
