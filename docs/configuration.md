# Configuration

The zpools.io client (CLI and SDK) reads configuration from an **rcfile** and from **environment variables**. The same keys apply to both tools.

## rcfile path

- **Default:** `~/.config/zpools.io/zpoolrc`
- **CLI:** You can override with `--rcfile <path>`.
- **SDK:** Use the same path by default; override by passing explicit arguments when creating the client (see [SDK API reference](../python/packages/sdk/docs/api-reference.md)).

## Required parameters

| Key                | Purpose                                                                |
| ------------------ | ---------------------------------------------------------------------- |
| `ZPOOL_USER`       | Your zpools.io username. (Required for authenticated HTTPS API access) |
| `SSH_PRIVKEY_FILE` | Path to your SSH private key file. (Required for SSH access)           |

## Optional overrides

| Key | Purpose |
|-----|---------|
| `ZPOOL_API_URL` | API base URL. Default: `https://api.zpools.io/v1`. |
| `SSH_HOST` | SSH endpoint for ZFS over SSH. Default: `ssh.zpools.io`. |
| `ZPOOL_TOKEN_CACHE_DIR` | Base directory for JWT token cache. Not set by default (no cache; most secure). Set explicitly to enable JWT token caching (e.g. `/dev/shm/zpools.io` for ephemeral RAM-backed cache). |

## BZFS parameters (optional)

| Key | Purpose |
|-----|---------|
| `BZFS_BIN` | Absolute path to `bzfs` for BzFS sync integration. |
| `LOCAL_POOL` | Local zpool/dataset for BzFS. |
| `REMOTE_POOL` | Remote target (e.g. `user@ssh.zpools.io:remote-zpool-id/remote-dataset`). |

**Password:** Password cannot be configured in the rcfile; the client does not read it from the rcfile. To supply a password use the `ZPOOL_PASSWORD` environment variable or an interactive prompt. The account password is not appropriate for scripts or other automation: it has access to billing and other non-operational mechanisms. For automation, use a [Personal Access Token](authentication.md#pat) (e.g. `ZPOOLPAT` env or client argument), scoped according to the principle of least privilege.

## Environment overrides

Environment variables override rcfile values. Commonly used:

- `ZPOOL_USER` — Username
- `ZPOOL_PASSWORD` — Password (JWT auth; env only, not read from rcfile)
- `ZPOOLPAT` — Personal Access Token (preferred for automation and non-interactive use)
- `ZPOOL_API_URL` — API endpoint

CLI and SDK both respect these. See [Authentication](authentication.md#using-a-pat) for how JWT and PAT are used.

## Example rcfile

```bash
ZPOOL_USER="your zpools.io username"
SSH_PRIVKEY_FILE="/path/to/your/private/key"

# Optional overrides (defaults in effect if omitted):
# ZPOOL_API_URL="https://api.zpools.io/v1"
# SSH_HOST="ssh.zpools.io"
# ZPOOL_TOKEN_CACHE_DIR=path/to/cache/dir  (optional; unset = no cache)

# Optional (BzFS sync):
# BZFS_BIN="/absolute/path/to/bzfs"
# LOCAL_POOL="your/local/zpool/dataset"
# REMOTE_POOL="user@ssh.zpools.io:remote-zpool-id/remote-dataset"
```

## See also

- [Authentication](authentication.md) — JWT vs PAT, token caching.
- [Quickstart](quickstart.md) — First zpool flow.
- CLI: [installation](../python/packages/cli/docs/installation.md) and config usage.
- SDK: [installation](../python/packages/sdk/docs/installation.md) and client options.
