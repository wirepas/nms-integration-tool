from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_base_object_custom import MetadataBaseObjectCustom


T = TypeVar("T", bound="UpdateNetworkBody")


@_attrs_define
class UpdateNetworkBody:
    """
    Attributes:
        name (str): Short descriptive name for the metadata resource. If not explicitly set, the system will generate
            the
            name based on the low level identifier of the resource.
        address (int): Wirepas low level network address for this network (must comply with addressing limitations)
        description (str | Unset): More versatile description of the metadata resource. This is optional information,
            i.e. there is no
            default content for this field.
        custom (MetadataBaseObjectCustom | Unset): A freeform dictionary that clients can utilize for storing their own
            metadata related to the managed resource.
            The main intention of the custom fields is to allow clients to manage the relations between the client side data
            objects and corresponding Wirepas NMS data object. Thus, client can e.g. add a custom field for storing the
            internal identifier of managed asset to which the corresponding Wirepas node or gateway is linked to. Naturally,
            as the fields are fully customizable other usage purposes are possible.

            The data management of the custom fields differ slightly from other fields or attributes in managed resources or
            objects. The main difference is that the contents of `custom` field itself shall always be considered as single
            managed field. Thus, when adding new fields as well as when updating or removing existing fields to/from the
            `custom`,
            all the custom fields shall be given. I.e. the provided custom fields directly reflect the end state of the
            whole
            `custom` field after the operation. This is mainly relevant for PATCH update operations, which differ from other
            fields.
    """

    name: str
    address: int
    description: str | Unset = UNSET
    custom: MetadataBaseObjectCustom | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        address = self.address

        description = self.description

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "address": address,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if custom is not UNSET:
            field_dict["custom"] = custom

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_base_object_custom import MetadataBaseObjectCustom

        d = dict(src_dict)
        name = d.pop("name")

        address = d.pop("address")

        description = d.pop("description", UNSET)

        _custom = d.pop("custom", UNSET)
        custom: MetadataBaseObjectCustom | Unset
        if isinstance(_custom, Unset):
            custom = UNSET
        else:
            custom = MetadataBaseObjectCustom.from_dict(_custom)

        update_network_body = cls(
            name=name,
            address=address,
            description=description,
            custom=custom,
        )

        update_network_body.additional_properties = d
        return update_network_body

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
