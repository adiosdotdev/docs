# adios.yaml Reference

`adios.yaml` describes how Adios builds, runs, connects, and publishes your
application.

## App and Runtime

```yaml
name: api
region: de
replicas: 2

build_cmd: go build -o /app/api .
start_cmd: /app/api

runtime:
  name: go@1.25
  port: 8080
  cpu: "0.5"
  memory_mb: 512
  disk_mb: 2048
  health_path: /healthz
```

Command fields are scalar shell commands:

```yaml
build_cmd: pnpm install && pnpm build
```

## Managed Resources

```yaml
resources:
  - name: db
    template: postgres:16
    database: aor
    username: aor_api
    password: secret://POSTGRES_PASSWORD
  - name: redis
    template: redis:7
    database: "0"
    password: secret://REDIS_PASSWORD
  - name: rabbitmq
    template: rabbitmq:3
    database: aor
    username: aor_api
    password: secret://RABBITMQ_PASSWORD
```

The `resources` field provisions and binds managed databases, caches, and
queues with the application. Supported resource families include Postgres,
pgvector, Redis, RabbitMQ, MongoDB, and MySQL. Use `ref` when the application
should bind to an existing resource instead of owning a new one.

Connection settings are injected into the application with a stable private
hostname. The unversioned hostname follows the promoted current resource; an
explicit version hostname can select a healthy `v1`, `v2`, or generated deploy
version. See [Managed Resources and Versioned Internal DNS](managed-resources.md)
for the complete naming, version pinning, security, and troubleshooting
contract.

## Secrets and Config

```yaml
env:
  PUBLIC_APP_URL: https://dashboard.example.com
  DATABASE_URL: secret://DATABASE_URL
  STRIPE_SECRET_KEY: secret://STRIPE_SECRET_KEY
```

Put both regular environment variables and `secret://NAME` references in `env`.
Create the referenced secret values with the CLI or Web IDE before deployment.
Use the top-level `secrets` block only to generate new values:

```yaml
env:
  PUBLIC_APP_URL: https://dashboard.example.com
  API_SIGNING_KEY: secret://API_SIGNING_KEY
  DJANGO_SECRET_KEY: secret://DJANGO_SECRET_KEY
secrets:
  API_SIGNING_KEY: secret://generate:64
  DJANGO_SECRET_KEY: secret://generate:32
```

The `secrets` block declares generation; `env` references the values the
application needs. Keep credential values out of Git. Runtime config can also
include feature flags, volumes, and deployment settings managed from the
workspace.

## Private Git Dependencies

Builds that fetch private Git repositories should use a build-only deploy key:

```yaml
build:
  ssh:
    - default=secret://BITBUCKET_DEPLOY_KEY
  env:
    GOPRIVATE: "bitbucket.org/your-workspace/*"
```

Register the public key with the Git provider, then store the private key in
the application's Adios team:

```bash
adios secrets set BITBUCKET_DEPLOY_KEY \
  --from-file ~/.ssh/adios-build
```

The worker resolves the key only for the build and removes its temporary copy
afterward. Do not commit a private key or put it in a repository URL. Follow
[Private Git Dependencies](private-git-dependencies.md) for key generation,
Bitbucket, GitHub, GitLab, Docker, and troubleshooting steps.

## Versions, Replicas, and Routing

```yaml
name: web
region: de
replicas: 2
routable: true

custom_hosts:
  - app.example.com
  - www.example.com

redirects:
  - from: example.com
    to: www.example.com
```

Each deployment creates a runtime version. Adios can keep older versions
inspectable and wakeable while routing traffic to the promoted current release.
Replicas can run regionally, and public traffic can be served through generated
routes, custom domains, CDN, and anycast-backed entry points.

`custom_hosts` attaches exact public hostnames to the promoted current release.
`redirects` creates exact-host redirect routes. A redirect destination without a
scheme defaults to HTTPS, and the gateway preserves the request path and query
string.

See [Domains and Redirects](routing.md) for the full routing flow.

## Workflow Manifests

Application runtimes use `build_cmd`, `start_cmd`, and `runtime`. Workflow
automation uses a workflow manifest with `workflow_id`, `triggers`, and `steps`.
See [Workflows](workflows.md) for a complete workflow `adios.yaml` example.

## Source and Workspaces

```yaml
build:
  excludes:
    - node_modules
    - .next
```

Source artifacts let the Web IDE open the code that produced a deployed app.
From a workspace you can edit files, use Git, run previews, inspect logs, and
deploy the current version.
