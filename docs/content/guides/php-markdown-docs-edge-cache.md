# Build and Deploy a PHP Markdown Documentation Site

Build a PHP documentation site that renders Markdown from MySQL, sends cache
headers, and serves fast pages without managing Nginx or certificates.

## The Stack

- PHP 8.2 with a minimal router or Laravel
- MySQL for document content
- Markdown rendering in the app
- Adios runtime plus edge-aware caching behavior

## Why This Architecture Fits Documentation

PHP renders the published Markdown while MySQL keeps the editable source. The
application sets cache headers for responses that can be reused, and Adios
provides the runtime, routing, TLS, logs, and configured cache behavior.

## 1. Build the App

Ask the Adios AI agent:

```txt
Build a PHP documentation app. Load Markdown pages from MySQL, render them as
HTML, add a sidebar, set Cache-Control headers for published pages, and expose
/healthz.
```

## 2. Add `adios.yaml`

```yaml
name: php-docs
region: de
replicas: 1
routable: true

build_cmd: composer install --no-dev --optimize-autoloader
start_cmd: php -S 0.0.0.0:$PORT public/index.php

runtime:
  name: php@8.2
  port: 8080
  health_path: /healthz
  memory_mb: 512

cache:
  enabled: true
  ttl_seconds: 300
  methods:
    - GET

env:
  DATABASE_URL: secret://DATABASE_URL

requires:
  - db
```

## 3. Deploy and Inspect

```bash
adios up
adios logs --runtime
```

Open a published page twice and inspect response headers in the browser network
tab. Your app controls cacheability with `Cache-Control`; Adios handles the
runtime and routing layer.

Review the [PHP deployment path](https://adios.dev/deploy-php), the
[MySQL deployment checks](https://adios.dev/deploy-mysql), and the
[Laravel deployment path](https://adios.dev/deploy-laravel) if the documentation application
uses that framework.
