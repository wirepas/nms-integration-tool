from enum import Enum


class MeshRadioProfile(str, Enum):
    DECT_TS_103_874_2_BAND_1 = "DECT_TS_103_874_2_BAND_1"
    DECT_TS_103_874_2_BAND_4 = "DECT_TS_103_874_2_BAND_4"
    DECT_TS_103_874_2_BAND_9 = "DECT_TS_103_874_2_BAND_9"
    ISM_24GHZ = "ISM_24GHZ"
    SUB_INDIA865 = "SUB_INDIA865"

    def __str__(self) -> str:
        return str(self.value)
