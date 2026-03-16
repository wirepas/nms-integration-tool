from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define

from ..models.gateway_device_type import GatewayDeviceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gateway_model_coordinates import GatewayModelCoordinates
    from ..models.metadata_base_object_custom import MetadataBaseObjectCustom


T = TypeVar("T", bound="Gateway")


@_attrs_define
class Gateway:
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
        model (str | Unset): Gateway vendor specific model information.

            This information is automatically updated based on the information provided by the gateway at the initial
            handshake.
        version (str | Unset): Gateway vendor specific version number.

            This information is automatically updated based on the information provided by the gateway at the initial
            handshake.
        gateway_api_version (float | Unset): API version implemented in the gateway.
        sink_nodes (list[UUID] | Unset): List of sink nodes attached to this gateways. Each sink node is identified by
            its UUID.

            This information is automatically updated based on the information provided by the gateway at the initial
            handshake.
        gateway_type (GatewayDeviceType | Unset): The type of gateway device, indicating roughly the capabilities and
            the nature of the device.
            The possible device types for the gateways are following:

            - `GENERIC`: A high end general purpose gateway device with full feature set.
            - `EMBEDDED`: Embedded / mobile gateway with more limited resources and possibly also limited feature set.
    """

    uuid: UUID
    modification_time: int | Unset = UNSET
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    custom: MetadataBaseObjectCustom | Unset = UNSET
    gateway_id: str | Unset = UNSET
    is_virtual: bool | Unset = UNSET
    location_uuid: UUID | Unset = UNSET
    network_uuid: UUID | Unset = UNSET
    coordinates: GatewayModelCoordinates | Unset = UNSET
    model: str | Unset = UNSET
    version: str | Unset = UNSET
    gateway_api_version: float | Unset = UNSET
    sink_nodes: list[UUID] | Unset = UNSET
    gateway_type: GatewayDeviceType | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        modification_time = self.modification_time

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

        network_uuid: str | Unset = UNSET
        if not isinstance(self.network_uuid, Unset):
            network_uuid = str(self.network_uuid)

        coordinates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        model = self.model

        version = self.version

        gateway_api_version = self.gateway_api_version

        sink_nodes: list[str] | Unset = UNSET
        if not isinstance(self.sink_nodes, Unset):
            sink_nodes = []
            for sink_nodes_item_data in self.sink_nodes:
                sink_nodes_item = str(sink_nodes_item_data)
                sink_nodes.append(sink_nodes_item)

        gateway_type: str | Unset = UNSET
        if not isinstance(self.gateway_type, Unset):
            gateway_type = self.gateway_type.value

        field_dict: dict[str, Any] = {}

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
        if model is not UNSET:
            field_dict["model"] = model
        if version is not UNSET:
            field_dict["version"] = version
        if gateway_api_version is not UNSET:
            field_dict["gatewayApiVersion"] = gateway_api_version
        if sink_nodes is not UNSET:
            field_dict["sinkNodes"] = sink_nodes
        if gateway_type is not UNSET:
            field_dict["gatewayType"] = gateway_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gateway_model_coordinates import GatewayModelCoordinates
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

        model = d.pop("model", UNSET)

        version = d.pop("version", UNSET)

        gateway_api_version = d.pop("gatewayApiVersion", UNSET)

        _sink_nodes = d.pop("sinkNodes", UNSET)
        sink_nodes: list[UUID] | Unset = UNSET
        if _sink_nodes is not UNSET:
            sink_nodes = []
            for sink_nodes_item_data in _sink_nodes:
                sink_nodes_item = UUID(sink_nodes_item_data)

                sink_nodes.append(sink_nodes_item)

        _gateway_type = d.pop("gatewayType", UNSET)
        gateway_type: GatewayDeviceType | Unset
        if isinstance(_gateway_type, Unset):
            gateway_type = UNSET
        else:
            gateway_type = GatewayDeviceType(_gateway_type)

        gateway = cls(
            uuid=uuid,
            modification_time=modification_time,
            name=name,
            description=description,
            custom=custom,
            gateway_id=gateway_id,
            is_virtual=is_virtual,
            location_uuid=location_uuid,
            network_uuid=network_uuid,
            coordinates=coordinates,
            model=model,
            version=version,
            gateway_api_version=gateway_api_version,
            sink_nodes=sink_nodes,
            gateway_type=gateway_type,
        )

        return gateway
