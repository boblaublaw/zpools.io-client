# Bash Prototype CLI — zpools.io-client

## Status
This Bash CLI is an early prototype for interacting with the zpools.io API and SSH-based ZFS operations.
It’s functional for basic workflows but subject to breaking changes during the private beta phase.

For more about the zpools.io service, visit https://zpools.io.
For questions, join the community Discord: https://discord.gg/q8C6zJYQ.

---

## Requirements
Tested on:
- Bash 5.2.21
- curl 8.9.1
- ZFS 2.2.2
- Miller (mlr) 6.11.0

Likely to work on a wide range of Unix-like systems.

Optional but useful tools:
- mlr (Miller) for table formatting
- jq for JSON post-processing
- pbcopy, xclip, xsel, or clip.exe for clipboard operations
- less or more for pager display

---

## Installation
1. Clone the client repository:

   git clone https://github.com/boblaublaw/zpools.io-client
   cd zpools.io-client/bash

2. Ensure the main CLI script is executable:

   chmod +x zpoolcli.sh

3. Create a configuration file at:

   ~/.config/zpools.io/zpoolrc

   Example content:
```
ZPOOLUSER="your_username_here"
SSH_PRIVKEY_FILE="/home/you/.ssh/id_ed25519"
API_DOMAIN="https://api.zpools.io/v1"
SSH_HOST="ssh.zpools.io"
BZFS_BIN="/home/you/bin/bzfs"
LOCAL_POOL="rpool/USERDATA/you_xxxxxx"
REMOTE_POOL="you@ssh.zpools.io:your-remote-zpool-id/your-remote-dataset"
```

4. Run the CLI:

   ./zpoolcli.sh --help

---

## Command Overview
The CLI organizes commands by feature group:

- Codes
  - claim <code>        (JWT)

- Billing
  - billing balance     (JWT)
  - billing ledger      (JWT)
  - billing start       (JWT)

- Personal Access Tokens (TBD docs)
  - pat list | create | revoke

- SSH Keys
  - sshkey list | add | delete     (JWT / PAT)

- Jobs
  - job list | show | history      (JWT / PAT)

- Zpools
  - zpool list | create | delete | scrub | modify   (JWT / PAT)

- ZFS (over SSH)
  - zfs list | destroy | snapshot | recv | ssh | bzfs   (SSH)

Run any group without arguments for detailed help:
- ./zpoolcli.sh billing
- ./zpoolcli.sh zpool
- ./zpoolcli.sh zfs

---

## Token Behavior
- The CLI prompts for your zpools.io username and password when needed.
- Tokens are cached securely in a temporary location for short reuse windows (e.g., /dev/shm).
- Long-lived Personal Access Tokens (PATs) are TBD and will be documented later.

---

## SSH / ZFS Operations
The zfs and bzfs command groups communicate with zpools.io’s SSH endpoints.
Ensure that:
- SSH_PRIVKEY_FILE points to a valid private key
- SSH_HOST is set correctly in your rcfile
- Your user has ZFS privileges on the target host

Destructive ZFS operations such as destroy are your responsibility.
Use with caution.

---

## Output Processing
The CLI emits JSON to stdout.
Use tools like jq or mlr to transform output into tables or filtered reports.

Examples:

List jobs in table form:
./zpoolcli.sh job list | jq '.detail.jobs' | mlr --ijson --opprint cut -o -f created_at,job_id,job_type

Show job history:
./zpoolcli.sh job history ${job_id} | jq '.detail.history' | mlr --ijson --opprint cut -o -f timestamp,event_type,message

---

## Troubleshooting
- If you see “Authentication failed”, ensure your username and password are correct.
- If API_DOMAIN or SSH_HOST are missing, set them in your rcfile.
- If you run non-interactively, Personal Access Tokens (PAT) are recommended. (Docs TBD)
- For SSH issues, verify that your private key file exists and has proper permissions.
- Running `bash -x ./zpoolcli.sh ...` will show underlying operations.

---

## Next Steps
- QUICKSTART.md will provide copy-paste setup and example workflows.
- llm.txt will contain a complete internal reference for API, CLI, and SDK design.
- PAT and bzfs documentation coming soon.

---

## Support
For questions, early access, and updates:
Discord: https://discord.gg/q8C6zJYQ

