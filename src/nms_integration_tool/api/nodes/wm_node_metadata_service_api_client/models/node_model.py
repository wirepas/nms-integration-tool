from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node_model_coordinates import NodeModelCoordinates


T = TypeVar("T", bound="NodeModel")


@_attrs_define
class NodeModel:
    """
    Attributes:
        address (int | Unset): Wirepas node address used in the Wirepas network communications. The given address must
            be in valid address range defined
            in the field (excludes reserved address e.g. for multicast).

            It is not recommended to change the address after the resource object has been attached to a real Wirepas node.
            This does
            not change the actual address of the node but instead may associate the resource object to some other node.
            However,
            this option is left open in order to fix potential mistakes during the installation time.
        network_uuid (UUID | Unset): A reference to the network resource this node is related to
        is_virtual (bool | Unset): *DEPRECATION NOTICE: This field will be removed, since there is no support for
            placement planning available in the tool.*

            A flag that indicates that this node is not a real one but only a planned / virtual placeholder (defaults to
            false).
        location_uuid (UUID | Unset): A reference to the location resource this node is related to
        coordinates (NodeModelCoordinates | Unset):
    """

    address: int | Unset = UNSET
    network_uuid: UUID | Unset = UNSET
    is_virtual: bool | Unset = UNSET
    location_uuid: UUID | Unset = UNSET
    coordinates: NodeModelCoordinates | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address: int | Unset
        if isinstance(self.address, Unset):
            address = UNSET
        else:
            address = self.address

        network_uuid: str | Unset = UNSET
        if not isinstance(self.network_uuid, Unset):
            network_uuid = str(self.network_uuid)

        is_virtual = self.is_virtual

        location_uuid: str | Unset = UNSET
        if not isinstance(self.location_uuid, Unset):
            location_uuid = str(self.location_uuid)

        coordinates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address is not UNSET:
            field_dict["address"] = address
        if network_uuid is not UNSET:
            field_dict["networkUuid"] = network_uuid
        if is_virtual is not UNSET:
            field_dict["isVirtual"] = is_virtual
        if location_uuid is not UNSET:
            field_dict["locationUuid"] = location_uuid
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.node_model_coordinates import NodeModelCoordinates

        d = dict(src_dict)

        def _parse_address(data: object) -> int | Unset:
            if isinstance(data, Unset):
                return data
            return cast(int | Unset, data)

        address = _parse_address(d.pop("address", UNSET))

        _network_uuid = d.pop("networkUuid", UNSET)
        network_uuid: UUID | Unset
        if isinstance(_network_uuid, Unset):
            network_uuid = UNSET
        else:
            network_uuid = UUID(_network_uuid)

        is_virtual = d.pop("isVirtual", UNSET)

        _location_uuid = d.pop("locationUuid", UNSET)
        location_uuid: UUID | Unset
        if isinstance(_location_uuid, Unset):
            location_uuid = UNSET
        else:
            location_uuid = UUID(_location_uuid)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: NodeModelCoordinates | Unset
        if isinstance(_coordinates, Unset):
            coordinates = UNSET
        else:
            coordinates = NodeModelCoordinates.from_dict(_coordinates)

        node_model = cls(
            address=address,
            network_uuid=network_uuid,
            is_virtual=is_virtual,
            location_uuid=location_uuid,
            coordinates=coordinates,
        )

        node_model.additional_properties = d
        return node_model

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
