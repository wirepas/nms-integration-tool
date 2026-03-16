# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from ..logger import get_logger
logger = get_logger(__name__)
from typing import List

from nms_integration_tool.transformer import Transformer

LEGACY_BOOLEAN_FIELDS = ("legacy_is_anchor", "legacy_approved", "legacy_virtual")


class NodesTransformer(Transformer):
    def __init__(self, data: List[dict], config_file: str) -> None:
        super().__init__(data, config_file)

    def get_transformed_data_item(self, data_item: dict) -> dict:
        """Returns data item with the same fields and types as in the nodes metadata api.

        networkAddress key must be used to identify the gateway's network
        while we don't have queried its uuid.
        """
        logger.debug("NodesTransformer -> Transform %s", data_item)
        transformed_data = {}
        for field_name, field_name_in_file in self._config.items():
            if field_name == "custom":
                transformed_data["custom"] = {}
                for custom_name, custom_name_in_file in field_name_in_file.items():
                    if not isinstance(custom_name_in_file, dict):
                        if custom_name in LEGACY_BOOLEAN_FIELDS and data_item[custom_name_in_file] in ["t", "f"]:
                            transformed_data["custom"][custom_name] = data_item[custom_name_in_file] == "t"
                        else:
                            transformed_data["custom"][custom_name] = data_item[custom_name_in_file]
                    else:
                        # Nested two level custom values support
                        transformed_data["custom"][custom_name] = {}
                        for level2_name, level2_name_in_file in custom_name_in_file.items():
                            transformed_data["custom"][custom_name][level2_name] = data_item[level2_name_in_file]

            elif field_name == "coordinates":
                transformed_data["coordinates"] = {}
                for coord_name, coord_name_in_file in field_name_in_file.items():
                    transformed_data["coordinates"][coord_name] = float(data_item[coord_name_in_file])
            elif field_name == "address" or field_name == "networkAddress":
                transformed_data[field_name] = int(data_item[field_name_in_file])
            elif field_name == "isVirtual":
                transformed_data[field_name] = data_item[field_name_in_file].lower() == "True"
            else:
                # If column value is not null
                if bool(data_item[field_name_in_file]):
                    transformed_data[field_name] = data_item[field_name_in_file]

        if "isVirtual" not in transformed_data:
            transformed_data["isVirtual"] = False
        return transformed_data

    def get_network_addresses(self) -> set:
        """Return the set of unique network addresses present in the raw input data."""
        network_address_col = self._config["networkAddress"]
        return {int(item[network_address_col]) for item in self._data}

    def exclude_sink_nodes(self, sink_node_keys: set) -> None:
        """Remove nodes from the data whose (address, networkAddress) pair is in sink_node_keys.

        Args:
            sink_node_keys: Set of (node_address, network_address) int tuples identifying SINK nodes.
        """
        address_col = self._config["address"]
        network_address_col = self._config["networkAddress"]
        self._data = [
            item for item in self._data
            if (int(item[address_col]), int(item[network_address_col])) not in sink_node_keys
        ]
