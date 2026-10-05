# Adios documentation

Adios is a Web IDE, AI coding agent, and deployment platform for apps, APIs,
and workflows. A workspace brings your source code, Git integration, previews,
logs, configuration, managed services, and deployment controls into one place.
You can also deploy an existing local application with `adios up`.

These docs explain how to use the platform and integrate with its public API.
Read them at [adios.dev/docs](https://adios.dev/docs/) or follow the guides below.

## Get started

| You want to… | Start here |
| --- | --- |
| Set up your account or team | [Accounts and teams](docs/content/accounts.md) |
| Deploy an existing application | [Install the CLI](docs/content/installation.md), then [deploy your first app](docs/content/quickstart.md) |
| Build or change an app with AI | [Workspaces](docs/content/workspaces.md) and [AI agent](docs/content/ai.md) |
| Integrate Adios into a client or script | [API quickstart](docs/content/api/quickstart.md) |
| Connect an external AI client | [MCP and integrations](docs/content/integrations.md) |
| Investigate a failed deployment | [Logs and troubleshooting](docs/content/observability.md) |

## Platform guides

- **Workspaces and AI:** [workspace source and previews](docs/content/workspaces.md), [AI coding](docs/content/ai.md), and [private Git dependencies](docs/content/private-git-dependencies.md).
- **Deployments:** [releases and rollbacks](docs/content/deployments.md), [the CLI](docs/content/cli.md), [adios.yaml](docs/content/manifest.md), and [templates](docs/content/templates.md).
- **Services and networking:** [managed resources](docs/content/managed-resources.md), [domains and routing](docs/content/routing.md), and [storage, volumes, and backups](docs/content/storage.md).
- **Configuration and automation:** [secrets](docs/content/secrets.md) and [workflows](docs/content/workflows.md).
- **Operations:** [logs and troubleshooting](docs/content/observability.md), [billing and usage](docs/content/billing.md), and [platform architecture](docs/content/architecture.md).

## API documentation

Use the public REST API to manage applications, workspaces, domains, workflows,
object storage, and related team resources.

1. [Authenticate](docs/content/api/authentication.md) with a supported team-bound bearer token.
2. [Make your first API requests](docs/content/api/quickstart.md).
3. Browse the [API reference](docs/content/api/index.md) and [Postman guide](docs/content/api/postman.md).
4. Review [errors and pagination](docs/content/api/errors.md) when building an integration.

The reference covers 140 core REST operations and four public MCP discovery
operations. Download the files to explore requests or generate a client:

- [Public OpenAPI specification](docs/content/assets/adios-public.openapi.yaml)
- [Core Postman collection](docs/content/assets/adios-api.postman_collection.json)
- [Read-only Postman quickstart](docs/content/assets/adios-quick-start.postman_collection.json)
- [Production Postman environment](docs/content/assets/adios-production.postman_environment.json), with credentials left blank

For AI client connections, follow the [MCP integration guide](docs/content/integrations.md).

## Examples and application guides

Start with deployment examples for [Next.js](docs/content/examples/nextjs.md),
[Go](docs/content/examples/go.md), [Python](docs/content/examples/python.md),
[Ruby](docs/content/examples/ruby.md), or [.NET](docs/content/examples/dotnet.md).
The [application guides](docs/content/guides/index.md) walk through projects such
as a webhook processor, a realtime analytics service, and semantic search.

## License

Copyright (c) 2026 Adios Global LLC. The documentation, code examples, API
specifications, and build tooling are licensed under [MIT](LICENSE). The same
license applies to these docs on adios.dev/docs and Read the Docs.
See [NOTICE](NOTICE.md) for the scope and branding exclusions.

To improve the documentation, see the [contributor guide](CONTRIBUTING.md).
