# Workspaces

Workspaces are where Adios apps are created, edited, previewed, and deployed.
The Web IDE opens the source code of your app, and the AI agent works directly
inside that codebase. Team members work from the same project context instead
of passing source, build output, previews, and deployment state between tools.

## What a Workspace Includes

- source files and project structure
- multi-user team access to the shared project context
- Git status, commits, push, pull, and sync
- AI agent plans, edits, and verification steps
- builds, tests, and build and runtime logs
- preview runtime controls and a stable generated URL
- secrets, feature flags, environment variables, and runtime config
- workflow definitions and run history
- deploy controls for the current runtime version

## Team Collaboration

A workspace keeps the source tree, Git state, AI agent activity, builds,
preview runtime, logs, configuration, workflows, and deployment state visible
in one shared project context. Team members can review the same changes and
runtime evidence before deciding what to commit or deploy.

## AI Agent Flow

1. Describe the app, API, full-stack feature, workflow, or integration.
2. The agent creates a plan and edits the workspace source.
3. You and your team review files, diffs, manifest changes, and workflow steps.
4. The workspace runs builds, tests, previews, and log checks.
5. You commit to Git, sync locally, or deploy the current version.

## Preview and Deploy

Workspace previews run from the current workspace source and return a stable
generated URL. Once the preview is verified, deploy the workspace as a runtime
version and promote it as the current release.

## Sync Locally

```bash
adios sync
adios sync --pull
```

Use `adios sync` to push local files into a workspace. Use `adios sync --pull`
to bring workspace changes back to your local project.
