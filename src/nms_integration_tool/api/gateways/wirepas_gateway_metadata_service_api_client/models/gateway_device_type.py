from enum import Enum


class GatewayDeviceType(str, Enum):
    EMBEDDED = "EMBEDDED"
    GENERIC = "GENERIC"

    def __str__(self) -> str:
        return str(self.value)
