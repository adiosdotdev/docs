# Private Git Dependencies

Use a build-only SSH deploy key when your application depends on code from a
private Git repository. This guide uses a private Go module on Bitbucket, but
the same `build.ssh` flow works with GitHub and GitLab.

If a build stops with an error like this, the dependency is private but the
build has no non-interactive credential:

```text
fatal: could not read Username for 'https://bitbucket.org': terminal prompts disabled
```

Do not put a password, access token, or private key in `adios.yaml`, `go.mod`,
or the repository URL. Give the repository a public deploy key, store the
private half in Adios, and reference its secret name from the manifest.

## 1. Create a Dedicated Deploy Key

Generate a new key for builds rather than uploading your personal SSH key:

```bash
ssh-keygen -t ed25519 \
  -C "adios-build" \
  -f ~/.ssh/adios-build \
  -N ""
```

This creates two files:

- `~/.ssh/adios-build.pub` is the public key. Add this to your Git provider.
- `~/.ssh/adios-build` is the private key. Store this in Adios and never commit
  it.

The key has no interactive passphrase because an automated build cannot answer
a passphrase prompt. Keep it dedicated, read-only, and limited to the source
repositories the build needs.

## 2. Give the Public Key Repository Access

Display the public key:

```bash
cat ~/.ssh/adios-build.pub
```

Add the complete line as a read-only repository access key or deploy key:

- **Bitbucket:** add it to the private repository's access keys.
- **GitHub:** add it as a read-only deploy key.
- **GitLab:** add it as a deploy key without write access.

For several private repositories, authorize the key everywhere it needs read
access or use a provider-supported machine account with the smallest practical
scope. Never paste the private file into the Git provider.

## 3. Store the Private Key in Adios

Make sure the CLI is using the team that owns the application, then upload the
private file:

```bash
adios teams switch <team-id>
adios secrets set BITBUCKET_DEPLOY_KEY \
  --from-file ~/.ssh/adios-build
```

You can target a team explicitly instead:

```bash
adios secrets set BITBUCKET_DEPLOY_KEY \
  --from-file ~/.ssh/adios-build \
  --team <team-id>
```

Confirm the secret name exists without revealing its value:

```bash
adios secrets list
```

`BITBUCKET_DEPLOY_KEY` is only an example name. You may choose another name,
but the name after `secret://` in `adios.yaml` must match it exactly.

## 4. Configure `adios.yaml`

For a private Go module hosted under a Bitbucket workspace:

```yaml
build:
  ssh:
    - default=secret://BITBUCKET_DEPLOY_KEY
  env:
    GOPRIVATE: "bitbucket.org/your-workspace/*"

build_cmd: |-
  set -e
  go build -o app ./cmd/api
```

`build.ssh` makes the key available only to the build. Adios resolves the
secret inside the worker and removes the temporary private-key file when the
build finishes. For native `build_cmd` builds, the worker also prepares SSH for
the supported Git hosts. The key is not added to the running application's
environment or filesystem. Docker builds must consume the SSH mount as shown
below.

`GOPRIVATE` tells Go which module paths must bypass the public module proxy and
checksum database. Match it to the module import path, not the repository's
display name:

| Git host | Example Go pattern |
| --- | --- |
| Bitbucket | `bitbucket.org/my-workspace/*` |
| GitHub | `github.com/my-organization/*` |
| GitLab | `gitlab.com/my-group/*` |

You do not need to change an existing HTTPS module import to include a username
or credential. For supported hosts, the Adios build worker uses SSH while the
repository keeps its normal canonical import path.

## 5. Deploy and Verify

Run the deployment again:

```bash
adios up
```

A successful dependency download proves both halves are connected: the
manifest found the private key in the correct Adios team, and the Git provider
accepted its public key for the requested repository.

After the first successful build, remove any temporary key copies you no longer
need from shared machines. Keep the public key registered for future builds and
rotate the pair when repository access changes.

## Docker Builds

For a Docker build, `build.ssh` enables the BuildKit SSH mount, but the
Dockerfile must use that mount on commands that fetch private source:

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25 AS build

ARG GOPRIVATE
ENV GOPRIVATE=$GOPRIVATE

WORKDIR /src
COPY go.mod go.sum ./

RUN mkdir -p -m 0700 /root/.ssh \
    && ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts \
    && git config --global \
      url."ssh://git@bitbucket.org/".insteadOf \
      "https://bitbucket.org/"

RUN --mount=type=ssh go mod download
```

Keep the matching manifest configuration under `build.ssh` and `build.env`.
Do not use `COPY` or a build argument to place the private key inside the image.

## Troubleshooting

### `terminal prompts disabled`

Check that `build.ssh` is present, the secret name matches exactly, and the
secret belongs to the application's active team. For Docker builds, also check
that the dependency command uses `RUN --mount=type=ssh`.

### `Permission denied (publickey)`

The private key was loaded, but the Git provider did not accept it. Confirm
that you registered the matching `.pub` file on the correct repository and
that the key still has read access.

### Go still contacts `proxy.golang.org` or the checksum database

Correct the `GOPRIVATE` pattern so it covers the full private module import
path. For multiple namespaces, separate patterns with commas.

### `invalid format` or `error in libcrypto`

The stored value must be the private key file, not the `.pub` file, a
fingerprint, or copied terminal formatting. Upload it again with `--from-file`
to preserve the key exactly.

### `repository not found`

Verify the module path and repository name first. If both are correct, the
deploy key may be attached to a different repository or lack access to one of
the transitive private dependencies.
