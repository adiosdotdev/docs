# Use the Postman collections

The public package contains a core REST reference, a read-only quickstart,
an environment with blank credentials, and MCP discovery and connection files.

## Import

1. Download the [core collection](../assets/adios-api.postman_collection.json),
   [quickstart collection](../assets/adios-quick-start.postman_collection.json),
   and [Production environment](../assets/adios-production.postman_environment.json).
2. Import them into your own private Postman workspace.
3. Select the environment. Keep `base_url` as `https://api.adios.dev`.
4. Follow [authentication](authentication.md) and set private `access_token`
   and `team_id` values. Leave shared values blank.
5. Run the quickstart collection in order and check that the returned identity
   and resources belong to your team.

The quickstart sends five read-only requests: API health, current user, teams,
deployment context, and workloads. The current-user request saves `user_id`
in the selected environment when the response contains one.

## Explore the reference

Set resource variables such as `workload_id`, `workspace_id`, and
`object_bucket_id` from your own API results. Set `region` from deployment
context, `hostname` to a domain you own, and `bucket_name` to your intended
globally unique bucket name. Enable optional query parameters only when needed.

Send core-reference requests individually. The collection includes mutations,
invitations, file changes, and runtime actions. Review the body and target before
sending. For object uploads, choose **Body → binary** and select a file.

The saved success responses are illustrative. A 2xx test checks response status;
it does not prove that an asynchronous build or deployment became healthy.
Inspect the corresponding build or runtime state afterward.

## MCP and local development

Use Postman's native MCP request for [MCP connections](../integrations.md).
Its connection JSON files are distinct from REST collection exports and use
a separate OAuth flow.

For local platform development, use the
[Local environment](../assets/adios-local.postman_environment.json) with the
local stack, trusted mkcert TLS, and the desktop app or Desktop Agent. Keep TLS
verification enabled. The public hosted API is the normal choice for platform users.
