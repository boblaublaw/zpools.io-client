# API reference

Main operations exposed by `ZPoolsClient`. The SDK is generated from the OpenAPI spec; for full request/response shapes see the [spec](../../../../spec/README.md) or the generated types in `zpools._generated`.

Configuration and auth: [Configuration](../../../../docs/configuration.md), [Authentication](../../../../docs/authentication.md). Storage units: [Storage units](../../../../docs/reference/storage-units.md). Async jobs: [Async jobs](../../../../docs/reference/async-jobs.md).

## Client constructor

```python
ZPoolsClient(
    api_url="https://api.zpools.io/v1",
    username=None,
    password=None,
    pat=None,
    ssh_host=None,
    ssh_privkey=None,
    token_cache_dir=None
)
```

- **api_url** — API base URL.
- **username** / **password** — JWT auth.
- **pat** — Personal Access Token (alternative to JWT).
- **ssh_host** / **ssh_privkey** — For ZFS-over-SSH helpers (optional).
- **token_cache_dir** — Base directory for JWT token cache (default: no cache). Optional.

The CLI layer typically loads rcfile and env and passes these into the client.

## Zpools

- **list_zpools()** — List all zpools. Returns response with parsed list.
- **create_zpool(size_gib=125, volume_type="gp3")** — Create a zpool (async). Returns 202 with job_id (and zpool_id when available).
- **delete_zpool(zpool_id)** — Delete a zpool (sync).
- **modify_zpool(zpool_id, target_volume_type)** — Change EBS volume type (e.g. gp3 ↔ sc1). Returns 202.
- **scrub_zpool(zpool_id)** — Start scrub (async). Returns 202 with job_id.

Sizes in GiB. See [Storage units](../../../../docs/reference/storage-units.md) and [Async jobs](../../../../docs/reference/async-jobs.md).

## Jobs

- **get_job(job_id)** — Get job status. Returns state and details.
- **list_jobs(limit=None, before=None, after=None, sort=None)** — List jobs with optional filters.
- **get_job_history(job_id)** — Get job history entries.

## SSH keys

- **list_sshkeys()** — List SSH keys for your account.
- **add_sshkey(public_key)** — Add a public key (string).
- **delete_sshkey(pubkey_id)** — Delete an SSH key by ID.

## PATs

- **list_pats()** — List PATs.
- **create_pat(label, scopes=None, expiry=None, tenant_id=None)** — Create a PAT (requires JWT first).
- **revoke_pat(key_id)** — Revoke a PAT.

## Billing

- **get_billing_balance()** — Get account balance.
- **get_billing_ledger(since=None, until=None, limit=None)** — Get ledger entries (date filters in YYYY-MM-DD).
- **get_billing_summary(since=None, until=None)** — Get aggregated billing summary.

## ZFS operations (over SSH)

Requires **ssh_host** and **ssh_privkey** (and account SSH key registered). See [Configuration](../../../../docs/configuration.md#required-parameters).

- **ssh_exec(command, stdin_data=None, ssh_key_file=None)** — Run a command over SSH. Returns (exit_code, stdout, stderr).
- **zfs_send_to_remote(local_snapshot, remote_dataset, ...)** — Send a local ZFS stream to remote.
- **zfs_recv_from_remote(remote_snapshot, local_dataset, ...)** — Receive a ZFS stream from remote.

## Raw client

- **get_authenticated_client()** — Return the low-level generated client with auth headers set. Use for operations not wrapped by `ZPoolsClient`.

## Errors

The generated client can raise `UnexpectedStatus` for non-2xx responses. See [Troubleshooting](troubleshooting.md).

## See also

- [Quickstart](quickstart.md) | [Installation](installation.md) | [Troubleshooting](troubleshooting.md)
- Top-level [docs](../../../../docs/README.md) (configuration, authentication, reference)
