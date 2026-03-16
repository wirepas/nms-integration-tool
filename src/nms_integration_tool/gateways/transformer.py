# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from ..logger import get_logger
logger = get_logger(__name__)
from typing import List

from nms_integration_tool.transformer import Transformer


class GatewaysTransformer(Transformer):
    """Transforms locations data for gateways metadata api."""

    def __init__(self, data: List[dict], config_file: str) -> None:
        super().__init__(data, config_file)

    def get_transformed_data_item(self, data_item: dict) -> dict:
        """Returns data item with the same fields and types as in the associated service API client.

        networkAddress key must be used to identify the gateway's network while we are querying its uuid.
        """
        logger.debug("GatewaysTransformer -> Transform %s", data_item)
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
            elif field_name == "networkAddress":
                transformed_data[field_name] = int(data_item[field_name_in_file])
            elif field_name == "isVirtual":
                transformed_data[field_name] = data_item[field_name_in_file].lower() == "true"
            else:
                transformed_data[field_name] = data_item[field_name_in_file]

        if "isVirtual" not in transformed_data:
            transformed_data["isVirtual"] = False

        return transformed_data
