# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from enum import Enum, auto
from .logger import get_logger
logger = get_logger(__name__)


class CacheType(Enum):
    LOCATION = auto()
    LOCATION_TYPE = auto()
    NETWORK = auto()
    GATEWAY = auto()
    NODE = auto()


class Cache:
    """
    Responsible for caching the elements of each metadata module.
    It is basically used to store the information received from
    metadata services.

    It contains a dictionary that separate data from each service.

    For example:
        {
            CacheType.NETWORK: [
                {
                    "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
                    "address": 11,
                    "name": "Simple Network",
                    "linkedLocations": [
                        "1e2f21ef-e1d9-4c66-9326-fa29d1847f2b"
                    ],
                    "modificationTime": 1637678502
                },
                ...
            ],
            CacheType.NODE: [
                ...
            ],
            ...
        }
    """
    def __init__(self) -> None:
        self._cache = {}

    def get_cache(self) -> dict:
        """ Return cache. """
        return self._cache

    def add(self, service_cache_type: CacheType, data: dict, data_key: str) -> None:
        """ Add data to the service cache type component of the cache.

        Args:
            service_cache_type: service cache type component of the cache.
            data: dictionary containing the data.
            data_key: key to retrieve the data inside the service component of the cache.
        """
        logger.debug("Add to cache %s to %s metadata service api with the following key: %s",
                      data, service_cache_type.name.lower(), data_key)
        if service_cache_type not in self._cache:
            self._cache[service_cache_type] = {}

        self._cache[service_cache_type][data_key] = data

    def get(self, service_cache_type: CacheType, key=None):
        """ Get cached data from a service.
        If key is provided, return the element with this key inside the service.
        Otherwise return the whole cache for the service.
        """
        if service_cache_type not in self._cache:
            return None
        elif key is None:
            return self._cache[service_cache_type]

        return self._cache[service_cache_type].get(key, None)
