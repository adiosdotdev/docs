# Build and Deploy Semantic Search with FastAPI and pgvector

Build a personal knowledge-base search engine where users paste paragraphs and
search by meaning, not just exact words.

## The Stack

- Python with FastAPI
- Postgres with the `pgvector` extension
- Gemini API for embeddings
- Adios runtime with secrets and managed database wiring

## Why This Architecture Fits Semantic Search

AI backends often import heavier Python libraries and initialize API clients at
startup. On Adios, your FastAPI app runs as a normal long-lived service, so your
backend can stay warm instead of rebuilding state on every request.

## 1. Build the API

Ask the Adios AI agent:

```txt
Build a FastAPI semantic search API. Add endpoints to insert documents and
search them using embeddings. Use Gemini for embeddings, Postgres pgvector for
similarity search, and /healthz for health checks.
```

## 2. Add `adios.yaml`

```yaml
name: semantic-search
region: de
replicas: 1

build_cmd: python -m pip install -r requirements.txt
start_cmd: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT

runtime:
  name: python@3.13
  port: 8000
  health_path: /healthz
  memory_mb: 1024

env:
  DATABASE_URL: secret://DATABASE_URL
  GEMINI_API_KEY: secret://GEMINI_API_KEY

requires:
  - vector-db
```

Create a Postgres pgvector resource named `vector-db`, or set `DATABASE_URL`
manually if you already have one.

## 3. Deploy

```bash
adios secrets set GEMINI_API_KEY
adios up
```

Your app gets a generated Adios route with TLS, runtime logs, and managed
database connection details without a Dockerfile or cloud console setup.

Review the [FastAPI deployment path](https://adios.dev/deploy-fastapi), the
[pgvector deployment checks](https://adios.dev/deploy-pgvector), and the exact
[pgvector template](https://adios.dev/deploy-pgvector#templates) before adapting this example to a
production document corpus.
