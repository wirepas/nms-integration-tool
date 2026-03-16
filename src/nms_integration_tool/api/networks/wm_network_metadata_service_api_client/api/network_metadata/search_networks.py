from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.search_networks_body import SearchNetworksBody
from ...models.search_networks_response_200 import SearchNetworksResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: SearchNetworksBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/metadata/networks/search",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SearchNetworksResponse200 | str:
    if response.status_code == 200:
        response_200 = SearchNetworksResponse200.from_dict(response.json())

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
) -> Response[ErrorResponse | SearchNetworksResponse200 | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchNetworksBody,
) -> Response[ErrorResponse | SearchNetworksResponse200 | str]:
    r"""Advanced search of networks

     Search for networks with complex query parameters and conditions. The filtering and search
    conditions are defined
    in the request body using RSQL / FIQL, see short description from here:
    [https://github.com/jirutka/rsql-parser#grammar-and-semantic](https://github.com/jirutka/rsql-
    parser#grammar-and-semantic)

    It is worth pointing out that this operation does not change the server state nor it does not save
    the query.
    Instead, the operation is purposed solely for providing more freedom in the definition of complex
    search filter
    conditions in cases where the basic filtering with query parameters would end up to extremely long
    URLs.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\". Nested fields can be accessed with a dot operator
    e.g. `coordinates.latitude`.

    The query rules shall use the property field names of the Network resource/object. In order to
    utilize array type of fields
    (`linkedLocations`) in the query filter, the searched location identifier can be given by adding
    nested `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get all the networks linked
    to a specific location, following filter can be used:

    `linkedLocations.uuid==1e2f21ef-e1d9-4c66-9326-fa29d1847f2b`

    Similarly, multiple location identifiers can be given with `=in=` operator to get networks linked to
    any of the given locations,
    e.g. as follows:

    `linkedLocations.uuid=in=(1e2f21ef-e1d9-4c66-9326-fa29d1847f2b,80b43985-415a-44f2-a3e2-
    3c8c0b8b9dcd)`

    Args:
        body (SearchNetworksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchNetworksResponse200 | str]
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
    body: SearchNetworksBody,
) -> ErrorResponse | SearchNetworksResponse200 | str | None:
    r"""Advanced search of networks

     Search for networks with complex query parameters and conditions. The filtering and search
    conditions are defined
    in the request body using RSQL / FIQL, see short description from here:
    [https://github.com/jirutka/rsql-parser#grammar-and-semantic](https://github.com/jirutka/rsql-
    parser#grammar-and-semantic)

    It is worth pointing out that this operation does not change the server state nor it does not save
    the query.
    Instead, the operation is purposed solely for providing more freedom in the definition of complex
    search filter
    conditions in cases where the basic filtering with query parameters would end up to extremely long
    URLs.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\". Nested fields can be accessed with a dot operator
    e.g. `coordinates.latitude`.

    The query rules shall use the property field names of the Network resource/object. In order to
    utilize array type of fields
    (`linkedLocations`) in the query filter, the searched location identifier can be given by adding
    nested `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get all the networks linked
    to a specific location, following filter can be used:

    `linkedLocations.uuid==1e2f21ef-e1d9-4c66-9326-fa29d1847f2b`

    Similarly, multiple location identifiers can be given with `=in=` operator to get networks linked to
    any of the given locations,
    e.g. as follows:

    `linkedLocations.uuid=in=(1e2f21ef-e1d9-4c66-9326-fa29d1847f2b,80b43985-415a-44f2-a3e2-
    3c8c0b8b9dcd)`

    Args:
        body (SearchNetworksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchNetworksResponse200 | str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchNetworksBody,
) -> Response[ErrorResponse | SearchNetworksResponse200 | str]:
    r"""Advanced search of networks

     Search for networks with complex query parameters and conditions. The filtering and search
    conditions are defined
    in the request body using RSQL / FIQL, see short description from here:
    [https://github.com/jirutka/rsql-parser#grammar-and-semantic](https://github.com/jirutka/rsql-
    parser#grammar-and-semantic)

    It is worth pointing out that this operation does not change the server state nor it does not save
    the query.
    Instead, the operation is purposed solely for providing more freedom in the definition of complex
    search filter
    conditions in cases where the basic filtering with query parameters would end up to extremely long
    URLs.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\". Nested fields can be accessed with a dot operator
    e.g. `coordinates.latitude`.

    The query rules shall use the property field names of the Network resource/object. In order to
    utilize array type of fields
    (`linkedLocations`) in the query filter, the searched location identifier can be given by adding
    nested `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get all the networks linked
    to a specific location, following filter can be used:

    `linkedLocations.uuid==1e2f21ef-e1d9-4c66-9326-fa29d1847f2b`

    Similarly, multiple location identifiers can be given with `=in=` operator to get networks linked to
    any of the given locations,
    e.g. as follows:

    `linkedLocations.uuid=in=(1e2f21ef-e1d9-4c66-9326-fa29d1847f2b,80b43985-415a-44f2-a3e2-
    3c8c0b8b9dcd)`

    Args:
        body (SearchNetworksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchNetworksResponse200 | str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SearchNetworksBody,
) -> ErrorResponse | SearchNetworksResponse200 | str | None:
    r"""Advanced search of networks

     Search for networks with complex query parameters and conditions. The filtering and search
    conditions are defined
    in the request body using RSQL / FIQL, see short description from here:
    [https://github.com/jirutka/rsql-parser#grammar-and-semantic](https://github.com/jirutka/rsql-
    parser#grammar-and-semantic)

    It is worth pointing out that this operation does not change the server state nor it does not save
    the query.
    Instead, the operation is purposed solely for providing more freedom in the definition of complex
    search filter
    conditions in cases where the basic filtering with query parameters would end up to extremely long
    URLs.

    Queries are case-insensitive. Pattern matching is supported in the query: an asterisk sign ('*') can
    be used to match zero
    or more arbitrary characters. Plain asterisk query (e.g. `name==*`) can be used for excluding null
    items.

    If your operator is one of following <, >, <= or >= and your comparison string is only digits you
    can use \"str(string)\" to ensure
    it is treated as a string e.g. name>=\"str(123)\". Nested fields can be accessed with a dot operator
    e.g. `coordinates.latitude`.

    The query rules shall use the property field names of the Network resource/object. In order to
    utilize array type of fields
    (`linkedLocations`) in the query filter, the searched location identifier can be given by adding
    nested `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get all the networks linked
    to a specific location, following filter can be used:

    `linkedLocations.uuid==1e2f21ef-e1d9-4c66-9326-fa29d1847f2b`

    Similarly, multiple location identifiers can be given with `=in=` operator to get networks linked to
    any of the given locations,
    e.g. as follows:

    `linkedLocations.uuid=in=(1e2f21ef-e1d9-4c66-9326-fa29d1847f2b,80b43985-415a-44f2-a3e2-
    3c8c0b8b9dcd)`

    Args:
        body (SearchNetworksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchNetworksResponse200 | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
