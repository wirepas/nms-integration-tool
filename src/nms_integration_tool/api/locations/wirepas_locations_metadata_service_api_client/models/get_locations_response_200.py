from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location import Location
    from ..models.response_paging_information import ResponsePagingInformation


T = TypeVar("T", bound="GetLocationsResponse200")


@_attrs_define
class GetLocationsResponse200:
    """
    Attributes:
        results (list[Location] | Unset): Actual results, i.e. the list of locations matching the request parameters.
            Note that the list might not be full
            result set but contain only a partial result set (more information in metadata)
        metadata (ResponsePagingInformation | Unset):
    """

    results: list[Location] | Unset = UNSET
    metadata: ResponsePagingInformation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location import Location
        from ..models.response_paging_information import ResponsePagingInformation

        d = dict(src_dict)
        _results = d.pop("results", UNSET)
        results: list[Location] | Unset = UNSET
        if _results is not UNSET:
            results = []
            for results_item_data in _results:
                results_item = Location.from_dict(results_item_data)

                results.append(results_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: ResponsePagingInformation | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ResponsePagingInformation.from_dict(_metadata)

        get_locations_response_200 = cls(
            results=results,
            metadata=metadata,
        )

        get_locations_response_200.additional_properties = d
        return get_locations_response_200

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
