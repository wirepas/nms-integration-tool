from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.search_gateways_body import SearchGatewaysBody
from ...models.search_gateways_response_200 import SearchGatewaysResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: SearchGatewaysBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/metadata/gateways/search",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SearchGatewaysResponse200 | str:
    if response.status_code == 200:
        response_200 = SearchGatewaysResponse200.from_dict(response.json())

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
) -> Response[ErrorResponse | SearchGatewaysResponse200 | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchGatewaysBody,
) -> Response[ErrorResponse | SearchGatewaysResponse200 | str]:
    r"""Advanced search of gateways

     Search for gateways with complex query parameters and conditions. The filtering and search
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

    If the `locationUuid` field, either single or as an array, is used in the search filter, the query
    will return the gateways
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    The query rules shall use the property field names of the Gateway resource/object. In order to
    utilize array type of fields
    (`sinkNodes`) in the query filter, the searched sink node identifier can be given by adding nested
    `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get a gateway with a
    specific sink node, following filter can be used:

    `sinkNodes.uuid==af1168ea-5a3b-4814-9a02-f107be9ff244`

    Similarly, multiple sink nodes can be given with `=in=` operator to get gateway(s) with given sink
    nodes, e.g. as follows:

    `sinkNodes.uuid=in=(af1168ea-5a3b-4814-9a02-f107be9ff244,be5d0bf5-7218-43d9-9d21-a61c2a615996)`

    Args:
        body (SearchGatewaysBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchGatewaysResponse200 | str]
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
    body: SearchGatewaysBody,
) -> ErrorResponse | SearchGatewaysResponse200 | str | None:
    r"""Advanced search of gateways

     Search for gateways with complex query parameters and conditions. The filtering and search
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

    If the `locationUuid` field, either single or as an array, is used in the search filter, the query
    will return the gateways
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    The query rules shall use the property field names of the Gateway resource/object. In order to
    utilize array type of fields
    (`sinkNodes`) in the query filter, the searched sink node identifier can be given by adding nested
    `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get a gateway with a
    specific sink node, following filter can be used:

    `sinkNodes.uuid==af1168ea-5a3b-4814-9a02-f107be9ff244`

    Similarly, multiple sink nodes can be given with `=in=` operator to get gateway(s) with given sink
    nodes, e.g. as follows:

    `sinkNodes.uuid=in=(af1168ea-5a3b-4814-9a02-f107be9ff244,be5d0bf5-7218-43d9-9d21-a61c2a615996)`

    Args:
        body (SearchGatewaysBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchGatewaysResponse200 | str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchGatewaysBody,
) -> Response[ErrorResponse | SearchGatewaysResponse200 | str]:
    r"""Advanced search of gateways

     Search for gateways with complex query parameters and conditions. The filtering and search
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

    If the `locationUuid` field, either single or as an array, is used in the search filter, the query
    will return the gateways
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    The query rules shall use the property field names of the Gateway resource/object. In order to
    utilize array type of fields
    (`sinkNodes`) in the query filter, the searched sink node identifier can be given by adding nested
    `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get a gateway with a
    specific sink node, following filter can be used:

    `sinkNodes.uuid==af1168ea-5a3b-4814-9a02-f107be9ff244`

    Similarly, multiple sink nodes can be given with `=in=` operator to get gateway(s) with given sink
    nodes, e.g. as follows:

    `sinkNodes.uuid=in=(af1168ea-5a3b-4814-9a02-f107be9ff244,be5d0bf5-7218-43d9-9d21-a61c2a615996)`

    Args:
        body (SearchGatewaysBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchGatewaysResponse200 | str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SearchGatewaysBody,
) -> ErrorResponse | SearchGatewaysResponse200 | str | None:
    r"""Advanced search of gateways

     Search for gateways with complex query parameters and conditions. The filtering and search
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

    If the `locationUuid` field, either single or as an array, is used in the search filter, the query
    will return the gateways
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    The query rules shall use the property field names of the Gateway resource/object. In order to
    utilize array type of fields
    (`sinkNodes`) in the query filter, the searched sink node identifier can be given by adding nested
    `uuid` to the array field
    name. It is worth noting, that even if the filter targets to certain nested array elements, the
    results contain the main object
    and all of its fields and nested elements (honoring the field selection). As an example, in order to
    get a gateway with a
    specific sink node, following filter can be used:

    `sinkNodes.uuid==af1168ea-5a3b-4814-9a02-f107be9ff244`

    Similarly, multiple sink nodes can be given with `=in=` operator to get gateway(s) with given sink
    nodes, e.g. as follows:

    `sinkNodes.uuid=in=(af1168ea-5a3b-4814-9a02-f107be9ff244,be5d0bf5-7218-43d9-9d21-a61c2a615996)`

    Args:
        body (SearchGatewaysBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchGatewaysResponse200 | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
