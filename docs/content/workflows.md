# Workflows

Adios Workflows connects APIs, scripts, databases, email, object storage, and AI
agents in a sequence of tracked actions. Start a run manually, from a webhook
or event, or on a repeating interval. Add a human approval before an action
that needs review.

Start with a complete recipe: [process a webhook](https://adios.dev/workflows/webhook-processing),
[send a scheduled report](https://adios.dev/workflows/scheduled-reports), or
[review before publishing](https://adios.dev/workflows/approval-workflows).
The [workflow overview](https://adios.dev/workflows#examples) also includes S3 and script examples.

On this page: [manifest](#manifest), [triggers](#triggers),
[all ten actions](#actions), [outputs and dependencies](#outputs),
[secrets and environment variables](#secrets-and-environment-variables), and
[create and inspect](#create).

## Workflow manifest {#manifest}

A workflow manifest describes triggers, shared context, and ordered
steps. In a workflow-only repository you can name the file `adios.yaml`. In an
application repository, keep the app runtime manifest at the project root and
store workflow manifests under a directory such as `workflows/`.

```yaml
workflow_id: daily-market-brief
title: Daily market brief
team_id: team-local
enabled: true
version: "1"

triggers:
  - type: schedule
    interval: 24h
  - type: webhook
    event: market.brief.requested

context:
  market_api_url: https://api.example.com
  symbols:
    - AAPL
    - MSFT
    - NVDA

steps:
  - step_id: fetch-prices
    name: Fetch prices
    kind: http
    command:
      method: GET
      url: "{{ .context.market_api_url }}/quotes?symbols=AAPL,MSFT,NVDA"
      headers:
        X-API-Key: secret://MARKET_DATA_API_KEY

  - step_id: select-close
    name: Select close prices
    kind: data-json
    dependencies:
      - fetch-prices
    command:
      from_step: fetch-prices
      path: ".quotes"

  - step_id: publish-brief
    name: Publish brief
    kind: http
    dependencies:
      - select-close
    command:
      method: POST
      url: https://dashboard.example.com/api/market-briefs
      body: "{{ index .steps \"select-close\" \"output\" }}"
```

Replace `team-local` with your team ID, configure the API endpoints, and create
`MARKET_DATA_API_KEY` in Adios secrets before deploying this example. Its source
API expects an `X-API-Key` header; its destination receives the selected quotes
as JSON. The schedule runs once a day at 00:00 UTC. Remove `triggers` for a
manual-only test before enabling recurring delivery.

## Triggers and scheduling {#triggers}

- **Manual:** start a run from Workflows or with `adios workflow run`. A
  workflow with no `triggers` only runs this way.
- **Webhook:** use `type: webhook` and an event name, such as `order.created`.
  The incoming event payload is available as `.payload`.
- **Event:** use `type: event` and the internal event name to match.
- **Cron:** use `type: cron` with a five-field expression such as
  `cron: "0 8 * * 1-5"`. Add `timezone: Europe/Berlin` to run at a local time;
  without it, cron uses UTC.
- **Interval:** use `type: schedule` with a duration such as `interval: 1h` or
  `interval: 24h`. `cron: "@every 1h"` is the same as `interval: 1h`.

```yaml
triggers:
  - type: cron
    cron: "0 8 * * 1-5"
    timezone: Europe/Berlin
    concurrency: forbid
```

Intervals line up with UTC boundaries, so `interval: 24h` runs once a day at
00:00 UTC, not 24 hours after you deploy. Use cron with a `timezone` when you
need a specific local time. The scheduler checks for due slots about every
30 seconds. Slots missed while the scheduler was down are skipped, not replayed.

Set `concurrency: forbid` to skip a scheduled slot while an earlier event from
the same trigger is still pending or a run is waiting for approval. The skipped
slot is recorded as a skipped event. If a repeated run could still send
duplicate reports or writes, deduplicate in your application or destination.

### Public webhook endpoints {#public-webhooks}

Set `public: true` on a `webhook` or `event` trigger to receive HTTP requests
from outside Adios:

```yaml
triggers:
  - type: webhook
    event: order.created
    public: true
    public_path_pattern: /hooks/orders/{order_id}
    public_methods: [POST]
    public_hosts: [api.example.com]
    public_secret_ref: secret://ORDER_WEBHOOK_SECRET
    response_mode: queued_json
```

- `public_path_pattern` is required. Segments in braces, such as `{order_id}`,
  are captured as path parameters.
- `public_methods` and `public_hosts` limit which requests match. Leave them
  out to accept any method or host.
- `public_secret_ref` makes the caller send the secret value in the
  `X-Workflow-Secret` header. Requests without the matching value are rejected.
- `response_mode` sets the reply. `queued_json` (the default) and `async_json`
  answer right away. `sync_json` and `sync_html` wait for the run and return its
  output.

## All ten supported actions {#actions}

Every step has a unique `step_id`, a `kind`, and optionally `dependencies` and
`command`. The configuration below describes platform execution. The local CLI
runner implements only a subset of these actions.

### http — Call an API {#action-http}

Set `command.method`, `url`, optional `headers`, and `body`. The response body
becomes the step output. Use a previous step's `.output` to forward JSON as text.
See the [webhook recipe](https://adios.dev/workflows/webhook-processing#use-recipe).

```yaml
- step_id: deliver
  kind: http
  dependencies: [order]
  command:
    method: POST
    url: https://api.example.com/orders
    headers:
      X-API-Key: secret://API_TOKEN
    body: "{{ .steps.order.output }}"
```

### request-parser — Extract request fields {#action-request-parser}

Use `command.extract` to build an object from selectors such as `.payload.order`,
or `command.path` to select one value. Request metadata, when supplied by the
trigger, is available under `.request`. Extraction does not validate a schema.

```yaml
- step_id: parse
  kind: request-parser
  command:
    extract:
      order: .payload.order
```

### data-json — Select JSON values {#action-data-json}

Use `command.from_step` with the source step ID and `path` with the value to
select. `path: .` keeps the whole value; `.rows[0].orders` selects a field from
the first row. You can also supply `command.input`; without a source, the action
uses the run payload. This is a selector, not a jq expression engine.

### bash — Run shell commands {#action-bash}

Put the script in `command: |` and its environment in the step's `env` block.
The workflow worker runs it and captures stdout as the step output. Use JSON
stdout when another step needs structured data.

### python — Run a Python script {#action-python}

Use the same `command` and step-level `env` structure as Bash. Read variables
with `os.environ` and print the result. The
[script example](https://adios.dev/workflows#examples) passes JSON from Bash to Python and
calculates a total of `97` without external credentials.

### sql — Query PostgreSQL or MySQL {#action-sql}

Set `command.driver` to `postgres` or `mysql`, `dsn` to a connection secret, and
`query` to SQL. Read queries return `columns`, `rows`, and `row_count`, with at
most 100 rows. Queries that modify data require `write: true` and return
`rows_affected`. See the [report recipe](https://adios.dev/workflows/scheduled-reports#use-recipe).

### email — Send a message {#action-email}

Set `command.provider`, `from`, `to`, `subject`, and `text` or `html`, along with
provider credentials. Supported providers are `smtp`, `sendgrid`, `postmark`,
`mailgun`, `brevo`, `mailjet`, and `mailchimp-transactional` (also `mandrill`).
SMTP uses `host`, `port`, `username`, and `password`; SendGrid uses `api_key`.
Other providers require their own credential and domain fields. The
[report recipe](https://adios.dev/workflows/scheduled-reports#use-recipe) shows SendGrid setup.
A successful action confirms submission to the provider, not inbox delivery.

### s3 — Manage an object {#action-s3}

Set `command.operation` to `put`, `get`, `head` (or `stat`), or `delete`. Configure
`endpoint` as a hostname without a URL scheme, `region`, `use_ssl`, `access_key`,
`secret_key`, `bucket`, and `key`. For uploads, supply `body` and optionally
`content_type`. Use an existing bucket. The
[snapshot example](https://adios.dev/workflows#examples) writes JSON under a key containing the
run ID.

### wait — Pause for human approval {#action-wait}

A `wait` step creates a pending approval and pauses the run. Approval lets its
dependent steps continue. Rejection fails the step and stops the run; an
unanswered approval remains waiting. There are no command fields for timed
delays, reviewer assignment, or automatic expiry.

```yaml
- step_id: approve
  kind: wait
  dependencies: [draft]
```

Make the protected action depend on `approve`. See the
[approval recipe](https://adios.dev/workflows/approval-workflows#use-recipe) for the complete flow.

### agent — Run a configured AI agent {#action-agent}


An agent action requires a pinned `agent_binding_id`,
`agent_binding_revision_id`, `agent_binding_revision_digest`, and `workspace_id`
in `command`. The digest must be `sha256:` followed by 64 hexadecimal characters.
Use the exact values from your configured binding revision, then set `input` to
the task. The workflow waits for the agent to finish before continuing.


The output is the agent result envelope as JSON, including run information and
results; it is not just the draft text. Inspect it before selecting a field or
forwarding the whole result. The [approval recipe](https://adios.dev/workflows/approval-workflows)
shows all required fields.

## Dependencies and step outputs {#outputs}

List upstream step IDs in `dependencies` and place those steps earlier in the
manifest. A failed dependency prevents the downstream action from running. The
current runtime executes steps sequentially; listing independent steps does not
make them run in parallel.

Templates use Go template syntax. Useful values include:

- `{{ .context.destination_url }}` for shared configuration.
- `{{ .steps.report.output }}` for a step's raw output string, suitable for a JSON body.
- `{{ .steps.count.value }}` for its parsed value, suitable for inserting a scalar into text.
- `{{ index .steps "fetch-prices" "output" }}` for an ID containing a hyphen.
- `{{ .run.ID }}` for the current run ID.

Use `.output` to pass a complete JSON object as text. Rendering a parsed object
through `.value` does not JSON-encode it. For selection from arrays, use paths
such as `.rows[0].orders` in a `data-json` action.

## Secrets and environment variables {#secrets-and-environment-variables}

For HTTP, SQL, email, and S3 actions, put `secret://NAME` directly in the command
field that needs the value. The reference must occupy the whole field:
`X-API-Key: secret://API_TOKEN` resolves, but
`Authorization: "Bearer secret://API_TOKEN"` is sent literally. For bearer
authentication, store the complete `Bearer …` header value in a secret and use
`Authorization: secret://API_AUTHORIZATION`.

Bash and Python actions receive environment variables through the **step's
`env` block**. The worker resolves secret references before starting the script:

```yaml
steps:
  - step_id: fetch
    kind: python
    env:
      API_TOKEN: secret://API_TOKEN
      API_URL: https://api.example.com/data
    command: |
      import os
      import urllib.request

      request = urllib.request.Request(
          os.environ["API_URL"],
          headers={"Authorization": "Bearer " + os.environ["API_TOKEN"]},
      )
      with urllib.request.urlopen(request, timeout=30) as response:
          print(response.read().decode())
```

A top-level workflow `secrets` map is retained by the data model, but the current
runtime does not use it to populate step environments or resolve aliases. It is
not required for either pattern above. Step templates can read workflow context,
trigger payload, request data, and previous step outputs.

## Create and inspect a run {#create}

Create or update this manifest from the workflow builder, the AI agent, or the
workflow CLI:

```bash
adios workflow push "Daily market brief" ./workflows/daily-market-brief.yaml --create
adios workflow run "Daily market brief"
adios workflow runs --workflow "Daily market brief"
adios workflow logs "Daily market brief"
```

Leave out `--create` to update a workflow that already exists. Use
`adios workflow validate` to check a manifest before pushing it, and
`adios workflow run --local` for quick checks on your machine. The local runner
supports only a subset of platform step kinds.

Start with a manual run and sample inputs. Inspect each step's status, output,
and error in Workflows before connecting a live event source or recurring
schedule. For approvals, test both approval and rejection and verify that the
protected step stays pending until the decision.

Use `timeout_seconds` on HTTP, script, SQL, or agent steps when the default is
unsuitable. HTTP, script, and SQL steps default to 30 seconds; agent steps
default to 30 minutes. A wait step is governed by its approval state, not this timeout.
