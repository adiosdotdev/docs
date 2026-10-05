# Architecture

Adios is organized around workspaces, source, deploys, runtime versions, and
managed infrastructure.

```txt
Web IDE workspace -> AI agent -> preview -> deploy current version
CLI project       -> adios up -> deploy current version
```

## Product Flow

1. Create a workspace or connect an existing app.
2. Open and edit the source code in the Web IDE.
3. Ask the AI agent to build a frontend, API, database integration, workflow, or
   feature.
4. Run builds, tests, previews, logs, and checks from the workspace.
5. Commit through Git, sync locally, or deploy.
6. Promote the current runtime version when the app is ready.

## Runtime Model

- **Source:** every deploy is tied to source that can be reopened in a
  workspace.
- **Versions:** each deploy creates a version with logs, artifacts, and release
  state.
- **Replicas:** versions can run as one or more runtime replicas.
- **Regions:** replicas can be placed regionally.
- **Current:** generated routes and custom domains point at the promoted current
  release.
- **Config:** feature flags, secrets, environment variables, volumes, and
  backups stay with the app.

## Platform Services

Adios provides the services apps normally need around the code:

- CDN and custom domain routing
- anycast IP entry points
- object storage for artifacts, uploads, and backups
- managed databases and queues
- runtime logs, build logs, HTTP events, metrics, traces, and errors
- workflow creation and execution

## Workspaces and Git

Workspaces are source-backed. You can open deployed app code, make changes in
the Web IDE, ask the agent to modify the app, review diffs, commit, push, pull,
and sync files with the local CLI.
