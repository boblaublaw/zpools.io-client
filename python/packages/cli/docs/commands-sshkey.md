# SSH key commands

`zpcli sshkey` — Manage SSH public keys for your account. A registered SSH key is required for ZFS over SSH.

See also: [Configuration](../../../../docs/configuration.md#required-parameters) (e.g. `SSH_PRIVKEY_FILE`), [Authentication](../../../../docs/authentication.md#scopes), [Resource IDs](../../../../docs/reference/ids.md) (key IDs).

## Commands

- `zpcli sshkey list` — List SSH keys.
- `zpcli sshkey add [path or key]` — Add a public key
- `zpcli sshkey delete <pubkey_id>` — Delete an SSH key by ID.

---

## list

```text
zpcli sshkey list [--json]
```

Lists all SSH keys for the authenticated user.

**Output columns**

- **ID** — Key ID (same key content always gets the same ID).
- **Fingerprint (from key)** — SHA256 fingerprint for the key.
- **Comment (from key)** — Comment from the key (e.g. `user@host`).

---

## add

```text
zpcli sshkey add [PUBKEY]
zpcli sshkey add [--json]
```

Adds a public key. `PUBKEY` is optional: it can be a path to a `.pub` file or the raw public key string (e.g. pasted or quoted on the command line).

### Input resolution (path vs key)

The CLI does **not** guess from slashes or extensions. It uses a single order:

1. **Try as key** — If the input is a valid public key, it is used as the key content.
2. **Try as path** — If not, the input is treated as a file path (with `~` expanded). If the path is an existing file, its contents are read and validated as a key.
3. **Fail** — If the input is neither valid key content nor an existing file, the CLI reports: *Could not parse as public key and file not found: &lt;path&gt;*

So you can:

- **Paste a key** in the interactive prompt (full line, e.g. `ssh-ed25519 AAAA... comment`).
- **Paste or type a path** (e.g. `/home/you/.ssh/id_ed25519.pub` or `~/.ssh/mykey.pub`). If the file exists, it is read and used.
- **Pass as argument:** use a path, or a **quoted** full key line so the shell keeps it as one argument:  
  `zpcli sshkey add "ssh-ed25519 AAAA... comment"`

If you omit the argument and the session is **interactive**, the CLI prompts:

```text
Enter the path or public key to add [default_from_rcfile.pub]:
```

The default in brackets is `SSH_PRIVKEY_FILE` from your rcfile plus `.pub`. Press Enter to use that path, or type a different path or paste a key.

In a **non-interactive** session, omitting the argument is an error; you must pass a path or key.

### Validation

The CLI validates that the resolved content is a valid public key. Invalid content (e.g. a path that doesn’t exist, or text that isn’t a key) causes the CLI to report an error.

### Duplicate key

If the same key is already registered, the CLI reports that the key is already registered and shows the existing key ID. No duplicate is stored.

### Success output

On success, the CLI prints the new key ID and its fingerprint.

### Options

- `--json` — Emit raw JSON instead of the formatted messages above.

---

## delete

```text
zpcli sshkey delete <pubkey_id> [--json]
```

Deletes the SSH key with the given ID. Use `zpcli sshkey list` to see IDs.

In non-JSON mode, the CLI asks for confirmation unless you pass `--json`. Reports an error if the key is not found.

---

## Tab completion

Tab completion for `zpcli sshkey add` (e.g. completing files under `~/.ssh/` or path completion) is not implemented. Use the interactive prompt or type or paste the path or key.

---

## See also

- [Command reference](commands.md)
- [Resource IDs](../../../../docs/reference/ids.md) — Key IDs (pubkey_id) and the four-word hyphenated format
- [Configuration](../../../../docs/configuration.md#required-parameters) — `SSH_PRIVKEY_FILE`, rcfile
- [Authentication](../../../../docs/authentication.md#scopes) — JWT, PAT, scopes
