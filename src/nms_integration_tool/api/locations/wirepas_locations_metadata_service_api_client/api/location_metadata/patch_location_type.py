from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.location_type import LocationType
from ...models.location_type_info import LocationTypeInfo
from ...types import Response


def _get_kwargs(
    location_type_uuid: UUID,
    *,
    body: LocationTypeInfo,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/metadata/locations/types/{location_type_uuid}".format(
            location_type_uuid=quote(str(location_type_uuid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LocationType | str:
    if response.status_code == 200:
        response_200 = LocationType.from_dict(response.json())

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
) -> Response[ErrorResponse | LocationType | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    location_type_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LocationTypeInfo,
) -> Response[ErrorResponse | LocationType | str]:
    """Partially/patch update the location type object

     Update the given fields in a specific location type object identified by UUID. It is worth noting,
    that the item given in
    the body may not be a complete location object, thus only those fields that are given are updated.

    **NOTE:** Changing the parent hierarchy is not allowed, if the location type is assigned to any
    location. This restriction
    is to prevent incorrect parent references between the actual location objects.

    Args:
        location_type_uuid (UUID):
        body (LocationTypeInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LocationType | str]
    """

    kwargs = _get_kwargs(
        location_type_uuid=location_type_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    location_type_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LocationTypeInfo,
) -> ErrorResponse | LocationType | str | None:
    """Partially/patch update the location type object

     Update the given fields in a specific location type object identified by UUID. It is worth noting,
    that the item given in
    the body may not be a complete location object, thus only those fields that are given are updated.

    **NOTE:** Changing the parent hierarchy is not allowed, if the location type is assigned to any
    location. This restriction
    is to prevent incorrect parent references between the actual location objects.

    Args:
        location_type_uuid (UUID):
        body (LocationTypeInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LocationType | str
    """

    return sync_detailed(
        location_type_uuid=location_type_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    location_type_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LocationTypeInfo,
) -> Response[ErrorResponse | LocationType | str]:
    """Partially/patch update the location type object

     Update the given fields in a specific location type object identified by UUID. It is worth noting,
    that the item given in
    the body may not be a complete location object, thus only those fields that are given are updated.

    **NOTE:** Changing the parent hierarchy is not allowed, if the location type is assigned to any
    location. This restriction
    is to prevent incorrect parent references between the actual location objects.

    Args:
        location_type_uuid (UUID):
        body (LocationTypeInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LocationType | str]
    """

    kwargs = _get_kwargs(
        location_type_uuid=location_type_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    location_type_uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: LocationTypeInfo,
) -> ErrorResponse | LocationType | str | None:
    """Partially/patch update the location type object

     Update the given fields in a specific location type object identified by UUID. It is worth noting,
    that the item given in
    the body may not be a complete location object, thus only those fields that are given are updated.

    **NOTE:** Changing the parent hierarchy is not allowed, if the location type is assigned to any
    location. This restriction
    is to prevent incorrect parent references between the actual location objects.

    Args:
        location_type_uuid (UUID):
        body (LocationTypeInfo):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LocationType | str
    """

    return (
        await asyncio_detailed(
            location_type_uuid=location_type_uuid,
            client=client,
            body=body,
        )
    ).parsed
