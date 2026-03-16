# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from typing import List

import nms_integration_tool.api.nodes.wm_node_metadata_service_api_client.api.node_metadata as node_metadata
import nms_integration_tool.api.nodes.wm_node_metadata_service_api_client.models as node_models
from nms_integration_tool.cache import Cache, CacheType
from nms_integration_tool.locations.requester import LocationsRequester
from nms_integration_tool.networks.requester import NetworksRequester
from nms_integration_tool.nodes.transformer import NodesTransformer
from nms_integration_tool.requester import Requester


class NodesRequester(Requester):
    """Requester for nodes metadata api service."""

    def __init__(self, client, cache: Cache = None, transformer: NodesTransformer = None, **kargs) -> None:
        super().__init__(client, CacheType.NODE, cache, transformer, **kargs)

    def get_db_key_names(self) -> list:
        return ["address", "networkUuid"]

    def get_cache_key_names(self) -> list:
        return ["address"]

    def _prepare_data(self, prevent_location_queries=False, **kwargs) -> List[dict]:
        cache_content = self.cache.get_cache()
        if CacheType.NETWORK not in cache_content:
            # retrieve all networks data from metadata api client and
            # add these to the cache if the cache does not contain any network.
            NetworksRequester(client=self.client, cache=self.cache).get_data_and_update_cache()

        if not prevent_location_queries and CacheType.LOCATION not in cache_content:
            # retrieve all locations and location types data
            # from metadata api client and add these to the cache
            # if the cache does not contain any location.
            location_req = LocationsRequester(client=self.client, cache=self.cache)
            location_req.location_types_requester.get_data_and_update_cache()
            location_req.get_data_and_update_cache()

        data = super()._prepare_data(**kwargs)
        for node_data in data:
            # Transform network infos as, it should be possible to find the network uuids at this point
            self._network_info_to_uuid(node_data)
            # Transform location infos as, it should be possible to find the location uuids at this point
            self._location_info_to_uuid(node_data)

        return data

    def _request_post(self, data: List[dict]):
        data_to_send = []
        for node_dict in data:
            data_to_send.append(node_models.CreateNodesBodyItem.from_dict(node_dict))

        return node_metadata.create_nodes.sync_detailed(client=self.client, body=data_to_send)

    def _request_get(self, query="", **kwargs):
        search_nodes = node_models.SearchNodesBody.from_dict({"query": query, **kwargs})

        return node_metadata.search_nodes.sync_detailed(client=self.client, body=search_nodes, **kwargs)

    def _request_patch(self, data: List[dict]):
        data_to_send = []
        for node_dict in data:
            data_to_send.append(node_models.Node.from_dict(node_dict))

        return node_metadata.patch_nodes.sync_detailed(client=self.client, body=data_to_send)
