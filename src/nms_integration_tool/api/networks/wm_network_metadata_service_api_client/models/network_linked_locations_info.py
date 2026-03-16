from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetworkLinkedLocationsInfo")


@_attrs_define
class NetworkLinkedLocationsInfo:
    """
    Attributes:
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

    linked_locations: list[UUID] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        linked_locations: list[str] | Unset = UNSET
        if not isinstance(self.linked_locations, Unset):
            linked_locations = []
            for linked_locations_item_data in self.linked_locations:
                linked_locations_item = str(linked_locations_item_data)
                linked_locations.append(linked_locations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if linked_locations is not UNSET:
            field_dict["linkedLocations"] = linked_locations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _linked_locations = d.pop("linkedLocations", UNSET)
        linked_locations: list[UUID] | Unset = UNSET
        if _linked_locations is not UNSET:
            linked_locations = []
            for linked_locations_item_data in _linked_locations:
                linked_locations_item = UUID(linked_locations_item_data)

                linked_locations.append(linked_locations_item)

        network_linked_locations_info = cls(
            linked_locations=linked_locations,
        )

        network_linked_locations_info.additional_properties = d
        return network_linked_locations_info

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
