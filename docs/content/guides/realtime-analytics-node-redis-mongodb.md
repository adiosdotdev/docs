# Build and Deploy a Realtime Analytics Dashboard with Node.js, Redis, and MongoDB

Build a live analytics dashboard that tracks clicks, stores historical trends,
and streams events to the browser over WebSockets.

## The Stack

- Node.js with Express and Socket.io
- MongoDB for historical events
- Redis for active counters and pub/sub
- Adios runtime with a long-running Node process

## Why This Workload Needs a Persistent Process

WebSocket apps need a process that stays alive. Serverless functions can be
awkward for long-lived connections because they are designed around short
requests. On Adios, the Node.js server runs as a persistent runtime, while the
platform handles routing, TLS, logs, and managed service connections.

## 1. Build the App

Ask the Adios AI agent:

```txt
Build an Express and Socket.io analytics dashboard. Track click events, store
them in MongoDB, publish live counts through Redis, and show a realtime chart in
the browser. Add /healthz.
```

## 2. Add `adios.yaml`

```yaml
name: realtime-analytics
region: de
replicas: 1
routable: true

build_cmd: npm ci
start_cmd: node server.js

runtime:
  name: node@24
  port: 3000
  health_path: /healthz
  memory_mb: 1024

env:
  MONGODB_URI: secret://MONGODB_URI
  REDIS_URL: secret://REDIS_URL

requires:
  - mongo
  - cache
```

Create a MongoDB resource named `mongo` and a Redis resource named `cache`, or
set the two URLs as secrets if you already have managed services.

## 3. Deploy

```bash
adios up
adios logs --runtime
```

## 4. Test It

Open the dashboard from a laptop and a phone, click around, and watch both
clients receive the same live stream. Then inspect runtime logs and MongoDB
rows to confirm the app is handling both live and historical paths.

Review the [Node.js deployment path](https://adios.dev/deploy-nodejs), the
[Redis deployment checks](https://adios.dev/deploy-redis), and the
[MongoDB deployment checks](https://adios.dev/deploy-mongo) before adapting this stack for
production analytics.
