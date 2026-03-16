from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.gateway import Gateway
from ...types import Response


def _get_kwargs(
    *,
    body: list[Gateway],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/metadata/gateways",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[Gateway] | str:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Gateway.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    response_default = response.text
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | list[Gateway] | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: list[Gateway],
) -> Response[ErrorResponse | list[Gateway] | str]:
    """Update one or multiple gateways

     Update the metadata attributes of one or multiple gateways. The items in the list are all updated
    and the return value of the
    operation reflects the success of the whole operation. Thus, all items in the list are either
    updated as requested by the
    operation, or no changes are made in any of the items in case of an error. All the gateways
    identified in the operation shall
    be found, otherwise the operation will fail.

    The items may not be complete gateway objects, thus only those fields that are given are updated. It
    is not possible to remove
    an attribute of a gateway object with this operation. Instead, if that kind of functionality is
    needed, an update operation (PUT)
    of a specific gateway object shall be used.

    Args:
        body (list[Gateway]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[Gateway] | str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: list[Gateway],
) -> ErrorResponse | list[Gateway] | str | None:
    """Update one or multiple gateways

     Update the metadata attributes of one or multiple gateways. The items in the list are all updated
    and the return value of the
    operation reflects the success of the whole operation. Thus, all items in the list are either
    updated as requested by the
    operation, or no changes are made in any of the items in case of an error. All the gateways
    identified in the operation shall
    be found, otherwise the operation will fail.

    The items may not be complete gateway objects, thus only those fields that are given are updated. It
    is not possible to remove
    an attribute of a gateway object with this operation. Instead, if that kind of functionality is
    needed, an update operation (PUT)
    of a specific gateway object shall be used.

    Args:
        body (list[Gateway]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[Gateway] | str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: list[Gateway],
) -> Response[ErrorResponse | list[Gateway] | str]:
    """Update one or multiple gateways

     Update the metadata attributes of one or multiple gateways. The items in the list are all updated
    and the return value of the
    operation reflects the success of the whole operation. Thus, all items in the list are either
    updated as requested by the
    operation, or no changes are made in any of the items in case of an error. All the gateways
    identified in the operation shall
    be found, otherwise the operation will fail.

    The items may not be complete gateway objects, thus only those fields that are given are updated. It
    is not possible to remove
    an attribute of a gateway object with this operation. Instead, if that kind of functionality is
    needed, an update operation (PUT)
    of a specific gateway object shall be used.

    Args:
        body (list[Gateway]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[Gateway] | str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: list[Gateway],
) -> ErrorResponse | list[Gateway] | str | None:
    """Update one or multiple gateways

     Update the metadata attributes of one or multiple gateways. The items in the list are all updated
    and the return value of the
    operation reflects the success of the whole operation. Thus, all items in the list are either
    updated as requested by the
    operation, or no changes are made in any of the items in case of an error. All the gateways
    identified in the operation shall
    be found, otherwise the operation will fail.

    The items may not be complete gateway objects, thus only those fields that are given are updated. It
    is not possible to remove
    an attribute of a gateway object with this operation. Instead, if that kind of functionality is
    needed, an update operation (PUT)
    of a specific gateway object shall be used.

    Args:
        body (list[Gateway]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[Gateway] | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
