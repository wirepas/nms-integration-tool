from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SinkNodeInfo")


@_attrs_define
class SinkNodeInfo:
    """The object with an additional information about sink nodes. It is defined only if the current resource is a sink
    node.

        Attributes:
            sink_gateway_uuid (str | Unset): The UUID that identifies the sink gateway
    """

    sink_gateway_uuid: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        sink_gateway_uuid = self.sink_gateway_uuid

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if sink_gateway_uuid is not UNSET:
            field_dict["sinkGatewayUuid"] = sink_gateway_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sink_gateway_uuid = d.pop("sinkGatewayUuid", UNSET)

        sink_node_info = cls(
            sink_gateway_uuid=sink_gateway_uuid,
        )

        return sink_node_info
