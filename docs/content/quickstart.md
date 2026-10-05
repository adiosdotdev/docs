# Quickstart

Deploy an existing app from your terminal with the user CLI.

First [install the CLI](installation.md), run `adios login`, and select your
team with `adios teams switch YOUR_TEAM_ID`. This example assumes a Node app
with `pnpm` scripts named `build` and `start`, and a working `/api/health`
endpoint. Use the [application guides](guides/index.md) for other examples.

## 1. Add `adios.yaml`

Create an `adios.yaml` file at the root of your project:

```yaml
name: dashboard
region: de
replicas: 1

build_cmd: pnpm install --frozen-lockfile && pnpm build
start_cmd: pnpm start

runtime:
  name: node@24
  port: 3000
  health_path: /api/health
  memory_mb: 1024

```

This describes the app, runtime port, health check, resource size, replica
count, and region. Choose a region available to your team. Make the app listen
on port 3000 on a network-accessible interface and return HTTP 200 from
`/api/health`. If the app needs a database, configure it through
[managed resources](managed-resources.md) before deployment.

## 2. Deploy the Current App

```bash
adios up
```

The deploy uploads your current source, builds the app, creates a runtime
version, starts replicas, and promotes the current release when the deployment
is healthy.

## 3. Inspect Logs

```bash
adios logs --build
adios logs --runtime
```

Use build logs to debug package installs and compile output. Use runtime logs to
debug the live app.

## 4. Continue in a Workspace

After an app has source attached, open it in the Web IDE to inspect and edit the
same code that produced the deployed runtime. From there you can ask the AI
agent to add features, edit APIs, create workflows, run previews, commit to Git,
or sync files back to your local repo.

```bash
adios sync
adios sync --pull
```

`adios sync` pushes local files into a linked workspace. `adios sync --pull`
copies workspace files back down to your local directory.
