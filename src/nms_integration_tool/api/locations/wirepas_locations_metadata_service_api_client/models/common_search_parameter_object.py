from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.common_search_parameter_object_order import CommonSearchParameterObjectOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="CommonSearchParameterObject")


@_attrs_define
class CommonSearchParameterObject:
    """
    Attributes:
        order (CommonSearchParameterObjectOrder | Unset): Desired ordering of sorted results, either `asc` (ascending)
            or `desc` (descending) Default: CommonSearchParameterObjectOrder.ASC.
        fields (list[str] | Unset): Desired selection of fields to be returned with results. Uuid and sortBy field are
            always selected by default.
        total_results_count_only (bool | Unset): If set to true, only total results count matching query, ignoring
            cursor is returned in metadata response.
    """

    order: CommonSearchParameterObjectOrder | Unset = CommonSearchParameterObjectOrder.ASC
    fields: list[str] | Unset = UNSET
    total_results_count_only: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order: str | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.value

        fields: list[str] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields

        total_results_count_only = self.total_results_count_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if order is not UNSET:
            field_dict["order"] = order
        if fields is not UNSET:
            field_dict["fields"] = fields
        if total_results_count_only is not UNSET:
            field_dict["totalResultsCountOnly"] = total_results_count_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _order = d.pop("order", UNSET)
        order: CommonSearchParameterObjectOrder | Unset
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = CommonSearchParameterObjectOrder(_order)

        fields = cast(list[str], d.pop("fields", UNSET))

        total_results_count_only = d.pop("totalResultsCountOnly", UNSET)

        common_search_parameter_object = cls(
            order=order,
            fields=fields,
            total_results_count_only=total_results_count_only,
        )

        common_search_parameter_object.additional_properties = d
        return common_search_parameter_object

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
