from __future__ import annotations

import json
from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import File

if TYPE_CHECKING:
    from ..models.node_provisioning_csv_metadata import NodeProvisioningCsvMetadata


T = TypeVar("T", bound="ImportNodeProvisioningDataBody")


@_attrs_define
class ImportNodeProvisioningDataBody:
    """
    Attributes:
        provisioning_csv_metadata (NodeProvisioningCsvMetadata): Metadata characterizing the provisioning CSV file
            content.
            Notice that when this is passed on multipart requests this is a non-file field (without a filename) i.e. is a
            plain string.
        provisioning_csv_data (File): CSV file content. Header row is mandatory and must match one of the supported
            layouts.
            System configuration might require the file to be encrypted with NMS public key.
    """

    provisioning_csv_metadata: NodeProvisioningCsvMetadata
    provisioning_csv_data: File
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provisioning_csv_metadata = self.provisioning_csv_metadata.to_dict()

        provisioning_csv_data = self.provisioning_csv_data.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provisioningCsvMetadata": provisioning_csv_metadata,
                "provisioningCsvData": provisioning_csv_data,
            }
        )

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(
            (
                "provisioningCsvMetadata",
                (None, json.dumps(self.provisioning_csv_metadata.to_dict()).encode(), "application/json"),
            )
        )

        files.append(("provisioningCsvData", self.provisioning_csv_data.to_tuple()))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.node_provisioning_csv_metadata import NodeProvisioningCsvMetadata

        d = dict(src_dict)
        provisioning_csv_metadata = NodeProvisioningCsvMetadata.from_dict(d.pop("provisioningCsvMetadata"))

        provisioning_csv_data = File(payload=BytesIO(d.pop("provisioningCsvData")))

        import_node_provisioning_data_body = cls(
            provisioning_csv_metadata=provisioning_csv_metadata,
            provisioning_csv_data=provisioning_csv_data,
        )

        import_node_provisioning_data_body.additional_properties = d
        return import_node_provisioning_data_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
