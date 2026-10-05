# Installation

Install the Adios CLI to manage your apps from the terminal.

On macOS or Linux, install the checksummed release for Intel or ARM with Homebrew:

```bash
brew install adiosdotdev/tap/adios
```

Upgrade later with `brew upgrade adiosdotdev/tap/adios`.

Alternatively, use the standalone installer:

```bash
curl -fsSL https://adios.dev/install.sh | sh
```

The installer downloads the latest Adios CLI release from
https://github.com/adiosdotdev/cli/releases/latest.

## Verify and authenticate

```sh
adios version
adios login
adios teams
adios teams switch YOUR_TEAM_ID
```

`adios login` opens the secure browser-based OAuth flow. Choose the account
and team you intend to use. The CLI and dashboard maintain their own active
team selection. Use `adios login --context work --environment production`
when keeping a named profile for this account.

Run `adios --help` or `adios COMMAND --help` to inspect the flags supported by
your installed release. Start with the [deployment quickstart](quickstart.md)
or [first API requests](api/quickstart.md).
