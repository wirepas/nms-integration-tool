# PostgreSQL Import Script

A reference Python script that periodically imports data from an external PostgreSQL database into Wirepas NMS (Network
Management System).

## Overview

This script demonstrates how to:

- Connect to an external PostgreSQL database
- Execute custom SQL queries to fetch data
- Transform and map database columns to NMS API fields
- Continuously synchronize data on a scheduled interval

**Note**: This is a reference implementation requiring customization before production use.

## Configuration Requirements

The following parameters must be configured within the script:

| Parameter                        | Description                                                                                                               |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| **NMS API Credentials**          | Hostname, client ID, and client secret for authenticating with the NMS API                                                |
| **PostgreSQL Connection String** | Database URI (see [psycopg documentation](https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection)) |
| **Data Configuration File**      | JSON file path defining the mapping between database columns and NMS API fields                                           |
| **SQL Query**                    | SELECT statement to retrieve data from the external database                                                              |

## PostgreSQL Data Source

The `PostgresDataSource` class provides a simple interface for executing SQL queries against an external database and
retrieving results as Python dictionaries.

### SQL Query Design

The SQL query controls which data is extracted and how it is structured before being sent to NMS.

**Best Practices**:

- Perform column renaming, filtering, and aggregation at the SQL level
- Select only required columns to minimize data transfer
- Use appropriate WHERE clauses to filter records
- Add ORDER BY clauses for consistent processing order

### Incremental Synchronization

To avoid processing the same records multiple times, implement incremental fetching using timestamp-based filtering,
example query for an example table can be:

```sql
SELECT name,
       address,
       lat,
       lon,
       alt,
       custom_field1
FROM <EXAMPLE_DB_TABLE>
WHERE updated_at > :last_checkpoint
ORDER BY updated_at ASC;
```

**Implementation Notes**:

- The provided example script performs full data refresh on each execution
- Incremental logic requires maintaining a persistent checkpoint (e.g., last successful sync timestamp)
- Consider using a database table or file to store checkpoint state between runs

## Data Mapping Configuration

The configuration file maps SQL query result columns to NMS API field names.

**File Format**: JSON

**Structure**:

```json
{
  "nms_api_field": "database_column_name"
}
```

**Requirements**:

- All fields to be imported must be explicitly defined
- Column names must exactly match those returned by the SQL query
- Nested objects are supported for complex field mappings

**Reference**: See [examples/configs](../configs/README.md) for complete configuration examples

## Running the Script

The script executes as a continuous daemon process, synchronizing data at regular intervals.

**Default Behavior**:

- Runs indefinitely until manually stopped
- Imports data every 60 seconds
- Schedule configurable via `@repeat(every(1).minutes)` decorator

**Execution**:

```bash
python postgres_import.py
```

**Stopping**: Press `Ctrl+C` to terminate

## Setup Instructions

### Step 1: Install Dependencies

Install the package from the repository root:

**Using pip:**

```bash
pip install -e ".[examples]"
```

**Using uv (recommended):**

```bash
uv pip install -e ".[examples]"
```

## Complete Example: Node Location Import

This walkthrough demonstrates configuring the script to import node location data from PostgreSQL to NMS.

### Step 1: Configure Database Connection

Edit `postgres_import.py` and set the PostgreSQL connection parameters:

```python
# PostgreSQL connection URI
# Format: postgresql://username:password@host:port/database?options
PG_CONN_URI = "postgresql://<user>:<pass>@localhost/external-meta?connect_timeout=10"

# Example SQL query to fetch node metadata from <EXAMPLE_DB_TABLE>,
# it should be modified based on the schemas and tables
SQL_QUERY = """
    SELECT name,
           address,
           network_address,
           lat,
           lon,
           alt,
           custom_field1,
           custom_field2
    FROM <EXAMPLE_DB_TABLE>"""
```

### Step 2: Define Field Mappings

Create or edit the configuration file specified in `DATA_CONFIG_FILE` (e.g., `examples/configs/nodes/config.json`):

```json
{
  "name": "name",
  "address": "address",
  "networkAddress": "network_address",
  "coordinates": {
    "latitude": "lat",
    "longitude": "lon",
    "altitude": "alt"
  },
  "customFields": {
    "field1": "custom_field1",
    "field2": "custom_field2"
  }
}
```

**Mapping Rules**:

- Left side(keys): NMS API field names (fixed by API specification)
- Right side(values): Column names from SQL query results (must match exactly)
- Nested structures (like `coordinates`) map to complex API objects
- Custom fields allow arbitrary key-value pairs to be stored with nodes

### Step 3: Configure API Authentication

Update the `API_CONFIG` dictionary in `postgres_import.py` with your NMS instance credentials:

```python
API_CONFIG = {
    "hostname": "https://[wnms]-integration.example.com",  # Your NMS hostname
    "client_id": "wnms-data-import",  # OAuth2 client ID
    "client_secret": "<client secret>",  # OAuth2 client secret
    "insecure": False,  # Set True to disable SSL verification (not recommended)
    "timeout": 10.0,  # API request timeout in seconds
}
```

### Step 4: Execute the Script

Navigate to the examples directory and run:

```bash
cd examples/scripts
python postgres_import.py
```

The script will continue running and synchronizing data every minute until terminated with `Ctrl+C`.