from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeProvisioningInfo")


@_attrs_define
class NodeProvisioningInfo:
    """An object providing more details related to the node provisioning and security related
    information. The information consists of node low level identification (UID) and per
    device provisioning keys, which are used for securing the provisioning handshake during initial
    provisioning or required as a key management operation failsafe mechanism.

    The information is populated by importing the key information (see `metadata/nodes/import`
    API). If the provisioning information is not available or the provisioning is not supported by the node,
    this information will not be available.

        Attributes:
            node_uid (UUID | Unset): Unique device identifier that is assigned to each node during manufacturing. It is used
                to identify a node during
                the provisioning process. The UID is critical for security - it is used for whitelisting, meaning only nodes
                with
                known UIDs can be provisioned and allowed to join the network. The UID is a UUIDv4 string.
                 Example: 22047a15-6893-4796-8ba3-3f93afe592f5.
            is_keys_populated (bool | Unset): Flag indicating whether the provisioning keys for this device are populated in
                the NMS.
            keys_crc (str | Unset): 16-bit checksum over the provisioning keys of the given device. It's calculated from the
                combined provisioning keys data
                (encryption key + authentication key). The CRC (Cyclic Redundancy Check) is used to verify that the provisioning
                key data
                hasn't been corrupted and can be used to identify the keys. CRC value is zero-padded to 2 bytes or 4 characters,
                and
                all a-f characters are in lowercase, e.g. 0xf14c.
                 Example: 0xf14c.
    """

    node_uid: UUID | Unset = UNSET
    is_keys_populated: bool | Unset = UNSET
    keys_crc: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        node_uid: str | Unset = UNSET
        if not isinstance(self.node_uid, Unset):
            node_uid = str(self.node_uid)

        is_keys_populated = self.is_keys_populated

        keys_crc = self.keys_crc

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if node_uid is not UNSET:
            field_dict["nodeUid"] = node_uid
        if is_keys_populated is not UNSET:
            field_dict["isKeysPopulated"] = is_keys_populated
        if keys_crc is not UNSET:
            field_dict["keysCRC"] = keys_crc

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _node_uid = d.pop("nodeUid", UNSET)
        node_uid: UUID | Unset
        if isinstance(_node_uid, Unset):
            node_uid = UNSET
        else:
            node_uid = UUID(_node_uid)

        is_keys_populated = d.pop("isKeysPopulated", UNSET)

        keys_crc = d.pop("keysCRC", UNSET)

        node_provisioning_info = cls(
            node_uid=node_uid,
            is_keys_populated=is_keys_populated,
            keys_crc=keys_crc,
        )

        node_provisioning_info.additional_properties = d
        return node_provisioning_info

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
