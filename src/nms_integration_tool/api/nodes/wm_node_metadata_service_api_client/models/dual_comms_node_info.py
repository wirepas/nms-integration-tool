from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DualCommsNodeInfo")


@_attrs_define
class DualCommsNodeInfo:
    """The object with additional information about the nodes which can be either connected directly through gateway or
    through Mesh network.
    This field is available only if the node type is `DUAL_COMMS`, and it provides more details about the direct gateway
    linkage and about
    the internal state of the linkage.

        Attributes:
            connected_gateway_uuid (Union[Unset, UUID]): The UUID that identifies the gateway device to which this dual
                comms node is directly attached to.
    """

    connected_gateway_uuid: Union[Unset, UUID] = UNSET

    def to_dict(self) -> dict[str, Any]:
        connected_gateway_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.connected_gateway_uuid, Unset):
            connected_gateway_uuid = str(self.connected_gateway_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if connected_gateway_uuid is not UNSET:
            field_dict["connectedGatewayUuid"] = connected_gateway_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _connected_gateway_uuid = d.pop("connectedGatewayUuid", UNSET)
        connected_gateway_uuid: Union[Unset, UUID]
        if isinstance(_connected_gateway_uuid, Unset):
            connected_gateway_uuid = UNSET
        else:
            connected_gateway_uuid = UUID(_connected_gateway_uuid)

        dual_comms_node_info = cls(
            connected_gateway_uuid=connected_gateway_uuid,
        )

        return dual_comms_node_info
