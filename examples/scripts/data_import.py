"""
    Wirepas Data Import Script
    =================
    Copyright Wirepas Oy 2026 licensed under Apache 2.0

    Please see file LICENSE for full license details.

    Please see data_import.md for documentation.
"""

import os

import click

from nms_integration_tool.logger import get_logger
from nms_integration_tool.api_client import ApiClientBuilder
import nms_integration_tool.data_source as ds

from nms_integration_tool.api.gateways.wirepas_gateway_metadata_service_api_client import client as gw_client
from nms_integration_tool.api.locations.wirepas_locations_metadata_service_api_client import client as loc_client
from nms_integration_tool.api.networks.wm_network_metadata_service_api_client import client as nw_client
from nms_integration_tool.api.nodes.wm_node_metadata_service_api_client import client as node_client

from nms_integration_tool.locations.requester import LocationsRequester
from nms_integration_tool.locations.transformer import LocationsTransformer
from nms_integration_tool.networks.requester import NetworksRequester
from nms_integration_tool.networks.transformer import NetworksTransformer
from nms_integration_tool.gateways.requester import GatewaysRequester
from nms_integration_tool.gateways.transformer import GatewaysTransformer
from nms_integration_tool.nodes.requester import NodesRequester
from nms_integration_tool.nodes.transformer import NodesTransformer
from nms_integration_tool.cache import Cache, CacheType

AVAILABLE_APIS = [
    'NETWORKS', 'GATEWAYS', 'NODES', 'LOCATIONS', 'LOCATION_TYPES'
]


@click.command()
@click.option('--hostname', '-h', required=True, type=str,
              help='Name of the hostname')
@click.option('--client_id', required=False, type=str, default=None,
              help='Client id for authentication')
@click.option('--client_secret', required=False, type=str, default=None,
              help='Client secret for authentication')
@click.option('--api', required=True, type=click.Choice(AVAILABLE_APIS, case_sensitive=False), default=None,
              help='Available API names, case-insensitive')
@click.option('--data', '-d', 'input_data', required=False, type=str, default=None,
              help='Path of the data dile. Supports only CSV and XLSX files detected by their extensions')
@click.option('--dataconf', '-c', 'input_data_conf', required=False, type=str, default=None,
              help='Path of the configuration file')
@click.option('--batch_size', '-b', required=False, type=int, default=1000,
              help='Batch size per request')
@click.option('--log_level', '-l', required=False, default="info",
              type=click.Choice(["debug", "info", "warning", "error", "critical"], case_sensitive=False),
              help='Log level of the module')
@click.option('--prevent_location_queries', required=False, type=bool, default=False,
              help='Prevent gateways and nodes services from querying the location data. '
                   'It should be True if the data have no location to be linked to.')
@click.option('--insecure', '-k', is_flag=True, required=False, default=False,
              help='Insecure HTTPS connection that not requires CA certificate validation')
@click.option('--timeout', '-t', 'timeout', required=False, type=float, default=5.0,
              help='Timeout of HTTP connection')
@click.option('--ignore_sinks', is_flag=True, required=False, default=False,
              help='Exclude SINK nodes from import. Only applicable when --api NODES is used.')
