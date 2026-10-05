# Deployments and releases

A deployment builds source into an artifact and starts a workload version.
The promoted current release is the version used by the application's current
routes. A workspace preview is a separate development runtime.

## Deploy from local source

Install and authenticate the [CLI](installation.md), choose your team, and run
these commands in the directory containing `adios.yaml`:

```sh
adios up
adios apps list
adios logs --build
adios logs --runtime
```

The manifest specifies the runtime, build and start commands, port, health
path, region, replicas, environment, and managed resources. Follow the
[quickstart](quickstart.md) for an application example.

`adios up` waits for the requested deployment's runtime state and route health.
A working older release does not prove that the new deployment succeeded.
Use `adios up --debug` when you need live build output and internal identifiers.
On failure, review the build output and the reported deployment state.

## Deploy from a workspace or template

For a workspace, review the source diff, manifest, build, and preview before
using its deployment controls. For a template, inspect the chosen runtime and
resource configuration before launch. See [templates](templates.md).

Managed database, cache, and queue templates create service runtimes. They do
not open code workspaces. Follow the service-specific guides to configure
credentials, persistence, and connections.

## Health, regions, and replicas

Make the application listen on the configured port and a network-accessible
interface. The `health_path` must respond as expected without an interactive
login. Select a region available to your team; don't assume every runtime or
resource is available in every region.

Increasing `replicas` creates more runtime instances. Persistent local state
and connection limits need explicit planning before an app runs in several
instances. Consult [managed resources](managed-resources.md) and
[storage](storage.md) for data placement and persistence.

## Deploy a project with several manifests

The CLI discovers independently deployable manifests at the root and in child
directories. A root manifest can define stable aliases and deployment order:

```yaml
name: product
projects:
  api:
    path: api
    deploy: auto
  web:
    path: web
    deploy: auto
    depends_on: [api]
```

Run `adios up` for the automatic projects, or `adios up api` for a selected
project and its dependencies. `deploy` accepts `auto`, `manual`, or `disabled`.
The CLI deploys independent projects concurrently; use `--parallel` to adjust
the concurrency limit.

## Verify a release

Check the requested version and replica status, open the returned URL, exercise
the main application flow, and inspect runtime logs. For a custom domain, also
verify DNS and TLS as described in [routing](routing.md).

Older version state and retained artifacts depend on your application's
configuration. Inspect the available versions before attempting recovery;
redeploy a known-good source revision when you need a reproducible replacement.
