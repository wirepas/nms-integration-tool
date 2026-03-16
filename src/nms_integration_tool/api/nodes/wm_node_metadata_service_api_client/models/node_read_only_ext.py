from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node_provisioning_info import NodeProvisioningInfo
    from ..models.node_read_only_ext_service_refs import NodeReadOnlyExtServiceRefs
    from ..models.sink_node_info import SinkNodeInfo


T = TypeVar("T", bound="NodeReadOnlyExt")


@_attrs_define
class NodeReadOnlyExt:
    """
    Attributes:
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
    """

    service_refs: NodeReadOnlyExtServiceRefs | Unset = UNSET
    sink_node_info: SinkNodeInfo | Unset = UNSET
    provisioning_info: NodeProvisioningInfo | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_refs: dict[str, Any] | Unset = UNSET
        if not isinstance(self.service_refs, Unset):
            service_refs = self.service_refs.to_dict()

        sink_node_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sink_node_info, Unset):
            sink_node_info = self.sink_node_info.to_dict()

        provisioning_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provisioning_info, Unset):
            provisioning_info = self.provisioning_info.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service_refs is not UNSET:
            field_dict["serviceRefs"] = service_refs
        if sink_node_info is not UNSET:
            field_dict["sinkNodeInfo"] = sink_node_info
        if provisioning_info is not UNSET:
            field_dict["provisioningInfo"] = provisioning_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.node_provisioning_info import NodeProvisioningInfo
        from ..models.node_read_only_ext_service_refs import NodeReadOnlyExtServiceRefs
        from ..models.sink_node_info import SinkNodeInfo

        d = dict(src_dict)
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

        node_read_only_ext = cls(
            service_refs=service_refs,
            sink_node_info=sink_node_info,
            provisioning_info=provisioning_info,
        )

        node_read_only_ext.additional_properties = d
        return node_read_only_ext

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
