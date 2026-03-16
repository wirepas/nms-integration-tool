## NMS Metadata API Clients

The import module requests are based on metadata services API clients.
These libraries are generated using the `openapi-python-client` Python library from OpenAPI JSON configurations.

Each generated library has its own folder at the same level as the configuration
and contains three major components:

- A **client library** for connecting to the service (can be reused for other services)
- A **models folder** containing functions to create message payloads for querying the service
- An **api folder** containing functions to send queries to the service

### Configuration Modifications

The OpenAPI JSON configurations of the metadata services have been slightly modified to ensure compatibility.

The `openapi-python-client` library does not support duplicate property definitions in the configuration.
The JSON configurations of the metadata services add a `required` field to some API query messages, which results in duplicate property references.
Since the tool validates the presence of required fields before sending messages to the API, the duplicate property references can be safely removed.

In the current version of the metadata services, the following duplicate properties exist:

#### Locations Metadata API

- **Duplicate property:** `approxCoordinates` in the POST and PUT query definitions

#### Nodes Metadata API

- **Duplicate property:** `coordinates` in the POST and PUT query definitions

#### Gateways Metadata API

- **Duplicate property:** `coordinates` in the POST and PUT query definitions

#### Networks Metadata API

- **Duplicate property:** `address` in the PATCH query definitions
