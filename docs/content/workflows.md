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
as JSON. The schedule repeats every 24 hours. Remove `triggers` for a manual-only
test before enabling recurring delivery.

## Triggers and scheduling {#triggers}

- **Manual:** omit `triggers` and start a run from Workflows.
- **Webhook:** use `type: webhook` and an event name, such as `order.created`.
  The incoming event payload is available as `.payload`.
- **Event:** use `type: event` and the internal event name to match.
- **Interval:** use `type: schedule` with a positive duration such as
  `interval: 1h` or `interval: 24h`.
- **Cron:** the current scheduler supports `@every 1h`, `* * * * *`, and minute
  intervals such as `*/5 * * * *`. It does not evaluate general calendar cron
  expressions such as `0 8 * * *`.

Intervals measure elapsed time; they are not aligned to a wall-clock time. A
newly observed schedule can run on the next scheduler check, and restarting the
scheduler resets its in-memory interval tracking. Although `timezone` and
`concurrency` are accepted manifest fields, the current scheduler does not apply
them. Do not rely on `concurrency: forbid` to prevent overlapping runs.

For a fixed local time, use an external scheduler to send a webhook. If a repeat
could send duplicate reports or writes, implement deduplication in your
application or destination.

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

Create or apply this manifest from the workflow builder, the AI agent, or the
workflow CLI. The local CLI runner is useful for simple development checks, but
it supports a subset of platform step kinds.

```bash
adios workflow deploy ./workflows/daily-market-brief.yaml
```

Start with a manual run and sample inputs. Inspect each step's status, output,
and error in Workflows before connecting a live event source or recurring
schedule. For approvals, test both approval and rejection and verify that the
protected step stays pending until the decision.

Use `timeout_seconds` on HTTP, script, SQL, or agent steps when the default is
unsuitable. HTTP, script, and SQL steps default to 30 seconds; agent steps
default to 30 minutes. A wait step is governed by its approval state, not this timeout.
