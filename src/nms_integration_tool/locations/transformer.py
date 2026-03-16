# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from ..logger import get_logger
logger = get_logger(__name__)
from typing import List
from nms_integration_tool.transformer import Transformer


class LocationsTransformer(Transformer):
    """Transforms locations data for locations metadata api.

    Transformation consists of:
        - A list of data items represented by dictionaries.
            The keys of each of the dictionaries must be the fields
            of the data in the database.
        - The name of the configuration JSON file containing a dictionary
            with the following keys and their associated values:
                "locationHierarchy": <A list of dictionaries with the following keys:
                    "key": name of the location type row in the data source,
                    "type": corresponding name of the location type in the database,
                    "children" (optional): dictionaries of the location type
                            which depends on this location type>
                The other keys must provide a mapping between names of the keys
                in the provided data and the name in the location metadata service.

    Note that, get_transformed_data_item is not implemented/overridden in this class.
    Indeed, both locations data and location types data must be transformed.
    Therefore, get_transformed_locations_data and get_transformed_location_types_data
    are replacing this function.
    """

    def __init__(self, data: List[dict] | None, config_file: str) -> None:
        super().__init__(data, config_file)
        self._ordered_location_types = self._location_types_from_tree_struct(
            location_type_dependencies_tree=self._config["locationHierarchy"]
        )

    def _get_data_from_configuration(self,
                                     data: List[dict],
                                     parent: str = None) -> List[dict]:
        """Converts location types config to required locations metadata api hierarchy.

        Args:
            data: Tree-like structure of location types data.
            parent: Name of the parent of the actual data.
        """
        location_types_data = []
        for step in data:
            location_types_data.append({"name": step["type"], "parent": parent})

            if "children" in step:
                location_types_data += self._get_data_from_configuration(data=step["children"],
                                                                         parent=step["type"])

        return location_types_data

    def _transform_location_item(self, loc_item: dict, data_row: dict) -> dict:
        """Completes a location item with the content of input data."""
        logger.debug("LocationsTransformer -> Transform %s", data_row)

        for field_name, field_name_in_file in self._config.items():
            if field_name == "locationHierarchy":
                continue
            elif field_name == "custom":
                loc_item["custom"] = {}
                for custom_name, custom_name_in_file in field_name_in_file.items():
                    loc_item["custom"][custom_name] = data_row[custom_name_in_file]
            elif field_name == "approxCoordinates":
                loc_item["approxCoordinates"] = {}
                for coord_name, coord_name_in_file in field_name_in_file.items():
                    loc_item["approxCoordinates"][coord_name] = float(data_row[coord_name_in_file])
            elif field_name == "sequenceNumber":
                loc_item[field_name] = int(data_row[field_name_in_file])
            else:
                loc_item[field_name] = data_row[field_name_in_file]

        return loc_item

    def _location_types_from_tree_struct(self, location_type_dependencies_tree: list) -> List[dict]:
        """Returns the flatten list of ordered location types and add keys.

        Used to retrieve the data dependencies from a tree-like structure of data.
        """
        location_types = []
        for step in location_type_dependencies_tree:
            location_type = {k: v for k, v in step.items() if k != "children"}
            location_types.append(location_type)
            if "children" in step:
                location_types += self._location_types_from_tree_struct(step['children'])

        return location_types

    def _add_location_data_in_tree(self, data_row: dict, tree: list) -> None:
        """Add a data dictionary to a dependencies tree-like structure."""
        for location_level in self._ordered_location_types:
            key_location = location_level["key"]
            type_location = location_level["type"]
            name_location = data_row[key_location]
            if not name_location:  # ensure that the name is not empty
                # It is possible when the location types structure is complex
                continue

            tree_component = {"name": name_location, "type": type_location}

            if "children" not in tree_component:
                tree_component["children"] = []

            should_add = True
            for other in tree:
                if other["name"] == name_location and other["type"] == type_location:
                    # the tree node is already added
                    should_add = False
                    tree_component = other
                    break

            if should_add:
                tree.append(tree_component)

            if "children" not in tree_component:
                break
            tree = tree_component["children"]

        if "children" in tree_component and not tree_component["children"]:
            # tree leaves should not have children key.
            del tree_component["children"]
        self._transform_location_item(tree_component, data_row)

    def _get_tree_structure(self) -> list:
        """Returns the dependency tree structure of the data."""
        tree = []
        # This is called also for location types, thus check for data validity
        if self._data is not None:
            for data_row in self._data:
                self._add_location_data_in_tree(data_row, tree)
        return tree

    def _get_locations_from_tree_struct(self,
                                        data: list,
                                        parent_name: str = None,
                                        grand_parent_name: str = None) -> List[dict]:
        """Gets locations data list from a dependency tree structure.

        Adds 'parent', 'grand_parent_name' keys to retrieve the whole data dependencies without the tree structure.
        """
        locations_data = []
        for location in data:
            component = {k: v for k, v in location.items() if k != "children"}
            component["parent"] = parent_name
            component["grand_parent_name"] = grand_parent_name
            locations_data.append(component)
            if "children" in location:
                locations_data += self._get_locations_from_tree_struct(data=location['children'],
                                                                       parent_name=location["name"],
                                                                       grand_parent_name=parent_name)

        return locations_data

    def get_transformed_location_types_data(self) -> List[dict]:
        """Returns a list of location types data items with additional keys to retrieve parent dependencies."""
        logger.info(f"{self.__class__.__name__} transformer -> Transform location types data items")

        return self._get_data_from_configuration(data=self._config["locationHierarchy"])

    def get_transformed_locations_data(self) -> List[dict]:
        """Returns a list of locations data items with additional keys to retrieve parent dependencies."""
        tree = self._get_tree_structure()
        logger.info(f"{self.__class__.__name__} transformer -> Transform {str(len(tree))} items in tree")
        return self._get_locations_from_tree_struct(data=tree)
