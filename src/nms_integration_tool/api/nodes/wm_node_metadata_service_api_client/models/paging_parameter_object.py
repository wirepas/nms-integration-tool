from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PagingParameterObject")


@_attrs_define
class PagingParameterObject:
    """
    Attributes:
        limit (int | Unset): Number of items to return in a single response. If the total number of results matching the
            query / request
            then the results are limited to the given amount. In that case, the service will provide cursors that allow
            traversing between the pages.

            **NOTE:** It is highly recommended to use reasonable page sizes especially if connecting from a client
            application. However, the maximum value for the limit is kept quite high in order to ease integration of
            customer backend services.
             Default: 1000.
        cursor (str | Unset): Cursor pointing to the next / first item to be returned
    """

    limit: int | Unset = 1000
    cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit", UNSET)

        cursor = d.pop("cursor", UNSET)

        paging_parameter_object = cls(
            limit=limit,
            cursor=cursor,
        )

        paging_parameter_object.additional_properties = d
        return paging_parameter_object

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
