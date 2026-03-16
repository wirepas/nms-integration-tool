from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.related_object_reference import RelatedObjectReference


T = TypeVar("T", bound="NodeReadOnlyExtServiceRefs")


@_attrs_define
class NodeReadOnlyExtServiceRefs:
    """*DEPRECATION NOTICE: This field will be removed, since there is no use for it anymore in the current tool version.*

    A dictionary of references to other Wirepas backend managed application specific metadata resources that are
    related to this node but owned by another service

    """

    additional_properties: dict[str, RelatedObjectReference] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.related_object_reference import RelatedObjectReference

        d = dict(src_dict)
        node_read_only_ext_service_refs = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RelatedObjectReference.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        node_read_only_ext_service_refs.additional_properties = additional_properties
        return node_read_only_ext_service_refs

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> RelatedObjectReference:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: RelatedObjectReference) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
