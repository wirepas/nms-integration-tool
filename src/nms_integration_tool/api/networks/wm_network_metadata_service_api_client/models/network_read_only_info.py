from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.network_read_only_info_network_info import NetworkReadOnlyInfoNetworkInfo


T = TypeVar("T", bound="NetworkReadOnlyInfo")


@_attrs_define
class NetworkReadOnlyInfo:
    """
    Attributes:
        network_info (NetworkReadOnlyInfoNetworkInfo | Unset): Read only information about the low level parameters of
            the Wirepas Mesh network. This includes data defining the Mesh network radio
            profile and some key communication parameters related to the network. If some information is not readily
            available, it is not provided.
    """

    network_info: NetworkReadOnlyInfoNetworkInfo | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        network_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.network_info, Unset):
            network_info = self.network_info.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if network_info is not UNSET:
            field_dict["networkInfo"] = network_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.network_read_only_info_network_info import NetworkReadOnlyInfoNetworkInfo

        d = dict(src_dict)
        _network_info = d.pop("networkInfo", UNSET)
        network_info: NetworkReadOnlyInfoNetworkInfo | Unset
        if isinstance(_network_info, Unset):
            network_info = UNSET
        else:
            network_info = NetworkReadOnlyInfoNetworkInfo.from_dict(_network_info)

        network_read_only_info = cls(
            network_info=network_info,
        )

        network_read_only_info.additional_properties = d
        return network_read_only_info

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
