# API errors and pagination

Inspect the HTTP status and response body when a request fails. Keep the body
private if it contains account, source, or application data.

## Status codes

| Status | What to check |
| --- | --- |
| 400 | Required fields, body encoding, resource IDs, query values, and `X-Tenant-ID`. |
| 401 | Missing, expired, or incompatible token. Obtain a new diagnostic token when needed. |
| 402 | The team's subscription or resource entitlement for the operation. |
| 403 | Team membership, role, resource permission, and token/team match. |
| 404 | Resource ID, active team, and route. |
| 409 | Conflicting resource state or an operation already in progress. |
| 429 | Wait before retrying and honor `Retry-After` when present. |
| 5xx | Service availability. Retain the time, route, and sanitized response for troubleshooting. |

Successful operations return a 2xx status. Generated CRUD deletes use HTTP 200
with a message, while documented object deletes use 204. Use each endpoint's
contract instead of assuming one success status for every method.

## List pagination

Generated CRUD lists accept:

| Parameter | Default | Limit |
| --- | --- | --- |
| `page` | 1 | Use the returned pagination information to request further pages. |
| `per_page` | 20 | Maximum 100. |

They return records in `data` and metadata in `pagination`. Custom endpoints
can use different list formats or cursors; consult their parameters and
response contract. Copy IDs from returned data for later operations.

## Retries and asynchronous work

Retry reads after a transient failure with a bounded delay. Before retrying a
create, deploy, workflow trigger, upload, or other mutation, inspect the target
state to determine whether the first attempt already took effect. This public
reference does not promise a universal idempotency-key contract.

A successful build, deployment, preview, or command request may start work that
finishes later. Read its status and logs before treating the action as complete.
See [deployment verification](../deployments.md) and
[logs and metrics](../observability.md).
