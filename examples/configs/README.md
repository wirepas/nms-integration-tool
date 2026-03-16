# Example Import Configurations for Datasources

When importing data from data sources (i.e., CSV, XLSX), configuration files map source fields to NMS fields. Since column
names in source files may differ from those used by NMS APIs, these mappings ensure proper data translation.

The examples in this directory demonstrate how to configure field mappings between source data and NMS.

For instance, a network address field named `nw_address` in the source file corresponds to `networkAddress` in NMS.
Configuration files define these equivalencies to enable correct data imports.