from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gateway_device_type import GatewayDeviceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="GatewayDeviceInfo")


@_attrs_define
class GatewayDeviceInfo:
    """
    Attributes:
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

    model: str | Unset = UNSET
    version: str | Unset = UNSET
    gateway_api_version: float | Unset = UNSET
    sink_nodes: list[UUID] | Unset = UNSET
    gateway_type: GatewayDeviceType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        d = dict(src_dict)
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

        gateway_device_info = cls(
            model=model,
            version=version,
            gateway_api_version=gateway_api_version,
            sink_nodes=sink_nodes,
            gateway_type=gateway_type,
        )

        gateway_device_info.additional_properties = d
        return gateway_device_info

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
