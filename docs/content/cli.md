# CLI Reference

The Adios CLI (`adios`) is the user-facing tool for login, deploys, logs,
workspaces, databases, secrets, and local source sync.

## Global Flags

- `--config string`: Path to the config file
- `--context string`: Context to use
- `--api-url string`: API base URL
- `--debug`: Stream build logs and include internal identifiers

---

## Core Commands

### `adios up [app-name]`

Uploads the current source, reads `adios.yaml`, builds the app, reconciles
managed resources, starts runtime replicas, and promotes the current release
when the deployment is healthy.

**Flags:**

- `--no-cache`: Force build from scratch
- `--allow-risk`: Proceed even if security issues are found during the local scan

### `adios login`

Log in to Adios.

**Flags:**

- `--context string`: Context to save the login into
- `--environment string`: `production`, `staging`, or `custom`

Login uses browser-based OAuth. Inspect `adios login --help` for your release.

### `adios teams` and `adios teams switch YOUR_TEAM_ID`

List accessible teams and select the active team for CLI operations.

### `adios auth print-token --ttl 15m`

Team administrators can mint a short-lived, team-bound bearer token for manual
REST requests. Raw CLI credentials are DPoP-bound and cannot replace this flow.
See [API authentication](api/authentication.md).

### `adios logs [app-name]`

Read build or runtime logs.

**Flags:**

- `--build`: Show build logs
- `--runtime`: Show runtime logs
- `--build-id string`: Show logs for a specific build ID

### `adios sync [workspace-id]`

Push local source files into an existing workspace. When no workspace ID is
provided, the CLI resolves it from `adios.yaml` or linked app workspaces.

**Flags:**

- `--pull`: Copy workspace files back down to the local directory
- `--delete`: Mirror deletes in the selected direction
- `--target string`: Sync a workspace subdirectory
- `--dry-run`: Preview the planned changes

---

## Apps

### `adios apps list`
List applications.

### `adios apps get <app-id-or-name>`
Get application details.

### `adios apps builds <app-id-or-name>`
List builds and runtime versions for an application.

---

## Workspaces

Manage development workspaces with `adios workspace`, `adios workspaces`, or
`adios ws`.

### `adios ws list`
List workspaces.

### `adios ws get <workspace-id>`
Get workspace details.

### `adios ws create`
Create a workspace.

### `adios ws run start <workspace-id>`
Start a workspace preview runtime.

### `adios ws run stop <workspace-id>`
Stop a workspace preview runtime.

### `adios ws run restart <workspace-id>`
Restart a workspace preview runtime.

Workspace run commands build the workspace source and return a stable generated
preview URL for the active workspace replica.

---

## Workflows

### `adios workflow run <manifest.yaml>`
Run a workflow manifest locally for simple development checks. The local runner
supports a subset of platform step kinds.

### `adios workflow deploy <manifest.yaml>`
Deploy a workflow manifest to the Adios platform.

### `adios workflow worker`
Start a local workflow worker connected to RabbitMQ.

### `adios workflow event publish <event-name>`
Publish a workflow event with an optional JSON payload.

Workflow manifests define `workflow_id`, `title`, `triggers`, `steps`, and
secret references. See [Workflows](workflows.md) for a complete YAML
example.

---

## Databases and Secrets

### `adios databases list`
List managed database workloads.

### `adios databases create`
Create a managed database from a supported template such as Postgres, Redis,
RabbitMQ, MongoDB, or MySQL.

### `adios databases launch <database-id-or-name>`
Launch the managed database runtime.

### `adios secrets list`
List team-scoped secrets.

### `adios secrets set <name>`
Create or update a team-scoped secret.

Pass a simple value as a positional argument, through standard input with
`--stdin`, or directly from a file. Use `--from-file` for multiline values such
as SSH private keys so shell quoting does not alter them:

```bash
adios secrets set BITBUCKET_DEPLOY_KEY \
  --from-file ~/.ssh/adios-build
```

Add `--team <team-id>` to target a team other than the active CLI team. See
[Private Git Dependencies](private-git-dependencies.md) for the complete
deploy-key setup.

### `adios secrets delete <name>`
Delete a team-scoped secret.

---

## Domains and Routing

### `adios domains list`
List custom domains.

### `adios domains add <hostname>`
Add a custom domain to an app.

### `adios domains remove <domain-id>`
Remove a custom domain.

### `adios ingress list`
List ingress routes.

### `adios ingress add`
Add an ingress route mapping a host or path to a workload.

See [Domains and Redirects](routing.md) for `adios.yaml` examples using
`custom_hosts` and `redirects`.
