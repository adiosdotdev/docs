# API authentication

Protected REST requests need a compatible bearer token and the active team ID:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
X-Tenant-ID: YOUR_TEAM_ID
```

The wire header is `X-Tenant-ID`. Do not substitute the `team_id` parameter
name used by parts of the internal generated specification.

## Obtain a diagnostic token

A team administrator can use the CLI's supported diagnostic-token flow:

```sh
adios login
adios teams
adios teams switch YOUR_TEAM_ID
adios auth print-token --ttl 15m
```

Install the CLI using the [installation guide](../installation.md). Copy the
printed token into a private client environment. These tokens expire after
1–15 minutes, cannot be refreshed, and remain bound to the selected team.
Mint a replacement after expiration.

Send `X-Tenant-ID` on every protected example, including current-user and
team-list requests. Its value must match the token's team. Membership and
resource permissions still apply.

## Credential types

Raw CLI credentials are DPoP-bound and cannot simply be copied into Bearer
authentication. Use `adios auth print-token` for manual REST access. MCP OAuth
credentials carry an MCP audience and cannot call general REST routes.

The password grant is disabled. This documentation does not provide a
password-based or one-click REST OAuth login in Postman. Non-admin users need
an authorized bearer credential compatible with their deployment; the public
collection does not provision one. Contact a team administrator if you do not
have access to the supported flow.

## Keep credentials private

Use your client's private environment or secret storage. Leave shared Postman
values empty. Avoid putting tokens in URLs, repository files, public screenshots,
shell history, or response captures. Public health and plan-catalog requests do
not require a bearer token.

See [API quickstart](quickstart.md) for a first request and
[errors](errors.md) for `401` and `403` troubleshooting.
