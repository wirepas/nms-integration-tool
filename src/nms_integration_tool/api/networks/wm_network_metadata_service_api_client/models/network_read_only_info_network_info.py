from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.mesh_radio_profile import MeshRadioProfile
from ..types import UNSET, Unset

T = TypeVar("T", bound="NetworkReadOnlyInfoNetworkInfo")


@_attrs_define
class NetworkReadOnlyInfoNetworkInfo:
    """Read only information about the low level parameters of the Wirepas Mesh network. This includes data defining the
    Mesh network radio
    profile and some key communication parameters related to the network. If some information is not readily available,
    it is not provided.

        Attributes:
            radio_profile (MeshRadioProfile | Unset): The low level radio profile of the network. The radio profile is
                defined by the actual hardware and its configuration, thus it cannot
                be configured or changed. It is also worth noting that even though all profiles have somewhat identical Wirepas
                Mesh stack, each radio
                profile have unique characteristics resulting from the radio frequency and modulation.

                The possible radio profiles for a Wirepas Mesh network are following:

                - `ISM_24GHZ`: Proprietary Wirepas Mesh radio profile on top of Bluetooth Low Energy (BLE) physical layer
                - `SUB_INDIA865`: Proprietary SubGHz Wirepas Mesh radio profile compatible with India regulation and frequency
                bands
                - `DECT_TS_103_874_2_BAND_1`: 5G Mesh radio profile operating on global 1.9GHz DECT frequency band
                - `DECT_TS_103_874_2_BAND_4`: 5G Mesh radio profile operating on 915MHz ISM band compliant with North America
                regulation and frequency bands
                - `DECT_TS_103_874_2_BAND_9`: 5G Mesh radio profile operating on 1.9GHz frequency compliant with North America
                regulation and frequency bands
            network_channel (int | Unset): Wirepas Mesh network low level network control channel used for network discovery
                and coordination.
    """

    radio_profile: MeshRadioProfile | Unset = UNSET
    network_channel: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        radio_profile: str | Unset = UNSET
        if not isinstance(self.radio_profile, Unset):
            radio_profile = self.radio_profile.value

        network_channel = self.network_channel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if radio_profile is not UNSET:
            field_dict["radioProfile"] = radio_profile
        if network_channel is not UNSET:
            field_dict["networkChannel"] = network_channel

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _radio_profile = d.pop("radioProfile", UNSET)
        radio_profile: MeshRadioProfile | Unset
        if isinstance(_radio_profile, Unset):
            radio_profile = UNSET
        else:
            radio_profile = MeshRadioProfile(_radio_profile)

        network_channel = d.pop("networkChannel", UNSET)

        network_read_only_info_network_info = cls(
            radio_profile=radio_profile,
            network_channel=network_channel,
        )

        network_read_only_info_network_info.additional_properties = d
        return network_read_only_info_network_info

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
