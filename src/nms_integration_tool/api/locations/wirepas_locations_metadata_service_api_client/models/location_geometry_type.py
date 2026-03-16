from enum import Enum


class LocationGeometryType(str, Enum):
    AREA_POLYGON = "AREA_POLYGON"
    CENTER_POINT = "CENTER_POINT"
    NONE = "NONE"

    def __str__(self) -> str:
        return str(self.value)
