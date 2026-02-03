# Authentication

The zpools.io client supports two authentication mechanisms: **JWT** (short-lived, interactive) and **PAT** (Personal Access Token, long-lived, for automation). Both CLI and SDK use the same concepts.

## JWT (interactive)

- You sign in with **username and password** (prompted or from env/rcfile).
- The client receives a short-lived **JWT** and uses it for API calls.
- Password is not read from the rcfile. Store `ZPOOL_USER` in the rcfile if you like; the client will prompt for password when needed. The account password is not appropriate for scripts or automation—it has access to billing and other non-operational mechanisms. For automation, use a PAT scoped with least privilege.

### JWT caching

- By default, JWT tokens are **not cached** (most secure). The client will prompt for password on each session.
- To enable caching, set `ZPOOL_TOKEN_CACHE_DIR` in the rcfile or environment (e.g. `/dev/shm/zpools.io` for ephemeral RAM-backed cache). Cached tokens are stored with restricted permissions and cleared on reboot.
- To explicitly disable caching, set `ZPOOL_TOKEN_CACHE_DIR=` (empty value) in the rcfile.
- For long-running sessions, the client may refresh the token; see the [CLI command reference](../python/packages/cli/docs/commands.md) and [SDK API reference](../python/packages/sdk/docs/api-reference.md) for details.

## PAT

PATs (Personal Access Tokens) are long-lived tokens you create from your account. Use them for **non-interactive** use: CI/CD, scripts, automation. Unlike the account password, PATs can be scoped to only the access needed (least privilege) and do not expose billing and other non-operational mechanisms unless you grant those scopes. Store the PAT in the environment (e.g. `ZPOOLPAT`) or pass it explicitly to the client. Do not commit PATs to version control. PATs can be scoped and revoked.

### Scopes

When creating a PAT you must specify at least one scope or use `*` to grant all scopes. If you omit scopes (or pass an empty list), the PAT is created with no scopes and the server returns **403 Forbidden** for every request.

| Scope     | Purpose |
|----------|---------|
| `*`      | All features (full access). Same access as your user account. |
| `zpool`  | List, create, delete, modify, scrub zpools. |
| `job`    | List jobs, get job details, get job history. |
| `sshkey` | List, add, delete SSH keys. |
| `pat`    | List and create PATs; revoke PATs (use with care). |
| `billing`| Billing balance, ledger, summary, claim code. |

**Scope strategies:**

- **Full access:** Use `*` when you need unrestricted access.
- **Least privilege:** Grant only the scopes needed (e.g. `zpool` + `job` for CI that manages pools).
- **Short-lived:** Combine limited scopes with an expiry date for temporary automation.

### Using a PAT

Set `ZPOOLPAT` in your environment (or pass it explicitly). No password or JWT is needed when a valid PAT is present.

```bash
export ZPOOLPAT="zpat_xxxxxxxxxxxxxxxxxxxxxxxx"
zpcli hello  # Confirms the PAT works
```

### Managing PATs

You must be logged in with username/password (JWT) to create or revoke PATs.

- **CLI:** See [`zpcli pat` commands](../python/packages/cli/docs/commands-pat.md) for full syntax and options.
- **SDK:** See [API reference](../python/packages/sdk/docs/api-reference.md#pats) for programmatic PAT management.

## rcfile and environment

The CLI and SDK read configuration from an rcfile and/or from environment variables. Password is only from the `ZPOOL_PASSWORD` environment variable (not from the rcfile). For rcfile path, configuration keys (e.g. `ZPOOL_USER`, `ZPOOLPAT`), and how environment overrides rcfile, see [Configuration](configuration.md).

## See also

- [Configuration](configuration.md) — rcfile path and keys.
- [Troubleshooting](troubleshooting.md#authentication-failures) — Auth failures, non-interactive PAT.
- CLI: auth behavior in [command reference](../python/packages/cli/docs/commands.md) and [troubleshooting](../python/packages/cli/docs/troubleshooting.md).
- SDK: auth in [quickstart](../python/packages/sdk/docs/quickstart.md) and [API reference](../python/packages/sdk/docs/api-reference.md).
