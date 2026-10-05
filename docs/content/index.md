# Adios documentation

Adios is a Web IDE, AI coding agent, and deployment platform for apps, APIs, full-stack products, and workflows.

Adios starts with a workspace. A workspace gives you the source code of your
app, Git integration, previews, logs, runtime config, secrets, managed
databases, workflows, and deploy controls in one place. The AI agent works
inside that workspace so generated code stays inspectable and editable.

You can also deploy an existing local app directly with `adios up`.

## Choose a starting point

| You want to… | Start here |
| --- | --- |
| Set up access for yourself or a team | [Accounts and teams](accounts.md) |
| Deploy code you already have | [Installation](installation.md), then [quickstart](quickstart.md) |
| Build or change an app with AI | [Workspaces](workspaces.md) and [AI agent](ai.md) |
| Integrate Adios into a client or script | [API quickstart](api/quickstart.md) and [API reference](api/index.md) |
| Connect an external AI client | [MCP and integrations](integrations.md) |
| Investigate a failed deployment | [Logs and troubleshooting](observability.md) |

These guides cover the platform's user workflows and the reviewed public API.

## What You Can Build

- **Full-stack apps:** frontend, API routes, database schema, background jobs,
  feature flags, secrets, and deployment config.
- **APIs and services:** versioned runtimes with replicas, regions, logs,
  metrics, traces, volumes, and backups.
- **Managed infrastructure:** CDN routes, custom domains, anycast IPs, object
  storage, Postgres, Redis, RabbitMQ, MongoDB, and MySQL.
- **Workflows:** webhook, event, schedule, approval, HTTP, data transform, wait,
  and exec steps that run as tracked automation.

## How the Agent Works

1. Open or create a workspace in the Web IDE.
2. Ask the agent to build an app, API, workflow, integration, or feature.
3. Review the source changes, generated manifest, database resources, and
   workflow steps.
4. Run tests, builds, previews, and logs from the workspace.
5. Commit through Git, sync locally, or deploy the current version.

## Runtime Concepts

- **Versions:** each deploy creates a version that can be previewed, inspected,
  and promoted.
- **Current release:** one version is promoted as the current live release.
- **Replicas:** runtime replicas can run across regions for availability and
  scale.
- **Config:** feature flags, secrets, environment variables, volumes, and
  backups stay attached to the app.

## Next Steps

- [Deploy an existing app](quickstart.md)
- [Create workflows](workflows.md)
- [Connect domains](routing.md)
- [Follow application guides](guides/index.md)
- [Manage secrets](secrets.md), [storage](storage.md), and [billing](billing.md)
- [Download OpenAPI and Postman files](api/index.md)
