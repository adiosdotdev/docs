# Your first API requests

Start with read-only requests to verify connectivity, credentials, and team
context. You need the [CLI](../installation.md) and, for the documented bearer
flow, administrator access to the selected team.

## Check public health

```sh
curl --fail-with-body https://api.adios.dev/v1/health
```

This request needs no authentication. A successful health response verifies
the public API path; it does not verify your account or runtime deployment.

## Set your private credentials

Use [API authentication](authentication.md) to obtain a diagnostic token, then
enter it without placing the value in shell history. For bash:

```bash
export ADIOS_API_URL=https://api.adios.dev
export ADIOS_TEAM_ID=YOUR_TEAM_ID
read -r -s -p 'Access token: ' ADIOS_ACCESS_TOKEN
export ADIOS_ACCESS_TOKEN
```

Replace `YOUR_TEAM_ID` with the team selected in the CLI. The token must be
for that same team.

## Check your identity and resources

```sh
curl --fail-with-body "$ADIOS_API_URL/v1/auth/me" \
  -H "Authorization: Bearer $ADIOS_ACCESS_TOKEN" \
  -H "X-Tenant-ID: $ADIOS_TEAM_ID"

curl --fail-with-body "$ADIOS_API_URL/v1/workload?page=1&per_page=20" \
  -H "Authorization: Bearer $ADIOS_ACCESS_TOKEN" \
  -H "X-Tenant-ID: $ADIOS_TEAM_ID"

curl --fail-with-body "$ADIOS_API_URL/v1/team/deployment-context" \
  -H "Authorization: Bearer $ADIOS_ACCESS_TOKEN" \
  -H "X-Tenant-ID: $ADIOS_TEAM_ID"
```

Verify your identity, team resources, and the available deployment context.
Use returned resource IDs and available regions in later requests. Don't invent
an ID from the synthetic examples.

Clean up the temporary token variable after the session:

```sh
unset ADIOS_ACCESS_TOKEN
```

Prefer a client secret store for regular work. For Postman, follow the
[collection setup](postman.md). Investigate a failing status using
[errors and pagination](errors.md).
