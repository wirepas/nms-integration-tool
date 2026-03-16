# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from ..logger import get_logger
logger = get_logger(__name__)
from typing import List

import nms_integration_tool.api.locations.wirepas_locations_metadata_service_api_client.api.location_metadata as location_metadata
import nms_integration_tool.api.locations.wirepas_locations_metadata_service_api_client.models as location_models
from nms_integration_tool.cache import Cache, CacheType
from nms_integration_tool.locations.transformer import LocationsTransformer
from nms_integration_tool.requester import Requester


class LocationTypesRequester(Requester):
    """Requester for locations metadata api service."""

    def __init__(self, client, cache: Cache, transformer: LocationsTransformer = None, **kwargs) -> None:
        super().__init__(client, CacheType.LOCATION_TYPE, cache, transformer, **kwargs)

        # POST requests in location types api can only be sent 1 by 1
        self.max_nb_elements_post_requests = 1

    def get_db_key_names(self) -> list:
        return ["name"]

    def get_cache_key_names(self) -> list:
        return ["name"]

    def get_parent_key_names(self) -> list:
        return ["parent"]

    def dependency_specific_keys(self) -> list:
        return ["parent"]

    def _get_parent_key_data(self, data: dict, get_uuid: bool = False):
        if "parentTypeUuid" in data:  # data coming from database or cache
            if get_uuid:
                return data["parentTypeUuid"]
            elif data["parentTypeUuid"] in self.uuid_mapping:
                return self._keys_values_of_data(
                    element=self.uuid_mapping[data["parentTypeUuid"]],
                    keys=self.get_cache_key_names()
                )

        elif not get_uuid and "parent" in data and data["parent"] is not None:  # data coming from data source
            return self._keys_values_of_data(element=data, keys=self.get_parent_key_names())

        # No parent can be identified
        return None

    def _prepare_data(self, **kwargs) -> List[dict]:
        # get data from transformer attribute
        return self.transformer.get_transformed_location_types_data()

    def _add_cache_keys_to_db_data(self, db_data: dict) -> bool:
        db_data["parent"] = None
        if "parentTypeUuid" in db_data:
            try:
                db_data["parent"] = self.uuid_mapping[db_data["parentTypeUuid"]]["name"]
            except KeyError:
                logger.warning(f"{self.service_cache_type.name.lower()} service -> "
                                f"Data from database could not be converted: {db_data}.")
                return False

        return True

    def _import_location_types_to_db(self, data: List[dict], **kwargs) -> list:
        """Imports location types data to database.

        As these data have dependencies, query data levels by levels
        in the associated dependency data tree structure.
        """
        responses = []
        assert isinstance(data, list)
        for data_level in self._get_dependency_levels_from_data(data):
            assert isinstance(data_level, list)
            messages_to_send = []
            for location_type in data_level:
                location_type_data = {
                    k: v for k, v in location_type.items() if k not in self.dependency_specific_keys()
                }
                parent = location_type["parent"]
                if parent is not None:
                    location_type_data["parentTypeUuid"] = self.cache.get(
                        service_cache_type=CacheType.LOCATION_TYPE,
                        key=self._get_parent_key_data(location_type)
                    )["uuid"]

                messages_to_send.append(location_type_data)

            for resp in super()._create_data(messages_to_send, **kwargs):
                self._add_response_to_cache(resp)
                responses.append(resp)

        return responses

    def _create_data(self, data: List[dict] = None, **kwargs) -> list:
        return self._import_location_types_to_db(data, **kwargs)

    def _get_data_in_db_to_complete_cache(self, data: List[dict]) -> None:
        # Sort by location level before completing the cache.
        for data_level in self._get_dependency_levels_from_data(data):
            super()._get_data_in_db_to_complete_cache(data_level)

    def _add_responses_to_cache(self, responses: list) -> None:
        resp_json = []
        for resp in responses:
            resp_json += self._get_response_content(resp)

        levels = self._get_dependency_levels_from_data(resp_json, ["uuid"], True)

        for level in levels:
            self._treat_response_content(level)
            for data in level:
                self._add_to_uuid_mapping(data)
            self._add_json_data_to_cache(self._delete_unwanted_fields_from_responses_json(level))

    def _request_post(self, data: List[dict]):
        data_to_send = []
        for location_type in data:
            data_to_send.append(location_models.CreateLocationTypesBodyItem.from_dict(location_type))

        return location_metadata.create_location_types.sync_detailed(client=self.client, body=data_to_send)

    def _request_get(self, query=None, **kwargs):
        return location_metadata.get_location_types.sync_detailed(client=self.client, query=query, **kwargs)

    def _request_patch(self, data: List[dict]):
        # data is a list of one data item as, self.max_nb_elements_post_requests equals 1
        # it means that the data to update are patch in groups of 1.
        location_type_uuid = data[0].pop("uuid")
        data_to_send = location_models.LocationTypeInfo.from_dict(data[0])

        # put back uuid in the data, as this data might be re-used
        data[0]["uuid"] = location_type_uuid

        return location_metadata.patch_location_type.sync_detailed(
            location_type_uuid=location_type_uuid,
            client=self.client, body=data_to_send
        )


