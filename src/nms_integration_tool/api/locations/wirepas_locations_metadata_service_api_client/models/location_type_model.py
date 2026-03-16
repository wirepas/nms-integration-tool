from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.location_geometry_type import LocationGeometryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationTypeModel")


@_attrs_define
class LocationTypeModel:
    """Location type enables the creation of typed hierarchy for the location objects. The types and therefore the
    levels of hierarchy and their relations are not limited. Each type can have only one parent, thus making it
    possible to create tree like structures with one or more root types.

    The purpose of the location types is to provide means to model real world concepts to the system. These can
    be for example geospatial areas within a country, like states, districts and cities, or somewhat narrower
    context within a manufacturing facilities, like sites, buildings, warehouses, etc.

    Following gives a couple of concrete examples of different typings.

    Simple hierarchy with sequential order:

    ```
    COUNTRY -> STATE -> DISTRICT -> CITY
    ```

    An example of a tree type of hierarchy:

    ```
    SITE -> BUILDING -> FLOOR
         `> PARKING
    ```

    After location types are defined, these can be then assigned to locations. When setting parent linkage to a
    single location, it is checked that it follows also the type hierarchy.

        Attributes:
            parent_type_uuid (UUID | Unset): An UUID reference to the parent location location type for building the
                location type hierarchy. A location type
                can have only one parent type, creating a tree like structure for location types. For root location type(s),
                this
                field is empty.
            geometry_type (LocationGeometryType | Unset): Defines the type of the geospatial location (coordinates)
                definition for the location objects of this type. If set, all
                location objects created with this type shall allow only defining geometry of that type. Defaults to
                AREA_POLYGON.

                Possible geometry types are:

                - `CENTER_POINT`: Approximated central coordinate point of the location
                - `AREA_POLYGON`: Area boundaries defined as a polygon
                - `NONE`: Reserved for location types that do not have geospatial reference (like organizations etc.)
            is_filter_type (bool | Unset): Flag indicating, that the locations of this type should be included in the
                location filtering.

                The flag defaults to true.
            is_sequential (bool | Unset): Flag indicating, whether the locations of this type are such that they are ordered
                under their parent relation.

                The flag defaults to false.

                Simple examples for the ordering are e.g. numbered buildings within a specific site, like Building 1, Building 2
                (or Building A, Building B), or for example floors within a building (Ground floor, 1st floor, 2nd floor, ...)
    """

    parent_type_uuid: UUID | Unset = UNSET
    geometry_type: LocationGeometryType | Unset = UNSET
    is_filter_type: bool | Unset = UNSET
    is_sequential: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parent_type_uuid: str | Unset = UNSET
        if not isinstance(self.parent_type_uuid, Unset):
            parent_type_uuid = str(self.parent_type_uuid)

        geometry_type: str | Unset = UNSET
        if not isinstance(self.geometry_type, Unset):
            geometry_type = self.geometry_type.value

        is_filter_type = self.is_filter_type

        is_sequential = self.is_sequential

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if parent_type_uuid is not UNSET:
            field_dict["parentTypeUuid"] = parent_type_uuid
        if geometry_type is not UNSET:
            field_dict["geometryType"] = geometry_type
        if is_filter_type is not UNSET:
            field_dict["isFilterType"] = is_filter_type
        if is_sequential is not UNSET:
            field_dict["isSequential"] = is_sequential

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _parent_type_uuid = d.pop("parentTypeUuid", UNSET)
        parent_type_uuid: UUID | Unset
        if isinstance(_parent_type_uuid, Unset):
            parent_type_uuid = UNSET
        else:
            parent_type_uuid = UUID(_parent_type_uuid)

        _geometry_type = d.pop("geometryType", UNSET)
        geometry_type: LocationGeometryType | Unset
        if isinstance(_geometry_type, Unset):
            geometry_type = UNSET
        else:
            geometry_type = LocationGeometryType(_geometry_type)

        is_filter_type = d.pop("isFilterType", UNSET)

        is_sequential = d.pop("isSequential", UNSET)

        location_type_model = cls(
            parent_type_uuid=parent_type_uuid,
            geometry_type=geometry_type,
            is_filter_type=is_filter_type,
            is_sequential=is_sequential,
        )

        location_type_model.additional_properties = d
        return location_type_model

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
