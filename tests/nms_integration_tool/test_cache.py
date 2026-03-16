# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import unittest

from nms_integration_tool.cache import CacheType, Cache


class CacheTesting(unittest.TestCase):
    def test_get_data(self):
        data = {
            "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
            "address": 11,
            "name": "Simple Network",
            "linkedLocations": ["1e2f21ef-e1d9-4c66-9326-fa29d1847f2b"]
        }

        cache = Cache()
        cache._cache = {CacheType.NETWORK: {"key": data}}

        self.assertIsNone(cache.get(CacheType.NODE))
        self.assertEqual(cache.get(CacheType.NETWORK), {"key": data})
        self.assertEqual(cache.get(CacheType.NETWORK, "key"), data)

    def test_add_one_data_item(self):
        cache = Cache()
        data = {
            "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
            "address": 11,
            "name": "Simple Network",
            "linkedLocations": ["1e2f21ef-e1d9-4c66-9326-fa29d1847f2b"]
        }

        cache.add(service_cache_type=CacheType.NETWORK, data=data, data_key="key")
        self.assertEqual(cache.get(CacheType.NETWORK, "key"), data)

    def test_multiple_add_data_items(self):
        data1 = {"address": 1, "name": "Simple Network"}
        data2 = {"address": 2, "name": "Another Network"}
        data3 = {"address": 3, "name": "Node"}

        cache = Cache()
        cache.add(service_cache_type=CacheType.NETWORK, data=data1, data_key=1)
        cache.add(service_cache_type=CacheType.NETWORK, data=data2, data_key=2)
        cache.add(service_cache_type=CacheType.NODE, data=data3, data_key=3)

        self.assertEqual(cache.get(CacheType.NETWORK, 1), data1)
        self.assertEqual(cache.get(CacheType.NETWORK, 2), data2)
        self.assertEqual(cache.get(CacheType.NETWORK), {1: data1, 2: data2})
        self.assertIsNone(cache.get(CacheType.LOCATION, 2))
        self.assertEqual(cache.get(CacheType.NODE, 3), data3)

    def test_update_data_item(self):
        cache = Cache()
        data = {
            "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
            "address": 11,
            "name": "Simple Network",
            "linkedLocations": ["1e2f21ef-e1d9-4c66-9326-fa29d1847f2b"]
        }

        cache.add(service_cache_type=CacheType.NETWORK, data=data, data_key="key")
        self.assertEqual(cache.get(CacheType.NETWORK, "key"), data)

        updated_data = {
            "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
            "address": 11,
            "name": "Changed name",
            "linkedLocations": ["1e2f21ef-e1d9-4c66-9326-fa29d1847f2b"]
        }
        cache.add(service_cache_type=CacheType.NETWORK, data=updated_data, data_key="key")
        self.assertEqual(len(cache.get(CacheType.NETWORK)), 1)
        self.assertEqual(cache.get(CacheType.NETWORK, "key"), updated_data)

    def test_get_cache_returns_full_dict(self):
        cache = Cache()
        cache.add(CacheType.NETWORK, {"name": "net"}, "n1")
        cache.add(CacheType.NODE, {"name": "node"}, "node1")

        full = cache.get_cache()
        self.assertIn(CacheType.NETWORK, full)
        self.assertIn(CacheType.NODE, full)

    def test_get_nonexistent_key_returns_none(self):
        cache = Cache()
        cache.add(CacheType.NETWORK, {"name": "net"}, "n1")
        self.assertIsNone(cache.get(CacheType.NETWORK, "no-such-key"))

    def test_fresh_cache_is_empty(self):
        cache = Cache()
        for cache_type in CacheType:
            self.assertIsNone(cache.get(cache_type))

    def test_tuple_key(self):
        cache = Cache()
        data = {"name": "building", "parent": "campus"}
        cache.add(CacheType.LOCATION, data, ("building", "campus"))
        self.assertEqual(cache.get(CacheType.LOCATION, ("building", "campus")), data)


if __name__ == "__main__":
    unittest.main()
