from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location_model_approx_coordinates import LocationModelApproxCoordinates


T = TypeVar("T", bound="LocationModel")


@_attrs_define
class LocationModel:
    """
    Attributes:
        location_type_uuid (UUID | Unset): Type of the location object. This is a UUID reference to location type object
            representing the type of this
            location object.
        sequence_number (int | Unset): Optional indexing number for the location objects, which may be used by client to
            define the ordering of the
            the given type of location objects under their parent relation.

            Simple examples for the ordering are e.g. numbered buildings within a specific site, like Building 1, Building 2
            (or Building A, Building B), etc. or for example floors within a building (Ground floor, 1st floor, 2nd floor,
            ...)

            Following should be noted related to the sequence numbering:
            * Sequence numbers under a parent reference should be unique, but it is on the responsibility of the client
              to guarantee this.
            * Sequence numbers do not need to be consecutive but the usage is totally up to the client
        approx_coordinates (LocationModelApproxCoordinates | Unset):
        parent_location_uuid (UUID | Unset): An UUID reference to the parent location resource, to which this location
            is related to. The given parent shall follow
            the hierarchy defined by the location type hierarchy.
    """

    location_type_uuid: UUID | Unset = UNSET
    sequence_number: int | Unset = UNSET
    approx_coordinates: LocationModelApproxCoordinates | Unset = UNSET
    parent_location_uuid: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location_type_uuid: str | Unset = UNSET
        if not isinstance(self.location_type_uuid, Unset):
            location_type_uuid = str(self.location_type_uuid)

        sequence_number = self.sequence_number

        approx_coordinates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.approx_coordinates, Unset):
            approx_coordinates = self.approx_coordinates.to_dict()

        parent_location_uuid: str | Unset = UNSET
        if not isinstance(self.parent_location_uuid, Unset):
            parent_location_uuid = str(self.parent_location_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if location_type_uuid is not UNSET:
            field_dict["locationTypeUuid"] = location_type_uuid
        if sequence_number is not UNSET:
            field_dict["sequenceNumber"] = sequence_number
        if approx_coordinates is not UNSET:
            field_dict["approxCoordinates"] = approx_coordinates
        if parent_location_uuid is not UNSET:
            field_dict["parentLocationUuid"] = parent_location_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location_model_approx_coordinates import LocationModelApproxCoordinates

        d = dict(src_dict)
        _location_type_uuid = d.pop("locationTypeUuid", UNSET)
        location_type_uuid: UUID | Unset
        if isinstance(_location_type_uuid, Unset):
            location_type_uuid = UNSET
        else:
            location_type_uuid = UUID(_location_type_uuid)

        sequence_number = d.pop("sequenceNumber", UNSET)

        _approx_coordinates = d.pop("approxCoordinates", UNSET)
        approx_coordinates: LocationModelApproxCoordinates | Unset
        if isinstance(_approx_coordinates, Unset):
            approx_coordinates = UNSET
        else:
            approx_coordinates = LocationModelApproxCoordinates.from_dict(_approx_coordinates)

        _parent_location_uuid = d.pop("parentLocationUuid", UNSET)
        parent_location_uuid: UUID | Unset
        if isinstance(_parent_location_uuid, Unset):
            parent_location_uuid = UNSET
        else:
            parent_location_uuid = UUID(_parent_location_uuid)

        location_model = cls(
            location_type_uuid=location_type_uuid,
            sequence_number=sequence_number,
            approx_coordinates=approx_coordinates,
            parent_location_uuid=parent_location_uuid,
        )

        location_model.additional_properties = d
        return location_model

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
