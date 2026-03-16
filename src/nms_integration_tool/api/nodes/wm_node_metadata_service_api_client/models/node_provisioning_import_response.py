from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.node_provisioning_import_response_errors_item import NodeProvisioningImportResponseErrorsItem


T = TypeVar("T", bound="NodeProvisioningImportResponse")


@_attrs_define
class NodeProvisioningImportResponse:
    """
    Attributes:
        imported_count (int): Number of CSV rows successfully imported
        updated_count (int): Number of existing node records updated
        created_count (int): Number of new node records created
        errors (list[NodeProvisioningImportResponseErrorsItem]): List of validation errors encountered during import
    """

    imported_count: int
    updated_count: int
    created_count: int
    errors: list[NodeProvisioningImportResponseErrorsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        imported_count = self.imported_count

        updated_count = self.updated_count

        created_count = self.created_count

        errors = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "importedCount": imported_count,
                "updatedCount": updated_count,
                "createdCount": created_count,
                "errors": errors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.node_provisioning_import_response_errors_item import NodeProvisioningImportResponseErrorsItem

        d = dict(src_dict)
        imported_count = d.pop("importedCount")

        updated_count = d.pop("updatedCount")

        created_count = d.pop("createdCount")

        errors = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = NodeProvisioningImportResponseErrorsItem.from_dict(errors_item_data)

            errors.append(errors_item)

        node_provisioning_import_response = cls(
            imported_count=imported_count,
            updated_count=updated_count,
            created_count=created_count,
            errors=errors,
        )

        node_provisioning_import_response.additional_properties = d
        return node_provisioning_import_response

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
