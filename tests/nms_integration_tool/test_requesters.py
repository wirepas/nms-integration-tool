# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import logging
import json
from nms_integration_tool.networks.requester import NetworksRequester
from mockito import verify, when, mock, spy, unstub, spy2, verifyStubbedInvocationsAreUsed, patch
import unittest
import http

from nms_integration_tool.api.networks.wm_network_metadata_service_api_client.types import Response
from nms_integration_tool.cache import Cache, CacheType
from nms_integration_tool.transformer import Transformer
from nms_integration_tool.gateways.transformer import GatewaysTransformer
from nms_integration_tool.locations.transformer import LocationsTransformer
from nms_integration_tool.networks.transformer import NetworksTransformer
from nms_integration_tool.nodes.transformer import NodesTransformer
from nms_integration_tool.requester import Requester
from nms_integration_tool.gateways.requester import GatewaysRequester
from nms_integration_tool.locations.requester import LocationsRequester
from nms_integration_tool.locations.requester import LocationTypesRequester
from nms_integration_tool.nodes.requester import NodesRequester

query = [{"identifier": 11, "name": "Simple Object", "description": "Simple description"},
         {"identifier": 222, "name": "Another Object"}]

body_response = [
    {
        "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
        "identifier": 11,
        "name": "Simple Object",
        "description": "simple description",
        "modificationTime": 1637678502
    },
    {
        "uuid": "e1c13899-dfc5-40e8-a35d-d61c73f552aa",
        "identifier": 222,
        "name": "Another Object",
        "modificationTime": 1637676879
    }
]

cache_content = {
    11: {
        "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
        "identifier": 11,
        "name": "Simple Object",
        "description": "simple description",
        "modificationTime": 1637678502
    },
    222: {
        "uuid": "e1c13899-dfc5-40e8-a35d-d61c73f552aa",
        "identifier": 222,
        "name": "Another Object",
        "modificationTime": 1637676879
    }
}


