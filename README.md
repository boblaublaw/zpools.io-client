# zpools.io-client

## Overview
This is the open-source client repository for **zpools.io** — home-use ZFS storage with durable offsite replication. For service details, pricing, and sign-up, visit https://zpools.io.
This repo currently ships a Bash prototype CLI and will grow to include SDKs and additional tooling over time.

## Status
- **Service:** private beta — early features and limited access.
- **Repo:** brand new — expect frequent changes as we stabilize the interface.
- **Community:** join our Discord for updates, questions, and beta access: https://discord.gg/q8C6zJYQ

## Languages & Layout
- **Languages supported:**
  - **Bash** (prototype)
  - **Python** (SDK & CLI)
- **Top-level structure:**
  - `bash/` — prototype CLI
    - Entry point: `bash/zpoolcli.sh` (the CLI you’ll run)
  - `python/` — Python Workspace
    - `packages/sdk` — Official Python SDK
    - `packages/cli` — Official Python CLI (`zpools`)
  - `spec/` — OpenAPI Specification
  - (Future) `docs/` — additional docs such as QUICKSTART.md, llm.txt (TBD)

---

## Authentication (high-level)
- **Bash:** Prompts for username/password, caches JWT in `/dev/shm`.
- **Python:** Supports `~/.config/zpools.io/zpoolrc`, env vars, and interactive prompts. Caches tokens similarly to Bash.
- **PATs:** Supported in both tools for CI/CD use.
- This README does **not** document the REST API; the CLI handles the necessary requests and responses for you.

---

## Common rcfile details
The CLI reads configuration from an rcfile to avoid repeatedly passing flags and environment variables.

- **Default path:** `~/.config/zpools.io/zpoolrc`
- **Set the following keys (example values shown):**
```bash
ZPOOLUSER="your zpools.io username"
SSH_PRIVKEY_FILE="/path/to/your/private/key"
API_DOMAIN="https://api.zpools.io/v1"
SSH_HOST="ssh.zpools.io"

# Optional (BzFS sync integration):
BZFS_BIN="/absolute/path/to/bzfs"
LOCAL_POOL="your/local/zpool/dataset"
REMOTE_POOL="user@ssh.zpools.io:remote-zpool-id/remote-dataset"
```
- **Notes:**
  - Store **usernames** here if you like; **do not** store passwords. The CLI will prompt as needed and cache a short-lived token.
  - The CLI also supports `--rcfile <path>` if you prefer a non-default config location.
  - If you’re using ZFS over SSH features, ensure `SSH_PRIVKEY_FILE` points to a valid private key and that your user has appropriate access on `ssh.zpools.io`.

---

## What’s in the Bash CLI (prototype)
The CLI groups commands into functional areas. Full usage and flags are shown by the CLI itself (`--help`) and will be expanded in `bash/README.md` (coming soon).

- **Identity & Codes**
  - `claim <code>`
  - claim codes for your account (joining the beta, adding features, claiming account credits)
- **Billing**
  - `billing balance | ledger | start`
  - high-level billing flows (auth-prompted)
- **Personal Access Tokens** (TBD docs)
  - `pat ...`
  - create/list/revoke long-lived tokens (docs pending)
- **SSH Keys**
  - `sshkey ...`
  - manage public keys associated with your account
  - a public key is required for all the ZFS operations
- **Jobs**
  - `job ...`
  - inspect asynchronous operations (list/show/history)
- **Zpools**
  - `zpool ...`
  - view and manage zpools
- **ZFS over SSH**
  - `zfs ...`
  - for ZFS operations on zpools.io SSH endpoints

For all operations, destructive commands are your responsibility.

---

## Requirements (high-level)
- A POSIX-like environment with:
  - `bash`, `curl`, and the `zpool` / `zfs` commands available
- Optional, recommended tools for working with JSON/tabular output:
  - `jq` and `mlr (Miller)`
- Tested versions (informational, not strict minimums):
  - Bash 5.2.21, curl 8.9.1, ZFS 2.2.2, mlr 6.11.0
  (Likely works across a broad range of versions and platforms; primary testing is on Ubuntu.)

> Detailed install and environment guidance will live in `bash/README.md` (prototype) and `QUICKSTART.md`.

---

## Installing & Using (high-level)
1) Clone this repo: `git clone https://github.com/<your-org-or-user>/zpools.io-client`
2) Navigate to the Bash prototype: `cd zpools.io-client/bash`
3) Create your `~/.config/zpools.io/zpoolrc` with the keys outlined above.
4) Run the CLI: `./zpoolcli.sh --help` (or invoke command groups directly)

> A step-by-step **QUICKSTART.md** will follow, containing copy-paste setup and common workflows.

---

## Roadmap & Documentation Index
- `bash/README.md` — CLI prototype usage, requirements, and install guidance (coming soon)
- `QUICKSTART.md` — concise, copy-paste onboarding guide (coming soon)
- `llm.txt` — deep technical reference for RAG / power-user queries (coming soon)
- bzfs (replication helper) documentation — TBD

---

## Support
- Questions, feedback, or beta access: **Discord** → https://discord.gg/q8C6zJYQ

## Contributing
- PRs and issues are welcome once the CLI stabilizes. For now, please use Discord to coordinate changes and avoid duplicating early work.
