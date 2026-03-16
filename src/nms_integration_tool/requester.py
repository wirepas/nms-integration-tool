# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import json
from math import ceil
from typing import List

from .logger import get_logger
from .transformer import Transformer
from .cache import Cache, CacheType

logger = get_logger(__name__)

# Response fields to be deleted before being pushed to cache
FIELDS_TO_DELETE_FROM_RESPONSES = ["modificationTime"]


class Requester:
    def __init__(
            self,
            api_client,
            service_cache_type: CacheType,
            cache: Cache,
            transformer: Transformer = None,
            max_nb_elements_requests: int = 1000
    ):
        """Initialize a generic class for metadata services data import.

        Args:
            api_client: Client to be used to connect to metadata API services.
            service_cache_type: Service cache type.
            cache: Cache to store data from metadata services responses.
            transformer: Transformer
            max_nb_elements_requests: Max number of data items handled in post and patch requests.
        """
        self.client = api_client
        self.service_cache_type = service_cache_type
        self.cache = cache
        self.transformer = transformer
        self.max_nb_elements_requests = max_nb_elements_requests

        # maps the uuid of the elements to their associated data
        self.uuid_mapping = {}

    # Private methods
    def _request_get(self, **kwargs):
        """Get data from the concerned metadata service.

        Note: It must be implemented by children classes.
        """
        raise NotImplementedError

    def _request_post(self, data: List[dict]):
        """Post data to the concerned metadata service.

        Note: It must be implemented by children classes.
        """
        raise NotImplementedError

    def _request_patch(self, data: List[dict]):
        """Patch data from the concerned metadata service.

        Note: It must be implemented by children classes.
        """
        raise NotImplementedError

    def get_db_key_names(self) -> list:
        """Return the keys linked to the related database metadata data.

        Note: This method needs to be implemented by children classes
        """
        raise NotImplementedError

    def get_cache_key_names(self) -> list:
        """Return the keys associated to the data in the cache.

        Note: The key list should include the list returned by get_db_key_names method
              This method needs to be implemented by children classes
              if the database key is different from the cache key.
        """
        return self.get_db_key_names()

    def dependency_specific_keys(self) -> list:
        """Return the keys which have been added to the data
        to retrieve the dependency between data items
        while they have no uuid and to cache those.

        These keys must be removed from data
        before pushing those to the metadata service API.
        """
        return []

    def _get_parent_key_data(self, data: dict, get_uuid: bool = False):
        """Return the key data of a parent of a data item.
        If the item has a parent, None otherwise.

        Args:
            data: data whose parent data information are searched
            get_uuid: If True, return the uuid of the parent, otherwise return its keys.
                    The keys are the cache keys of the parent if they can be obtained
                    otherwise the parent field of the data.

        Note: It should only be implemented for data with parent dependencies.
        """
        return

    @staticmethod
    def is_response_valid(resp) -> bool:
        """Return True if a response or a list of responses
        from the client is valid, otherwise raise an AssertionError. """
        if isinstance(resp, list):
            for response in resp:
                assert 200 <= response.status_code.value <= 299, \
                    (f"Data could not be retrieved! "
                     f"Error code: {response.status_code.value}, response: {response.content}")
        else:
            assert 200 <= resp.status_code.value <= 299, \
                f"Data could not be retrieved! Error code: {resp.status_code.value}, response: {resp.content}"
        return True

    @staticmethod
    def _delete_unwanted_fields_from_responses_json(resp_json: List[dict]) -> List[dict]:
        """Delete inplace the fields present in FIELDS_TO_DELETE_FROM_RESPONSES
            from a list of data items and return the list.
        """
        if isinstance(resp_json, list):
            for resp in resp_json:
                for field in FIELDS_TO_DELETE_FROM_RESPONSES:
                    if field in resp:
                        del resp[field]

        return resp_json

    @staticmethod
    def _keys_values_of_data(element: dict, keys: list):
        """Returns values of the keys that identify a data element.

        Returns a tuple of the values if the key contains more than 1 element.
        """
        if len(keys) == 1:
            return element[keys[0]]
        return tuple(element[name] for name in keys)

    @staticmethod
    def _chunk_list(list_to_chunk: list, chunk_len: int):
        """Chunks a list into a list of chunks of size chunk_len."""
        return [list_to_chunk[chunk_len * i:chunk_len * (i + 1)]
                for i in range(ceil(len(list_to_chunk) / chunk_len))]

    def _network_info_to_uuid(self, data: dict) -> None:
        """Transforms network info inside a data item to the related network uuid.

        Replace networkAddress key with associated networkUuid key if networkUuid is not provided.
        """
        nk_uuid = data.get("networkUuid", None)
        if nk_uuid is None:
            network = self.cache.get(CacheType.NETWORK, data["networkAddress"])
            if network is None:
                raise KeyError(f"{self.service_cache_type.name.lower()} service -> "
                               f"Could not find network. "
                               f"Network {data["networkAddress"]} should be created before this client is used!")

            del data["networkAddress"]
            nk_uuid = network["uuid"]

        data["networkUuid"] = nk_uuid

    def _location_info_to_uuid(self, data: dict) -> None:
        """Transforms location info inside a data item to the related location uuid.

        Replaces locationName and locationParentName keys
        with the associated locationUuid key if locationUuid is not provided.
        """
        loc_uuid = data.get("locationUuid", None)
        if loc_uuid is None and "locationName" in data and "locationParentName" in data:
            location_key = (data["locationName"], data["locationParentName"])
            location = self.cache.get(CacheType.LOCATION, location_key)
            if location is None:
                logger.error("%s service -> Could not find location in cache "
                              "when trying to transform location information to location uuid "
                              "with the name: %s and with the parent: %s",
                              self.service_cache_type.name.lower(),
                              data["locationName"],
                              data["locationParentName"])
                raise KeyError

            del data["locationName"]
            del data["locationParentName"]
            loc_uuid = location["uuid"]

        if loc_uuid:
            data["locationUuid"] = loc_uuid

    def _prepare_data(self, **kwargs) -> List[dict]:
        """Prepares and returns data contained in the transformer attribute.

        Note: It must be implemented by children classes that have parent dependencies.
        """
        # return data from transformer attribute
        return self.transformer.get_transformed_data()

    def _add_cache_keys_to_db_data(self, db_data: dict) -> bool:
        """Adds cache keys fields to a data item taken from database.

        Basically, keys that are not present in self.get_db_key_names, but are
        in self.get_cache_key_names to identify their parent must be initialized.
        Return True if the resulting data can be added to the cache, else False.

        Note: It must be implemented by children classes that have specific needs.
        """
        return True

    def _get_dependency_levels_from_data(self, data: List[dict], validation_key: list = None,
                                         only_service_data: bool = False) -> List[List[dict]]:
        """Returns the data tree dependencies level by level.

        e.g. The first element in data is the list containing all the data
        without dependencies/parent. The second list will contain the data
        that are dependant of the data contained in the first one and so on...

        Note: It requires _get_parent_key_data method to be implemented.
        """
        if validation_key is None:
            validation_key = self.get_cache_key_names()

        validated_data_keys = []  # list of data keys which have already been added.
        all_data = data + list(self.cache.get(self.service_cache_type).values()) \
            if self.cache.get(self.service_cache_type) else data

        # Add data from cache to complete the tree
        next_level = [item for item in all_data if self._get_parent_key_data(item, only_service_data) is None]
        levels = [[item for item in next_level if item in data]]
        while True:
            validated_data_keys += [self._keys_values_of_data(completed, validation_key) for completed in next_level]
            next_level = [item for item in all_data if
                          self._keys_values_of_data(item, validation_key) not in validated_data_keys and
                          self._get_parent_key_data(item, only_service_data) in validated_data_keys]

            if not next_level:
                break
            # Only adds the data contained in data variable
            levels.append([added_data for added_data in next_level if added_data in data])

        return levels

    def _create_data(self, data: List[dict] = None) -> list:
        """Posts data to database by chunks and return the responses of the server."""
        logger.info("%s service -> Creation of %s data items",
                     self.service_cache_type.name.lower(), len(data))

        responses = []
        for chunk_data in self._chunk_list(data, self.max_nb_elements_requests):
            logger.debug("%s service -> Data creation request with the content: %s",
                          self.service_cache_type.name.lower(), data)
            resp = self._request_post(chunk_data)
            self.is_response_valid(resp)

            logger.debug("%s service -> Data creation response: %s",
                          self.service_cache_type.name.lower(),
                          json.loads(resp.content))
            responses.append(resp)

        return responses

    def _update_data(self, data: List[dict]) -> list:
        """
        Post data to database by chunks and return the responses from the server.
        """
        logger.info("%s service -> %s data items are being updated",
                     self.service_cache_type.name.lower(), len(data))
        responses = []
        for chunk_data in self._chunk_list(data, self.max_nb_elements_requests):
            logger.debug("%s service -> Update data request with the content: %s",
                          self.service_cache_type.name.lower(), data)
            resp = self._request_patch(chunk_data)
            self.is_response_valid(resp)

            logger.debug("%s service -> Update data response with the content: %s",
                          self.service_cache_type.name.lower(),
                          json.loads(resp.content))
            responses.append(resp)

        return responses

    def _prepare_cache_data_to_be_sent(self, cache_data: dict, data_from_source: dict) -> dict:
        """Prepares cache by deleting file specifics fields before sent to through metadata apis."""
        key_to_delete = self.dependency_specific_keys()
        data_to_send = cache_data.copy()
        for key in data_from_source:
            data_to_send[key] = data_from_source[key]

        for key in key_to_delete:
            if key in data_to_send:
                del data_to_send[key]

        return data_to_send

    def _data_unknown_and_modified_in_cache(self, data_list: List[dict]) -> tuple[List, List]:
        """Returns posted and updated data.

        Note: Cache must be filled before calling this function.
        """
        assert isinstance(data_list, list)
        data_to_post = []
        data_to_update = []
        cache_keys = self.get_cache_key_names()
        for data in data_list:
            keys = self._keys_values_of_data(data, cache_keys)
            cache_data = self.cache.get(self.service_cache_type, keys)
            if cache_data is None:
                data_to_post.append(data)
            else:
                data_item_to_update = self._prepare_cache_data_to_be_sent(cache_data, data)
                for field in cache_data:
                    # delete fields that don't need to be updated
                    if field in data_item_to_update and field != "uuid" and \
                            cache_data[field] == data_item_to_update[field]:
                        del data_item_to_update[field]

                if data_item_to_update:
                    # verify that there is another field than the uuids
                    update_this_data = False
                    for key in data_item_to_update:
                        if key.lower() != "uuid":
                            update_this_data = True

                    if update_this_data:
                        data_to_update.append(data_item_to_update)

        return data_to_post, data_to_update

    def _add_json_data_to_cache(self, resp_json: List[dict]) -> None:
        """Adds a list of JSON data items to the cache."""
        keys = self.get_cache_key_names()
        if keys and resp_json:
            for element in resp_json:
                element_keys = self._keys_values_of_data(element, keys)
                self.cache.add(self.service_cache_type, element, element_keys)

    def _add_to_uuid_mapping(self, db_data: dict):
        """Adds a JSON element to the uuid_mapping attribute."""
        self.uuid_mapping[db_data["uuid"]] = db_data

    def _get_response_content(self, resp) -> List[dict]:
        """Gets the content of a server response."""
        if not self.is_response_valid(resp):
            raise ValueError

        resp_json = json.loads(resp.content)
        if 'results' in resp_json:
            resp_json = resp_json['results']

        if isinstance(resp_json, dict):
            # the response body content is a dictionary if the query is about only one object
            resp_json = [resp_json]

        return resp_json

    def _treat_response_content(self, response_content) -> None:
        """Treats the response content by deleting metadata specific keys that needs to be removed."""
        # delete items that can't be converted (data with same "keys" as another data)
        items_to_delete = []
        for index, db_data in enumerate(response_content):
            is_converted = self._add_cache_keys_to_db_data(db_data)
            if not is_converted:
                # Data which can't be converted are to be deleted
                # This object have the same "keys" as another one queried
                items_to_delete.append(index)

        items_to_delete.reverse()
        for item_to_delete in items_to_delete:
            response_content.pop(item_to_delete)

    def _add_response_to_cache(self, resp) -> None:
        """Gets content of a server response and adds it to the cache and the uuid mapping."""
        resp_json = self._get_response_content(resp)
        self._treat_response_content(resp_json)
        for db_data in resp_json:
            self._add_to_uuid_mapping(db_data)

        self._add_json_data_to_cache(self._delete_unwanted_fields_from_responses_json(resp_json))

    def _add_responses_to_cache(self, responses: list) -> None:
        """Adds content of server responses to the cache and the uuid mapping for data having dependencies."""
        resp_json = []
        for resp in responses:
            resp_json += self._get_response_content(resp)

        self._treat_response_content(resp_json)
        for db_data in resp_json:
            self._add_to_uuid_mapping(db_data)

        self._add_json_data_to_cache(self._delete_unwanted_fields_from_responses_json(resp_json))

    def _get_data_in_db_to_complete_cache(self, data: List[dict]) -> None:
        """Queries database to complete the cache with input data if they are already present in the database.

        Note: It filters the query with the data keys.
        """

        def elt_to_str(elt: str):
            """ Adds ' string around the element if it contains a space """
            if isinstance(elt, str) and " " in elt:
                return "'" + elt + "'"
            return str(elt)

        logger.info("%s service -> Get %s data items in db to complete the cache",
                     self.service_cache_type.name.lower(), len(data))
        for chunk_data in self._chunk_list(data, self.max_nb_elements_requests):
            query_list = []
            for key in self.get_db_key_names():
                # keys are sorted for the purpose of easy mocking while testing
                query_list.append(
                    f"{key}=in=(" + ",".join(sorted(set(elt_to_str(row[key]) for row in chunk_data))) + ")"
                )
            query = ";".join(query_list)
            self.get_data_and_update_cache(query=query)

    # Public methods to use
    def get_data_and_update_cache(self, **params) -> None:
        """Sends request and return response after populating the cache with it."""

        def get_data(**_params):
            _responses = []
            logger.debug("%s service -> Get data and update cache with %s parameter",
                          self.service_cache_type.name.lower(), _params)

            resp = self._request_get(**_params)
            self.is_response_valid(resp)
            _responses.append(resp)
            logger.debug("%s service -> Get data response: %s",
                          self.service_cache_type.name.lower(),
                          json.loads(resp.content))

            resp_json = json.loads(resp.content)
            if "metadata" in resp_json and "nextCursor" in resp_json["metadata"]:
                if not _params:
                    _params = {}
                _params["cursor"] = resp_json["metadata"]["nextCursor"]
                _responses += get_data(**_params)

            return _responses

        responses = get_data(**params)
        self._add_responses_to_cache(responses)

    def import_data(self, **kwargs) -> None:
        """Imports data using metadata service APIs.

        Import data that are not already present to the database and update those that are present.

        All parameters can be passed to _prepare_data interface method.
        """
        if self.transformer is None:
            logger.error(
                "A transformer must be provided to import data. "
                "The Requester needs data to be transformed, "
                "so that they can be associated to their related metadata services objects. "
                "Check Transformer class for more information.")
            exit(1)

        try:
            data = self._prepare_data(**kwargs)
            self._get_data_in_db_to_complete_cache(data)
            data_to_post, data_to_update = self._data_unknown_and_modified_in_cache(data)
            if data_to_update:
                responses = self._update_data(data_to_update)
                for response in responses:
                    self._add_response_to_cache(response)

            if not data_to_post:
                logger.warning(f"{self.service_cache_type.name.lower()} service -> "
                                f"No data were posted while trying to import.")
                return

            responses = self._create_data(data_to_post)
            for response in responses:
                self._add_response_to_cache(response)
        except Exception as e:
            logger.error("%s service -> Import failed: %s: %s",
                          self.service_cache_type.name.lower(), type(e).__name__, e, exc_info=True)
            exit(1)
