from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ErrorResponseServiceRef")


@_attrs_define
class ErrorResponseServiceRef:
    """Error reference identifier, which makes it possible locate related error message from server side logs.
    This is mainly purposed for development time use, but can be benefit also when tracking production system
    problems.

        Attributes:
            service_id (str): Identifier of the backend service instance being a source of the error
            error_ref (str): UUID type of reference to the error, which can be used to track error from server side
    """

    service_id: str
    error_ref: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        error_ref = self.error_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serviceId": service_id,
                "errorRef": error_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("serviceId")

        error_ref = d.pop("errorRef")

        error_response_service_ref = cls(
            service_id=service_id,
            error_ref=error_ref,
        )

        error_response_service_ref.additional_properties = d
        return error_response_service_ref

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
