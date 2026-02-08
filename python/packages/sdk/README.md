# zpools-sdk

The official Python SDK for zpools.io — home-use ZFS storage with durable offsite replication. Use `ZPoolsClient` for zpools, jobs, SSH keys, PATs, billing, and ZFS-over-SSH operations.

## Installation

The SDK is not yet on PyPI. Install from the repo:

```bash
cd python
uv pip install -e packages/sdk
```

Or with pip: `pip install -e packages/sdk` (from the `python` directory). See [Installation](docs/installation.md) for details and Python version.

## Quick start

```python
from zpools import ZPoolsClient

client = ZPoolsClient(username="your-username", password="your-password")
# Or: ZPoolsClient(pat="your-pat")

zpools = client.list_zpools()
job = client.create_zpool(size_gib=125, volume_type="gp3")
status = client.get_job(job.parsed.detail.job_id)
```

**Configuration:** Use rcfile `~/.config/zpools.io/zpoolrc` or env (`ZPOOL_USER`, `ZPOOL_PASSWORD`, `ZPOOLPAT`, `ZPOOL_API_URL`). The SDK accepts explicit constructor args; the CLI loads rcfile/env. See the [top-level docs](../../../docs/README.md) for [configuration](../../../docs/configuration.md), [authentication](../../../docs/authentication.md), [quickstart](../../../docs/quickstart.md), and [reference](../../../docs/reference/storage-units.md).

## Documentation

- **This package:** [Installation](docs/installation.md) | [Quickstart](docs/quickstart.md) | [API reference](docs/api-reference.md) | [Troubleshooting](docs/troubleshooting.md)
- **Top-level (language-independent):** [docs/](../../../docs/README.md) — quickstart, configuration, authentication, reference (storage units, async jobs), troubleshooting

## Links

- **Service:** https://zpools.io
- **Discord:** https://zpools.io/discord
- **CLI:** [zpools-cli](../cli/README.md) in this repo
