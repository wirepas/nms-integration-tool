from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.epsg_code import EpsgCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateNodeBodyCoordinates")


@_attrs_define
class UpdateNodeBodyCoordinates:
    """
    Attributes:
        latitude (float): Decimal presentation of the latitude (in given coordinate system)
        longitude (float): Decimal presentation of the longitude (in given coordinate system)
        altitude (float): Altitude in meters above sea level
        epsg (EpsgCode | Unset): EPSG code of the coordinate system used to represent latitude and longitude. The
            available options are
            limited to those supported by the services. Currently available EPSG codes are following:
            * `EPSG:4326`: WGS84 (default)
    """

    latitude: float
    longitude: float
    altitude: float
    epsg: EpsgCode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        latitude = self.latitude

        longitude = self.longitude

        altitude = self.altitude

        epsg: str | Unset = UNSET
        if not isinstance(self.epsg, Unset):
            epsg = self.epsg.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude,
            }
        )
        if epsg is not UNSET:
            field_dict["epsg"] = epsg

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        altitude = d.pop("altitude")

        _epsg = d.pop("epsg", UNSET)
        epsg: EpsgCode | Unset
        if isinstance(_epsg, Unset):
            epsg = UNSET
        else:
            epsg = EpsgCode(_epsg)

        update_node_body_coordinates = cls(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            epsg=epsg,
        )

        update_node_body_coordinates.additional_properties = d
        return update_node_body_coordinates

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
