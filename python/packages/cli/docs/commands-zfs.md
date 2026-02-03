# ZFS over SSH commands

`zpcli zfs` — Run ZFS operations on your **remote** zpool over SSH: list datasets, create snapshots, destroy datasets or snapshots, receive ZFS streams (e.g. from a local `zfs send`), or open an SSH session to the remote host. These commands talk to the zpools.io SSH endpoint; they do not run ZFS on your local machine.

**Scope and permitted use:** The ZFS module is a **wrapper** intended to facilitate ZFS and zpool operations over SSH. Operations are **restricted**. The only expected, supported, and permitted use cases are: sending and receiving data (e.g. `zfs send` / `zfs recv`), listing datasets, and managing datasets (snapshots, destroy). Datasets **cannot be mounted** on the service; **contents cannot be examined** (e.g. no general file or directory access). Use the CLI only for these intended operations.

**Requirements:** ZFS over SSH uses your config (rcfile or environment). You need your username (**ZPOOL_USER**) and SSH private key path (**SSH_PRIVKEY_FILE**). Your SSH **public** key must be registered with the service (`zpcli sshkey add`). See [Configuration](../../../../docs/configuration.md) and [SSH keys](commands-sshkey.md).

**Asides:** In this document we use blockquote asides:

- **Note:** Clarifications or caveats.
- **Tip:** Optional guidance.
- **In development / TBD:** Features or integrations that are planned but not yet available in the CLI.

## Commands

- `zpcli zfs list <dataset>` — List ZFS datasets under the given dataset on the remote zpool. Options: `-r` / `--recursive`.
- `zpcli zfs snapshot <dataset@snapname>` — Create a snapshot on the remote.
- `zpcli zfs destroy <dataset>` — Destroy a dataset or snapshot on the remote. Options: `-r` / `--recursive`.
- `zpcli zfs recv <dataset>` — Receive a ZFS stream from stdin (e.g. pipe from local `zfs send`). Options: `-F` / `--force`.
- `zpcli zfs ssh [command...]` — Open an interactive SSH session to the remote host, or run the given command.

Destructive operations (e.g. `destroy`) are your responsibility; the CLI does not prompt for confirmation.

---

## list

```text
zpcli zfs list <dataset> [-r | --recursive]
```

Lists ZFS datasets under the given **dataset** on your remote zpool. The dataset is the **remote** path (e.g. your zpool ID or a path under it). Output is the same as running `zfs list` (and optionally `zfs list -r`) on the remote host.

**Argument**

- **dataset** — Remote dataset path. Use the **zpool ID** (from `zpcli zpool list`) as the root, e.g. `law-hotel-shape-community`, or a path under it, e.g. `law-hotel-shape-community/backups`. The dataset must exist on the remote.

**Options**

- `-r` / `--recursive` — List recursively: show the given dataset and all descendants. Without this, only direct children are shown (same as `zfs list` vs `zfs list -r`).

**Output**

The remote `zfs list` output is printed to stdout (name, used, avail, refer, mountpoint, etc.). If the dataset does not exist or you lack permission, the remote `zfs` command fails and the CLI exits with a non-zero code.

**Examples**

```text
# List top-level datasets under your zpool (replace with your zpool ID from zpcli zpool list)
zpcli zfs list law-hotel-shape-community

# List recursively to see all datasets under a path
zpcli zfs list law-hotel-shape-community/backups -r
zpcli zfs list law-hotel-shape-community --recursive
```

---

## snapshot

```text
zpcli zfs snapshot <dataset@snapname>
```

Creates a ZFS snapshot on the **remote** zpool. The snapshot name must be in the form **dataset@snapname** (e.g. `law-hotel-shape-community/data@nightly`).

**Argument**

- **dataset@snapname** — Full snapshot spec: the remote dataset path, then `@`, then the snapshot name. The dataset must exist on the remote. The snapshot name is any valid ZFS snapshot name (e.g. alphanumeric and hyphens; avoid spaces).

**Output**

On success, the remote `zfs snapshot` runs and the CLI exits with code 0. No output is printed unless the remote command produces it. On failure (e.g. dataset does not exist, or snapshot name invalid), the remote error is shown and the CLI exits with a non-zero code.

**Examples**

```text
# Snapshot a top-level dataset
zpcli zfs snapshot law-hotel-shape-community@before-update

# Snapshot a child dataset
zpcli zfs snapshot law-hotel-shape-community/backups@nightly-2025-01-15
```

---

## destroy

```text
zpcli zfs destroy <dataset> [-r | --recursive]
```

Destroys a ZFS **dataset** or **snapshot** on the **remote** zpool. This is **irreversible**; the CLI does **not** ask for confirmation. Use with care.

**Argument**

- **dataset** — Remote dataset or snapshot to destroy. For a snapshot, use the full form **dataset@snapname** (e.g. `law-hotel-shape-community/data@old`). For a dataset, use the dataset path (e.g. `law-hotel-shape-community/trash`). The target must exist on the remote.

