from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.delete_list_response import DeleteListResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    network_uuid: UUID,
    *,
    query: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/metadata/networks/{network_uuid}/linkedLocations".format(
            network_uuid=quote(str(network_uuid), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteListResponse | ErrorResponse | str:
    if response.status_code == 200:
        response_200 = DeleteListResponse.from_dict(response.json())

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
) -> Response[DeleteListResponse | ErrorResponse | str]:
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
    query: str,
) -> Response[DeleteListResponse | ErrorResponse | str]:
    """Remove one or multiple location linkages from the network

     Remove one or multiple location linkages from a network. Linked locations from a network are removed
    based on the query filter
    attributes given as a parameters for the request. All linked locations matching the given query are
    removed. The return value
    reflects the success of the whole operation, thus either all matching location references are
    removed from the network or none
    is removed in case of an error.

    The success of the operation is based on the requested target state, e.g. if a location reference
    removal is requested based
    on the locationUuid of the entry, the operation is successful also in a case where there is no
    relation to the given location.

    Args:
        network_uuid (UUID):
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteListResponse | ErrorResponse | str]
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
    query: str,
) -> DeleteListResponse | ErrorResponse | str | None:
    """Remove one or multiple location linkages from the network

     Remove one or multiple location linkages from a network. Linked locations from a network are removed
    based on the query filter
    attributes given as a parameters for the request. All linked locations matching the given query are
    removed. The return value
    reflects the success of the whole operation, thus either all matching location references are
    removed from the network or none
    is removed in case of an error.

    The success of the operation is based on the requested target state, e.g. if a location reference
    removal is requested based
    on the locationUuid of the entry, the operation is successful also in a case where there is no
    relation to the given location.

    Args:
        network_uuid (UUID):
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteListResponse | ErrorResponse | str
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
    query: str,
) -> Response[DeleteListResponse | ErrorResponse | str]:
    """Remove one or multiple location linkages from the network

     Remove one or multiple location linkages from a network. Linked locations from a network are removed
    based on the query filter
    attributes given as a parameters for the request. All linked locations matching the given query are
    removed. The return value
    reflects the success of the whole operation, thus either all matching location references are
    removed from the network or none
    is removed in case of an error.

    The success of the operation is based on the requested target state, e.g. if a location reference
    removal is requested based
    on the locationUuid of the entry, the operation is successful also in a case where there is no
    relation to the given location.

    Args:
        network_uuid (UUID):
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteListResponse | ErrorResponse | str]
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
    query: str,
) -> DeleteListResponse | ErrorResponse | str | None:
    """Remove one or multiple location linkages from the network

     Remove one or multiple location linkages from a network. Linked locations from a network are removed
    based on the query filter
    attributes given as a parameters for the request. All linked locations matching the given query are
    removed. The return value
    reflects the success of the whole operation, thus either all matching location references are
    removed from the network or none
    is removed in case of an error.

    The success of the operation is based on the requested target state, e.g. if a location reference
    removal is requested based
    on the locationUuid of the entry, the operation is successful also in a case where there is no
    relation to the given location.

    Args:
        network_uuid (UUID):
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteListResponse | ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            network_uuid=network_uuid,
            client=client,
            query=query,
        )
    ).parsed
