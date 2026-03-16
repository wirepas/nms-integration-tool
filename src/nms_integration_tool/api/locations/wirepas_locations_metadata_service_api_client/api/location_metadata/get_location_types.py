from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.location_type import LocationType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    query: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metadata/locations/types",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[LocationType] | str:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = LocationType.from_dict(response_200_item_data)

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
) -> Response[ErrorResponse | list[LocationType] | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: str | Unset = UNSET,
) -> Response[ErrorResponse | list[LocationType] | str]:
    r"""Get a list of location types

     Returns list of location types. It is expected that the number of location types is rather limited,
    thus paging and
    sorting of the results is not supported. Filtering of the results is according to different
    attributes is supported.
    The filtering conditions are defined in the query parameter using RSQL / FIQL, see more details from
    query filter
    description.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\".

    The query rules shall use the property field names of the location type resource.

    Args:
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[LocationType] | str]
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
    query: str | Unset = UNSET,
) -> ErrorResponse | list[LocationType] | str | None:
    r"""Get a list of location types

     Returns list of location types. It is expected that the number of location types is rather limited,
    thus paging and
    sorting of the results is not supported. Filtering of the results is according to different
    attributes is supported.
    The filtering conditions are defined in the query parameter using RSQL / FIQL, see more details from
    query filter
    description.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\".

    The query rules shall use the property field names of the location type resource.

    Args:
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[LocationType] | str
    """

    return sync_detailed(
        client=client,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: str | Unset = UNSET,
) -> Response[ErrorResponse | list[LocationType] | str]:
    r"""Get a list of location types

     Returns list of location types. It is expected that the number of location types is rather limited,
    thus paging and
    sorting of the results is not supported. Filtering of the results is according to different
    attributes is supported.
    The filtering conditions are defined in the query parameter using RSQL / FIQL, see more details from
    query filter
    description.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\".

    The query rules shall use the property field names of the location type resource.

    Args:
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[LocationType] | str]
    """

    kwargs = _get_kwargs(
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: str | Unset = UNSET,
) -> ErrorResponse | list[LocationType] | str | None:
    r"""Get a list of location types

     Returns list of location types. It is expected that the number of location types is rather limited,
    thus paging and
    sorting of the results is not supported. Filtering of the results is according to different
    attributes is supported.
    The filtering conditions are defined in the query parameter using RSQL / FIQL, see more details from
    query filter
    description.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\".

    The query rules shall use the property field names of the location type resource.

    Args:
        query (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[LocationType] | str
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
        )
    ).parsed
