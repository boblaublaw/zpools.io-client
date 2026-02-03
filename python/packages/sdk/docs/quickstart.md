# SDK Quickstart

Minimal code to list zpools, create a zpool, and check job status. Copy-paste and replace credentials.

## Authenticate

Use username/password (JWT) or a Personal Access Token (PAT). See [Authentication](../../../../docs/authentication.md).

```python
from zpools import ZPoolsClient

# Option A: Username and password (interactive or from env)
client = ZPoolsClient(
    username="your-username",
    password="your-password"
)

# Option B: PAT (recommended for scripts / non-interactive)
client = ZPoolsClient(pat="your-personal-access-token")
```

The client also reads from `~/.config/zpools.io/zpoolrc` and environment variables (`ZPOOL_USER`, `ZPOOL_PASSWORD`, `ZPOOLPAT`, `ZPOOL_API_URL`). See [Configuration](../../../../docs/configuration.md).

## List zpools

```python
response = client.list_zpools()
if response.status_code == 200:
    for zpool in response.parsed.detail.zpools.values():
        print(f"Pool: {zpool.name}, Size: {zpool.size_gib} GiB")
```

## Create a zpool

Create is **async**: the API returns a job ID. Sizes are in **GiB**. See [Storage units](../../../../docs/reference/storage-units.md) and [Async jobs](../../../../docs/reference/async-jobs.md).

```python
response = client.create_zpool(size_gib=125, volume_type="gp3")
if response.status_code == 202:
    job_id = response.parsed.detail.job_id
    print(f"Job ID: {job_id}")
```

## Get job status

Poll until the job completes or fails:

```python
job_response = client.get_job(job_id=job_id)
if job_response.status_code == 200:
    state = job_response.parsed.detail.state
    print(f"State: {state}")
```

Use a loop or a helper (e.g. `JobPoller` in `zpools.helpers`) to wait for completion. See [API reference](api-reference.md) and [Async jobs](../../../../docs/reference/async-jobs.md).

## Full example

```python
from zpools import ZPoolsClient

client = ZPoolsClient(pat="your-pat")  # or username=..., password=...

# List existing zpools
zpools = client.list_zpools()
print(zpools.parsed)

# Create a new zpool (async)
create = client.create_zpool(size_gib=125, volume_type="gp3")
if create.status_code == 202:
    job_id = create.parsed.detail.job_id
    print(f"Created job: {job_id}")
    # Poll job status
    job = client.get_job(job_id=job_id)
    print(f"Job state: {job.parsed.detail.state}")
```

## See also

- [Configuration](../../../../docs/configuration.md) | [Authentication](../../../../docs/authentication.md)
- [API reference](api-reference.md) | [Troubleshooting](troubleshooting.md)
