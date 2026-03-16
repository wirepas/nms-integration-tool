# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import unittest
from unittest.mock import patch

from mockito import unstub, verifyStubbedInvocationsAreUsed

from nms_integration_tool.gateways.transformer import GatewaysTransformer
from nms_integration_tool.locations.transformer import LocationsTransformer
from nms_integration_tool.networks.transformer import NetworksTransformer
from nms_integration_tool.nodes.transformer import NodesTransformer
from nms_integration_tool.transformer import Transformer


class TransformersTesting(unittest.TestCase):
    def tearDown(self):
        try:
            verifyStubbedInvocationsAreUsed()
        finally:
            unstub()

    @patch.object(Transformer, '_get_configuration')
    def test_networks_transformer(self, mock_get_config):
        networks_configuration = {
            "custom": {
                "customField1": "custom_field1",
                "customField2": "custom_field2",
            },
            "description": "description",
            "name": "name",
            "address": "address"
        }
        mock_get_config.return_value = networks_configuration

        networks_data = [
            {
                "name": "network 1",
                "address": "1",
                "description": "small description",
                "custom_field1": "custom field 1",
                "custom_field2": "custom field 2",
                "field_to_delete": "values to delete"
            },
            {
                "name": "network 2",
                "address": "2",
                "description": "small description",
                "custom_field1": "another custom field 1",
                "custom_field2": "another custom field 2"
            }
        ]

        expected = [
            {
                "name": "network 1",
                "address": 1,
                "description": "small description",
                "custom": {"customField1": "custom field 1", "customField2": "custom field 2"},
            },
            {
                "name": "network 2",
                "address": 2,
                "description": "small description",
                "custom": {"customField1": "another custom field 1", "customField2": "another custom field 2"},
            }
        ]

        net_transformer = NetworksTransformer(networks_data, None)
        self.assertEqual(net_transformer.get_transformed_data(), expected)

    @patch.object(Transformer, '_get_configuration')
    def test_networks_transformer_with_coordinates(self, mock_get_config):
        configuration = {
            "name": "name",
            "address": "address",
            "coordinates": {
                "latitude": "lat",
                "longitude": "lon",
                "altitude": "alt"
            }
        }
        mock_get_config.return_value = configuration

        data = [{"name": "net", "address": "10", "lat": "48.5", "lon": "2.3", "alt": "100"}]
        expected = [{"name": "net", "address": 10,
                     "coordinates": {"latitude": 48.5, "longitude": 2.3, "altitude": 100.0}}]

        result = NetworksTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_gateways_transformer(self, mock_get_config):
        gateways_configuration = {
            "name": "name",
            "description": "description",
            "custom": {
                "customField1": "custom_field1",
                "customField2": "custom_field2"
            },
            "gatewayId": "gateway_id",
            "networkAddress": "network",
            "locationName": "location",
            "locationParentName": "location_parent"
        }
        mock_get_config.return_value = gateways_configuration

        gateways_data = [
            {
                "name": "gateway 1",
                "network": "1",
                "gateway_id": "GW 1",
                "description": "small description",
                "custom_field1": "custom field 1",
                "custom_field2": "custom field 2",
                "field_to_delete": "values to delete",
                "location": "location",
                "location_parent": "location parent"
            },
            {
                "name": "gateway 2",
                "network": "1",
                "gateway_id": "GW 2",
                "description": "small description",
                "custom_field1": "another custom field 1",
                "custom_field2": "another custom field 2",
                "location": "location",
                "location_parent": "location parent"
            }
        ]

        expected = [
            {
                "name": "gateway 1", "networkAddress": 1, "gatewayId": "GW 1",
                "description": "small description",
                "custom": {"customField1": "custom field 1", "customField2": "custom field 2"},
                "isVirtual": False,
                "locationName": "location", "locationParentName": "location parent"
            },
            {
                "name": "gateway 2", "networkAddress": 1, "gatewayId": "GW 2",
                "description": "small description",
                "custom": {"customField1": "another custom field 1", "customField2": "another custom field 2"},
                "isVirtual": False,
                "locationName": "location", "locationParentName": "location parent"
            }
        ]

        result = GatewaysTransformer(gateways_data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_gateways_transformer_explicit_is_virtual_true(self, mock_get_config):
        configuration = {
            "name": "name",
            "networkAddress": "network",
            "gatewayId": "gw_id",
            "isVirtual": "is_virtual"
        }
        mock_get_config.return_value = configuration

        data = [{"name": "vgw", "network": "5", "gw_id": "VGW1", "is_virtual": "true"}]
        expected = [{"name": "vgw", "networkAddress": 5, "gatewayId": "VGW1", "isVirtual": True}]

        result = GatewaysTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_gateways_transformer_with_coordinates(self, mock_get_config):
        configuration = {
            "name": "name",
            "networkAddress": "network",
            "gatewayId": "gw_id",
            "coordinates": {"latitude": "lat", "longitude": "lon", "altitude": "alt"}
        }
        mock_get_config.return_value = configuration

        data = [{"name": "gw", "network": "3", "gw_id": "GW3", "lat": "60.1", "lon": "24.9", "alt": "50.0"}]
        expected = [{"name": "gw", "networkAddress": 3, "gatewayId": "GW3",
                     "isVirtual": False,
                     "coordinates": {"latitude": 60.1, "longitude": 24.9, "altitude": 50.0}}]

        result = GatewaysTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer(self, mock_get_config):
        nodes_configuration = {
            "name": "name",
            "description": "description",
            "custom": {
                "customField1": "custom_field1",
                "customField2": "custom_field2"
            },
            "address": "node_id",
            "networkAddress": "network",
            "locationName": "location",
            "locationParentName": "location_parent"
        }
        mock_get_config.return_value = nodes_configuration

        nodes_data = [
            {
                "name": "node 1", "network": "1", "node_id": "111",
                "description": "small description",
                "custom_field1": "custom field 1", "custom_field2": "custom field 2",
                "field_to_delete": "values to delete",
                "location": "location", "location_parent": "location parent",
            },
            {
                "name": "node 2", "network": "1", "node_id": "112",
                "description": "small description",
                "custom_field1": "another custom field 1", "custom_field2": "another custom field 2",
                "location": "location", "location_parent": "location parent",
            }
        ]

        expected = [
            {
                "name": "node 1", "networkAddress": 1, "address": 111,
                "description": "small description",
                "custom": {"customField1": "custom field 1", "customField2": "custom field 2"},
                "isVirtual": False,
                "locationName": "location", "locationParentName": "location parent"
            },
            {
                "name": "node 2", "networkAddress": 1, "address": 112,
                "description": "small description",
                "custom": {"customField1": "another custom field 1", "customField2": "another custom field 2"},
                "isVirtual": False,
                "locationName": "location", "locationParentName": "location parent"
            }
        ]

        result = NodesTransformer(nodes_data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_legacy_boolean_fields(self, mock_get_config):
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
            "custom": {
                "legacy_is_anchor": "is_anchor",
                "legacy_approved": "approved",
                "legacy_virtual": "virtual",
            }
        }
        mock_get_config.return_value = configuration

        data = [{"node_id": "10", "network": "1", "is_anchor": "t", "approved": "f", "virtual": "t"}]
        expected = [{"address": 10, "networkAddress": 1,
                     "custom": {"legacy_is_anchor": True, "legacy_approved": False, "legacy_virtual": True},
                     "isVirtual": False}]

        result = NodesTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_null_values_are_skipped(self, mock_get_config):
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
            "description": "desc",
            "name": "name"
        }
        mock_get_config.return_value = configuration

        # Empty string evaluates as falsy and should be skipped
        data = [{"node_id": "5", "network": "2", "desc": "", "name": "active-node"}]
        expected = [{"address": 5, "networkAddress": 2, "name": "active-node", "isVirtual": False}]

        result = NodesTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_nested_two_level_custom(self, mock_get_config):
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
            "custom": {
                "meta": {
                    "source": "src_col",
                    "region": "region_col"
                }
            }
        }
        mock_get_config.return_value = configuration

        data = [{"node_id": "7", "network": "3", "src_col": "db", "region_col": "EU"}]
        expected = [{"address": 7, "networkAddress": 3,
                     "custom": {"meta": {"source": "db", "region": "EU"}},
                     "isVirtual": False}]

        result = NodesTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_locations_transformer(self, mock_get_config):
        locations_configuration = {
            "locationHierarchy": [
                {"type": "Region", "key": "Region Name", "children": [
                    {"type": "City", "key": "City Name", "children": [
                        {"type": "Building", "key": "Building Name"}
                    ]}
                ]}
            ],
            "approxCoordinates": {
                "latitude": "lat",
                "longitude": "long",
                "altitude": "alt"
            },
            "custom": {
                "customField1": "custom_field1",
                "customField2": "custom_field2",
                "customField3": "custom_field3"
            },
            "description": "description"
        }
        mock_get_config.return_value = locations_configuration

        locations_data = [
            {
                "Region Name": "region 1", "City Name": "city 1", "Building Name": "A normal building",
                "lat": "46.3", "long": "5.1", "alt": "8",
                "description": "small description",
                "custom_field1": "custom field 1", "custom_field2": "custom field 2",
                "custom_field3": "custom field 3",
                "field_to_delete": "values to delete"
            },
            {
                "Region Name": "region 1", "City Name": "city 2", "Building Name": "Another normal building",
                "lat": "45.3", "long": "6.1", "alt": "7",
                "description": "small description",
                "custom_field1": "custom field 1", "custom_field2": "custom field 2",
                "custom_field3": "custom field 3",
            }
        ]

        expected_location_types = [
            {"name": "Region", "parent": None},
            {"name": "City", "parent": "Region"},
            {"name": "Building", "parent": "City"}
        ]

        expected_locations = [
            {"name": "region 1", "type": "Region", "parent": None, "grand_parent_name": None},
            {"name": "city 1", "type": "City", "parent": "region 1", "grand_parent_name": None},
            {
                "name": "A normal building", "type": "Building",
                "approxCoordinates": {"latitude": 46.3, "longitude": 5.1, "altitude": 8.0},
                "custom": {"customField1": "custom field 1", "customField2": "custom field 2",
                           "customField3": "custom field 3"},
                "description": "small description",
                "parent": "city 1", "grand_parent_name": "region 1"
            },
            {"name": "city 2", "type": "City", "parent": "region 1", "grand_parent_name": None},
            {
                "name": "Another normal building", "type": "Building",
                "approxCoordinates": {"latitude": 45.3, "longitude": 6.1, "altitude": 7.0},
                "custom": {"customField1": "custom field 1", "customField2": "custom field 2",
                           "customField3": "custom field 3"},
                "description": "small description",
                "parent": "city 2", "grand_parent_name": "region 1"
            }
        ]

        transformer = LocationsTransformer(locations_data, None)
        self.assertEqual(transformer.get_transformed_location_types_data(), expected_location_types)
        self.assertEqual(transformer.get_transformed_locations_data(), expected_locations)

    @patch.object(Transformer, '_get_configuration')
    def test_networks_transformer_ignores_extra_columns(self, mock_get_config):
        # CSV rows may contain columns not present in the config (e.g., an 'Id' index column).
        # The transformer must iterate over config keys, so extra columns are silently ignored.
        configuration = {
            "name": "name",
            "address": "address",
        }
        mock_get_config.return_value = configuration

        data = [{"Id": "0", "name": "net-x", "address": "42", "irrelevant_col": "noise"}]
        expected = [{"name": "net-x", "address": 42}]

        result = NetworksTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)
        self.assertNotIn("Id", result[0])

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_with_coordinates(self, mock_get_config):
        # Nodes config supports GPS coordinates (latitude/longitude/altitude as floats)
        configuration = {
            "address": "address",
            "networkAddress": "network_address",
            "coordinates": {
                "latitude": "lat",
                "longitude": "lon",
                "altitude": "alt",
            },
            "locationName": "location_name",
            "locationParentName": "location_parent_name",
        }
        mock_get_config.return_value = configuration

        data = [{
            "address": "1", "network_address": "1",
            "lat": "45.82336682980463", "lon": "5.481666990161637", "alt": "7",
            "location_name": "Grenoble Building 1", "location_parent_name": "Grenoble",
        }]
        expected = [{
            "address": 1, "networkAddress": 1,
            "coordinates": {"latitude": 45.82336682980463, "longitude": 5.481666990161637, "altitude": 7.0},
            "locationName": "Grenoble Building 1", "locationParentName": "Grenoble",
            "isVirtual": False,
        }]

        result = NodesTransformer(data, None).get_transformed_data()
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_locations_transformer_two_tree_location_types(self, mock_get_config):
        # location_types/config.json contains two independent root trees:
        # Region→Village  and  Country→{Town, City→Suburb}
        configuration = {
            "locationHierarchy": [
                {"type": "Region", "key": "Region Name", "children": [
                    {"type": "Village", "key": "Village Name"}
                ]},
                {"type": "Country", "key": "Country Name", "children": [
                    {"type": "Town", "key": "Town Name"},
                    {"type": "City", "key": "City Name", "children": [
                        {"type": "Suburb", "key": "Suburb Name"}
                    ]},
                ]},
            ]
        }
        mock_get_config.return_value = configuration

        expected_types = [
            {"name": "Region", "parent": None},
            {"name": "Village", "parent": "Region"},
            {"name": "Country", "parent": None},
            {"name": "Town", "parent": "Country"},
            {"name": "City", "parent": "Country"},
            {"name": "Suburb", "parent": "City"},
        ]

        transformer = LocationsTransformer(None, None)
        self.assertEqual(transformer.get_transformed_location_types_data(), expected_types)

    @patch.object(Transformer, '_get_configuration')
    def test_locations_transformer_two_tree_with_data(self, mock_get_config):
        # Rows where Region Name is populated belong to the Region tree;
        # rows where Country Name is populated belong to the Country tree.
        # Empty keys in each row skip that branch during traversal.
        configuration = {
            "locationHierarchy": [
                {"type": "Region", "key": "Region Name", "children": [
                    {"type": "Village", "key": "Village Name"}
                ]},
                {"type": "Country", "key": "Country Name", "children": [
                    {"type": "Town", "key": "Town Name"},
                ]},
            ]
        }
        mock_get_config.return_value = configuration

        data = [
            {"Region Name": "region", "Village Name": "village1", "Country Name": "", "Town Name": ""},
            {"Region Name": "region", "Village Name": "village2", "Country Name": "", "Town Name": ""},
            {"Region Name": "", "Village Name": "", "Country Name": "country", "Town Name": "town1"},
        ]

        transformer = LocationsTransformer(data, None)
        locations = transformer.get_transformed_locations_data()

        loc_by = {(l["name"], l["type"]): l for l in locations}

        # Region tree
        self.assertIsNone(loc_by[("region", "Region")]["parent"])
        self.assertEqual(loc_by[("village1", "Village")]["parent"], "region")
        self.assertEqual(loc_by[("village2", "Village")]["parent"], "region")

        # Country tree (independent root, no parent)
        self.assertIsNone(loc_by[("country", "Country")]["parent"])
        self.assertEqual(loc_by[("town1", "Town")]["parent"], "country")

    @patch.object(Transformer, '_get_configuration')
    def test_data_with_non_existing_field_name(self, mock_get_config):
        configuration = {
            "name": "name",
            "address": "address",
            "description": "non_existing_field_name"
        }
        mock_get_config.return_value = configuration

        data = [{"name": "network 1", "address": "1"}]

        net_transformer = NetworksTransformer(data, None)

        with self.assertRaises(KeyError):
            net_transformer.get_transformed_data()

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_get_network_addresses(self, mock_get_config):
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
        }
        mock_get_config.return_value = configuration

        data = [
            {"node_id": "1", "network": "100"},
            {"node_id": "2", "network": "200"},
            {"node_id": "3", "network": "100"},  # duplicate network address
        ]

        transformer = NodesTransformer(data, None)
        result = transformer.get_network_addresses()

        self.assertEqual(result, {100, 200})

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_exclude_sink_nodes(self, mock_get_config):
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
            "name": "name",
        }
        mock_get_config.return_value = configuration

        data = [
            {"node_id": "111", "network": "1", "name": "regular node"},
            {"node_id": "222", "network": "1", "name": "sink node"},
            {"node_id": "333", "network": "2", "name": "another regular node"},
        ]

        transformer = NodesTransformer(data, None)
        transformer.exclude_sink_nodes({(222, 1)})
        result = transformer.get_transformed_data()

        expected = [
            {"address": 111, "networkAddress": 1, "name": "regular node", "isVirtual": False},
            {"address": 333, "networkAddress": 2, "name": "another regular node", "isVirtual": False},
        ]
        self.assertEqual(result, expected)

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_exclude_sink_nodes_empty_set(self, mock_get_config):
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
            "name": "name",
        }
        mock_get_config.return_value = configuration

        data = [
            {"node_id": "111", "network": "1", "name": "node 1"},
            {"node_id": "222", "network": "1", "name": "node 2"},
        ]

        transformer = NodesTransformer(data, None)
        transformer.exclude_sink_nodes(set())
        result = transformer.get_transformed_data()

        self.assertEqual(len(result), 2)

    @patch.object(Transformer, '_get_configuration')
    def test_nodes_transformer_exclude_sink_nodes_multiple_networks(self, mock_get_config):
        # Same node address in different networks — only the sink network's node is excluded
        configuration = {
            "address": "node_id",
            "networkAddress": "network",
        }
        mock_get_config.return_value = configuration

        data = [
            {"node_id": "100", "network": "1"},  # sink in network 1
            {"node_id": "100", "network": "2"},  # same address but different network — keep
        ]

        transformer = NodesTransformer(data, None)
        transformer.exclude_sink_nodes({(100, 1)})
        result = transformer.get_transformed_data()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["networkAddress"], 2)


if __name__ == "__main__":
    unittest.main()
