# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
from typing import List

import nms_integration_tool.api.networks.wm_network_metadata_service_api_client.api.network_metadata as network_metadata
import nms_integration_tool.api.networks.wm_network_metadata_service_api_client.models as network_models
from nms_integration_tool.api.networks.wm_network_metadata_service_api_client.types import UNSET
from nms_integration_tool.cache import Cache, CacheType
from nms_integration_tool.networks.transformer import NetworksTransformer
from nms_integration_tool.requester import Requester


class NetworksRequester(Requester):
    """Requester for networks metadata api service."""

    def __init__(self, client, cache: Cache = None, transformer: NetworksTransformer = None, **kwargs) -> None:
        super().__init__(client, CacheType.NETWORK, cache, transformer, **kwargs)

    def get_db_key_names(self) -> list:
        return ["address"]

    def _request_post(self, data: List[dict]):
        data_to_send = []
        for network_dict in data:
            data_to_send.append(network_models.CreateNetworksBodyItem.from_dict(network_dict))

        return network_metadata.create_networks.sync_detailed(client=self.client, body=data_to_send)

    def _request_get(self, query="", **kwargs):
        search_networks = network_models.SearchNetworksBody.from_dict({"query": query, **kwargs})

        return network_metadata.search_networks.sync_detailed(client=self.client, body=search_networks, **kwargs)

    def _request_patch(self, data: List[dict]):
        data_to_send = []
        for network_dict in data:
            # Latest API client sets "nested" read only field linked_locations always to empty array []
            # instead of "unset". Explicitly set to "unset" here to make sure that PATCH update succeeds 
            network_item = network_models.PatchNetworksBodyItem.from_dict(network_dict)
            network_item.linked_locations = UNSET
            data_to_send.append(network_item)

        return network_metadata.patch_networks.sync_detailed(client=self.client, body=data_to_send)
