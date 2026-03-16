from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_base_object_custom import MetadataBaseObjectCustom
    from ..models.node_model_coordinates import NodeModelCoordinates
    from ..models.node_provisioning_info import NodeProvisioningInfo
    from ..models.node_read_only_ext_service_refs import NodeReadOnlyExtServiceRefs
    from ..models.sink_node_info import SinkNodeInfo


T = TypeVar("T", bound="Node")


@_attrs_define
class Node:
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
        service_refs (NodeReadOnlyExtServiceRefs | Unset): *DEPRECATION NOTICE: This field will be removed, since there
            is no use for it anymore in the current tool version.*

            A dictionary of references to other Wirepas backend managed application specific metadata resources that are
            related to this node but owned by another service
        sink_node_info (SinkNodeInfo | Unset): The object with an additional information about sink nodes. It is defined
            only if the current resource is a sink node.
        provisioning_info (NodeProvisioningInfo | Unset): An object providing more details related to the node
            provisioning and security related
            information. The information consists of node low level identification (UID) and per
            device provisioning keys, which are used for securing the provisioning handshake during initial
            provisioning or required as a key management operation failsafe mechanism.

            The information is populated by importing the key information (see `metadata/nodes/import`
            API). If the provisioning information is not available or the provisioning is not supported by the node,
            this information will not be available.
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

    uuid: UUID
    modification_time: int | Unset = UNSET
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    custom: MetadataBaseObjectCustom | Unset = UNSET
    service_refs: NodeReadOnlyExtServiceRefs | Unset = UNSET
    sink_node_info: SinkNodeInfo | Unset = UNSET
    provisioning_info: NodeProvisioningInfo | Unset = UNSET
    address: int | Unset = UNSET
    network_uuid: UUID | Unset = UNSET
    is_virtual: bool | Unset = UNSET
    location_uuid: UUID | Unset = UNSET
    coordinates: NodeModelCoordinates | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        modification_time = self.modification_time

        name = self.name

        description = self.description

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

        service_refs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.service_refs, Unset):
            service_refs = self.service_refs.to_dict()

        sink_node_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sink_node_info, Unset):
            sink_node_info = self.sink_node_info.to_dict()

        provisioning_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provisioning_info, Unset):
            provisioning_info = self.provisioning_info.to_dict()

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
        if service_refs is not UNSET:
            field_dict["serviceRefs"] = service_refs
        if sink_node_info is not UNSET:
            field_dict["sinkNodeInfo"] = sink_node_info
        if provisioning_info is not UNSET:
            field_dict["provisioningInfo"] = provisioning_info
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
        from ..models.metadata_base_object_custom import MetadataBaseObjectCustom
        from ..models.node_model_coordinates import NodeModelCoordinates
        from ..models.node_provisioning_info import NodeProvisioningInfo
        from ..models.node_read_only_ext_service_refs import NodeReadOnlyExtServiceRefs
        from ..models.sink_node_info import SinkNodeInfo

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

        _service_refs = d.pop("serviceRefs", UNSET)
        service_refs: NodeReadOnlyExtServiceRefs | Unset
        if isinstance(_service_refs, Unset):
            service_refs = UNSET
        else:
            service_refs = NodeReadOnlyExtServiceRefs.from_dict(_service_refs)

        _sink_node_info = d.pop("sinkNodeInfo", UNSET)
        sink_node_info: SinkNodeInfo | Unset
        if isinstance(_sink_node_info, Unset):
            sink_node_info = UNSET
        else:
            sink_node_info = SinkNodeInfo.from_dict(_sink_node_info)

        _provisioning_info = d.pop("provisioningInfo", UNSET)
        provisioning_info: NodeProvisioningInfo | Unset
        if isinstance(_provisioning_info, Unset):
            provisioning_info = UNSET
        else:
            provisioning_info = NodeProvisioningInfo.from_dict(_provisioning_info)

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

        node = cls(
            uuid=uuid,
            modification_time=modification_time,
            name=name,
            description=description,
            custom=custom,
            service_refs=service_refs,
            sink_node_info=sink_node_info,
            provisioning_info=provisioning_info,
            address=address,
            network_uuid=network_uuid,
            is_virtual=is_virtual,
            location_uuid=location_uuid,
            coordinates=coordinates,
        )

        return node
