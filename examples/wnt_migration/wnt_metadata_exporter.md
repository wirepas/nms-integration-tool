# WNT Metadata Migration Helper

This guide describes exemplary how to migrate node metadata from Wirepas Network Tool (WNT) to Wirepas Network
Management System (NMS) using the NMS Metadata APIs.

## Overview

The migration process consists of two main steps:

1. **Export**: Extract node metadata from WNT's PostgreSQL database and export it to CSV format
2. **Import**: Upload the CSV data to NMS using the data import script

## Prerequisites

Before starting the migration, ensure you have the following:

### 1. WNT Backend Access

- Access to the WNT backend instance
- PostgreSQL user credentials (found in the `wnt.env` file)

### 2. NMS Instance

- NMS integration API hostname
- OAuth2 client credentials (`CLIENT_ID` and `CLIENT_SECRET`)
- Necessary client permissions to access the Nodes Metadata API, aka. `Service Account Roles` in Keycloak.

> Please refer
> to
> [Wirepas NMS System Administration And Maintenance User Guide](https://developer.wirepas.com/support/solutions/articles/77000556653#Clients)
> for NMS API client usage and permissions.

### 3. Existing Wirepas Mesh networks in NMS

- Before data migration is started, ensure that the Wirepas Mesh network is already created in NMS by connecting
  gateways into NMS.
- Or, create networks from NMS UI or using NMS Networks API.

### 4. Python Environment

Prepare your Python environemnt with `uv`:

1. Install [uv](https://docs.astral.sh/uv/) for WNT Ubuntu machine.
2. `cd ~/wnt` or main wnt directory.
3. `uv python install 3.13`
4. `uv venv`
5. `uv pip install nms-integration-tool~=1.3.0`
6. Copy the `data_import.py` script to WNT instance. You can clone the repo like below or copy the scripts from host
   machine:

```
# in ~/wnt directory
git clone https://github.com/wirepas/nms-integration-tool.git
cp nms-integration-tool/examples/scripts/{data_import.py,wnt_metadata_exporter.sh} .
# now their paths are 
- ~/wnt/data_import.py
- ~/wnt/wnt_metadata_exporter.sh
```

## Field Mapping

The NMS Nodes Metadata API supports a subset of WNT fields. Standard fields such as `address` and `networkAddress` are
mapped directly to their NMS equivalents, while WNT-specific fields are stored in the `custom` object with a `legacy_`
prefix to mark their origin.

The field mapping configuration is defined in [joined_meta_node_config.json](joined_meta_node_config.json) and can be
customized to meet your specific requirements.

### Default Field Mapping

| NMS Field                        | WNT Field                   | Description              |
|----------------------------------|-----------------------------|--------------------------|
| `networkAddress`                 | `nodemeta.networkid`        | Network identifier       |
| `address`                        | `nodemeta.nodeid`           | Node address             |
| `name`                           | `nodemeta.nodename`         | Node name                |
| `description`                    | `nodemeta.nodedesc`         | Node description         |
| `coordinates.latitude`           | `nodemeta.latitude`         | GPS latitude             |
| `coordinates.longitude`          | `nodemeta.longitude`        | GPS longitude            |
| `coordinates.altitude`           | `nodemeta.altitude`         | GPS altitude             |
| `custom.legacy_is_anchor`        | `nodemeta.is_anchor`        | Anchor node flag         |
| `custom.legacy_approved`         | `nodemeta.approved`         | WNT Approval status      |
| `custom.legacy_virtual`          | `nodemeta.virtual`          | Virtual node flag        |
| `custom.legacy_pixel_location_x` | `nodemeta.pixel_location_x` | Map X coordinate         |
| `custom.legacy_pixel_location_y` | `nodemeta.pixel_location_y` | Map Y coordinate         |
| `custom.legacy_rssi_offset`      | `nodemeta.rssi_offset`      | RSSI calibration offset  |
| `custom.legacy_update_time`      | `nodemeta.update_time`      | Last update timestamp    |
| `custom.legacy_mapgroupid`       | `mapgroups.mapgroupid`      | Building/area identifier |
| `custom.legacy_mapgroupname`     | `mapgroups.mapgroupname`    | Building/area name       |
| `custom.legacy_mapid`            | `maps.mapid`                | Map identifier           |
| `custom.legacy_mapname`          | `maps.mapname`              | Map name                 |
| `custom.legacy_mapfloorindex`    | `maps.mapfloorindex`        | Floor level              |

## Step 1: Export WNT Metadata to CSV

The `wnt_metadata_exporter.sh` script exports node metadata from the WNT PostgreSQL database. It executes a SQL JOIN
query to combine node metadata with location information (buildings, maps, and floors) from multiple WNT tables.

Run the script with WNT Postgres instance credentials:

```bash
cd ~/wnt

# Find POSTGRES_USER value in wnt.env file, password is not required in most of the cases
./wnt_metadata_exporter.sh -u $POSTGRES_USER
```

### Script Options

| Option | Description                                                                   |
|--------|-------------------------------------------------------------------------------|
| `-h`   | Display help message                                                          |
| `-u`   | PostgreSQL database user (from `POSTGRES_USER` in `wnt.env`)                  |
| `-p`   | PostgreSQL password (optional, from `POSTGRES_PASSWORD` environment variable) |

### Output Files

The script creates folder `~/wnt/exported_data` with following files:

| File                | Description                              | Required for Import |
|---------------------|------------------------------------------|---------------------|
| `JOINED_META.csv`   | Combined node metadata and location data | **Yes**             |
| `nodemeta.csv`      | Node metadata only                       | No (reference)      |
| `maps.csv`          | Map data only                            | No (reference)      |
| `mapgroups.csv`     | Map group data only                      | No (reference)      |
| `exported_data.tar` | Compressed archive of all exports        | No (backup)         |

**Note**: Only `JOINED_META.csv` is required for NMS import. Other files are provided for reference or
alternative import methods.

## Step 2: Import Metadata to NMS

### Configure Environment Variables

Set the required environment variables for your NMS instance:

```bash
export CLIENT_ID=wnms-data-import
export CLIENT_SECRET=<your-secret>
export NMS_INTEGRATION_HOST=https://[wnms]-integration.example.com
# if there is single LoadBalancer:
#   export NMS_INTEGRATION_HOST=https://[wnms]-admin.example.com
```

### Run the Import

Execute the data import script. Please read more on how to use the data import script in
the [data_import.md](../scripts/data_import.md):

   ```bash
   uv run python data_import.py \
       --hostname "$NMS_INTEGRATION_HOST" \
       --client_id "$CLIENT_ID" \
       --client_secret "$CLIENT_SECRET" \
       --api NODES \
       --batch_size 1000 \
       --data exported_data/JOINED_META.csv \
       --dataconf joined_meta_node_config.json \
       --prevent_location_queries true \
       --log_level debug \
       --timeout 100
   ```

**Note:** If gateways are already connected and JOINED_META.csv includes sink nodes too, sink nodes metadata update can
be ignored
using `--ignore_sinks` parameter. Read more in [data_import.md](../scripts/data_import.md#important-notes).

## Customizing the Migration

### Modify Field Mapping

You can customize the field mapping by editing the `joined_meta_node_config.json` file. Possible customizations include:

- Adding or removing fields in the `custom` section
- Modifying custom NMS field names and renaming
- Adjusting coordinate field mappings

### Adjust Batch Size

Optimize the batch size based on your network conditions and dataset size:

| Scenario                               | Recommended Batch Size |
|----------------------------------------|------------------------|
| Slow network or connection issues      | 100-500                |
| Standard network and dataset           | 1000 (default)         |
| Fast network with high server capacity | 2000-5000              |

### Increase Timeout

If you experience timeout errors with large batches or slow server responses, increase the timeout value:

```bash
--timeout 300  # 5 minutes for very large datasets
```

## Troubleshooting

### Authentication Errors

**Symptoms**: HTTP 401 or 403 errors during import

**Solutions**:

- Verify that NMS URL, `CLIENT_ID` and `CLIENT_SECRET` are correct
- Confirm the OAuth2 client(i.e. wnms-data-import) has the necessary permissions to access the Nodes Metadata API.
  Please ask NMS admin and refer to its
  documentation [Wirepas NMS System Administration And Maintenance User Guide](https://developer.wirepas.com/support/solutions/articles/77000556653#Clients)
- Check that the client credentials are valid and not expired

### Import Failures

**Symptoms**: Data import stops or reports errors

**Solutions**:

- Enable debug logging with `--log_level debug` to view detailed error messages
- Ensure all network addresses referenced in the CSV already exist in NMS (import networks first if necessary)
- Preferred to connect Wirepas Mesh network to NMS first before any data import
- Check that the field mapping configuration matches the CSV column names

### Timeout Issues

**Symptoms**: HTTP timeout errors or slow import progress

**Solutions**:

- Reduce `--batch_size` to process fewer nodes per request (e.g., from 1000 to 500)
- Increase `--timeout` to allow more time for each request (e.g., `--timeout 300`)
- Verify network connectivity and bandwidth between the import client and NMS server
- Check NMS server load and performance

## Additional Resources

For more information about the data import script and its capabilities, see:

- [Data Import Documentation](../scripts/data_import.md)
- [Configuration Examples](../configs/README.md)
- [Wirepas NMS Backend API Documentation](https://developer.wirepas.com/support/solutions/articles/77000553346)
- [Wirepas NMS System Administration And Maintenance User Guide](https://developer.wirepas.com/support/solutions/articles/77000556653#Clients)
