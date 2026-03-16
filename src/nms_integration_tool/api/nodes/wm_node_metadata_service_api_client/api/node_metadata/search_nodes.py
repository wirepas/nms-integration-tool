from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.search_nodes_body import SearchNodesBody
from ...models.search_nodes_response_200 import SearchNodesResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: SearchNodesBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/metadata/nodes/search",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SearchNodesResponse200 | str:
    if response.status_code == 200:
        response_200 = SearchNodesResponse200.from_dict(response.json())

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
) -> Response[ErrorResponse | SearchNodesResponse200 | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchNodesBody,
) -> Response[ErrorResponse | SearchNodesResponse200 | str]:
    r"""Advanced search of nodes

     Search for nodes with complex query parameters and conditions. The filtering and search conditions
    are defined
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
    will return the nodes
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    As a special case, `sinkNodeInfo` field can be used for querying sink vs \"normal\" (non-sink) nodes
    as follows:

    - Filter `sinkNodeInfo.sinkGatewayUuid!=*` matches \"normal\" (non-sink) nodes
    - Filter `sinkNodeInfo.sinkGatewayUuid==*` matches only sink nodes

    The query rules shall use the property field names of the Node resource/object. Currently, following
    fields are not
    supported in the query filtering:

    - Contents of `serviceRefs` cannot be used (these should be queried via the respective service APIs)

    Args:
        body (SearchNodesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchNodesResponse200 | str]
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
    body: SearchNodesBody,
) -> ErrorResponse | SearchNodesResponse200 | str | None:
    r"""Advanced search of nodes

     Search for nodes with complex query parameters and conditions. The filtering and search conditions
    are defined
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
    will return the nodes
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    As a special case, `sinkNodeInfo` field can be used for querying sink vs \"normal\" (non-sink) nodes
    as follows:

    - Filter `sinkNodeInfo.sinkGatewayUuid!=*` matches \"normal\" (non-sink) nodes
    - Filter `sinkNodeInfo.sinkGatewayUuid==*` matches only sink nodes

    The query rules shall use the property field names of the Node resource/object. Currently, following
    fields are not
    supported in the query filtering:

    - Contents of `serviceRefs` cannot be used (these should be queried via the respective service APIs)

    Args:
        body (SearchNodesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchNodesResponse200 | str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SearchNodesBody,
) -> Response[ErrorResponse | SearchNodesResponse200 | str]:
    r"""Advanced search of nodes

     Search for nodes with complex query parameters and conditions. The filtering and search conditions
    are defined
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
    will return the nodes
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    As a special case, `sinkNodeInfo` field can be used for querying sink vs \"normal\" (non-sink) nodes
    as follows:

    - Filter `sinkNodeInfo.sinkGatewayUuid!=*` matches \"normal\" (non-sink) nodes
    - Filter `sinkNodeInfo.sinkGatewayUuid==*` matches only sink nodes

    The query rules shall use the property field names of the Node resource/object. Currently, following
    fields are not
    supported in the query filtering:

    - Contents of `serviceRefs` cannot be used (these should be queried via the respective service APIs)

    Args:
        body (SearchNodesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SearchNodesResponse200 | str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SearchNodesBody,
) -> ErrorResponse | SearchNodesResponse200 | str | None:
    r"""Advanced search of nodes

     Search for nodes with complex query parameters and conditions. The filtering and search conditions
    are defined
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
    will return the nodes
    linked to the given location(s) AND all its/their subsequent children from the location hierarchy
    tree. The location hierarchy
    is considered for both inclusions and exclusions.

    As a special case, `sinkNodeInfo` field can be used for querying sink vs \"normal\" (non-sink) nodes
    as follows:

    - Filter `sinkNodeInfo.sinkGatewayUuid!=*` matches \"normal\" (non-sink) nodes
    - Filter `sinkNodeInfo.sinkGatewayUuid==*` matches only sink nodes

    The query rules shall use the property field names of the Node resource/object. Currently, following
    fields are not
    supported in the query filtering:

    - Contents of `serviceRefs` cannot be used (these should be queried via the respective service APIs)

    Args:
        body (SearchNodesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SearchNodesResponse200 | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
