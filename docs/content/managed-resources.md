# Managed Resources and Versioned Internal DNS

Managed Postgres, MySQL, MongoDB, Redis, and RabbitMQ services receive a stable
private hostname. Your application can use that hostname for the promoted
current release or add a version label to reach a specific healthy deployment.

## Define resources with the application

The `resources` section keeps the service configuration and application binding
in one `adios.yaml` file:

```yaml
name: aor-api
region: de

resources:
  - name: db
    template: postgres:16
    database: aor
    username: aor_api
    password: secret://POSTGRES_PASSWORD
  - name: redis
    template: redis:7
    database: "0"
    password: secret://REDIS_PASSWORD
  - name: rabbitmq
    template: rabbitmq:3
    database: aor
    username: aor_api
    password: secret://RABBITMQ_PASSWORD
```

Adios gives every managed resource a unique App ID. With the example above, the
Postgres resource will normally have an ID similar to `aor-api-db`, even though
its short resource name is `db`. Internal DNS uses the unique App ID so another
application can also have a resource named `db` without sharing its target.

## Team ID and VPC ID

`team_id` identifies the team that owns the application, resources, secrets,
and deployment records. `vpc_id` identifies the private network in which the
workloads receive addresses and resolve internal services.

They are separate fields, but `vpc_id` defaults to `team_id` when you don't set
one:

```yaml
name: aor-api
team_id: team-a
# vpc_id defaults to team-a
```

That default produces a current resource name such as:

```text
aor-api-db.de.team-a.svc.internal
```

If the application explicitly uses `vpc_id: production`, the corresponding
name is `aor-api-db.de.production.svc.internal`. DNS labels are normalized to
lowercase, so an uppercase or mixed-case team or VPC ID appears lowercase in a
generated hostname.

## Use the injected connection settings

`adios up` adds engine-native connection settings to the application. For a
Postgres resource named `db`, the runtime receives values like these:

```text
DB_HOST=aor-api-db.de.<vpc-id>.svc.internal
DB_PORT=5432
DB_DATABASE=aor
DB_USER=aor_api
DB_PASSWORD=<secret reference>
DB_DATABASE_URL=secret://ADIOS_AOR_API_DB_DB_DATABASE_URL
DATABASE_URL=secret://ADIOS_AOR_API_DB_DATABASE_URL
```

Secret references are resolved for the runtime. The password and derived URL
aren't written into source control or returned to a browser.

Each engine also receives a conventional global URL when the application has
not supplied its own value:

| Template | Global URL | Native port |
| --- | --- | ---: |
| Postgres / pgvector | `DATABASE_URL` | `5432` |
| MySQL | `DATABASE_URL` | `3306` |
| MongoDB | `MONGODB_URL` | `27017` |
| Redis | `REDIS_URL` | `6379` |
| RabbitMQ | `AMQP_URL` | `5672` |

Resource-prefixed variables remain available when an application has more than
one service of the same engine. A resource named `sessions`, for example, gets
`SESSIONS_HOST`, `SESSIONS_PORT`, and `SESSIONS_REDIS_URL`.

### Short names such as `DB_HOST=db`

Adios runtimes receive DNS search domains for their region and VPC. A standard
system resolver can therefore expand the short name `db` to names such as
`db.de.team-a.svc.internal` and `db.team-a.svc.internal`.

That short name is a friendly service alias, not the unique managed-resource
App ID. It can be ambiguous when two applications in the same VPC both have a
resource named `db`, and custom DNS clients don't always honor system search
domains. Don't use it as the managed database endpoint.

When a managed resource is named `db`, Adios normally replaces a plain value
such as `DB_HOST=db` with the generated App-ID hostname during deployment. Use
the injected `DB_HOST` or `DATABASE_URL`. If you need to write the host
explicitly, use `aor-api-db.de.team-a.svc.internal` for current or
`aor-api-db.v1.de.team-a.svc.internal` for an exact version. An explicit
`secret://` value remains under your control and is not replaced.

## Current and exact-version names

The region-qualified forms are the clearest and are what generated managed
resource connections use:

| Target | Internal DNS name |
| --- | --- |
| Promoted current release | `<app-id>.<region>.<vpc-id>.svc.internal` |
| Exact version | `<app-id>.<version>.<region>.<vpc-id>.svc.internal` |

For a resource with App ID `aor-api-db` in region `de` and VPC `team-a`:

```text
# Promoted current release
aor-api-db.de.team-a.svc.internal

# Exact healthy versions
aor-api-db.v1.de.team-a.svc.internal
aor-api-db.v2.de.team-a.svc.internal
```

`current` means the version recorded in the promoted release. It does not mean
the greatest version string. If `v2` has been deployed but not promoted, the
unversioned name continues to reach `v1`. After `v2` is promoted, new
connections through the unversioned name reach `v2`.

The DNS name resolves to a stable service VIP. The internal proxy chooses a
healthy replica for the selected App ID, version, region, VPC, native port, and
protocol. An established database or queue connection is not moved in place;
clients must reconnect before they use a newly promoted target.

## Pin a resource version in the manifest

Set `version` when an application must bind to an exact managed-resource
deployment:

```yaml
resources:
  - name: db
    template: postgres:16
    version: v1
    database: aor
    username: aor_api
    password: secret://POSTGRES_PASSWORD
```

The generated host includes `.v1.` instead of following the unversioned current
name. On a deployment that promotes managed resources, the selected resource
version may also become current. Treat this as an intentional pin or rollback,
not as a read-only inspection switch.

For a diagnostic workload that must compare versions without changing the
current pointer, keep its normal credentials in Secret Manager and connect to
the explicit version hostname directly.

## What a resource version represents

A versioned DNS name selects a runtime deployment. It is not a database
snapshot and does not reconstruct historical data. The exact-version name only
returns a target when that version has a healthy running replica.

Persistent services are also subject to volume ownership and single-writer
fencing. An older runtime may be stopped or unable to run beside the current
writer. Use managed snapshots and the documented restore workflow when you
need historical data, rather than assuming that `v1` is a point-in-time copy.

## Network and security boundaries

- `svc.internal` names are available to deployed workloads on the permitted
  private VPC network. They are not public database endpoints and normally
  won't resolve from a developer laptop.
- Source-aware DNS prevents a workload from resolving a different VPC's
  internal service name.
- The hostname is not a credential. Keep passwords and complete connection URLs
  in Secret Manager.
- A local Docker development deployment may use `host.docker.internal` and a
  published port instead of `svc.internal`.
- A resource explicitly configured for an external network does not receive an
  internal service hostname.

## Troubleshooting

**The current name has no record.** Confirm that the resource has a promoted
current release and at least one healthy replica in the requested region. A
deployment can exist without being current.

**An exact version has no record.** Check the complete version label and verify
that version is still running and healthy. Retained metadata alone is not
enough to create a DNS target.

**The name resolves but the connection fails.** Use the engine's native port,
check the target's readiness, and confirm that the application and resource are
in the same VPC. Existing connection pools may also need to reconnect after a
promotion.

**The application reaches the wrong version.** Check the promoted release
instead of comparing version strings. Use the explicit version form to test a
specific deployment.

**Two resources are both named `db`.** Use the generated resource App IDs. The
short name is for manifest variables; the App ID is the unique DNS service key.

See the engine guides for template-specific configuration:
[PostgreSQL](examples/postgres.md), [MySQL](examples/mysql.md),
[MongoDB](examples/mongodb.md), [Redis](examples/redis.md), and
[RabbitMQ](examples/rabbitmq.md).
