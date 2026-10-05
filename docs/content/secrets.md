# Secrets and configuration

Use team secrets for passwords, signing keys, provider credentials, and other
private values. Your manifest stores references; the secret value stays in the
platform's secret storage.

## Create a secret

Select your team, then use **Secrets** in the dashboard or the CLI:

```sh
adios teams switch YOUR_TEAM_ID
adios secrets set DATABASE_URL --stdin
adios secrets list
```

Provide the value through standard input. For a multiline value, use a file:

```sh
adios secrets set BUILD_DEPLOY_KEY --from-file ~/.ssh/adios-build
```

Add `--team YOUR_TEAM_ID` when you need an explicit target. Before deleting or
replacing a secret, check which applications and workflows use it.

## Reference values in adios.yaml

```yaml
env:
  PUBLIC_APP_URL: https://app.example.com
  DATABASE_URL: secret://DATABASE_URL
  API_SIGNING_KEY: secret://API_SIGNING_KEY
```

Regular configuration and secret references both belong in `env`. Use the
top-level `secrets` block when the manifest should generate a value:

```yaml
env:
  API_SIGNING_KEY: secret://API_SIGNING_KEY
secrets:
  API_SIGNING_KEY: secret://generate:64
```

See the [manifest reference](manifest.md) for build environment settings and
[private Git dependencies](private-git-dependencies.md) for build-only SSH keys.

## Rotate and verify

Update the stored value, then deploy or restart the affected application as
needed to pick up the new configuration. Test the connection and inspect logs
without printing credentials. Revoke the previous credential at its provider
after the replacement is working.

Application environment variables are not automatically safe for frontend
code. Frameworks can bake public-prefixed variables into browser bundles.
Keep private credentials on the server, and avoid logging full connection URLs.
