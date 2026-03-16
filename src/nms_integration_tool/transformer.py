# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import json
from .logger import get_logger
logger = get_logger(__name__)
from typing import List


class Transformer:
    def __init__(self, data: list, config_file: str) -> None:
        """ Transform raw data from data source module into transformed data.
        The transformed data are represented by dictionaries with keys
        corresponding to the fields of the associated metadata services object.

        Args:
            data (list): A list of locations data items.
            config_file: Name of the configuration file.
                This configuration gives a mapping between names of the fields
                in the provided data and the name in the metadata service.
        """
        self._data = data
        self._config = self._get_configuration(config_file)

    @staticmethod
    def _get_configuration(config_file):
        with open(config_file) as json_file:
            return json.load(json_file)

    def get_transformed_data(self) -> List[dict]:
        """ Return a list of transformed data items. """
        logger.info("%s transformer -> Transform %s data items",
                     self.__class__.__name__, len(self._data))
        return [self.get_transformed_data_item(data_item) for data_item in self._data]

    def get_transformed_data_item(self, data_item: dict) -> dict:
        """ Return the data item with the same fields and types as
        in the associated service API client. """
        raise NotImplementedError
