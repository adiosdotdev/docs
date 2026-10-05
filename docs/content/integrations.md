# MCP and integrations

Adios exposes a hosted Model Context Protocol (MCP) server for supported AI
clients. It lets an authorized client work with Adios workspaces, files,
commands, previews, builds, deployments, and runtime state.

## Connect an MCP client

Create a remote Streamable HTTP connection using:

```text
https://api.adios.dev/v1/mcp
```

Let the client complete Adios OAuth in the browser. Select the intended account
and team and review the requested access. MCP uses authorization code with PKCE;
its tokens are scoped to MCP and cannot replace a general REST bearer token.

Clients that start a local stdio command can use the published bridge, which
requires Node.js 20.18.1 or later and npm:

```json
{
  "mcpServers": {
    "adios": {
      "command": "npx",
      "args": ["-y", "@adiosdotdev/mcp"]
    }
  }
}
```

The bridge connects to the hosted service and handles OAuth. It does not run
the Adios platform on your machine. Client-specific setup is available on the
[MCP integration page](https://adios.dev/mcp) and in the
[official client package](https://github.com/adiosdotdev/mcp).

## Inspect tools and review actions

Public discovery is available at:

```text
https://api.adios.dev/v1/mcp/config
https://api.adios.dev/v1/mcp/tools
```

The live tool catalog describes current names and input schemas. Discovery
does not execute tools. Inspect the workspace and team context before asking a
client to make changes, and review its approval requests for deployments,
runtime operations, deletion, or remote Git writes.

For example, ask the client to inspect a workspace, run its build, and start a
preview. Verify the result before approving a deployment. The official plugin
includes build/deploy and operational debugging workflows.

## Postman MCP

Download the [HTTP connection configuration](assets/adios-mcp-http.json),
[stdio connection configuration](assets/adios-mcp-stdio.json), or
[public discovery collection](assets/adios-mcp-discovery.postman_collection.json).
The connection JSON files configure native MCP requests; they are not REST
collection exports. Use Postman's native MCP request and OAuth support to connect.

Direct Postman OAuth requires the deployed API to allow Postman's callback URL.
The stdio bridge is an alternative when native HTTP sign-in is unavailable.
Keep MCP credentials and authenticated tool output private.

## Manage connections

Use the dashboard's **Integrations** settings to inspect and revoke authorized
connections. Disconnect clients you no longer use. Configure Git access and
build-only keys through the relevant provider settings; follow
[private Git dependencies](private-git-dependencies.md) for dependency builds.
