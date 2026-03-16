# Tests

## Structure

```
tests/
├── nms_integration_tool/       # Unit tests for the nms_integration_tool package
│   ├── test_api_client.py      # ApiClientBuilder — URL construction, auth, SSL, timeout
│   ├── test_cache.py           # Cache — add, get, update, key types
│   ├── test_data_source.py     # CsvDataSource, XlsxDataSource, PostgresDataSource
│   ├── test_requesters.py      # Requester logic — prepare, create, update, cache
│   └── test_transformers.py    # All transformers — field mapping, type casts, edge cases
│
└── examples/                   # Tests for the example scripts and configs
    ├── conftest.py             # sys.path setup and module-level mocks (schedule)
    ├── test_configs.py         # Config/CSV structure validation + transformer integration tests
    ├── test_data_import.py     # data_import.py CLI — routing, data source selection, flags
    ├── test_postgres_import.py # postgres_import.py — import_job(), main() scheduler
    └── test_wnt_migration.py   # WNT migration config and exporter script validation
```

## Requirements

Install the package with dev dependencies:

```shell
uv sync --extra dev
# or, to also include examples dependencies (required for tests/examples/):
uv sync --all-extras
```

> **Note:** `tests/examples/` tests import `data_import.py` and `postgres_import.py` from
> `examples/scripts/`, which depend on the `examples` extra (`click`, `schedule`, etc.).
> Install with `--all-extras` to run the full test suite.

## Running Tests

### Run all tests

```shell
uv run pytest
```

### Run a specific test directory

```shell
uv run pytest tests/nms_integration_tool/
uv run pytest tests/examples/
```

### Run a specific file or test

```shell
uv run pytest tests/nms_integration_tool/test_transformers.py
uv run pytest tests/examples/test_configs.py::NetworksTransformerIntegrationTest
uv run pytest tests/nms_integration_tool/test_cache.py::CacheTesting::test_add_one_data_item
```

### Run with verbose output

```shell
uv run pytest -v
```

## Coverage

Install `pytest-cov` (included in the `dev` extra) and run:

```shell
uv run pytest --cov
```

This uses the `[tool.coverage.run]` config in `pyproject.toml`, which measures coverage
for the `nms_integration_tool` source package (excluding generated API clients under `api/`).

For a full HTML report:

```shell
uv run pytest --cov --cov-report=html
# open htmlcov/index.html
```

## Test Categories

### Unit tests (`tests/nms_integration_tool/`)

Pure unit tests for the library. External I/O (files, network, database) is mocked.
Transformer tests use [mockito](https://github.com/kaste/mockito-python) to stub
`_get_configuration()` so no config file is needed on disk.

### Integration tests (`tests/examples/test_configs.py`)

Load real config files and CSV data from `examples/configs/` and run them through
the actual transformers without any mocking. These verify end-to-end field mapping,
type casting, and hierarchy construction against the shipped example data.

### Script tests (`tests/examples/test_data_import.py`, `test_postgres_import.py`)

Test the example scripts via `click.testing.CliRunner` and `unittest.mock`.
`conftest.py` adds `examples/scripts/` to `sys.path` and mocks the `schedule`
module so `postgres_import.py` can be imported without the package installed.

### Migration tests (`tests/examples/test_wnt_migration.py`)

Validate the WNT → NMS migration config (`examples/wnt_migration/joined_meta_node_config.json`)
and the exporter shell script (`examples/wnt_migration/wnt_metadata_exporter.sh`).
