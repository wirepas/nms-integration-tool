# NMS Integration Tool

[![image](https://img.shields.io/pypi/v/nms-integration-tool.svg)](https://pypi.python.org/pypi/nms-integration-tool)
[![image](https://img.shields.io/pypi/l/nms-integration-tool.svg)](https://pypi.python.org/pypi/nms-integration-tool)
[![image](https://img.shields.io/pypi/pyversions/nms-integration-tool.svg)](https://pypi.python.org/pypi/nms-integration-tool)
[![Actions status](https://github.com/wirepas/nms-integration-tool/actions/workflows/publish.yml/badge.svg)](https://github.com/wirepas/nms-integration-tool/actions)

This python package imports location, network, node, and gateway data into the associated Wirepas NMS backend metadata
services.

## Repository Organization

### Python Package

The `nms_integration_tool` package is organized as follows:

- **[src/nms_integration_tool/](src/nms_integration_tool/)**
    - **[api/](src/nms_integration_tool/api)** - OpenAPI generated NMS Metadata Service API Python libraries to connect
      to and query services.
    - **\<service name>/** - Contains requester/transformer module implementations for importing data to each service
    - **[data_source.py](src/nms_integration_tool/data_source.py)** - Provides classes to extract data from various data
      sources. These classes provide an `ingest` method that returns a list of data items. Future data sources can be
      implemented using the `DataSource` interface.
    - **[transformer.py](src/nms_integration_tool/transformer.py)** file defines a template class with methods to ingest
      data from any data source. Each child class must provide a specific implementation detailing how input data is
      transformed into a format compatible with the metadata APIs. The class provides methods that return a list of
      transformed data items. Transformed data are represented as dictionaries with keys corresponding to the fields of
      the associated metadata service objects, which can then be sent to the import module.
    - **[requester.py](src/nms_integration_tool/requester.py)** file provides an interface class to import data and
      update existing database records. Each service must implement the main function in its own child class inheriting
      from this interface. The `import_data` method imports new data and updates existing records in the database. An
      optional cache can be provided to store data from service responses.

Classes are provided for importing locations, location types, networks, nodes, and gateway metadata.

**Note:** For gateway, node, and location services, data with coordinates may be automatically updated with no actual
changes. This occurs because services return non-identical data (the EPSG field is added to coordinates, and
floating-point approximation errors can occur when comparing data source values with queried data). The import module
detects these differences and updates records without modifying any fields, which may cause a small delay in POST
queries.

### WNT Metadata Exporter

Helper script to import metadata from WNT to NMS:
**[wnt_metadata_exporter.md](examples/wnt_migration/wnt_metadata_exporter.md)**

### Example Scripts

#### [data_import.md](examples/scripts/data_import.md)

Helper script to import data from file sources to NMS with example [configs](examples/configs) to map data with NMS
schemas.

#### [postgres_import.md](examples/scripts/postgres_import.md)

Basic and exemplary data importer from Postgres database to NMS.

---

## Requirements

- [uv](https://docs.astral.sh/uv/) (recommended package manager)

## Module Configuration

Create a virtual environment and install the package using `uv`:

```shell
# Create venv and install package with all runtime dependencies
uv sync

# Install with examples dependencies (e.g. for running examples)
uv sync --extra examples

# or for all dependencies
uv sync --all-extras

# Install in editable mode for local development
uv pip install -e .
```

## Installation

### PyPI Installation

```shell
pip install nms-integration-tool==<NMS VERSION>.*

# For NMS version 1.3.0: pip install nms-integration-tool==1.3.0.*
```

### Local Installation

```shell
# Install in editable mode for local development
uv pip install -e .
```

# [LICENSE](LICENSE)

---