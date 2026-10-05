# Domains and Redirects

Adios can publish a runtime on generated platform routes, exact custom domains,
and redirect routes. Routing follows the promoted current release for the app,
so new deploys can move traffic without changing DNS again.

## Add Custom Domains

Add `custom_hosts` to the runtime `adios.yaml`:

```yaml
name: web
region: de
replicas: 2
routable: true

build_cmd: pnpm install && pnpm build
start_cmd: pnpm start

runtime:
  name: node@24
  port: 3000
  health_path: /api/health

custom_hosts:
  - app.example.com
  - www.example.com
```

Deploy the app after the domain is verified:

```bash
adios up
```

Each custom host points at the app's current release. Generated Adios run hosts
stay available unless you remove them from routing settings.

## Redirect a Host

Use `redirects` for exact host redirects, such as apex-to-www:

```yaml
name: web
routable: true

custom_hosts:
  - www.example.com

redirects:
  - from: example.com
    to: www.example.com
```

The redirect uses a permanent `308`, preserves the incoming path and query
string, and treats a bare destination host as HTTPS. For example,
`https://example.com/pricing?plan=pro` redirects to
`https://www.example.com/pricing?plan=pro`.

## DNS Checklist

1. Add the custom host in the Adios dashboard or manifest.
2. Point DNS for the hostname to the Adios-provided target.
3. Wait for domain verification.
4. Deploy or redeploy the runtime.
5. Confirm the route with `adios domains list` and `adios ingress list`.

## Runtime Notes

- Use `routable: false` for internal services that should not receive public
  traffic.
- Custom hosts follow the current release, not a single immutable deploy
  version.
- Redirect hosts are independent routes. Remove a redirect before reusing the
  same host as an app runtime route.
- If a runtime also needs app-level redirects, keep those in the app framework.
  Use Adios redirects for whole-host routing decisions.
