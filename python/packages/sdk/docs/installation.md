# SDK Installation

Install the official Python SDK for zpools.io to use the API from Python (zpools, jobs, SSH keys, PATs, billing).

**Note:** The SDK is not yet published to PyPI. Install from the repo for now; PyPI publication is planned.

## Prerequisites

- **Python 3.9+**
- **pip** or **uv**

## Install from repo

From the **zpools-io-client** repo root:

```bash
cd python
uv pip install -e packages/sdk
```

Or with pip:

```bash
cd python
pip install -e packages/sdk
```

From another directory (path to your clone):

```bash
pip install -e /path/to/zpools-io-client/python/packages/sdk
```

Using the repo’s uv workspace (for development):

```bash
cd python
uv sync
# Then use: uv run python -c "from zpools import ZPoolsClient; ..."
```

## Verify

```python
from zpools import ZPoolsClient
client = ZPoolsClient(username="user", password="pass")
zpools = client.list_zpools()
```

## See also

- [Quickstart](quickstart.md)
- [API reference](api-reference.md)
- [Configuration](../../../../docs/configuration.md) and [Authentication](../../../../docs/authentication.md) (top-level docs)
