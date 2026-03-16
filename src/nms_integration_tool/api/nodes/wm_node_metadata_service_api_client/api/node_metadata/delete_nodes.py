from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.delete_list_response import DeleteListResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    query: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/metadata/nodes",
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
    *,
    client: AuthenticatedClient,
    query: str,
) -> Response[DeleteListResponse | ErrorResponse | str]:
    """Deletes one or multiple nodes

     Deletes one or multiple nodes based on the query filter attributes given as a parameters for the
    request. All nodes
    matching the given query are removed, thus caution should be exercised when using this operation.
    The return value reflects
    the success of the whole operation, thus either all nodes are removed or none is removed in case of
    an error.

    The success of the operation is based on the requested target state, e.g. if a node deletion is
    requested based on UUID
    of the node, the operation for that node is successful also in a case where the given node does not
    exist (anymore).

    See advanced search for supported query fields and pattern matching.

    Args:
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteListResponse | ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: str,
) -> DeleteListResponse | ErrorResponse | str | None:
    """Deletes one or multiple nodes

     Deletes one or multiple nodes based on the query filter attributes given as a parameters for the
    request. All nodes
    matching the given query are removed, thus caution should be exercised when using this operation.
    The return value reflects
    the success of the whole operation, thus either all nodes are removed or none is removed in case of
    an error.

    The success of the operation is based on the requested target state, e.g. if a node deletion is
    requested based on UUID
    of the node, the operation for that node is successful also in a case where the given node does not
    exist (anymore).

    See advanced search for supported query fields and pattern matching.

    Args:
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteListResponse | ErrorResponse | str
    """

    return sync_detailed(
        client=client,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
) -> Response[DeleteListResponse | ErrorResponse | str]:
    """Deletes one or multiple nodes

     Deletes one or multiple nodes based on the query filter attributes given as a parameters for the
    request. All nodes
    matching the given query are removed, thus caution should be exercised when using this operation.
    The return value reflects
    the success of the whole operation, thus either all nodes are removed or none is removed in case of
    an error.

    The success of the operation is based on the requested target state, e.g. if a node deletion is
    requested based on UUID
    of the node, the operation for that node is successful also in a case where the given node does not
    exist (anymore).

    See advanced search for supported query fields and pattern matching.

    Args:
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteListResponse | ErrorResponse | str]
    """

    kwargs = _get_kwargs(
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: str,
) -> DeleteListResponse | ErrorResponse | str | None:
    """Deletes one or multiple nodes

     Deletes one or multiple nodes based on the query filter attributes given as a parameters for the
    request. All nodes
    matching the given query are removed, thus caution should be exercised when using this operation.
    The return value reflects
    the success of the whole operation, thus either all nodes are removed or none is removed in case of
    an error.

    The success of the operation is based on the requested target state, e.g. if a node deletion is
    requested based on UUID
    of the node, the operation for that node is successful also in a case where the given node does not
    exist (anymore).

    See advanced search for supported query fields and pattern matching.

    Args:
        query (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteListResponse | ErrorResponse | str
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
        )
    ).parsed