**Options**

- `-r` / `--recursive` — Destroy recursively: destroy the given dataset and all descendants (or all snapshots in a hierarchy, depending on target). Required when the dataset has children; without it, `zfs destroy` on the remote will fail if there are dependents.

**Output**

On success, the remote `zfs destroy` runs and the CLI exits with code 0. On failure (e.g. dataset in use, or has children and `-r` not used), the remote error is shown and the CLI exits with a non-zero code.

> **Note:** Destroying a dataset that holds snapshots may require destroying snapshots first, or using recursive destroy. The behavior matches standard ZFS `zfs destroy` on the remote.

**Examples**

```text
# Destroy a single snapshot
zpcli zfs destroy law-hotel-shape-community/backups@nightly-old

# Destroy a dataset and all its children
zpcli zfs destroy law-hotel-shape-community/trash -r
zpcli zfs destroy law-hotel-shape-community/trash --recursive
```

---

## recv

```text
zpcli zfs recv <dataset> [-F | --force]
```

Receives a **ZFS stream** from **stdin** and writes it to the **remote** dataset. You typically pipe a stream from a **local** `zfs send` into this command so that data is sent from your machine to the remote zpool (ingress). This is the standard way to back up or replicate data to zpools.io.

**Argument**

- **dataset** — Remote **target** dataset that will hold the received stream. It can be an existing dataset (to be replaced or updated, depending on stream type and `-F`) or a new dataset path under your zpool. Use your zpool ID as the root (e.g. `law-hotel-shape-community` or `law-hotel-shape-community/backups/home`).

**Options**

- `-F` / `--force` — Force receive: rollback the target dataset to the most recent snapshot before applying the stream, if required. Use when you want to overwrite or resync and the remote dataset has diverged. Without `-F`, receive may fail if the target already has different data or snapshots.

**How it works**

1. You run `zfs send` locally (e.g. `sudo zfs send pool/ds@snap`).
2. You pipe that into `zpcli zfs recv <remote-dataset>`.
3. The CLI forwards stdin over SSH to the remote host, where `zfs recv` runs with the given options and target dataset.
4. Exit code is the remote `zfs recv` exit code (0 on success).

> **Tip:** For a full send, the target dataset usually should not exist, or you use `-F` to force. For incremental sends, the target must have the prior snapshot; see ZFS documentation for send/recv rules.

**Examples**

```text
# Full send from local to remote (replace local pool/dataset@snap and remote zpool ID)
sudo zfs send rpool/home@snap1 | zpcli zfs recv law-hotel-shape-community/backups/home

# Force receive (rollback target if needed)
sudo zfs send rpool/home@snap1 | zpcli zfs recv -F law-hotel-shape-community/backups/home
sudo zfs send rpool/home@snap1 | zpcli zfs recv --force law-hotel-shape-community/backups/home
```

---

## ssh

```text
zpcli zfs ssh [command...]
```

Opens an **SSH connection** to the zpools.io SSH host using the same config as the other ZFS commands (`SSH_HOST`, `SSH_PRIVKEY_FILE`, `ZPOOL_USER`). With **no arguments**, you get an **interactive** shell on the remote. With **arguments**, the CLI runs that command on the remote and exits with its exit code.

Use this when you need to run arbitrary commands on the remote (e.g. `zfs list -t filesystem`, `zfs get`, or other SSH-based workflows). For structured ZFS operations, prefer the dedicated commands (`zfs list`, `zfs snapshot`, etc.) so that options and behavior are consistent and documented.

**Arguments**

- **command...** — Optional. If present, the full list of arguments is passed through to the remote shell. So you can run e.g. `zpcli zfs ssh zfs list -t filesystem` or `zpcli zfs ssh zfs get all law-hotel-shape-community`. Flags and options are passed as-is (the CLI uses `ignore_unknown_options` and `allow_extra_args` so that `-t`, `-r`, etc. are not consumed by the CLI).

**Output**

- **Interactive (no command):** Your terminal is attached to the remote shell. Exit with `exit` or Ctrl+D.
- **With command:** The remote command’s stdout and stderr are printed; the CLI exits with the remote command’s exit code.

**Examples**

```text
# Interactive shell on the remote
zpcli zfs ssh

# Run a single command
zpcli zfs ssh zfs list

# Pass flags through to the remote zfs command
zpcli zfs ssh zfs list -t filesystem
zpcli zfs ssh zfs list -r law-hotel-shape-community
zpcli zfs ssh zfs get all law-hotel-shape-community
```

---

## See also

- [Command reference](commands.md)
- [Configuration](../../../../docs/configuration.md) — SSH_HOST, SSH_PRIVKEY_FILE, ZPOOL_USER, rcfile
- [SSH keys](commands-sshkey.md) — Register your public key for ZFS over SSH
- [Zpool commands](commands-zpool.md) — List zpools to get zpool IDs for use as dataset roots
