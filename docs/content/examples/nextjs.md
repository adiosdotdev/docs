# Deploy Next.js

Deploy an existing Next.js app as a persistent Node.js process. Static pages,
server-rendered routes, and API routes can ship in the same application.

Use the [Next.js deployment page](https://adios.dev/deploy-nextjs) to review production fit,
pricing, templates, and release checks before following the implementation
steps below.

Starting from an empty folder? Follow the [complete Next.js build and deploy
tutorial](https://adios.dev/guides/build-and-deploy-nextjs), or use the [AI-assisted app build
workflow](https://adios.dev/guides/build-apps-with-ai) for Codex, ChatGPT, Gemini, and Claude.

## Prerequisites

- A Next.js project that installs and builds from a clean checkout
- A production start script, such as `next start`
- The [Adios CLI](../installation.md) installed and authenticated

## 1. Add a health route

For an App Router project, add `app/api/health/route.js`:

```js
export function GET() {
  return Response.json({ status: "ok" });
}
```

The route should return a successful response when the application is ready to
receive traffic. If it depends on a database or another required service,
decide whether the health response should verify that dependency too.

## 2. Configure the runtime

Create `adios.yaml` in the project root:

```yaml
name: my-nextjs-app
region: de
replicas: 1

build_cmd: npm ci && npm run build
start_cmd: npm start

runtime:
  name: node@24
  port: 3000
  health_path: /api/health
  memory_mb: 1024
```

Keep the package manager and lockfile your project already uses. For pnpm,
replace the command fields with the equivalent pnpm commands:

```yaml
build_cmd: pnpm install --frozen-lockfile && pnpm build
start_cmd: pnpm start
```

Adjust the Node.js version, port, memory, region, and health path to match the
application. See the [manifest reference](../manifest.md) for every supported
field.

### Choose your build compiler

Adios runs your project's build command. You can use webpack or Turbopack.
For compatible Next.js projects, we recommend trying Turbopack to reduce build
time. Select it in your project's `package.json`:

```json
{
  "scripts": {
    "build": "next build --turbopack"
  }
}
```

Keep `next build --webpack` if your application depends on webpack plugins or
configuration. Check [Next.js compatibility](https://nextjs.org/docs/app/api-reference/turbopack)
and test your pages, API routes and generated assets before switching.

If you deploy `.next/standalone/server.js`, keep `output: "standalone"` in your
Next.js configuration. Dependency tracing identifies the files required by
that server package; Turbopack still produces those dependencies through its
own build path. Removing standalone output does not automatically disable
Next.js tracing and requires a different deployment package.

## 3. Add configuration and secrets

Public runtime configuration can be declared in the manifest. Keep sensitive
values outside Git and reference them by name:

```yaml
env:
  NEXT_PUBLIC_APP_URL: https://app.example.com
  DATABASE_URL: secret://DATABASE_URL
  AUTH_SECRET: secret://AUTH_SECRET
```

Create the referenced secret values with the CLI or Web IDE before the app
needs them at runtime.

## 4. Deploy

Run the deployment from the project root:

```bash
adios up
```

Adios uploads the current source, runs the build command, starts the production
process, checks `/api/health`, and promotes the version after it reports
healthy. The deployment returns a generated HTTPS route.

## 5. Inspect and verify

Separate build output from the running process output:

```bash
adios logs --build
adios logs --runtime
```

Open the generated route and verify a static page, a server-rendered page, and
any API route the application depends on. If the build or health check fails,
use the relevant log stream before deploying the next version.

## Custom domains

After the generated route works, attach and verify the production hostname.
Adios manages TLS for the verified domain and keeps it connected to the
promoted release. Follow [Domains and Redirects](../routing.md) for the DNS and
verification order.

## Start from a template

If you do not have an existing repository, choose an official JavaScript or
TypeScript Next.js starter with npm or pnpm in the [template catalog](https://adios.dev/deploy-nextjs#templates).
