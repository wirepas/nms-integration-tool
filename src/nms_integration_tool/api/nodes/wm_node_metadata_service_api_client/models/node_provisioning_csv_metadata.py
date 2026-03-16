from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NodeProvisioningCsvMetadata")


@_attrs_define
class NodeProvisioningCsvMetadata:
    """Metadata characterizing the provisioning CSV file content.
    Notice that when this is passed on multipart requests this is a non-file field (without a filename) i.e. is a plain
    string.

        Attributes:
            md_5_checksum (str): MD5 checksum over the whole binary data content. The checksum information is used to first
                to make sure that server
                receives the CSV file data without errors.
    """

    md_5_checksum: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        md_5_checksum = self.md_5_checksum

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "md5Checksum": md_5_checksum,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        md_5_checksum = d.pop("md5Checksum")

        node_provisioning_csv_metadata = cls(
            md_5_checksum=md_5_checksum,
        )

        node_provisioning_csv_metadata.additional_properties = d
        return node_provisioning_csv_metadata

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
