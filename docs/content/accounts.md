# Accounts and teams

Adios keeps applications, workspaces, secrets, storage, and billing in a team.
Select the right team before creating a resource or running a deployment.

## Sign in and choose a team

1. Open the [Adios dashboard](https://app.adios.dev) and sign in or create an account.
2. Use the team selector in the top bar to choose your team.
3. Open **Teams** to review your teams, settings, and membership.
4. Open an application or workspace in that team to start working.

The browser and CLI each keep their own active team. Switching teams in the
dashboard does not change the team selected in your local CLI:

```sh
adios login
adios teams
adios teams switch YOUR_TEAM_ID
```

Use the team ID returned by `adios teams`. See [installation](installation.md)
if you haven't installed the CLI yet.

## Invite a teammate

Open the team's **Members** page, choose **Invite member**, enter the person's
email address, and select the role offered by your account. Invitations support
**Team admin**, **Manager**, and **User**; your permissions determine which roles
you can assign. The recipient accepts the invitation through the invitation link.

The members page shows existing members and pending invitations. Review the
email address and role before sending, and remove access when someone leaves
the team. Adios does not disclose whether an invited email already has an account.

## Understand permissions

An active team selects the context for a request; it does not grant extra
permissions. Your membership, role, and the resource's access rules still apply.
Some settings and billing actions require elevated permissions. If a control
is unavailable, ask a team administrator to review your access.

REST requests identify the active team with `X-Tenant-ID`. A diagnostic token is
bound to one team, so changing that header cannot switch the token to another
team. See [API authentication](api/authentication.md) for the supported token flow.

## Next steps

- [Deploy your first app](quickstart.md).
- [Use an AI workspace](workspaces.md).
- [Review billing and usage](billing.md).
