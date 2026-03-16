from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.common_search_parameter_object_order import CommonSearchParameterObjectOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchNodesBody")


@_attrs_define
class SearchNodesBody:
    """
    Attributes:
        query (str): More detailed search query for limiting the request to subset of nodes based on the defined
            filters.
            The syntax of the query is based on RSQL / FIQL, which is shortly described in here:
            [https://github.com/jirutka/rsql-parser#grammar-and-semantic](https://github.com/jirutka/rsql-parser#grammar-
            and-semantic)

            See more details in operation description.
        limit (int | Unset): Number of items to return in a single response. If the total number of results matching the
            query / request
            then the results are limited to the given amount. In that case, the service will provide cursors that allow
            traversing between the pages.

            **NOTE:** It is highly recommended to use reasonable page sizes especially if connecting from a client
            application. However, the maximum value for the limit is kept quite high in order to ease integration of
            customer backend services.
             Default: 1000.
        cursor (str | Unset): Cursor pointing to the next / first item to be returned
        order (CommonSearchParameterObjectOrder | Unset): Desired ordering of sorted results, either `asc` (ascending)
            or `desc` (descending) Default: CommonSearchParameterObjectOrder.ASC.
        fields (list[str] | Unset): Desired selection of fields to be returned with results. Uuid and sortBy field are
            always selected by default.
        total_results_count_only (bool | Unset): If set to true, only total results count matching query, ignoring
            cursor is returned in metadata response.
        sort_by (str | Unset): The field according to which the response data shall be sorted. By default, results are
            sorted by the "name" field. Default: 'name'.
    """

    query: str
    limit: int | Unset = 1000
    cursor: str | Unset = UNSET
    order: CommonSearchParameterObjectOrder | Unset = CommonSearchParameterObjectOrder.ASC
    fields: list[str] | Unset = UNSET
    total_results_count_only: bool | Unset = UNSET
    sort_by: str | Unset = "name"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        limit = self.limit

        cursor = self.cursor

        order: str | Unset = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.value

        fields: list[str] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields

        total_results_count_only = self.total_results_count_only

        sort_by = self.sort_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if order is not UNSET:
            field_dict["order"] = order
        if fields is not UNSET:
            field_dict["fields"] = fields
        if total_results_count_only is not UNSET:
            field_dict["totalResultsCountOnly"] = total_results_count_only
        if sort_by is not UNSET:
            field_dict["sortBy"] = sort_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        limit = d.pop("limit", UNSET)

        cursor = d.pop("cursor", UNSET)

        _order = d.pop("order", UNSET)
        order: CommonSearchParameterObjectOrder | Unset
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = CommonSearchParameterObjectOrder(_order)

        fields = cast(list[str], d.pop("fields", UNSET))

        total_results_count_only = d.pop("totalResultsCountOnly", UNSET)

        sort_by = d.pop("sortBy", UNSET)

        search_nodes_body = cls(
            query=query,
            limit=limit,
            cursor=cursor,
            order=order,
            fields=fields,
            total_results_count_only=total_results_count_only,
            sort_by=sort_by,
        )

        search_nodes_body.additional_properties = d
        return search_nodes_body

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
