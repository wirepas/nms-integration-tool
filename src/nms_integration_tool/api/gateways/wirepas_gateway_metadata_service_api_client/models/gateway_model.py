from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gateway_model_coordinates import GatewayModelCoordinates


T = TypeVar("T", bound="GatewayModel")


@_attrs_define
class GatewayModel:
    """
    Attributes:
        gateway_id (str | Unset): Gateway identifier provided by the vendor / installer. Identifier is expected to be
            unique in the context of a
            system.

            This value is defined at gateway configuration/installation time. After the initial handshake with the gateway,
            any changes to the field value do not affect to the actual gateway, instead they may change the association of
            this
            gateway resource to some other device. This is not recommended operation, but is allowed in order to remediate
            potential
            configuration mistakes.

            **NOTE:** This information is used for mapping the device communications to the gateway object, thus when
            creating (or updating with PUT) a gateway object, this information needs to be always provided.
        is_virtual (bool | Unset): *DEPRECATION NOTICE: This field will be removed, since there is no support for
            placement planning available in the tool.*

            A flag that indicates that this gateway is not a real one but only a planned / virtual placeholder (defaults to
            false).
        location_uuid (UUID | Unset): A reference to the location resource this gateway is related to
        network_uuid (UUID | Unset): A reference to the network resource this gateway is related to
        coordinates (GatewayModelCoordinates | Unset):
    """

    gateway_id: str | Unset = UNSET
    is_virtual: bool | Unset = UNSET
    location_uuid: UUID | Unset = UNSET
    network_uuid: UUID | Unset = UNSET
    coordinates: GatewayModelCoordinates | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gateway_id = self.gateway_id

        is_virtual = self.is_virtual

        location_uuid: str | Unset = UNSET
        if not isinstance(self.location_uuid, Unset):
            location_uuid = str(self.location_uuid)

        network_uuid: str | Unset = UNSET
        if not isinstance(self.network_uuid, Unset):
            network_uuid = str(self.network_uuid)

        coordinates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if gateway_id is not UNSET:
            field_dict["gatewayId"] = gateway_id
        if is_virtual is not UNSET:
            field_dict["isVirtual"] = is_virtual
        if location_uuid is not UNSET:
            field_dict["locationUuid"] = location_uuid
        if network_uuid is not UNSET:
            field_dict["networkUuid"] = network_uuid
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_model_coordinates import GatewayModelCoordinates

        d = dict(src_dict)
        gateway_id = d.pop("gatewayId", UNSET)

        is_virtual = d.pop("isVirtual", UNSET)

        _location_uuid = d.pop("locationUuid", UNSET)
        location_uuid: UUID | Unset
        if isinstance(_location_uuid, Unset):
            location_uuid = UNSET
        else:
            location_uuid = UUID(_location_uuid)

        _network_uuid = d.pop("networkUuid", UNSET)
        network_uuid: UUID | Unset
        if isinstance(_network_uuid, Unset):
            network_uuid = UNSET
        else:
            network_uuid = UUID(_network_uuid)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: GatewayModelCoordinates | Unset
        if isinstance(_coordinates, Unset):
            coordinates = UNSET
        else:
            coordinates = GatewayModelCoordinates.from_dict(_coordinates)

        gateway_model = cls(
            gateway_id=gateway_id,
            is_virtual=is_virtual,
            location_uuid=location_uuid,
            network_uuid=network_uuid,
            coordinates=coordinates,
        )

        gateway_model.additional_properties = d
        return gateway_model

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
