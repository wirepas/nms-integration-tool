from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.node import Node
from ...models.update_node_body import UpdateNodeBody
from ...types import Response


def _get_kwargs(
    node_uuid: UUID,
    *,
    body: UpdateNodeBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/metadata/nodes/{node_uuid}".format(
            node_uuid=quote(str(node_uuid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorResponse | Node | str:
    if response.status_code == 200:
        response_200 = Node.from_dict(response.json())

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
) -> Response[ErrorResponse | Node | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    node_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateNodeBody,
) -> Response[ErrorResponse | Node | str]:
    """Update the node

     Update the basic information and location related attributes of a specific node identified by UUID.
    This update operation
    expects to get a complete object and overrides existing values with it (allowing also removal of
    some fields).

    Args:
        node_uuid (UUID):
        body (UpdateNodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Node | str]
    """

    kwargs = _get_kwargs(
        node_uuid=node_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    node_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateNodeBody,
) -> ErrorResponse | Node | str | None:
    """Update the node

     Update the basic information and location related attributes of a specific node identified by UUID.
    This update operation
    expects to get a complete object and overrides existing values with it (allowing also removal of
    some fields).

    Args:
        node_uuid (UUID):
        body (UpdateNodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Node | str
    """

    return sync_detailed(
        node_uuid=node_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    node_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateNodeBody,
) -> Response[ErrorResponse | Node | str]:
    """Update the node

     Update the basic information and location related attributes of a specific node identified by UUID.
    This update operation
    expects to get a complete object and overrides existing values with it (allowing also removal of
    some fields).

    Args:
        node_uuid (UUID):
        body (UpdateNodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Node | str]
    """

    kwargs = _get_kwargs(
        node_uuid=node_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    node_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateNodeBody,
) -> ErrorResponse | Node | str | None:
    """Update the node

     Update the basic information and location related attributes of a specific node identified by UUID.
    This update operation
    expects to get a complete object and overrides existing values with it (allowing also removal of
    some fields).

    Args:
        node_uuid (UUID):
        body (UpdateNodeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Node | str
    """

    return (
        await asyncio_detailed(
            node_uuid=node_uuid,
            client=client,
            body=body,
        )
    ).parsed
