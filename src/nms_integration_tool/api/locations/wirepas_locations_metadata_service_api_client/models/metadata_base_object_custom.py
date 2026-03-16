from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MetadataBaseObjectCustom")


@_attrs_define
class MetadataBaseObjectCustom:
    """A freeform dictionary that clients can utilize for storing their own metadata related to the managed resource.
    The main intention of the custom fields is to allow clients to manage the relations between the client side data
    objects and corresponding Wirepas NMS data object. Thus, client can e.g. add a custom field for storing the
    internal identifier of managed asset to which the corresponding Wirepas node or gateway is linked to. Naturally,
    as the fields are fully customizable other usage purposes are possible.

    The data management of the custom fields differ slightly from other fields or attributes in managed resources or
    objects. The main difference is that the contents of `custom` field itself shall always be considered as single
    managed field. Thus, when adding new fields as well as when updating or removing existing fields to/from the
    `custom`,
    all the custom fields shall be given. I.e. the provided custom fields directly reflect the end state of the whole
    `custom` field after the operation. This is mainly relevant for PATCH update operations, which differ from other
    fields.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_base_object_custom = cls()

        metadata_base_object_custom.additional_properties = d
        return metadata_base_object_custom

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
