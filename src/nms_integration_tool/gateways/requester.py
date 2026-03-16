# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from typing import List

import nms_integration_tool.api.gateways.wirepas_gateway_metadata_service_api_client.api.gateway_metadata as \
    gateway_metadata
import nms_integration_tool.api.gateways.wirepas_gateway_metadata_service_api_client.models as gateway_models
from nms_integration_tool.api.gateways.wirepas_gateway_metadata_service_api_client.types import UNSET
from nms_integration_tool.cache import Cache, CacheType
from nms_integration_tool.gateways.transformer import GatewaysTransformer
from nms_integration_tool.locations.requester import LocationsRequester
from nms_integration_tool.networks.requester import NetworksRequester
from nms_integration_tool.requester import Requester


class GatewaysRequester(Requester):
    """Requester for gateways metadata api."""

    def __init__(self, client, cache: Cache = None, transformer: GatewaysTransformer = None, **kwargs) -> None:
        super().__init__(client, CacheType.GATEWAY, cache, transformer, **kwargs)

    def get_db_key_names(self) -> list:
        return ["gatewayId", "networkUuid"]

    def get_cache_key_names(self) -> list:
        return ["gatewayId"]

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
        for gateway_data in data:
            # Transform network infos as, it should be possible to find the network uuids at this point
            self._network_info_to_uuid(gateway_data)
            # Transform location infos as, it should be possible to find the location uuids at this point
            self._location_info_to_uuid(gateway_data)

        return data

    def _request_post(self, data: List[dict]):
        data_to_send = []
        for gateway_dict in data:
            data_to_send.append(gateway_models.CreateGatewaysBodyItem.from_dict(gateway_dict))

        return gateway_metadata.create_gateways.sync_detailed(client=self.client, body=data_to_send)

    def _request_get(self, query="", **kwargs):
        search_gateways = gateway_models.SearchGatewaysBody.from_dict({"query": query, **kwargs})

        return gateway_metadata.search_gateways.sync_detailed(client=self.client, body=search_gateways, **kwargs)

    def _request_patch(self, data: List[dict]):
        data_to_send = []
        for gateway_dict in data:
            # Latest API client sets read only field sink_nodes always to empty array []
            # instead of "unset". Explicitly set to "unset" here to make sure that PATCH update succeeds 
            gateway_item = gateway_models.Gateway.from_dict(gateway_dict)
            gateway_item.sink_nodes = UNSET
            data_to_send.append(gateway_item)

        return gateway_metadata.patch_gateways.sync_detailed(client=self.client, body=data_to_send)
