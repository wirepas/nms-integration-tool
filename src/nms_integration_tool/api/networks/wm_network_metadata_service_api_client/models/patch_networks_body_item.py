from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_base_object_custom import MetadataBaseObjectCustom


T = TypeVar("T", bound="PatchNetworksBodyItem")


@_attrs_define
class PatchNetworksBodyItem:
    """
    Attributes:
        uuid (UUID): Globally unique ID (UUID) used for identifying the API resource
        modification_time (int | Unset): Epoch timestamp for the last modification time of the object
        name (str | Unset): Short descriptive name for the metadata resource. If not explicitly set, the system will
            generate the
            name based on the low level identifier of the resource.
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
        address (int | Unset): Wirepas low level network address for this network (must comply with addressing
            limitations)
        linked_locations (list[UUID] | Unset): A list of locations this network is linked to. In general, the objective
            of the network level location linkage is to allow clients
            to define "top level" location(s) to which the network is roughly deployed to. However, this linkage is merely
            indicative, thus it
            does not set any constraints at the low level. Instead, the client can use the information to control the
            filtering and selection
            dialogs within the scope of this network.

            The recommendation is to use top level locations for the linkage. The implementation does not force this, but
            instead it mandates
            that all the locations linked to a given network are of same type.

            This field is not directly writable, instead, the contents can be managed via a separate per network
            `linkedLocations` endpoint.
    """

    uuid: UUID
    modification_time: int | Unset = UNSET
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    custom: MetadataBaseObjectCustom | Unset = UNSET
    address: int | Unset = UNSET
    linked_locations: list[UUID] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        modification_time = self.modification_time

        name = self.name

        description = self.description

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        address = self.address

        linked_locations: list[str] | Unset = UNSET
        if not isinstance(self.linked_locations, Unset):
            linked_locations = []
            for linked_locations_item_data in self.linked_locations:
                linked_locations_item = str(linked_locations_item_data)
                linked_locations.append(linked_locations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
            }
        )
        if modification_time is not UNSET:
            field_dict["modificationTime"] = modification_time
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if custom is not UNSET:
            field_dict["custom"] = custom
        if address is not UNSET:
            field_dict["address"] = address
        if linked_locations is not UNSET:
            field_dict["linkedLocations"] = linked_locations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_base_object_custom import MetadataBaseObjectCustom

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        modification_time = d.pop("modificationTime", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _custom = d.pop("custom", UNSET)
        custom: MetadataBaseObjectCustom | Unset
        if isinstance(_custom, Unset):
            custom = UNSET
        else:
            custom = MetadataBaseObjectCustom.from_dict(_custom)

        address = d.pop("address", UNSET)

        _linked_locations = d.pop("linkedLocations", UNSET)
        linked_locations: list[UUID] | Unset = UNSET
        if _linked_locations is not UNSET:
            linked_locations = []
            for linked_locations_item_data in _linked_locations:
                linked_locations_item = UUID(linked_locations_item_data)

                linked_locations.append(linked_locations_item)

        patch_networks_body_item = cls(
            uuid=uuid,
            modification_time=modification_time,
            name=name,
            description=description,
            custom=custom,
            address=address,
            linked_locations=linked_locations,
        )

        patch_networks_body_item.additional_properties = d
        return patch_networks_body_item

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
