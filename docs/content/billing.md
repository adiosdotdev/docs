# Billing and usage

Billing belongs to the active team. Open **Billing** in the dashboard to review
the team's current plan, subscription state, usage, and available funding options.
Your role determines which billing controls you can change.

## Check before starting work

Deployment, previews, commands, workflows, storage, and AI runs can consume
resources. Review the current plan and entitlements for the operation you need.
Use the prices and limits displayed in your account; the
[public pricing page](https://adios.dev/pricing) provides product pricing information.

An HTTP `402` indicates that an operation needs a subscription or resource
entitlement. Check the team's billing state and the error details before retrying.
Changing teams can also change the available balance and entitlements.

## AI funding and BYOK

Managed AI access uses the platform's available funding and model eligibility.
The billing UI can expose AI balance or token-pack options for your team. Review
their current terms, expiration, and remaining balance before purchase.

BYOK uses a supported provider connection configured for the team. Provider
charges depend on that account, and BYOK does not make deployment or other
platform infrastructure free. If a run cannot start, inspect both its routing
mode and the relevant funding or provider error.

The workspace's **Usage** view shows recorded usage for the conversation;
team billing covers the account's financial state. Estimates, incomplete run
records, and current billing totals may represent different stages of accounting.

## Control resource use

Review active previews, replicas, workflows, and stored artifacts after a test.
Use the appropriate stop or cleanup controls for resources you no longer need.
Confirm what remains stored and billable before deleting an application or
assuming that stopping a runtime removes its storage.

See [deployments](deployments.md), [AI agent usage](ai.md), and
[storage](storage.md) for the related resource lifecycle.
