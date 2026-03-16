from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delete_list_response_metadata import DeleteListResponseMetadata


T = TypeVar("T", bound="DeleteListResponse")


@_attrs_define
class DeleteListResponse:
    """List of deleted items and metadata related to the delete operation

    Attributes:
        deleted_items (list[UUID]): The list of UUIDs identifying the items that were deleted.
        metadata (DeleteListResponseMetadata): Metadata about the delete operation
    """

    deleted_items: list[UUID]
    metadata: DeleteListResponseMetadata
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted_items = []
        for deleted_items_item_data in self.deleted_items:
            deleted_items_item = str(deleted_items_item_data)
            deleted_items.append(deleted_items_item)

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deletedItems": deleted_items,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delete_list_response_metadata import DeleteListResponseMetadata

        d = dict(src_dict)
        deleted_items = []
        _deleted_items = d.pop("deletedItems")
        for deleted_items_item_data in _deleted_items:
            deleted_items_item = UUID(deleted_items_item_data)

            deleted_items.append(deleted_items_item)

        metadata = DeleteListResponseMetadata.from_dict(d.pop("metadata"))

        delete_list_response = cls(
            deleted_items=deleted_items,
            metadata=metadata,
        )

        delete_list_response.additional_properties = d
        return delete_list_response

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
