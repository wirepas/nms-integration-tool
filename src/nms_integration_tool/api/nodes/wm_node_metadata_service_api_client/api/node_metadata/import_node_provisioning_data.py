from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.import_node_provisioning_data_body import ImportNodeProvisioningDataBody
from ...models.node_provisioning_import_response import NodeProvisioningImportResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ImportNodeProvisioningDataBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/metadata/nodes/import",
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | NodeProvisioningImportResponse | str:
    if response.status_code == 201:
        response_201 = NodeProvisioningImportResponse.from_dict(response.json())

        return response_201

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
) -> Response[ErrorResponse | NodeProvisioningImportResponse | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ImportNodeProvisioningDataBody,
) -> Response[ErrorResponse | NodeProvisioningImportResponse | str]:
    """Import node provisioning data (CSV)

     Uploads a CSV file containing rows of per-device provisioning data (UID and per-device
    authentication and encryption keys).
    Depending on the system configuration, the CSV file whole content is required to be either plain
    text or encrypted
    with Wirepas NMS specific (public) key.

    The CSV file must have a header row, which defines the contents for the rows within the file.
    The header row in the file must be the first data row in the file (comments can be added with '#').
    The fields/columns in the CSV are classified to mandatory and optional ones. The order of the
    fields is not relevant, but will be defined by the header row.

    The mandatory fields in the CSV are following:

      - `uid`: Individual identifier (UUIDv4) for the node, used for device identification and
    whitelisting.
      - `authenticationKey`: Device specific base64 encoded 128-bit AES key used for message integrity
    checking during provisioning.
      - `encryptionKey`: Device specific base64 encoded 128-bit AES key used for message encryption and
    decryption checking during provisioning.

    The optional fields in the CSV file facilitate the mapping of the imported information to existing
    nodes.
    These fields can be populated, when the devices are pre-provisioned with the needed data. When
    provided
    both fields shall be given:

      - `networkAddress`: Wirepas Mesh network address pre-provisioned to the node during manufacturing
      - `nodeAddress`: Individual node address pre-provisioned to the node during manufacturing

    **NOTE:** Provided network addresses are expected to be found from the system, i.e. new networks are
    not created based on imported data.

    Generally, the CSV file is required to be encrypted, in which case the following-encryption scheme
    must be followed:

      - The user must first generate a AES-256 encryption key.
      - The user encrypts the AES key with Wirepas NMS public key and save to a file with extension
    `.key`
      - The user encrypts the raw CSV file with the raw AES key and save it to a file. The file's
    extension must not be `.key`
      - The user creates a .tar tarball file for upload consists of exactly those 2 files.

    There is a helper script provided as a reference for this encryption and packaging scheme. More
    information related to this
    can be found from the user guide documentation.

    Args:
        body (ImportNodeProvisioningDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | NodeProvisioningImportResponse | str]
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
    body: ImportNodeProvisioningDataBody,
) -> ErrorResponse | NodeProvisioningImportResponse | str | None:
    """Import node provisioning data (CSV)

     Uploads a CSV file containing rows of per-device provisioning data (UID and per-device
    authentication and encryption keys).
    Depending on the system configuration, the CSV file whole content is required to be either plain
    text or encrypted
    with Wirepas NMS specific (public) key.

    The CSV file must have a header row, which defines the contents for the rows within the file.
    The header row in the file must be the first data row in the file (comments can be added with '#').
    The fields/columns in the CSV are classified to mandatory and optional ones. The order of the
    fields is not relevant, but will be defined by the header row.

    The mandatory fields in the CSV are following:

      - `uid`: Individual identifier (UUIDv4) for the node, used for device identification and
    whitelisting.
      - `authenticationKey`: Device specific base64 encoded 128-bit AES key used for message integrity
    checking during provisioning.
      - `encryptionKey`: Device specific base64 encoded 128-bit AES key used for message encryption and
    decryption checking during provisioning.

    The optional fields in the CSV file facilitate the mapping of the imported information to existing
    nodes.
    These fields can be populated, when the devices are pre-provisioned with the needed data. When
    provided
    both fields shall be given:

      - `networkAddress`: Wirepas Mesh network address pre-provisioned to the node during manufacturing
      - `nodeAddress`: Individual node address pre-provisioned to the node during manufacturing

    **NOTE:** Provided network addresses are expected to be found from the system, i.e. new networks are
    not created based on imported data.

    Generally, the CSV file is required to be encrypted, in which case the following-encryption scheme
    must be followed:

      - The user must first generate a AES-256 encryption key.
      - The user encrypts the AES key with Wirepas NMS public key and save to a file with extension
    `.key`
      - The user encrypts the raw CSV file with the raw AES key and save it to a file. The file's
    extension must not be `.key`
      - The user creates a .tar tarball file for upload consists of exactly those 2 files.

    There is a helper script provided as a reference for this encryption and packaging scheme. More
    information related to this
    can be found from the user guide documentation.

    Args:
        body (ImportNodeProvisioningDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | NodeProvisioningImportResponse | str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ImportNodeProvisioningDataBody,
) -> Response[ErrorResponse | NodeProvisioningImportResponse | str]:
    """Import node provisioning data (CSV)

     Uploads a CSV file containing rows of per-device provisioning data (UID and per-device
    authentication and encryption keys).
    Depending on the system configuration, the CSV file whole content is required to be either plain
    text or encrypted
    with Wirepas NMS specific (public) key.

    The CSV file must have a header row, which defines the contents for the rows within the file.
    The header row in the file must be the first data row in the file (comments can be added with '#').
    The fields/columns in the CSV are classified to mandatory and optional ones. The order of the
    fields is not relevant, but will be defined by the header row.

    The mandatory fields in the CSV are following:

      - `uid`: Individual identifier (UUIDv4) for the node, used for device identification and
    whitelisting.
      - `authenticationKey`: Device specific base64 encoded 128-bit AES key used for message integrity
    checking during provisioning.
      - `encryptionKey`: Device specific base64 encoded 128-bit AES key used for message encryption and
    decryption checking during provisioning.

    The optional fields in the CSV file facilitate the mapping of the imported information to existing
    nodes.
    These fields can be populated, when the devices are pre-provisioned with the needed data. When
    provided
    both fields shall be given:

      - `networkAddress`: Wirepas Mesh network address pre-provisioned to the node during manufacturing
      - `nodeAddress`: Individual node address pre-provisioned to the node during manufacturing

    **NOTE:** Provided network addresses are expected to be found from the system, i.e. new networks are
    not created based on imported data.

    Generally, the CSV file is required to be encrypted, in which case the following-encryption scheme
    must be followed:

      - The user must first generate a AES-256 encryption key.
      - The user encrypts the AES key with Wirepas NMS public key and save to a file with extension
    `.key`
      - The user encrypts the raw CSV file with the raw AES key and save it to a file. The file's
    extension must not be `.key`
      - The user creates a .tar tarball file for upload consists of exactly those 2 files.

    There is a helper script provided as a reference for this encryption and packaging scheme. More
    information related to this
    can be found from the user guide documentation.

    Args:
        body (ImportNodeProvisioningDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | NodeProvisioningImportResponse | str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ImportNodeProvisioningDataBody,
) -> ErrorResponse | NodeProvisioningImportResponse | str | None:
    """Import node provisioning data (CSV)

     Uploads a CSV file containing rows of per-device provisioning data (UID and per-device
    authentication and encryption keys).
    Depending on the system configuration, the CSV file whole content is required to be either plain
    text or encrypted
    with Wirepas NMS specific (public) key.

    The CSV file must have a header row, which defines the contents for the rows within the file.
    The header row in the file must be the first data row in the file (comments can be added with '#').
    The fields/columns in the CSV are classified to mandatory and optional ones. The order of the
    fields is not relevant, but will be defined by the header row.

    The mandatory fields in the CSV are following:

      - `uid`: Individual identifier (UUIDv4) for the node, used for device identification and
    whitelisting.
      - `authenticationKey`: Device specific base64 encoded 128-bit AES key used for message integrity
    checking during provisioning.
      - `encryptionKey`: Device specific base64 encoded 128-bit AES key used for message encryption and
    decryption checking during provisioning.

    The optional fields in the CSV file facilitate the mapping of the imported information to existing
    nodes.
    These fields can be populated, when the devices are pre-provisioned with the needed data. When
    provided
    both fields shall be given:

      - `networkAddress`: Wirepas Mesh network address pre-provisioned to the node during manufacturing
      - `nodeAddress`: Individual node address pre-provisioned to the node during manufacturing

    **NOTE:** Provided network addresses are expected to be found from the system, i.e. new networks are
    not created based on imported data.

    Generally, the CSV file is required to be encrypted, in which case the following-encryption scheme
    must be followed:

      - The user must first generate a AES-256 encryption key.
      - The user encrypts the AES key with Wirepas NMS public key and save to a file with extension
    `.key`
      - The user encrypts the raw CSV file with the raw AES key and save it to a file. The file's
    extension must not be `.key`
      - The user creates a .tar tarball file for upload consists of exactly those 2 files.

    There is a helper script provided as a reference for this encryption and packaging scheme. More
    information related to this
    can be found from the user guide documentation.

    Args:
        body (ImportNodeProvisioningDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | NodeProvisioningImportResponse | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
