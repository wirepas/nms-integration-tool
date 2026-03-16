from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.location import Location
from ...types import Response


def _get_kwargs(
    location_uuid: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metadata/locations/{location_uuid}".format(
            location_uuid=quote(str(location_uuid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Location | str:
    if response.status_code == 200:
        response_200 = Location.from_dict(response.json())

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
) -> Response[ErrorResponse | Location | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    location_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | Location | str]:
    """Obtain information about a location object

     Obtain information about a specific location object identified by the UUID

    Args:
        location_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Location | str]
    """

    kwargs = _get_kwargs(
        location_uuid=location_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    location_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | Location | str | None:
    """Obtain information about a location object

     Obtain information about a specific location object identified by the UUID

    Args:
        location_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Location | str
    """

    return sync_detailed(
        location_uuid=location_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    location_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | Location | str]:
    """Obtain information about a location object

     Obtain information about a specific location object identified by the UUID

    Args:
        location_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Location | str]
    """

    kwargs = _get_kwargs(
        location_uuid=location_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    location_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | Location | str | None:
    """Obtain information about a location object

     Obtain information about a specific location object identified by the UUID

    Args:
        location_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Location | str
    """

    return (
        await asyncio_detailed(
            location_uuid=location_uuid,
            client=client,
        )
    ).parsed
