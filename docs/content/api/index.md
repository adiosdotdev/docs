# Adios API

Use the REST API to manage applications, source-backed workspaces, domains,
workflows, object storage, and related team resources. The public origin is:

```text
https://api.adios.dev
```

Paths include `/v1`; do not add it twice. MCP has a
[separate connection and authentication flow](../integrations.md).

## Start here

1. [Authenticate](authentication.md) with a supported team-bound bearer token.
2. [Make your first requests](quickstart.md) with curl or the read-only Postman collection.
3. [Use Postman](postman.md) to explore the downloadable reference.
4. Review [errors and pagination](errors.md) before integrating a client.

## Download the contract

- [Public OpenAPI document](../assets/adios-public.openapi.yaml).
- [Core Postman collection](../assets/adios-api.postman_collection.json).
- [Read-only quickstart collection](../assets/adios-quick-start.postman_collection.json).
- [Production environment with blank credentials](../assets/adios-production.postman_environment.json).

The endpoint pages and public OpenAPI download follow the reviewed Postman
catalog. They cover the core customer-facing routes, with runtime corrections
for tenant headers, custom request bodies, and response statuses. The platform's
internal generated specification contains additional routes outside this public
edition. General platform administration, service credentials, provider
callbacks, and advanced agent execution ledgers are not part of this reference.

Examples use synthetic data and editable variables. They are not authenticated
production captures. Custom endpoints without a complete response contract
describe the response status without inventing a payload.

## Endpoint groups

Browse the **API reference** navigation for each resource. Creating, updating,
deleting, inviting, building, or starting a runtime changes state. Read each
operation's target, parameters, and body before sending it.
