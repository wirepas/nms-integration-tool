from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleResponsePagingInformation")


@_attrs_define
class SimpleResponsePagingInformation:
    """
    Attributes:
        results_count (int | Unset): The number of items returned in the result list.
        next_cursor (str | Unset): A cursor pointing to the "next" data set, i.e. this should be given as a cursor
            parameter
            in the following request to get the following page in results. This is empty, if there is no
            following page.
        prev_cursor (str | Unset): A cursor pointing to the "previous" data set, thus when traversing backwards within
            the result
            set, this should be given as a cursor parameter in the following request. When this is empty,
            there is no previous page.
    """

    results_count: int | Unset = UNSET
    next_cursor: str | Unset = UNSET
    prev_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results_count = self.results_count

        next_cursor = self.next_cursor

        prev_cursor = self.prev_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if results_count is not UNSET:
            field_dict["resultsCount"] = results_count
        if next_cursor is not UNSET:
            field_dict["nextCursor"] = next_cursor
        if prev_cursor is not UNSET:
            field_dict["prevCursor"] = prev_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        results_count = d.pop("resultsCount", UNSET)

        next_cursor = d.pop("nextCursor", UNSET)

        prev_cursor = d.pop("prevCursor", UNSET)

        simple_response_paging_information = cls(
            results_count=results_count,
            next_cursor=next_cursor,
            prev_cursor=prev_cursor,
        )

        simple_response_paging_information.additional_properties = d
        return simple_response_paging_information

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
