"""
    Wirepas Postgres Data Source Example Script
    =================
    Copyright Wirepas Oy 2026 licensed under Apache 2.0

    Please see file LICENSE for full license details.

    Please see postgres_import.md for documentation.
"""

import time

from schedule import every, repeat, run_pending

from nms_integration_tool.api.nodes.wm_node_metadata_service_api_client import client as node_client
from nms_integration_tool.api_client import ApiClientBuilder
from nms_integration_tool.cache import Cache
from nms_integration_tool.data_source import PostgresDataSource
from nms_integration_tool.logger import get_logger
from nms_integration_tool.nodes.requester import NodesRequester
from nms_integration_tool.nodes.transformer import NodesTransformer

logger = get_logger(__name__)

API_CONFIG = {
    "hostname": "https://[wnms]-integration.example.com",
    "client_id": "wnms-data-import",
    "client_secret": "<client secret>",
    "insecure": False,
    "timeout": 10.0,
}

# Config file should map the SQL query results columns with NMS
# below SQL query is based on the example node config file
DATA_CONFIG_FILE = "examples/configs/nodes/config.json"

# Example db connection uri
PG_CONN_URI = "postgresql://<user>:<pass>@localhost/external-meta?connect_timeout=10"

# Example SQL query to run against external DB
# having similar fields with examples/configs/nodes/config.json
SQL_QUERY = """
            SELECT name,
                   address,
                   network_address,
                   lat,
                   lon,
                   alt,
                   custom_field1,
                   custom_field2
            FROM SOME_DB_TABLE"""

# Global cache instance
cache = Cache()


@repeat(every(1).minutes)
def import_job():
    """
    Scheduled job to import data from PostgreSQL to NMS.
    Runs every minute.
    """
    logger.info("Starting scheduled import job")

    try:
        # Create PostgreSQL data source
        postgres_source = PostgresDataSource(conn_str=PG_CONN_URI)

        # Test connection
        if not postgres_source.test_connection():
            logger.error("Failed to connect to PostgreSQL database")
            return

        logger.info("Successfully connected to PostgreSQL database")

        # Fetch data from database
        db_data = postgres_source.ingest(query=SQL_QUERY)

        if not db_data:
            logger.warning("No data retrieved from database query")
            return

        logger.info("Retrieved %d records from database", len(db_data))

        # Transform data using configuration
        transformer = NodesTransformer(data=db_data, config_file=DATA_CONFIG_FILE)

        # Build API client
        api_client = ApiClientBuilder(
            client=node_client,
            cache=cache,
            **API_CONFIG
        ).build()

        # Create requester and import data
        requester = NodesRequester(
            client=api_client,
            cache=cache,
            transformer=transformer,
            max_nb_elements_requests=1000
        )

        logger.info("Starting data import to NMS")
        requester.import_data(prevent_location_queries=True)
        logger.info("Data import completed successfully")

    except FileNotFoundError as e:
        logger.error("Configuration file not found: %s", e)
    except Exception as e:
        logger.exception("Unexpected error during import job: %s", e)


def main():
    """
    Main entry point. Runs the scheduler loop indefinitely.
    """
    logger.info("Starting PostgreSQL import scheduler")
    logger.info("Import job will run every 1 minute")

    try:
        while True:
            run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.exception("Fatal error in scheduler: %s", e)
        raise


if __name__ == "__main__":
    main()
