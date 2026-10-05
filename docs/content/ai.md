# Working with the AI agent

The Adios agent works on files in a source-backed workspace. Its conversation,
plan, tool activity, and verification results help you review a change before
committing or deploying it.

## Start a task

1. Open a code application's workspace in the dashboard.
2. Choose a model and connection mode in the agent controls.
3. Describe the change, the relevant files, and how you will judge success.
4. Follow the plan and tool activity while the agent works.
5. Inspect the diff and run the relevant checks before deploying.

For example:

> Add a health endpoint to this API. It should return HTTP 200 when the service
> is ready. Add a test, run it, and update adios.yaml to use that endpoint.

Give the agent concrete constraints: framework, database, compatibility needs,
and checks to run. A small, verifiable task is easier to review than a request
to change several unrelated parts of an app at once.

## Models and provider connections

The model catalog depends on current platform availability and the team's
configuration. Use the catalog shown in the workspace rather than assuming a
particular provider or model is available.

The connection controls offer automatic routing, managed access, and **BYOK**
(bring your own key). BYOK requires a supported model and a configured provider
connection for your team. Configure credentials through the platform's provider
settings; keep them out of prompts and repository files. Managed access and
BYOK have different funding requirements; provider charges for BYOK depend on
your provider account. Review [billing](billing.md) before starting a large run.

## Background work and stopping

Background jobs let work continue while you inspect the workspace. Review the
job's status, selected model, branch, and changes when it finishes. A running job
may prevent a second conflicting job from starting.

Use the run's stop control when you need to interrupt it. Cancellation may take
time to reach an active operation, and existing file changes remain in the
workspace. Inspect Git status and the diff before retrying. Retrying a failed
run should follow a review of its error and the state it left behind.

## Review and approvals

Check the files changed, commands executed, tests, preview, and deployment
configuration. When a workflow or client presents an approval, review the exact
action and target before accepting it. Deployment and other operational changes
can affect live applications and consume resources.

A successful agent response is one piece of evidence. Verify the application's
main behavior in the preview and inspect the resulting build and runtime state.

## Usage and integrations

The workspace's **Usage** view shows recorded input, output, cached, and tool
tokens and reported cost for the conversation. Missing usage data is not proof
that no usage occurred. Team billing is the place to review funding and balances.

You can also use Adios from an external AI client through [MCP](integrations.md).
The [workspaces guide](workspaces.md) covers source, Git, preview, and local sync.