class RequestersTesting(unittest.TestCase):
    def tearDown(self):
        """ Function to be executed at the end of each test functions. """
        try:
            # Ensure stubs (verify and when) of a test are used.
            verifyStubbedInvocationsAreUsed()
        finally:
            # Unstubs all stubbed methods and functions of a test, so that
            # tests do not influence each other.
            unstub()

    def test_post_data(self):
        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        response = mock({"content": json.dumps(body_response),
                         "status_code": http.HTTPStatus.CREATED},
                        spec=Response)

        requester = Requester(None, cache_type, None)
        when(Requester)._request_post(...).thenReturn(response)
        result_creation = requester._create_data(query)

        self.assertEqual(result_creation, [response])
        self.assertTrue(requester.is_response_valid(result_creation))

    def test_add_response_to_cache(self):
        response = mock({"content": json.dumps(body_response),
                         "status_code": http.HTTPStatus.CREATED},
                        spec=Response)

        requester = Requester(None, None, None)
        when(Requester)._add_cache_keys_to_db_data(...).thenReturn(True)
        when(Requester)._delete_unwanted_fields_from_responses_json(...).thenReturn(body_response)
        when(Requester)._add_to_uuid_mapping(...)
        when(Requester)._add_json_data_to_cache(...)

        requester._add_response_to_cache(response)
        verify(Requester, times=1)._add_cache_keys_to_db_data(body_response[0])
        verify(Requester, times=1)._add_cache_keys_to_db_data(body_response[1])
        verify(Requester, times=1)._add_to_uuid_mapping(body_response[0])
        verify(Requester, times=1)._add_to_uuid_mapping(body_response[1])
        verify(Requester, times=2)._add_to_uuid_mapping(...)
        verify(Requester, times=1)._add_json_data_to_cache(body_response)

    def test_add_response_to_cache_response_not_converted(self):
        response = mock({"content": json.dumps({"results": body_response}),
                         "status_code": http.HTTPStatus.CREATED},
                        spec=Response)

        requester = Requester(None, None, None)
        when(Requester)._add_cache_keys_to_db_data(body_response[1]).thenReturn(True)
        when(Requester)._add_cache_keys_to_db_data(body_response[0]).thenReturn(False)
        when(Requester)._delete_unwanted_fields_from_responses_json(...).thenReturn(body_response)
        when(Requester)._add_to_uuid_mapping(...)
        when(Requester)._add_json_data_to_cache(...)

        requester._add_response_to_cache(response)
        verify(Requester, times=1)._add_cache_keys_to_db_data(body_response[1])
        verify(Requester, times=1)._add_to_uuid_mapping(body_response[1])
        verify(Requester, times=1)._add_to_uuid_mapping(...)
        verify(Requester, times=1)._add_json_data_to_cache(body_response)

    def test_add_json_data_to_cache(self):
        cache = mock(spec=Cache)
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = Requester(None, cache_type, cache)
        when(cache).add(...)
        when(Requester).get_cache_key_names(...).thenReturn(["identifier"])

        requester._add_json_data_to_cache(body_response)

        verify(cache, times=2).add(...)
        verify(cache, times=1).add(cache_type, cache_content[11], 11)
        verify(cache, times=1).add(cache_type, cache_content[222], 222)

    def test_get_data(self):
        get_post_response_body_response = {
            "results": body_response,
            "metadata": {
                "resultsCount": 2,
                "remainingCount": 0,
                "totalResultsCount": 2
            }
        }

        response = mock({"content": json.dumps(get_post_response_body_response),
                         "status_code": http.HTTPStatus.OK},
                        spec=Response)

        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = spy(Requester(None, cache_type, None))
        when(Requester)._request_get(...).thenReturn(response)
        when(Requester)._add_responses_to_cache(...)
        requester.get_data_and_update_cache()

        # Verify that the response is added to the cache
        verify(Requester, times=1)._add_responses_to_cache([response])

    def test_get_with_cursor(self):
        response_body_response1 = {
            "results": body_response[:1],
            "metadata": {
                "resultsCount": 1,
                "remainingCount": 1,
                "totalResultsCount": 2,
                "nextCursor": "nextCursor"
            }
        }

        response1 = mock({"content": json.dumps(response_body_response1),
                          "status_code": http.HTTPStatus.OK},
                         spec=Response)

        response_body_response2 = {
            "results": body_response[1:2],
            "metadata": {
                "resultsCount": 1,
                "remainingCount": 0,
                "totalResultsCount": 1
            }
        }

        response2 = mock({"content": json.dumps(response_body_response2),
                          "status_code": http.HTTPStatus.OK},
                         spec=Response)

        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = Requester(None, cache_type, None)
        when(Requester)._request_get().thenReturn(response1)
        when(Requester)._request_get(cursor='nextCursor').thenReturn(response2)
        when(Requester)._add_responses_to_cache(...)

        requester.get_data_and_update_cache()

        # Verify that the requests are queried and added to the cache
        verify(Requester, times=2)._request_get(...)
        verify(Requester, times=1)._add_responses_to_cache([response1, response2])

    def test_add_responses_to_cache_location_types(self):
        location_types_data = [{
            "uuid": "uuid_2",
            "name": "Building",
            "parentLocationUuid": "uuid_1",
            "modificationTime": 1637679328
        },
            {
                "uuid": "uuid_1",
                "name": "City",
                "modificationTime": 1637679321
            }
        ]

        response1 = mock({"content": json.dumps(location_types_data[:1]),
                          "status_code": http.HTTPStatus.CREATED},
                         spec=Response)
        response2 = mock({"content": json.dumps(location_types_data[1:2]),
                          "status_code": http.HTTPStatus.CREATED},
                         spec=Response)
        responses = [response1, response2]

        requester = LocationTypesRequester(None, None)
        when(LocationTypesRequester)._add_cache_keys_to_db_data(...).thenReturn(True)
        when(LocationTypesRequester)._add_to_uuid_mapping(...)
        when(LocationTypesRequester)._get_dependency_levels_from_data(location_types_data, ...).thenReturn(
            [location_types_data[1:2], location_types_data[:1]])
        when(LocationTypesRequester)._add_json_data_to_cache(...)

        requester._add_responses_to_cache(responses)

        verify(LocationTypesRequester, times=1, inorder=True)._get_dependency_levels_from_data(...)

        # Make sure the data are added in hierarchy order to the cache.
        verify(LocationTypesRequester, times=1, inorder=True)._add_cache_keys_to_db_data(location_types_data[1])
        verify(LocationTypesRequester, times=1, inorder=True)._add_to_uuid_mapping(location_types_data[1])
        verify(LocationTypesRequester, atleast=1, inorder=True)._add_json_data_to_cache(...)
        verify(LocationTypesRequester, times=1, inorder=True)._add_cache_keys_to_db_data(location_types_data[0])
        verify(LocationTypesRequester, times=1, inorder=True)._add_to_uuid_mapping(location_types_data[0])
        verify(LocationTypesRequester, times=2)._add_json_data_to_cache(...)

    def test_add_responses_to_cache_locations(self):
        locations_data = [{
            "uuid": "uuid_2",
            "name": "Hermia Building",
            "parentLocationUuid": "uuid_1",
            "locationTypeUuid": "location_type_uuid_2",
            "modificationTime": 1637679328
        },
            {
                "uuid": "uuid_1",
                "name": "Hermia Campus",
                "locationTypeUuid": "location_type_uuid_1",
                "modificationTime": 1637679321
            }
        ]

        response1 = mock({"content": json.dumps(locations_data[:1]),
                          "status_code": http.HTTPStatus.CREATED},
                         spec=Response)
        response2 = mock({"content": json.dumps(locations_data[1:2]),
                          "status_code": http.HTTPStatus.CREATED},
                         spec=Response)
        responses = [response1, response2]

        requester = LocationsRequester(None, None)
        when(LocationsRequester)._add_cache_keys_to_db_data(...).thenReturn(True)
        when(LocationsRequester)._add_to_uuid_mapping(...)
        when(LocationsRequester)._get_dependency_levels_from_data(locations_data, ...).thenReturn(
            [locations_data[1:2], locations_data[:1]])
        when(LocationsRequester)._add_json_data_to_cache(...)

        requester._add_responses_to_cache(responses)

        verify(LocationsRequester, times=1, inorder=True)._get_dependency_levels_from_data(...)

        # Make sure the data are added in hierarchy order to the cache.
        verify(LocationsRequester, times=1, inorder=True)._add_cache_keys_to_db_data(locations_data[1])
        verify(LocationsRequester, times=1, inorder=True)._add_to_uuid_mapping(locations_data[1])
        verify(LocationsRequester, atleast=1, inorder=True)._add_json_data_to_cache(...)
        verify(LocationsRequester, times=1, inorder=True)._add_cache_keys_to_db_data(locations_data[0])
        verify(LocationsRequester, times=1, inorder=True)._add_to_uuid_mapping(locations_data[0])
        verify(LocationsRequester, times=2)._add_json_data_to_cache(...)

    def test_create_data(self):
        query = [
            {
                "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
                "identifier": 11,
                "name": "Simple Object",
                "description": "simple description",
            },
        ]
        response_body_response = [
            {
                "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
                "name": "Simple Object",
                "address": 11,
                "description": "simple description",
            }
        ]

        response = mock({"content": json.dumps(response_body_response),
                         "status_code": http.HTTPStatus.OK},
                        spec=Response)

        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = Requester(None, cache_type, None)
        when(Requester)._request_post(...).thenReturn(response)
        result_create = requester._create_data(query)

        self.assertEqual(result_create, [response])
        self.assertTrue(requester.is_response_valid(response))

    def test_update_data(self):
        query = [
            {
                "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
                "identifier": 11,
                "name": "Simple Object",
                "description": "simple description",
            },
        ]
        response_body_response = [
            {
                "uuid": "eb5ca0fd-32eb-4646-bc53-21c19d185848",
                "name": "Updated simple Object",
                "address": 11,
                "description": "simple description",
            }
        ]

        response = mock({"content": json.dumps(response_body_response),
                         "status_code": http.HTTPStatus.OK},
                        spec=Response)

        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = Requester(None, cache_type, None)
        when(Requester)._request_patch(...).thenReturn(response)
        result_update = requester._update_data(query)

        self.assertEqual(result_update, [response])
        self.assertTrue(requester.is_response_valid(response))

    def test_invalid_response(self):
        query = [
            {
                "address": 11,
                "name": "Simple Object"
            }
        ]

        response_body_response = [
            {
                "errorCode": "WERR_UNKNOWN_RESOURCE",
                "message": "Resource not found from service",
                "serviceRef": {
                    "serviceId": "example-service-id",
                    "errorRef": "71142ad3-631b-4b66-9b6e-214bd9ab1101"
                }
            }
        ]

        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        response = mock({"content": json.dumps(response_body_response),
                         "status_code": http.HTTPStatus.BAD_REQUEST},
                        spec=Response)

        network = Requester(None, cache_type, None)
        when(Requester)._request_post(...).thenReturn(response)

        # Verification that a AssertionError is raised
        with self.assertRaises(AssertionError):
            network._create_data(query)

    def test_data_unknown_and_modified_in_cache(self):
        cache = mock(spec=Cache)
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        when(cache).get(cache_type, ...)
        when(cache).get(cache_type, 11).thenReturn(cache_content[11])
        when(cache).get(cache_type, 222).thenReturn(cache_content[222])
        when(Requester).get_cache_key_names(...).thenReturn(["identifier"])
        requester = Requester(None, cache_type, cache)

        data_partially_updated = [
            body_response[0],  # this object is already in the cache
            {  # this object is already in the cache but is modified
                "uuid": "e1c13899-dfc5-40e8-a35d-d61c73f552aa",
                "identifier": 222,
                "name": "Example Object with another name",
                "modificationTime": 1637676879
            },
            {  # this object is not in the cache
                "identifier": 333,
                "name": "New object to be created",
                "modificationTime": 1637678000
            }
        ]

        data_to_post, data_to_update = requester._data_unknown_and_modified_in_cache(
            data_partially_updated)

        # uuid is necessary to recognize a data, and the name has been changed
        expected_data_to_update = {"uuid": "e1c13899-dfc5-40e8-a35d-d61c73f552aa",
                                   "name": "Example Object with another name"}

        self.assertEqual(data_to_post, [data_partially_updated[2]])
        self.assertEqual(data_to_update, [expected_data_to_update])

    def test_networks_prepare_data(self):
        data = [{"address": 11,
                 "name": "Simple network"}]

        transformer = mock(spec=NetworksTransformer)
        when(transformer).get_transformed_data().thenReturn(data)

        requester = NetworksRequester(client=None, cache=None, transformer=transformer)
        prepared_data = requester._prepare_data()

        expected_data = [{"address": 11,
                          "name": "Simple network"}]

        self.assertEqual(prepared_data, expected_data)
        verify(transformer, times=1).get_transformed_data()

    def test_nodes_prepare_data(self):
        cache = mock(spec=Cache)
        when(cache).get_cache().thenReturn({})  # Force networks and locations to be queried
        when(NetworksRequester).get_data_and_update_cache()
        when(cache).get(CacheType.NETWORK, 11).thenReturn(cache_content[11])

        location = {"locationName": "location", "locationParentName": "location_parent",
                    "uuid": "location_uuid", "type": "location_type"}
        when(LocationTypesRequester).get_data_and_update_cache()
        when(LocationsRequester).get_data_and_update_cache()
        when(cache).get(CacheType.LOCATION, ("location", "location_parent")).thenReturn(location)

        data = [{"address": 19216800, "networkAddress": 11,
                 "name": "Simple Node", "locationName": "location",
                 "locationParentName": "location_parent"}]

        transformer = mock(spec=NodesTransformer)
        when(transformer).get_transformed_data().thenReturn(data)

        requester = NodesRequester(client=None, cache=cache, transformer=transformer)
        prepared_data = requester._prepare_data()

        # networkAddress key should be replace by networkUuid
        expected_data = [{"address": 19216800, "name": "Simple Node",
                          "networkUuid": cache_content[11]["uuid"],
                          "locationUuid": "location_uuid"}]

        self.assertEqual(prepared_data, expected_data)

        verify(cache, inorder=True).get_cache()
        verify(NetworksRequester, inorder=True).get_data_and_update_cache()
        verify(LocationsRequester).get_data_and_update_cache()
        verify(cache, inorder=True).get(CacheType.NETWORK, 11)
        verify(cache, inorder=True).get(CacheType.LOCATION, ("location", "location_parent"))
        verify(transformer, inorder=True).get_transformed_data()

    def test_gateways_prepare_data(self):
        cache = mock(spec=Cache)
        when(cache).get_cache().thenReturn({})  # Force networks and locations to be queried
        when(NetworksRequester).get_data_and_update_cache()
        when(cache).get(CacheType.NETWORK, 11).thenReturn(cache_content[11])

        location = {"locationName": "location", "locationParentName": "location_parent",
                    "uuid": "location_uuid", "type": "location_type"}
        when(LocationTypesRequester).get_data_and_update_cache()
        when(LocationsRequester).get_data_and_update_cache()
        when(cache).get(CacheType.LOCATION, ("location", "location_parent")).thenReturn(location)

        data = [{"gatewayId": 19216800, "networkAddress": 11,
                 "isVirtual": False, "name": "Simple Gateway",
                 "locationName": "location",
                 "locationParentName": "location_parent"}]

        transformer = mock(spec=GatewaysTransformer)
        when(transformer).get_transformed_data().thenReturn(data)

        requester = GatewaysRequester(client=None, cache=cache, transformer=transformer)
        prepared_data = requester._prepare_data()

        # networkAddress key should be replace by networkUuid
        expected_data = [{"gatewayId": 19216800,
                          "name": "Simple Gateway",
                          "isVirtual": False,
                          "networkUuid": cache_content[11]["uuid"],
                          "locationUuid": "location_uuid"}]

        self.assertEqual(prepared_data, expected_data)

        verify(cache, inorder=True).get_cache()
        verify(NetworksRequester, inorder=True).get_data_and_update_cache()
        verify(LocationsRequester).get_data_and_update_cache()
        verify(cache, inorder=True).get(CacheType.NETWORK, 11)
        verify(cache, inorder=True).get(CacheType.LOCATION, ("location", "location_parent"))
        verify(transformer, inorder=True).get_transformed_data()

    def test_location_types_prepare_data(self):
        data = [{'name': 'Region', 'parent': None}]

        transformer = mock(spec=LocationsTransformer)
        when(transformer).get_transformed_location_types_data().thenReturn(data)

        requester = LocationTypesRequester(client=None, cache=None, transformer=transformer)
        prepared_data = requester._prepare_data()

        expected_data = [{'name': 'Region', 'parent': None}]

        self.assertEqual(prepared_data, expected_data)
        verify(transformer, times=1).get_transformed_location_types_data()

    def test_locations_prepare_data(self):
        data = [{'name': "Rhône-Alpes", "type": 'Region', 'parent': None}]

        when(LocationTypesRequester).import_data()
        transformer = mock(spec=LocationsTransformer)
        when(transformer).get_transformed_locations_data().thenReturn(data)

        requester = LocationsRequester(client=None, cache=None, transformer=transformer)
        prepared_data = requester._prepare_data()

        expected_data = [{'name': "Rhône-Alpes", "type": 'Region', 'parent': None}]

        self.assertEqual(prepared_data, expected_data)
        verify(LocationTypesRequester, inorder=True).import_data()
        verify(transformer, inorder=True).get_transformed_locations_data()

    def test_keys_values_of_data(self):
        requester = Requester(None, None, None)

        key1, key2, key3 = 1, 'data_identifier', 35834965
        data = {"key1": key1, "key2": key2, "key3": key3}

        data_unique_key2 = requester._keys_values_of_data(data, ["key2"])
        data_many_keys = requester._keys_values_of_data(data, ["key2", "key3"])

        self.assertEqual(data_unique_key2, key2)
        self.assertEqual(data_many_keys, (key2, key3))

        with self.assertRaises(KeyError):
            requester._keys_values_of_data(data, ["non_existing_key"])

    def test_generic_get_parent_key_data(self):
        requester = Requester(None, None, None)
        data = cache_content[11]
        self.assertIsNone(requester._get_parent_key_data(data))

    def test_location_types_get_parent_key_data(self):
        requester = LocationTypesRequester(None, None)
        parent = {'name': 'Region', 'parent': None}
        data_from_source = {'name': 'City', 'parent': 'Region'}
        data_from_cache = {'name': 'City', 'parentTypeUuid': "parent_uuid"}
        requester.uuid_mapping = {"parent_uuid": parent}

        parent_from_data = requester._get_parent_key_data(data_from_source)
        parent_from_cache = requester._get_parent_key_data(data_from_cache)

        expected_parent = 'Region'

        self.assertEqual(parent_from_cache, expected_parent)
        self.assertEqual(parent_from_data, expected_parent)
        self.assertIsNone(requester._get_parent_key_data(parent))

    def test_locations_get_parent_key_data(self):
        requester = LocationsRequester(None, None)
        parent = {'name': 'Grenoble', 'type': 'City', 'parent': None,
                  "uuid": "parent_uuid", "locationTypeUuid": "parent_type_uuid"}
        data_from_cache = {'name': 'Grenoble', 'locationTypeUuid': 'type_uuid',
                           'parentLocationUuid': "parent_uuid"}
        data_from_source = {'name': 'Grenoble Building 1', 'type': 'Building',
                            'parent': 'Grenoble', 'grand_parent_name': None}

        requester.uuid_mapping = {"parent_uuid": parent}

        parent_from_data = requester._get_parent_key_data(data_from_source)
        parent_from_source = requester._get_parent_key_data(data_from_cache)

        expected_parent = ('Grenoble', None)

        self.assertEqual(parent_from_source, expected_parent)
        self.assertEqual(parent_from_data, expected_parent)
        self.assertIsNone(requester._get_parent_key_data(parent))

    def test_data_hierarchy_with_empty_cache(self):
        cache = mock(spec=Cache)
        when(cache).get(...)
        requester = Requester(None, None, cache)

        data_grand_parent = {"key": 1, "parent": None, "information": "Information on data grand parent"}
        data_parent = {"key": 2, "parent": 1, "information": "Information on data parent"}
        data = {"key": 3, "parent": 2, "information": "Information on data"}
        data2 = {"key": 4, "parent": 2, "information": "Information on another data item"}

        when(Requester).get_cache_key_names(...).thenReturn(["key"])
        when(Requester)._get_parent_key_data(data_grand_parent, ...)
        when(Requester)._get_parent_key_data(data_parent, ...).thenReturn(1)
        when(Requester)._get_parent_key_data(data, ...).thenReturn(2)
        when(Requester)._get_parent_key_data(data2, ...).thenReturn(2)
        tree_levels = requester._get_dependency_levels_from_data(
            [data_grand_parent, data_parent, data2, data])

        expected_tree_levels = [
            [{'key': 1, 'parent': None, 'information': 'Information on data grand parent'}],
            [{'key': 2, 'parent': 1, 'information': 'Information on data parent'}],
            [{'key': 4, 'parent': 2, 'information': 'Information on another data item'},
             {'key': 3, 'parent': 2, 'information': 'Information on data'}]
        ]

        self.assertEqual(tree_levels, expected_tree_levels)

    def test_hierarchy_with_non_empty_cache(self):
        data_grand_parent = {"key": 1, "parent": None, "information": "Information on data grand parent"}
        data_parent = {"key": 2, "parent": 1, "information": "Information on data parent"}
        data = {"key": 3, "parent": 2, "information": "Information on data"}
        data2 = {"key": 4, "parent": 2, "information": "Information on another data item"}

        cache = mock(spec=Cache)
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        when(cache).get(cache_type).thenReturn({1: data_grand_parent})
        requester = Requester(None, cache_type, cache)

        when(Requester).get_cache_key_names(...).thenReturn(["key"])
        when(Requester)._get_parent_key_data(data_grand_parent, ...)
        when(Requester)._get_parent_key_data(data_parent, ...).thenReturn(1)
        when(Requester)._get_parent_key_data(data, ...).thenReturn(2)
        when(Requester)._get_parent_key_data(data2, ...).thenReturn(2)
        tree_levels = requester._get_dependency_levels_from_data(
            [data_parent, data2, data])

        expected_tree_levels = [
            [],  # Data from the first level only come from the cache
            [{'key': 2, 'parent': 1, 'information': 'Information on data parent'}],
            [{'key': 4, 'parent': 2, 'information': 'Information on another data item'},
             {'key': 3, 'parent': 2, 'information': 'Information on data'}]
        ]

        self.assertEqual(tree_levels, expected_tree_levels)

    def test_get_dependency_levels_from_data_with_no_dependencies(self):
        cache = mock(spec=Cache)
        when(cache).get(...)
        requester = Requester(None, None, cache)

        when(Requester).get_cache_key_names(...).thenReturn(["identifier"])
        when(Requester)._get_parent_key_data(...)
        tree_levels = requester._get_dependency_levels_from_data(body_response)
        self.assertEqual(tree_levels, [body_response])

    def test_get_data_in_db_to_complete_cache(self):
        # cache type name can be used for the logs in the Requester
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = Requester(None, cache_type, None)
        data = [{"key": 3, "info": "just info"}, {"key": 1, "info": "some info"}, {"key": 2, "info": "other info"}]
        when(Requester).get_db_key_names().thenReturn(["key"])
        when(Requester).get_data_and_update_cache(query="key=in=(1,2,3)")

        requester._get_data_in_db_to_complete_cache(data)
        verify(Requester, times=1).get_data_and_update_cache(query="key=in=(1,2,3)")

    def test_get_data_in_db_to_complete_cache_with_chunks(self):
        cache_type = mock({"name": "Requester Interface"}, spec=CacheType)
        requester = Requester(None, cache_type, None, max_nb_elements_requests=1)
        data = [{"key": 1, "info": "some info"}, {"key": 2, "info": "other info"}]
        when(Requester).get_db_key_names().thenReturn(["key"])
        when(Requester).get_data_and_update_cache(query="key=in=(1)")
        when(Requester).get_data_and_update_cache(query="key=in=(2)")

        requester._get_data_in_db_to_complete_cache(data)

    def test_add_cache_keys_to_db_data_generic(self):
        requester = Requester(None, None, None)
        self.assertTrue(requester._add_cache_keys_to_db_data(query[0]))
        self.assertTrue(requester._add_cache_keys_to_db_data(query[1]))
        self.assertTrue(requester._add_cache_keys_to_db_data({}))

    def test_add_cache_keys_to_db_data_location_types(self):
        loc_type_with_unknown_parent = {"name": "uncompleted_loc_type",
                                        "parentTypeUuid": "unknown_parent"}
        loc_type_with_no_parent = {"name": "loc_type_with_no_parent"}
        loc_type_with_parent = {"name": "loc_type_with_parent",
                                "parentTypeUuid": "parent_uuid"}

        expected_converted_loc_type_with_parent = {
            "name": "loc_type_with_parent", "parentTypeUuid": "parent_uuid",
            "parent": 'loc_type_with_no_parent'}

        expected_converted_loc_type_with_no_parent = {
            "name": "loc_type_with_no_parent", "parent": None}

        requester = LocationTypesRequester(None, None)
        requester.uuid_mapping["parent_uuid"] = loc_type_with_no_parent

        self.assertFalse(requester._add_cache_keys_to_db_data(loc_type_with_unknown_parent))
        self.assertTrue(requester._add_cache_keys_to_db_data(loc_type_with_no_parent))
        self.assertTrue(requester._add_cache_keys_to_db_data(loc_type_with_parent))
        self.assertEqual(loc_type_with_parent, expected_converted_loc_type_with_parent)
        self.assertEqual(loc_type_with_no_parent, expected_converted_loc_type_with_no_parent)

    def test_add_cache_keys_to_db_data_locations(self):
        loc_type = {"name": "loc_type"}

        loc_with_unknown_parent = {"name": "uncompleted_loc",
                                   "parentLocationUuid": "unknown_parent",
                                   "locationTypeUuid": "type_uuid"}
        loc_with_unknown_type = {"name": "uncompleted_loc",
                                 "parentLocationUuid": "unknown_parent",
                                 "locationTypeUuid": "unkown_type_uuid"}
        loc_with_no_loc_type = {"name": "loc_with_parent",
                                "parentLocationUuid": "parent_uuid"}
        loc_with_no_parent = {"name": "loc_with_no_parent",
                              "locationTypeUuid": "type_uuid"}
        loc_with_parent = {"name": "loc_with_parent",
                           "parentLocationUuid": "parent_uuid",
                           "locationTypeUuid": "type_uuid"}

        expected_converted_loc_with_parent = {
            "name": "loc_with_parent",
            "parentLocationUuid": "parent_uuid",
            "locationTypeUuid": "type_uuid",
            "parent": "loc_with_no_parent",
            "type": "loc_type"
        }

        expected_converted_loc_with_no_parent = {
            "name": "loc_with_no_parent",
            "locationTypeUuid": "type_uuid",
            "parent": None,
            "type": "loc_type"
        }

        location_types_requester = LocationTypesRequester(None, None)
        location_types_requester.uuid_mapping["type_uuid"] = loc_type

        requester = LocationsRequester(None, None)
        requester.location_types_requester = location_types_requester
        requester.uuid_mapping["parent_uuid"] = loc_with_no_parent

        self.assertFalse(requester._add_cache_keys_to_db_data(loc_with_unknown_parent))
        self.assertFalse(requester._add_cache_keys_to_db_data(loc_with_unknown_type))
        self.assertFalse(requester._add_cache_keys_to_db_data(loc_with_no_loc_type))
        self.assertTrue(requester._add_cache_keys_to_db_data(loc_with_no_parent))
        self.assertTrue(requester._add_cache_keys_to_db_data(loc_with_parent))
        self.assertEqual(loc_with_parent, expected_converted_loc_with_parent)
        self.assertEqual(loc_with_no_parent, expected_converted_loc_with_no_parent)

    def test_prepare_cache_data_to_be_sent(self):
        requester = Requester(None, None, None)
        when(Requester).dependency_specific_keys().thenReturn(['file_specific_key'])

        data_from_cache = {"unchanged_key": "unchanged_value",
                           "updated_key": "former_value"}
        data_from_source = {"updated_key": "updated_value",
                            "new_key": "new_value",
                            "file_specific_key": "file_specific_value"}

        updated_data_from_cache = requester._prepare_cache_data_to_be_sent(
            data_from_cache, data_from_source)
        expected_updated_data = {'unchanged_key': 'unchanged_value',
                                 'updated_key': 'updated_value',
                                 'new_key': 'new_value'}

        self.assertEqual(updated_data_from_cache, expected_updated_data)

    def test_import_location_types_to_db(self):
        location_types_data = [
            {'name': 'Region', 'parent': None},
            {'name': 'City', 'parent': 'Region', "description": "short description"},
            {'name': 'Building', 'parent': 'City'},
            {'name': 'Park', 'parent': 'City'}]
        region_key = "Region"
        city_key = "City"
        data_levels = [location_types_data[:1],
                       location_types_data[1:2],
                       location_types_data[2:4]]

        cache = mock(spec=Cache)
        requester = LocationTypesRequester(None, cache)

        # only uuid of the parent from the cache
        # should be necessary to import the next data items
        when(cache).get(service_cache_type=CacheType.LOCATION_TYPE, key=region_key).thenReturn({"uuid": "uuid_region"})
        when(cache).get(service_cache_type=CacheType.LOCATION_TYPE, key=city_key).thenReturn({"uuid": "uuid_city"})
        when(requester)._add_response_to_cache(...)

        when(requester).dependency_specific_keys().thenReturn(["parent"])
        when(requester)._get_dependency_levels_from_data(location_types_data).thenReturn(data_levels)
        when(requester)._get_parent_key_data(location_types_data[1]).thenReturn(region_key)
        when(requester)._get_parent_key_data(location_types_data[2]).thenReturn(city_key)
        when(requester)._get_parent_key_data(location_types_data[3]).thenReturn(city_key)

        # override the super class method _create_data
        patch(Requester._create_data, lambda x: ["response"])

        responses = requester._import_location_types_to_db(location_types_data)

        self.assertEqual(responses, ["response", "response", "response"])
        verify(Requester, times=1, inorder=True)._create_data(
            [{'name': 'Region'}])
        verify(Requester, times=1, inorder=True)._create_data(
            [{'name': 'City', 'description': 'short description',
              'parentTypeUuid': 'uuid_region'}])
        verify(Requester, times=1, inorder=True)._create_data(
            [{'name': 'Building', 'parentTypeUuid': 'uuid_city'},
             {'name': 'Park', 'parentTypeUuid': 'uuid_city'}])

    def test_import_locations_to_db(self):
        locations_data = [
            {'name': "Rhône-Alpes", "type": 'Region', 'parent': None},
            {'name': "Grenoble", 'type': 'City', 'parent': "Rhône-Alpes",
             'grand_parent_name': None, "description": "short description"},
            {'name': "building 1", 'type': 'Building', 'parent': 'Grenoble',
             'grand_parent_name': "Rhône-Alpes"},
            {'name': "Park Victor Hugo", 'type': 'Park', 'parent': 'Grenoble',
             'grand_parent_name': "Rhône-Alpes"}]

        region_type_key = "Region"
        city_type_key = "City"
        building_type_key = "Building"
        park_type_key = "Park"
        region_key = ("Rhône-Alpes", None)
        city_key = ("Grenoble", "Rhône-Alpes")
        data_levels = [locations_data[:1],
                       locations_data[1:2],
                       locations_data[2:4]]

        cache = mock(spec=Cache)
        requester = LocationsRequester(None, cache)

        # only uuid of the parent from the cache
        # should be necessary to import the next data items
        when(cache).get(service_cache_type=CacheType.LOCATION_TYPE, key=region_type_key).thenReturn(
            {"uuid": "uuid_type_region"})
        when(cache).get(service_cache_type=CacheType.LOCATION_TYPE, key=city_type_key).thenReturn(
            {"uuid": "uuid_type_city"})
        when(cache).get(service_cache_type=CacheType.LOCATION_TYPE, key=building_type_key).thenReturn(
            {"uuid": "uuid_type_building"})
        when(cache).get(service_cache_type=CacheType.LOCATION_TYPE, key=park_type_key).thenReturn(
            {"uuid": "uuid_type_park"})
        when(cache).get(service_cache_type=CacheType.LOCATION, key=region_key).thenReturn({"uuid": "uuid_region"})
        when(cache).get(service_cache_type=CacheType.LOCATION, key=city_key).thenReturn({"uuid": "uuid_city"})
        when(requester)._add_response_to_cache(...)

        when(requester).dependency_specific_keys().thenReturn(["type", "parent", "grand_parent_name"])
        when(requester)._get_dependency_levels_from_data(locations_data).thenReturn(data_levels)
        when(requester)._get_parent_key_data(locations_data[1]).thenReturn(region_key)
        when(requester)._get_parent_key_data(locations_data[2]).thenReturn(city_key)
        when(requester)._get_parent_key_data(locations_data[3]).thenReturn(city_key)
        patch(Requester._create_data, lambda x: ["response"])

        responses = requester._import_locations_to_db(locations_data)

        self.assertEqual(responses, ["response", "response", "response"])
        verify(Requester, times=1)._create_data([{'name': 'Rhône-Alpes', 'locationTypeUuid': 'uuid_type_region'}])
        verify(Requester, times=1)._create_data([{'name': 'Grenoble', 'description': 'short description',
                                                  'locationTypeUuid': 'uuid_type_city',
                                                  'parentLocationUuid': 'uuid_region'}])
        verify(Requester, times=1)._create_data([
            {'name': 'building 1', 'locationTypeUuid': 'uuid_type_building', 'parentLocationUuid': 'uuid_city'},
            {'name': 'Park Victor Hugo', 'locationTypeUuid': 'uuid_type_park', 'parentLocationUuid': 'uuid_city'}])

    def test_import_data(self):
        transformer = mock(spec=Transformer)
        requester = Requester(None, None, None, transformer=transformer)
        data_to_post = query[0:1]
        data_to_update = query[1:2]
        post_response = mock({"content": json.dumps(data_to_post),
                              "status_code": http.HTTPStatus.CREATED},
                             spec=Response)

        update_response = mock({"content": json.dumps(data_to_update),
                                "status_code": http.HTTPStatus.CREATED},
                               spec=Response)

        when(requester)._prepare_data(...).thenReturn(query)
        when(requester)._get_data_in_db_to_complete_cache(query)
        when(requester)._data_unknown_and_modified_in_cache(query).thenReturn((data_to_post, data_to_update))
        when(requester)._update_data(data_to_update).thenReturn([update_response])
        when(requester)._add_response_to_cache(update_response)
        when(requester)._create_data(data_to_post).thenReturn([post_response])
        when(requester)._add_response_to_cache(post_response)

        requester.import_data()

        # Verify the call order of the functions
        verify(requester, times=1, inorder=True)._prepare_data(...)
        verify(requester, times=1, inorder=True)._get_data_in_db_to_complete_cache(query)
        verify(requester, times=1, inorder=True)._data_unknown_and_modified_in_cache(query)
        verify(requester, times=1, inorder=True)._update_data(data_to_update)
        verify(requester, times=1, inorder=True)._add_response_to_cache(update_response)
        verify(requester, times=1, inorder=True)._create_data(data_to_post)
        verify(requester, times=1, inorder=True)._add_response_to_cache(post_response)


if __name__ == "__main__":
    logging.basicConfig(level="CRITICAL")
    unittest.main()