def main(hostname, client_id, client_secret, api, input_data, input_data_conf, batch_size, log_level,
         prevent_location_queries, insecure, timeout, ignore_sinks):
    """
    Example script to import data into NMS system.

    Usages:
        Please see data_import.md for usage examples.
    """
    click.echo(click.style('Starting', fg='green'))
    os.environ["LOG_LEVEL"] = log_level.upper()
    logger = get_logger(__name__)
    logger.debug(
        f"""Parameters: hostname:{hostname}, api:{api}, input_data:{input_data}, input_data_conf:{input_data_conf},
        batch_size:{batch_size}, log_level:{log_level}, prevent_location_queries:{prevent_location_queries},
        insecure:{insecure}, timeout:{timeout}""")

    # If file extension is xlsx, it will be behaved as XLSX file, otherwise CSV.
    if input_data.endswith(".xlsx"):
        extracted_data = ds.XlsxDataSource(input_data).ingest(read_only=True, data_only=True)
    else:
        extracted_data = ds.CsvDataSource(input_data).ingest()
    cache = Cache()

    if api == 'LOCATIONS':
        transformer = LocationsTransformer(extracted_data, input_data_conf)
        requester = LocationsRequester(
            client=ApiClientBuilder(
                client=loc_client, hostname=hostname, cache=cache, client_id=client_id, client_secret=client_secret,
                insecure=insecure, timeout=timeout
            ).build(),
            cache=cache, transformer=transformer, max_nb_elements_requests=batch_size
        )
    elif api == 'LOCATION_TYPES':
        transformer = LocationsTransformer(None, input_data_conf)
        requester = LocationsRequester(
            client=ApiClientBuilder(
                client=loc_client, hostname=hostname, cache=cache, client_id=client_id, client_secret=client_secret,
                insecure=insecure, timeout=timeout
            ).build(),
            cache=cache, transformer=transformer, max_nb_elements_requests=batch_size
        )
    elif api == 'NETWORKS':
        transformer = NetworksTransformer(extracted_data, input_data_conf)
        requester = NetworksRequester(
            client=ApiClientBuilder(
                client=nw_client, hostname=hostname, cache=cache, client_id=client_id, client_secret=client_secret,
                insecure=insecure, timeout=timeout
            ).build(),
            cache=cache, transformer=transformer, max_nb_elements_requests=batch_size
        )
    elif api == 'GATEWAYS':
        cache = cache
        transformer = GatewaysTransformer(extracted_data, input_data_conf)
        requester = GatewaysRequester(
            client=ApiClientBuilder(
                client=gw_client, hostname=hostname, cache=cache, client_id=client_id, client_secret=client_secret,
                insecure=insecure, timeout=timeout
            ).build(),
            cache=cache, transformer=transformer, max_nb_elements_requests=batch_size
        )
    elif api == 'NODES':
        transformer = NodesTransformer(extracted_data, input_data_conf)
        node_api_client = ApiClientBuilder(
            client=node_client, hostname=hostname, cache=cache, client_id=client_id, client_secret=client_secret,
            insecure=insecure, timeout=timeout
        ).build()

        if ignore_sinks:
            # 1. Fetch networks for the addresses present in the input data
            network_addresses = transformer.get_network_addresses()
            nw_query = "address=in=(" + ",".join(str(a) for a in network_addresses) + ")"
            NetworksRequester(
                client=ApiClientBuilder(
                    client=nw_client, hostname=hostname, cache=cache, client_id=client_id,
                    client_secret=client_secret, insecure=insecure, timeout=timeout
                ).build(),
                cache=cache
            ).get_data_and_update_cache(query=nw_query)

            # 2. Build networkUuid -> networkAddress reverse map from cache
            uuid_to_network_address = {
                data["uuid"]: int(address)
                for address, data in (cache.get(CacheType.NETWORK) or {}).items()
            }

            # 3. Fetch all sink nodes for those networks, then identify sinks client-side
            sinks_query = ("sinkNodeInfo.sinkGatewayUuid==*;"
                           "networkUuid=in=(") + ",".join(uuid_to_network_address.keys()) + ")"
            sink_requester = NodesRequester(client=node_api_client, cache=Cache())
            sink_requester.get_data_and_update_cache(query=sinks_query)

            # 4. Build (node_address, network_address) key set for nodes that have sinkNodeInfo
            sink_node_keys = {
                (node["address"], uuid_to_network_address[node["networkUuid"]])
                for node in sink_requester.uuid_mapping.values()
                if node.get("networkUuid") in uuid_to_network_address and "sinkNodeInfo" in node
            }
            logger.info("Excluded Sink nodes: %s", [{"sink": s, "network": n} for s, n in sink_node_keys])
            transformer.exclude_sink_nodes(sink_node_keys)

        requester = NodesRequester(
            client=node_api_client, cache=cache, transformer=transformer, max_nb_elements_requests=batch_size
        )
    else:
        return  # not possible because of input verification

    requester.import_data(prevent_location_queries=prevent_location_queries)

    logger.info("Import of data is finished !")


if __name__ == "__main__":
    main()
