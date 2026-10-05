# Build and Deploy a Go Webhook Processor

Build a Go service that receives third-party webhook payloads, validates them,
and writes clean event records into SQL.

## The Stack

- Go with `net/http` or Gin
- Postgres or MySQL
- A persistent runtime with native Go connection pooling
- Adios routing, TLS, logs, and deploy controls

## Why a Persistent Go Service Fits Webhooks

A compiled Go service can keep database connections open and handle signature
validation in one long-running process. Adios supplies the runtime, route, TLS,
logs, health checks, and secret references around that process.

## 1. Build the Handler

Ask the Adios AI agent:

```txt
Build a Go webhook processor with POST /webhooks/:provider. Verify a shared
signature header, decode JSON, store events in Postgres, and expose /healthz.
Use context-aware database calls and tests for invalid signatures.
```

## 2. Add `adios.yaml`

```yaml
name: webhook-processor
region: de
replicas: 2

build_cmd: go build -o /app/webhook-processor ./cmd/server
start_cmd: /app/webhook-processor

runtime:
  name: go@1.25
  port: 8080
  health_path: /healthz
  memory_mb: 512

env:
  DATABASE_URL: secret://DATABASE_URL
  WEBHOOK_SECRET: secret://WEBHOOK_SECRET

requires:
  - db
```

## 3. Deploy

```bash
adios secrets set WEBHOOK_SECRET
adios up
adios logs --runtime
```

## 4. Load Test the Handler

Use your preferred load-testing tool against the generated route. Watch request
latency, runtime logs, and database writes. The point is not to chase a fake
benchmark, but to learn how a small Go binary behaves under real traffic.

Review the [Go deployment path](https://adios.dev/deploy-golang), compare the
[Go API templates](https://adios.dev/deploy-golang#templates), and use the
[PostgreSQL deployment checks](https://adios.dev/deploy-postgres) before adapting the handler for
production events.
