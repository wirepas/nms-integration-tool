# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import csv
import json
import os
import unittest

from nms_integration_tool.gateways.transformer import GatewaysTransformer
from nms_integration_tool.networks.transformer import NetworksTransformer
from nms_integration_tool.nodes.transformer import NodesTransformer

_CONFIGS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "examples", "configs")
)


def _load_json(path):
    with open(path) as f:
        return json.load(f)


def _load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Config file structure validation
# ---------------------------------------------------------------------------

class NetworksConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = _load_json(os.path.join(_CONFIGS_DIR, "networks", "config.json"))

    def test_config_is_dict(self):
        self.assertIsInstance(self.config, dict)

    def test_required_top_level_keys(self):
        for key in ("address",):
            self.assertIn(key, self.config)

    def test_custom_is_dict_with_field_mappings(self):
        if "custom" in self.config:
            self.assertIsInstance(self.config["custom"], dict)
            self.assertGreater(len(self.config["custom"]), 0)


class NetworksCsvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = _load_csv(os.path.join(_CONFIGS_DIR, "networks", "networks.csv"))

    def test_csv_has_rows(self):
        self.assertGreater(len(self.rows), 0)

    def test_required_columns_present(self):
        for col in ("address",):
            self.assertIn(col, self.rows[0], f"Missing column: {col}")

    def test_address_column_is_numeric(self):
        for row in self.rows:
            self.assertTrue(row["address"].isdigit(), f"Non-numeric address: {row['address']}")

    def test_config_column_names_exist_in_csv(self):
        config = _load_json(os.path.join(_CONFIGS_DIR, "networks", "config.json"))
        cols = set(self.rows[0].keys())
        for field, col_name in config.items():
            if field == "custom":
                for _, csv_col in col_name.items():
                    self.assertIn(csv_col, cols, f"Custom column '{csv_col}' not in CSV")
            elif isinstance(col_name, str):
                self.assertIn(col_name, cols, f"Column '{col_name}' not in CSV")


class NodesConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = _load_json(os.path.join(_CONFIGS_DIR, "nodes", "config.json"))

    def test_config_is_dict(self):
        self.assertIsInstance(self.config, dict)

    def test_required_top_level_keys(self):
        for key in ("address", "networkAddress"):
            self.assertIn(key, self.config)

    def test_coordinates_has_lat_lon_alt(self):
        if "coordinates" in self.config:
            coords = self.config["coordinates"]
            for key in ("latitude", "longitude", "altitude"):
                self.assertIn(key, coords)

    def test_custom_is_dict(self):
        if "custom" in self.config:
            self.assertIsInstance(self.config["custom"], dict)


class NodesCsvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = _load_csv(os.path.join(_CONFIGS_DIR, "nodes", "nodes.csv"))

    def test_csv_has_rows(self):
        self.assertGreater(len(self.rows), 0)

    def test_required_columns_present(self):
        for col in ("address", "network_address"):
            self.assertIn(col, self.rows[0], f"Missing column: {col}")

    def test_lat_lon_alt_are_numeric(self):
        for row in self.rows:
            if "lat" in row:
                float(row["lat"])
            if "lon" in row:
                float(row["lon"])
            if "alt" in row:
                float(row["alt"])

    def test_address_is_numeric(self):
        for row in self.rows:
            self.assertTrue(row["address"].isdigit(), f"Non-numeric address: {row['address']}")
            self.assertTrue(row["network_address"].isdigit(), f"Non-numeric nw addr: {row['network_address']}")


class GatewaysConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = _load_json(os.path.join(_CONFIGS_DIR, "gateways", "config.json"))

    def test_config_is_dict(self):
        self.assertIsInstance(self.config, dict)

    def test_required_top_level_keys(self):
        for key in ("gatewayId", "networkAddress"):
            self.assertIn(key, self.config)

    def test_custom_is_dict(self):
        if "custom" in self.config:
            self.assertIsInstance(self.config.get("custom", {}), dict)


class GatewaysCsvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = _load_csv(os.path.join(_CONFIGS_DIR, "gateways", "gateways.csv"))

    def test_csv_has_rows(self):
        self.assertGreater(len(self.rows), 0)

    def test_required_columns_present(self):
        for col in ("gateway_id", "network_address"):
            self.assertIn(col, self.rows[0], f"Missing column: {col}")

    def test_network_address_is_numeric(self):
        for row in self.rows:
            self.assertTrue(row["network_address"].isdigit())


# ---------------------------------------------------------------------------
# Transformer integration tests: real config files + real CSV data
# ---------------------------------------------------------------------------

class NetworksTransformerIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = os.path.join(_CONFIGS_DIR, "networks", "config.json")
        cls.config = _load_json(cls.config_path)
        cls.rows = _load_csv(os.path.join(_CONFIGS_DIR, "networks", "networks.csv"))
        cls.result = NetworksTransformer(cls.rows, cls.config_path).get_transformed_data()

    def test_all_rows_transformed(self):
        self.assertEqual(len(self.result), len(self.rows))

    def test_output_has_required_fields(self):
        for item in self.result:
            for field in ("address",):
                self.assertIn(field, item)

    def test_address_is_int(self):
        for item in self.result:
            self.assertIsInstance(item["address"], int)

    def test_address_values_match_csv(self):
        for item, row in zip(self.result, self.rows):
            self.assertEqual(item["address"], int(row["address"]))

    def test_name_values_match_csv(self):
        for item, row in zip(self.result, self.rows):
            self.assertEqual(item["name"], row["name"])

    def test_custom_fields_mapped(self):
        if "custom" in self.config:
            for item in self.result:
                self.assertIn("customField1", item["custom"])
                self.assertIn("customField2", item["custom"])

    def test_extra_id_column_not_in_output(self):
        # networks.csv has an extra 'Id' index column not in the config
        for item in self.result:
            self.assertNotIn("Id", item)
            self.assertNotIn("id", item)


class NodesTransformerIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = os.path.join(_CONFIGS_DIR, "nodes", "config.json")
        cls.config = _load_json(cls.config_path)
        cls.rows = _load_csv(os.path.join(_CONFIGS_DIR, "nodes", "nodes.csv"))
        cls.result = NodesTransformer(cls.rows, cls.config_path).get_transformed_data()

    def test_all_rows_transformed(self):
        self.assertEqual(len(self.result), len(self.rows))

    def test_output_has_required_fields(self):
        for item in self.result:
            for field in ("address", "networkAddress"):
                self.assertIn(field, item)

    def test_address_and_network_address_are_ints(self):
        for item in self.result:
            self.assertIsInstance(item["address"], int)
            self.assertIsInstance(item["networkAddress"], int)

    def test_coordinates_are_floats(self):
        if "coordinates" in self.config:
            for item in self.result:
                for key in ("latitude", "longitude", "altitude"):
                    self.assertIsInstance(item["coordinates"][key], float)

    def test_is_virtual_defaults_to_false(self):
        if "isVirtual" not in self.config:
            for item in self.result:
                self.assertFalse(item["isVirtual"])

    def test_location_fields_match_csv(self):
        for item, row in zip(self.result, self.rows):
            if "locationName" in self.config:
                self.assertEqual(item["locationName"], row["location_name"])
            if "locationParentName" in self.config:
                self.assertEqual(item["locationParentName"], row["location_parent_name"])

    def test_first_row_coordinates_match_csv(self):
        if "coordinates" in self.config:
            first = self.result[0]
            row = self.rows[0]
            self.assertAlmostEqual(first["coordinates"]["latitude"], float(row["lat"]))
            self.assertAlmostEqual(first["coordinates"]["longitude"], float(row["lon"]))
            self.assertAlmostEqual(first["coordinates"]["altitude"], float(row["alt"]))


class GatewaysTransformerIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = os.path.join(_CONFIGS_DIR, "gateways", "config.json")
        cls.rows = _load_csv(os.path.join(_CONFIGS_DIR, "gateways", "gateways.csv"))
        cls.result = GatewaysTransformer(cls.rows, cls.config_path).get_transformed_data()

    def test_all_rows_transformed(self):
        self.assertEqual(len(self.result), len(self.rows))


if __name__ == "__main__":
    unittest.main()
