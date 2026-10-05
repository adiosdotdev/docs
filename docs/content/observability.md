# Logs, metrics, and troubleshooting

Start with the failing stage: source sync, build, startup, routing, or an
application request. Build logs and runtime logs answer different questions.

## Read logs

Open an application's **Logs** or **Observability** views in the dashboard, or
use the CLI from the linked local project:

```sh
adios logs --build
adios logs --runtime --lines 100
adios logs --runtime --follow
adios logs --http
adios logs --errors
```

Use `--build-id YOUR_BUILD_ID` to inspect a specific build. Use `--region` or
`--replica` to narrow runtime output when several instances are running. Stop
a live log stream with Ctrl+C.

## Diagnose a failed deploy

| Symptom | First checks |
| --- | --- |
| Dependency install or compilation fails | Build log, lockfile, runtime version, build command, private dependency credentials. |
| Build succeeds but startup fails | Start command, output path, required environment variables, runtime log. |
| Health check fails | Configured port, listening interface, health path, status code, application readiness. |
| Generated URL works but custom domain fails | Domain ownership verification, DNS target, TLS, current route. |
| Database connection fails | Team, private hostname, version, credentials, service health, region/network context. |
| Preview differs from production | Source revision, environment, manifest, build artifact, active version. |
| AI task is blocked | Run error, provider connection, selected model, funding, pending approval. |

Check the requested deployment's status as well as its public URL. A healthy
previous release can continue serving while a new build fails.

## Metrics and incidents

Use the application's **Observability** views to inspect the telemetry available
for that workload and time range. Review the displayed units, source times, and
gaps before comparing requests, CPU, memory, or other measurements. A missing
sample is not a measurement of zero, and a stopped runtime can have different
reporting behavior from a running one.

When investigating an incident, correlate the deployment or source change with
runtime logs and the affected time range. Keep secrets and private request data
out of screenshots or public issue reports.

## Share useful evidence

Record the team, workload, build or run ID, region, approximate UTC time,
command used, and the failing response or log excerpt. Include the expected
behavior and a minimal reproduction. Remove bearer tokens, passwords, cookies,
and personal data before sharing outside your team.

For HTTP status errors and API pagination, see [API errors](api/errors.md).
For persistence and recovery, see [storage](storage.md).
