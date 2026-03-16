from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gateway_model_coordinates import GatewayModelCoordinates
    from ..models.metadata_base_object_custom import MetadataBaseObjectCustom


T = TypeVar("T", bound="CreateGatewaysBodyItem")


@_attrs_define
class CreateGatewaysBodyItem:
    """
    Attributes:
        network_uuid (UUID): A reference to the network resource this gateway is related to
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
             Default: False.
        location_uuid (UUID | Unset): A reference to the location resource this gateway is related to
        coordinates (GatewayModelCoordinates | Unset):
    """

    network_uuid: UUID
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    custom: MetadataBaseObjectCustom | Unset = UNSET
    gateway_id: str | Unset = UNSET
    is_virtual: bool | Unset = False
    location_uuid: UUID | Unset = UNSET
    coordinates: GatewayModelCoordinates | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        network_uuid = str(self.network_uuid)

        name = self.name

        description = self.description

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        gateway_id = self.gateway_id

        is_virtual = self.is_virtual

        location_uuid: str | Unset = UNSET
        if not isinstance(self.location_uuid, Unset):
            location_uuid = str(self.location_uuid)

        coordinates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "networkUuid": network_uuid,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if custom is not UNSET:
            field_dict["custom"] = custom
        if gateway_id is not UNSET:
            field_dict["gatewayId"] = gateway_id
        if is_virtual is not UNSET:
            field_dict["isVirtual"] = is_virtual
        if location_uuid is not UNSET:
            field_dict["locationUuid"] = location_uuid
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_model_coordinates import GatewayModelCoordinates
        from ..models.metadata_base_object_custom import MetadataBaseObjectCustom

        d = dict(src_dict)
        network_uuid = UUID(d.pop("networkUuid"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _custom = d.pop("custom", UNSET)
        custom: MetadataBaseObjectCustom | Unset
        if isinstance(_custom, Unset):
            custom = UNSET
        else:
            custom = MetadataBaseObjectCustom.from_dict(_custom)

        gateway_id = d.pop("gatewayId", UNSET)

        is_virtual = d.pop("isVirtual", UNSET)

        _location_uuid = d.pop("locationUuid", UNSET)
        location_uuid: UUID | Unset
        if isinstance(_location_uuid, Unset):
            location_uuid = UNSET
        else:
            location_uuid = UUID(_location_uuid)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: GatewayModelCoordinates | Unset
        if isinstance(_coordinates, Unset):
            coordinates = UNSET
        else:
            coordinates = GatewayModelCoordinates.from_dict(_coordinates)

        create_gateways_body_item = cls(
            network_uuid=network_uuid,
            name=name,
            description=description,
            custom=custom,
            gateway_id=gateway_id,
            is_virtual=is_virtual,
            location_uuid=location_uuid,
            coordinates=coordinates,
        )

        create_gateways_body_item.additional_properties = d
        return create_gateways_body_item

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
