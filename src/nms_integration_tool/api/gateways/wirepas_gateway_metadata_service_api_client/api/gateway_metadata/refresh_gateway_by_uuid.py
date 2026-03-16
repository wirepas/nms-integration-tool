from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    gateway_uuid: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/metadata/gateways/{gateway_uuid}/refresh".format(
            gateway_uuid=quote(str(gateway_uuid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorResponse | str:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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

    if response.status_code == 409:
        response_409 = response.text
        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    response_default = response.text
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorResponse | str]:
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
) -> Response[Any | ErrorResponse | str]:
    r"""Refresh sink nodes attached to the gateway

     Triggers a sink configuration update towards the specific gateway identified by UUID. This operation
    is not available
    for gateways that have never connected to the system. Instead it is required that there is a known
    sink configuration.
    If that is not the case, a corresponding error code is returned. If the refresh is already in
    progress, the request
    returns immediately with success (duplicated refresh operation is not triggered towards the
    gateway).

    The refresh operation is asynchronous, i.e. when request is made, the operation is triggered at the
    background. At the
    low level, this operation reads the current sink configuration from the gateway device and update
    the internal bookkeeping
    accordingly. Potential mismatch in the sink configuration is aligned with the current state
    available at the device. The
    status of the background operation is not directly available, it can be only detected if/when the
    gateway configuration
    changes. In cases where there is no changes in the gateway configuration, the `modificationTime` is
    still updated in
    order to indicate the \"completion\" of the refresh operation towards the client.

    *NOTE:* This operation should not be needed nor periodically issued. This should be used only when
    potential misconfiguration
    is detected!

    Args:
        gateway_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        gateway_uuid=gateway_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Any | ErrorResponse | str | None:
    r"""Refresh sink nodes attached to the gateway

     Triggers a sink configuration update towards the specific gateway identified by UUID. This operation
    is not available
    for gateways that have never connected to the system. Instead it is required that there is a known
    sink configuration.
    If that is not the case, a corresponding error code is returned. If the refresh is already in
    progress, the request
    returns immediately with success (duplicated refresh operation is not triggered towards the
    gateway).

    The refresh operation is asynchronous, i.e. when request is made, the operation is triggered at the
    background. At the
    low level, this operation reads the current sink configuration from the gateway device and update
    the internal bookkeeping
    accordingly. Potential mismatch in the sink configuration is aligned with the current state
    available at the device. The
    status of the background operation is not directly available, it can be only detected if/when the
    gateway configuration
    changes. In cases where there is no changes in the gateway configuration, the `modificationTime` is
    still updated in
    order to indicate the \"completion\" of the refresh operation towards the client.

    *NOTE:* This operation should not be needed nor periodically issued. This should be used only when
    potential misconfiguration
    is detected!

    Args:
        gateway_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse | str
    """

    return sync_detailed(
        gateway_uuid=gateway_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Any | ErrorResponse | str]:
    r"""Refresh sink nodes attached to the gateway

     Triggers a sink configuration update towards the specific gateway identified by UUID. This operation
    is not available
    for gateways that have never connected to the system. Instead it is required that there is a known
    sink configuration.
    If that is not the case, a corresponding error code is returned. If the refresh is already in
    progress, the request
    returns immediately with success (duplicated refresh operation is not triggered towards the
    gateway).

    The refresh operation is asynchronous, i.e. when request is made, the operation is triggered at the
    background. At the
    low level, this operation reads the current sink configuration from the gateway device and update
    the internal bookkeeping
    accordingly. Potential mismatch in the sink configuration is aligned with the current state
    available at the device. The
    status of the background operation is not directly available, it can be only detected if/when the
    gateway configuration
    changes. In cases where there is no changes in the gateway configuration, the `modificationTime` is
    still updated in
    order to indicate the \"completion\" of the refresh operation towards the client.

    *NOTE:* This operation should not be needed nor periodically issued. This should be used only when
    potential misconfiguration
    is detected!

    Args:
        gateway_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        gateway_uuid=gateway_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    gateway_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Any | ErrorResponse | str | None:
    r"""Refresh sink nodes attached to the gateway

     Triggers a sink configuration update towards the specific gateway identified by UUID. This operation
    is not available
    for gateways that have never connected to the system. Instead it is required that there is a known
    sink configuration.
    If that is not the case, a corresponding error code is returned. If the refresh is already in
    progress, the request
    returns immediately with success (duplicated refresh operation is not triggered towards the
    gateway).

    The refresh operation is asynchronous, i.e. when request is made, the operation is triggered at the
    background. At the
    low level, this operation reads the current sink configuration from the gateway device and update
    the internal bookkeeping
    accordingly. Potential mismatch in the sink configuration is aligned with the current state
    available at the device. The
    status of the background operation is not directly available, it can be only detected if/when the
    gateway configuration
    changes. In cases where there is no changes in the gateway configuration, the `modificationTime` is
    still updated in
    order to indicate the \"completion\" of the refresh operation towards the client.

    *NOTE:* This operation should not be needed nor periodically issued. This should be used only when
    potential misconfiguration
    is detected!

    Args:
        gateway_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            gateway_uuid=gateway_uuid,
            client=client,
        )
    ).parsed
