# Data Import Script

A Python script for importing data into Wirepas NMS using Metadata APIs.

The script requires two inputs:

- **Data source**: CSV or XLSX file containing the data to import
- **Configuration file**: JSON file that maps data source columns to NMS API fields

## Authentication

For secure NMS installations, provide OAuth2 client credentials:

```
--client_id <id>         Client ID for authentication
--client_secret <secret> Client secret for authentication
```

The script automatically handles token generation and authentication.

## Data Source

### Supported Formats

The script supports the following data source formats:

- **CSV**: Comma-separated values files (default)
- **XLSX**: Excel spreadsheet files

File format is automatically detected by extension.

### Custom Data Sources

To support additional formats, implement a custom data source class:

1. Inherit from `DataSource` class in [data_source.py](../../src/nms_integration_tool/data_source.py)
2. Implement the required methods defined in the base class

## Configuration File

The configuration JSON file maps data source columns to NMS Metadata API fields.

**Structure**: JSON object where:

- **Keys**: NMS API field names
- **Values**: Corresponding column names in your data source

All fields to be imported must be included in the configuration.

Example configuration files: [examples/configs](../configs/README.md)

### Automatic UUID Resolution

For **Gateways** and **Nodes** APIs, the script automatically resolves references:

| Configuration Key                      | Resolves To    | Description                                  |
|----------------------------------------|----------------|----------------------------------------------|
| `networkAddress`                       | `networkUuid`  | Queries networks API to find UUID by address |
| `locationName` or `locationParentName` | `locationUuid` | Queries locations API to find UUID by name   |

This eliminates the need to manually query and map UUIDs before import.

## Usage

View all available options:

```bash
python data_import.py --help
```

### Supported APIs

The script supports importing data to the following NMS services:

- `NETWORKS` - Network metadata
- `GATEWAYS` - Gateway devices
- `NODES` - Node devices
- `LOCATIONS` - Physical locations
- `LOCATION_TYPES` - Location type definitions

## Prerequisites

### Install the Package

Install the package with the `examples` extra from the repository root (includes `click` required by this script):

**Using pip:**

```bash
pip install -e ".[examples]"
```

**Using uv (recommended):**

```bash
uv pip install -e ".[examples]"
```

**NOTE:** you can use all python commands as `uv run data_importer.py ... ` without using any pip install.

## Example: Import Node Location Data

Navigate to the examples directory:

```bash
cd examples/scripts
```

### 1. Prepare Data Source

Create a CSV file with node location data (e.g., `location_node_data.csv`):

```csv
Meter No.,Node ID,latitude,longitude,Network
MTRR0000001,100001,45.5012345,6.012345,123456
MTRR0000002,100002,45.5023456,6.023456,123456
MTRR0000003,100003,45.5034567,6.034567,123456
```

### 2. Create Configuration File

Create a JSON configuration file (e.g., `node_config.json`) that maps CSV columns to NMS API fields:

```json
{
  "name": "Meter No.",
  "address": "Node ID",
  "networkAddress": "Network",
  "coordinates": {
    "latitude": "latitude",
    "longitude": "longitude",
    "altitude": "longitude"
  }
}
```

**Note**: Adjust the configuration values to match your actual CSV column names.

### 3. Run the Import

Set environment variables for your NMS instance:

```bash
export CLIENT_ID=wnms-data-import
export CLIENT_SECRET=<your-secret>
export NMS_INTEGRATION_HOST=https://[wnms]-integration.example.com
```

**Example with long-form arguments:**

```bash
python data_import.py \
    --hostname "$NMS_INTEGRATION_HOST" \
    --client_id "$CLIENT_ID" \
    --client_secret "$CLIENT_SECRET" \
    --api NODES \
    --batch_size 1000 \
    --data location_node_data.csv \
    --dataconf node_config.json \
    --prevent_location_queries true \
    --log_level debug \
    --timeout 100
```

**Example with short-form arguments:**

```bash
python data_import.py \
  -h "$NMS_INTEGRATION_HOST" \
  --client_id "$CLIENT_ID" \
  --client_secret "$CLIENT_SECRET" \
  --api NODES \
  -b 1000 \
  -d location_node_data.csv \
  -c node_config.json \
  --prevent_location_queries true \
  -l debug \
  -t 100

```

#### Important Notes

**Order of Operations:**

- **Networks must be created first** before importing any other metadata (gateways, nodes, or locations).
- **Locations must exist** before assigning them to nodes or gateways. Therefore, location data must be imported before
  nodes or gateways.

**Sink Node Restrictions:**

- **Sink node locations** are managed by the gateway metadata service
- **Do not include sink nodes** in your CSV/XLSX data source, as their locations cannot be modified directly
- Use `--ignore_sinks` to automatically exclude sink nodes from the import. The script will query the nodes API for the
  networks present in the input file and remove any sink nodes before sending requests.

### Command Line Options

| Option (short) | Option (long)                | Required | Default | Description                                                                                                                                                        |
|----------------|------------------------------|----------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h`           | `--hostname`                 | Yes      | -       | NMS integration hostname                                                                                                                                           |
| -              | `--client_id`                | No*      | None    | OAuth2 client ID for authentication                                                                                                                                |
| -              | `--client_secret`            | No*      | None    | OAuth2 client secret for authentication                                                                                                                            |
| -              | `--api`                      | Yes      | -       | Target API: NETWORKS, GATEWAYS, NODES, LOCATIONS, LOCATION_TYPES                                                                                                   |
| `-d`           | `--data`                     | No**     | None    | Path to data file (CSV or XLSX)                                                                                                                                    |
| `-c`           | `--dataconf`                 | No       | None    | Path to configuration JSON file                                                                                                                                    |
| `-b`           | `--batch_size`               | No       | 1000    | Number of items per batch request                                                                                                                                  |
| `-l`           | `--log_level`                | No       | info    | Logging level: debug, info, warning, error                                                                                                                         |
| -              | `--prevent_location_queries` | No       | False   | Skip location UUID lookups (set to true if data has no location references)                                                                                        |
| `-k`           | `--insecure`                 | No       | False   | Allow insecure HTTPS without certificate validation                                                                                                                |
| `-t`           | `--timeout`                  | No       | 5.0     | HTTP request timeout in seconds                                                                                                                                    |
| -              | `--ignore_sinks`             | No       | False   | Exclude sink nodes from import. Only applicable with `--api NODES`. Queries the nodes API to find sink nodes in the input networks and removes them before import. |

**Notes:**

- *Required for secure NMS installations
- **Not required for LOCATION_TYPES API
