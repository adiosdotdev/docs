# Build and Deploy a .NET Crypto Price Ticker with Redis

Build a .NET Minimal API that polls a public crypto price feed, stores a compact
latest-price buffer in Redis, and serves a realtime dashboard endpoint.

## The Stack

- .NET 8 Minimal APIs
- Redis for latest prices and short-lived buffers
- Adios runtime for Linux-based deployment without IIS or Azure setup

## Why This Architecture Fits the Workload

A .NET Minimal API can run as a Linux service without an IIS-specific deployment
path. The application keeps its Redis connection and polling loop in source,
while Adios supplies the runtime, route, TLS, logs, and secret references.

## 1. Build the API

Ask the Adios AI agent:

```txt
Build a .NET 8 Minimal API crypto ticker. Poll a public crypto price endpoint,
store latest prices in Redis, expose GET /prices and /healthz, and add a simple
HTML dashboard.
```

## 2. Add `adios.yaml`

```yaml
name: dotnet-crypto-ticker
region: de
replicas: 1

build_cmd: dotnet publish -c Release -o /app/out
start_cmd: dotnet /app/out/CryptoTicker.dll

runtime:
  name: dotnet@8.0
  port: 8080
  health_path: /healthz
  memory_mb: 768

env:
  REDIS_URL: secret://REDIS_URL

requires:
  - cache
```

## 3. Deploy

```bash
adios up
adios logs --runtime
```

## 4. Verify

Open `/prices`, refresh the dashboard, and check the runtime logs while prices
update. Redis keeps the latest values close to the app without putting every
request through the external API.

Review the [.NET deployment path](https://adios.dev/deploy-dotnet), the
[Redis deployment checks](https://adios.dev/deploy-redis), or the complete
[.NET 8 template](https://adios.dev/deploy-dotnet#templates) before adapting this example.