class LocationsRequester(Requester):
    """Requester for location metadata api."""

    def __init__(self, client, cache: Cache = None, transformer: LocationsTransformer = None, **kwargs) -> None:
        super().__init__(client, CacheType.LOCATION, cache, transformer, **kwargs)
        self.location_types_requester = LocationTypesRequester(client, cache, transformer, **kwargs)

    def get_db_key_names(self) -> list:
        return ["name"]

    def get_cache_key_names(self) -> list:
        return ["name", "parent"]

    def get_parent_key_names(self) -> list:
        return ["parent", "grand_parent_name"]

    def dependency_specific_keys(self) -> list:
        return ["type", "parent", "grand_parent_name"]

    def _get_parent_key_data(self, data: dict, get_uuid: bool = False):
        # data coming from database or cache
        if "parentLocationUuid" in data:
            if get_uuid:
                return data["parentLocationUuid"]
            elif data["parentLocationUuid"] in self.uuid_mapping:
                return self._keys_values_of_data(
                    element=self.uuid_mapping[data["parentLocationUuid"]],
                    keys=self.get_cache_key_names()
                )

        elif not get_uuid and "parent" in data and data["parent"] is not None:  # data coming from data source
            cache_parent_key_names = self.get_parent_key_names()
            return self._keys_values_of_data(data, cache_parent_key_names)

        # No parent can be identified
        return None

    def _add_cache_keys_to_db_data(self, db_data: dict) -> bool:
        try:
            db_data["type"] = self.location_types_requester.uuid_mapping[db_data["locationTypeUuid"]]["name"]
        except KeyError:
            logger.warning(f"{self.service_cache_type.name.lower()} service -> "
                            f"Data from database could not be converted: {db_data}.")
            return False

        db_data["parent"] = None
        if "parentLocationUuid" in db_data:
            if db_data["parentLocationUuid"] not in self.uuid_mapping:
                # different data locations have the same name
                return False

            db_data["parent"] = self.uuid_mapping[db_data["parentLocationUuid"]]["name"]

        return True

    def _prepare_data(self, add_location_type=True, **kwargs) -> List[dict]:
        if add_location_type:
            self.location_types_requester.import_data()

        # return data from transformer attribute
        return self.transformer.get_transformed_locations_data()

    def _import_locations_to_db(self, data: List[dict], **kwargs) -> list:
        """Import location data to database."""
        responses = []
        dependency_specific_keys = self.dependency_specific_keys()

        for data_level in self._get_dependency_levels_from_data(data):
            assert isinstance(data_level, list)
            messages_to_send = []
            for location in data_level:
                parent_name = location["parent"]
                location_data = {k: v for k, v in location.items() if k not in dependency_specific_keys}

                location_data["locationTypeUuid"] = self.cache.get(service_cache_type=CacheType.LOCATION_TYPE,
                                                                   key=location["type"])["uuid"]

                if parent_name is not None:
                    location_data["parentLocationUuid"] = self.cache.get(
                        service_cache_type=CacheType.LOCATION,
                        key=self._get_parent_key_data(location))["uuid"]

                messages_to_send.append(location_data)

            if messages_to_send:
                for resp in super()._create_data(messages_to_send, **kwargs):
                    self._add_response_to_cache(resp)
                    responses.append(resp)

        return responses

    def _create_data(self, data: List[dict] = None, **kwargs) -> list:
        return self._import_locations_to_db(data, **kwargs)

    def _add_responses_to_cache(self, responses: list) -> None:
        resp_json = []
        for resp in responses:
            resp_json += self._get_response_content(resp)

        levels = self._get_dependency_levels_from_data(resp_json, ["uuid"], True)

        for level in levels:
            self._treat_response_content(level)
            for data in level:
                self._add_to_uuid_mapping(data)

            self._add_json_data_to_cache(self._delete_unwanted_fields_from_responses_json(level))

    def _get_data_in_db_to_complete_cache(self, data: List[dict]) -> None:
        # Sort by location level before completing the cache.
        for data_level in self._get_dependency_levels_from_data(data):
            super()._get_data_in_db_to_complete_cache(data_level)

    def _request_post(self, data: List[dict]):
        data_to_send = []
        for location in data:
            data_to_send.append(location_models.CreateLocationsBodyItem.from_dict(location))

        return location_metadata.create_locations.sync_detailed(
            client=self.client,
            body=data_to_send)

    def _request_get(self, query="", **kwargs):
        search_locations = location_models.SearchLocationsBody.from_dict({"query": query, **kwargs})

        return location_metadata.search_locations.sync_detailed(client=self.client, body=search_locations, **kwargs)

    def _request_patch(self, data: List[dict]):
        data_to_send = []

        for location in data:
            data_to_send.append(location_models.Location.from_dict(location))

        return location_metadata.patch_locations.sync_detailed(client=self.client, body=data_to_send)
