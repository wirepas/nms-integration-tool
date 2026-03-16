from enum import Enum


class NodeDeviceType(str, Enum):
    DUAL_COMMS = "DUAL_COMMS"
    MESH = "MESH"
    SINK = "SINK"

    def __str__(self) -> str:
        return str(self.value)
