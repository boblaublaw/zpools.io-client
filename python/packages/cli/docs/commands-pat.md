# Personal Access Token commands

`zpcli pat` — Manage Personal Access Tokens (PATs) via the CLI.

For PAT concepts, scopes, and when to use PATs vs JWT, see [Authentication](../../../../docs/authentication.md#pat). PAT key IDs use the standard [Resource IDs](../../../../docs/reference/ids.md) format.

## Commands

| Command | Description |
|---------|-------------|
| `zpcli pat list` | List your PATs |
| `zpcli pat create <label>` | Create a new PAT (requires JWT auth) |
| `zpcli pat revoke <key_id>` | Revoke a PAT |

---

## list

```text
zpcli pat list [OPTIONS]
```

Lists all PATs for the authenticated user. The token secret is never shown after creation; only metadata is displayed.

**Output columns**

| Column | Description |
|--------|-------------|
| ID | Key ID (use with `pat revoke`). Four-word hyphenated format. |
| Label | Name you gave the token at creation. |
| Status | Current state (e.g. active, revoked). |
| Created At | Creation timestamp. |
| Expiry | Expiry date, or "Never". |
| Last Used | When the token was last used, or "Never". |
| Scopes | Comma-separated scopes (e.g. `zpool`, `job` or `*`). |

**Options**

| Option | Description |
|--------|-------------|
| `--json` | Output raw JSON instead of table. |
| `--local` | Show timestamps in local timezone (default: UTC). |

**Examples**

```text
zpcli pat list
zpcli pat list --local
zpcli pat list --json
```

---

## create

```text
zpcli pat create <label> [OPTIONS]
```

Creates a new PAT. Requires JWT authentication (username/password); PATs cannot create other PATs unless they have the `pat` scope.

The token value is printed **only once**—copy it immediately and store it securely (e.g. secret manager, CI variable). Do not commit PATs to version control.

**Argument**

| Argument | Description |
|----------|-------------|
| `label` | Human-readable name (e.g. `"GitHub Actions"`). Quote if it contains spaces. |

**Options**

| Option | Description |
|--------|-------------|
| `--scope <scope>` | Scope to grant. **Required.** Repeat for multiple scopes. See [Scopes](../../../../docs/authentication.md#scopes). |
| `--expiry <YYYY-MM-DD>` | Optional expiry date. Omit for no expiry. |
| `--tenant-id <id>` | Optional tenant ID (multi-tenant scenarios). |
| `--json` | Output raw JSON. |

**Examples**

```text
# Full access (quote * to prevent shell globbing)
zpcli pat create "My CI Token" --scope '*'

# Least privilege: only zpool and job access
zpcli pat create "CI zpool only" --scope zpool --scope job

# With expiry
zpcli pat create "Temp token" --scope sshkey --expiry 2025-12-31
```

**Output**

On success, the CLI prints the key ID and token value. Copy the token immediately.

```text
PAT created successfully!
ID: law-hotel-shape-community
Token: zpat_xxxxxxxxxxxxxxxxxxxxxxxx
Make sure to copy your token now. You won't be able to see it again!
```

---

## revoke

```text
zpcli pat revoke <key_id> [OPTIONS]
```

Revokes a PAT by key ID. Revocation is permanent and immediate.

**Argument**

| Argument | Description |
|----------|-------------|
| `key_id` | Key ID to revoke (e.g. `law-hotel-shape-community`). Get from `pat list`. |

**Options**

| Option | Description |
|--------|-------------|
| `--json` | Output raw JSON and skip confirmation prompt. |

**Confirmation**

Without `--json`, the CLI prompts for confirmation before revoking.

**Examples**

```text
zpcli pat revoke law-hotel-shape-community
zpcli pat revoke law-hotel-shape-community --json
```

---

## See also

- [Authentication](../../../../docs/authentication.md#pat) — PAT concepts, scopes, JWT vs PAT
- [Command reference](commands.md)
- [Resource IDs](../../../../docs/reference/ids.md) — Key ID format
