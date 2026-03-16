from enum import Enum


class EpsgCode(str, Enum):
    EPSG4326 = "EPSG:4326"

    def __str__(self) -> str:
        return str(self.value)
