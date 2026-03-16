from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    network_uuid: UUID,
    *,
    query: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metadata/networks/{network_uuid}/linkedLocations".format(
            network_uuid=quote(str(network_uuid), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[UUID] | str:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UUID(response_200_item_data)

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
) -> Response[ErrorResponse | list[UUID] | str]:
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
    query: str | Unset = UNSET,
) -> Response[ErrorResponse | list[UUID] | str]:
    """Get a list of locations linked to then network identified by UUID

     Returns list of locations linked to the given network. While this supports query filter
    parameterization,
    it is probably more reasonable to filter at the network level. If the filter is given at this level,
    the
    returned list contains the list of UUIDs for those locations that are linked to this network and
    match the
    given filter.

    Args:
        network_uuid (UUID):
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[UUID] | str]
    """

    kwargs = _get_kwargs(
        network_uuid=network_uuid,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
    query: str | Unset = UNSET,
) -> ErrorResponse | list[UUID] | str | None:
    """Get a list of locations linked to then network identified by UUID

     Returns list of locations linked to the given network. While this supports query filter
    parameterization,
    it is probably more reasonable to filter at the network level. If the filter is given at this level,
    the
    returned list contains the list of UUIDs for those locations that are linked to this network and
    match the
    given filter.

    Args:
        network_uuid (UUID):
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[UUID] | str
    """

    return sync_detailed(
        network_uuid=network_uuid,
        client=client,
        query=query,
    ).parsed


async def asyncio_detailed(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
    query: str | Unset = UNSET,
) -> Response[ErrorResponse | list[UUID] | str]:
    """Get a list of locations linked to then network identified by UUID

     Returns list of locations linked to the given network. While this supports query filter
    parameterization,
    it is probably more reasonable to filter at the network level. If the filter is given at this level,
    the
    returned list contains the list of UUIDs for those locations that are linked to this network and
    match the
    given filter.

    Args:
        network_uuid (UUID):
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[UUID] | str]
    """

    kwargs = _get_kwargs(
        network_uuid=network_uuid,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    network_uuid: UUID,
    *,
    client: AuthenticatedClient,
    query: str | Unset = UNSET,
) -> ErrorResponse | list[UUID] | str | None:
    """Get a list of locations linked to then network identified by UUID

     Returns list of locations linked to the given network. While this supports query filter
    parameterization,
    it is probably more reasonable to filter at the network level. If the filter is given at this level,
    the
    returned list contains the list of UUIDs for those locations that are linked to this network and
    match the
    given filter.

    Args:
        network_uuid (UUID):
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[UUID] | str
    """

    return (
        await asyncio_detailed(
            network_uuid=network_uuid,
            client=client,
            query=query,
        )
    ).parsed
