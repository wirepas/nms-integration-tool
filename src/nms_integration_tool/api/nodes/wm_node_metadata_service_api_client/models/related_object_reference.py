from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RelatedObjectReference")


@_attrs_define
class RelatedObjectReference:
    """*DEPRECATION NOTICE: References will be removed, since there is no use for them anymore in the current tool
    version.*

    Reference to a resource that is related to the current resource

        Attributes:
            relation (str | Unset): Type or nature of the relation (usage depends on the context)
            href (str | Unset): Link to access the related resource
    """

    relation: str | Unset = UNSET
    href: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        relation = self.relation

        href = self.href

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if relation is not UNSET:
            field_dict["relation"] = relation
        if href is not UNSET:
            field_dict["href"] = href

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        relation = d.pop("relation", UNSET)

        href = d.pop("href", UNSET)

        related_object_reference = cls(
            relation=relation,
            href=href,
        )

        related_object_reference.additional_properties = d
        return related_object_reference

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
