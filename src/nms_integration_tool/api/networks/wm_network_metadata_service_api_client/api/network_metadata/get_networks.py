from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.get_networks_order import GetNetworksOrder
from ...models.get_networks_response_200 import GetNetworksResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 1000,
    cursor: str | Unset = UNSET,
    query: str | Unset = UNSET,
    order: GetNetworksOrder | Unset = GetNetworksOrder.ASC,
    fields: list[str] | Unset = UNSET,
    total_results_count_only: bool | Unset = UNSET,
    sort_by: str | Unset = "name",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params["query"] = query

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params["totalResultsCountOnly"] = total_results_count_only

    params["sortBy"] = sort_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metadata/networks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GetNetworksResponse200 | str:
    if response.status_code == 200:
        response_200 = GetNetworksResponse200.from_dict(response.json())

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
) -> Response[ErrorResponse | GetNetworksResponse200 | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 1000,
    cursor: str | Unset = UNSET,
    query: str | Unset = UNSET,
    order: GetNetworksOrder | Unset = GetNetworksOrder.ASC,
    fields: list[str] | Unset = UNSET,
    total_results_count_only: bool | Unset = UNSET,
    sort_by: str | Unset = "name",
) -> Response[ErrorResponse | GetNetworksResponse200 | str]:
    """Get a list of networks

     Return list of managed Wirepas Mesh networks. In general, client shall sort and page the results
    accordingly
    to avoid excess load on the service and communications media.

    This endpoint supports simple queries with reasonable set of different filter parameters. In case of
    more
    complex queries, separate search endpoint shall be used.

    See advanced search for supported query fields and pattern matching.

    Args:
        limit (int | Unset):  Default: 1000.
        cursor (str | Unset):
        query (str | Unset):
        order (GetNetworksOrder | Unset):  Default: GetNetworksOrder.ASC.
        fields (list[str] | Unset):
        total_results_count_only (bool | Unset):
        sort_by (str | Unset):  Default: 'name'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetNetworksResponse200 | str]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        query=query,
        order=order,
        fields=fields,
        total_results_count_only=total_results_count_only,
        sort_by=sort_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 1000,
    cursor: str | Unset = UNSET,
    query: str | Unset = UNSET,
    order: GetNetworksOrder | Unset = GetNetworksOrder.ASC,
    fields: list[str] | Unset = UNSET,
    total_results_count_only: bool | Unset = UNSET,
    sort_by: str | Unset = "name",
) -> ErrorResponse | GetNetworksResponse200 | str | None:
    """Get a list of networks

     Return list of managed Wirepas Mesh networks. In general, client shall sort and page the results
    accordingly
    to avoid excess load on the service and communications media.

    This endpoint supports simple queries with reasonable set of different filter parameters. In case of
    more
    complex queries, separate search endpoint shall be used.

    See advanced search for supported query fields and pattern matching.

    Args:
        limit (int | Unset):  Default: 1000.
        cursor (str | Unset):
        query (str | Unset):
        order (GetNetworksOrder | Unset):  Default: GetNetworksOrder.ASC.
        fields (list[str] | Unset):
        total_results_count_only (bool | Unset):
        sort_by (str | Unset):  Default: 'name'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetNetworksResponse200 | str
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        query=query,
        order=order,
        fields=fields,
        total_results_count_only=total_results_count_only,
        sort_by=sort_by,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 1000,
    cursor: str | Unset = UNSET,
    query: str | Unset = UNSET,
    order: GetNetworksOrder | Unset = GetNetworksOrder.ASC,
    fields: list[str] | Unset = UNSET,
    total_results_count_only: bool | Unset = UNSET,
    sort_by: str | Unset = "name",
) -> Response[ErrorResponse | GetNetworksResponse200 | str]:
    """Get a list of networks

     Return list of managed Wirepas Mesh networks. In general, client shall sort and page the results
    accordingly
    to avoid excess load on the service and communications media.

    This endpoint supports simple queries with reasonable set of different filter parameters. In case of
    more
    complex queries, separate search endpoint shall be used.

    See advanced search for supported query fields and pattern matching.

    Args:
        limit (int | Unset):  Default: 1000.
        cursor (str | Unset):
        query (str | Unset):
        order (GetNetworksOrder | Unset):  Default: GetNetworksOrder.ASC.
        fields (list[str] | Unset):
        total_results_count_only (bool | Unset):
        sort_by (str | Unset):  Default: 'name'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetNetworksResponse200 | str]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        query=query,
        order=order,
        fields=fields,
        total_results_count_only=total_results_count_only,
        sort_by=sort_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 1000,
    cursor: str | Unset = UNSET,
    query: str | Unset = UNSET,
    order: GetNetworksOrder | Unset = GetNetworksOrder.ASC,
    fields: list[str] | Unset = UNSET,
    total_results_count_only: bool | Unset = UNSET,
    sort_by: str | Unset = "name",
) -> ErrorResponse | GetNetworksResponse200 | str | None:
    """Get a list of networks

     Return list of managed Wirepas Mesh networks. In general, client shall sort and page the results
    accordingly
    to avoid excess load on the service and communications media.

    This endpoint supports simple queries with reasonable set of different filter parameters. In case of
    more
    complex queries, separate search endpoint shall be used.

    See advanced search for supported query fields and pattern matching.

    Args:
        limit (int | Unset):  Default: 1000.
        cursor (str | Unset):
        query (str | Unset):
        order (GetNetworksOrder | Unset):  Default: GetNetworksOrder.ASC.
        fields (list[str] | Unset):
        total_results_count_only (bool | Unset):
        sort_by (str | Unset):  Default: 'name'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetNetworksResponse200 | str
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            query=query,
            order=order,
            fields=fields,
            total_results_count_only=total_results_count_only,
            sort_by=sort_by,
        )
    ).parsed
