# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from ..logger import get_logger
logger = get_logger(__name__)
from typing import List

from nms_integration_tool.transformer import Transformer


class NetworksTransformer(Transformer):
    """Transforms locations data for networks metadata api."""

    def __init__(self, data: List[dict], config_file: str) -> None:
        super().__init__(data, config_file)

    def get_transformed_data_item(self, data_item: dict) -> dict:
        logger.debug("NetworksTransformer -> Transform %s", data_item)
        transformed_data = {}
        for field_name, field_name_in_file in self._config.items():
            if field_name == "custom":
                transformed_data["custom"] = {}
                for custom_name, custom_name_in_file in field_name_in_file.items():
                    transformed_data["custom"][custom_name] = data_item[custom_name_in_file]
            elif field_name == "coordinates":
                transformed_data["coordinates"] = {}
                for coord_name, coord_name_in_file in field_name_in_file.items():
                    transformed_data["coordinates"][coord_name] = float(data_item[coord_name_in_file])
            elif field_name == "address":
                transformed_data[field_name] = int(data_item[field_name_in_file])
            else:
                transformed_data[field_name] = data_item[field_name_in_file]

        return transformed_data
