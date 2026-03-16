from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.location_geometry_type import LocationGeometryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_base_object_custom import MetadataBaseObjectCustom


T = TypeVar("T", bound="UpdateLocationTypeBody")


@_attrs_define
class UpdateLocationTypeBody:
    """
    Attributes:
        name (str): Short descriptive name for the metadata resource. If not explicitly set, the system will generate
            the
            name based on the low level identifier of the resource.
        description (str | Unset): More versatile description of the metadata resource. This is optional information,
            i.e. there is no
            default content for this field.
        custom (MetadataBaseObjectCustom | Unset): A freeform dictionary that clients can utilize for storing their own
            metadata related to the managed resource.
            The main intention of the custom fields is to allow clients to manage the relations between the client side data
            objects and corresponding Wirepas NMS data object. Thus, client can e.g. add a custom field for storing the
            internal identifier of managed asset to which the corresponding Wirepas node or gateway is linked to. Naturally,
            as the fields are fully customizable other usage purposes are possible.

            The data management of the custom fields differ slightly from other fields or attributes in managed resources or
            objects. The main difference is that the contents of `custom` field itself shall always be considered as single
            managed field. Thus, when adding new fields as well as when updating or removing existing fields to/from the
            `custom`,
            all the custom fields shall be given. I.e. the provided custom fields directly reflect the end state of the
            whole
            `custom` field after the operation. This is mainly relevant for PATCH update operations, which differ from other
            fields.
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

    name: str
    description: str | Unset = UNSET
    custom: MetadataBaseObjectCustom | Unset = UNSET
    parent_type_uuid: UUID | Unset = UNSET
    geometry_type: LocationGeometryType | Unset = UNSET
    is_filter_type: bool | Unset = UNSET
    is_sequential: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        custom: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom, Unset):
            custom = self.custom.to_dict()

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
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if custom is not UNSET:
            field_dict["custom"] = custom
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
        from ..models.metadata_base_object_custom import MetadataBaseObjectCustom

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        _custom = d.pop("custom", UNSET)
        custom: MetadataBaseObjectCustom | Unset
        if isinstance(_custom, Unset):
            custom = UNSET
        else:
            custom = MetadataBaseObjectCustom.from_dict(_custom)

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

        update_location_type_body = cls(
            name=name,
            description=description,
            custom=custom,
            parent_type_uuid=parent_type_uuid,
            geometry_type=geometry_type,
            is_filter_type=is_filter_type,
            is_sequential=is_sequential,
        )

        update_location_type_body.additional_properties = d
        return update_location_type_body

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
