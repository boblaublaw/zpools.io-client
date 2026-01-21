# zpools-sdk

The official Python SDK for zpools.io — home-use ZFS storage with durable offsite replication.

## Overview

`zpools-sdk` provides a high-level Python interface to the zpools.io API, handling authentication, token management, and API operations. The SDK is auto-generated from OpenAPI specs and wrapped with a convenient client class.

## Installation

```bash
pip install zpools-sdk
```

Or with `uv`:
```bash
uv pip install zpools-sdk
```

## Quick Start

```python
from zpools import ZPoolsClient

# Initialize client (reads from ~/.config/zpools.io/zpoolrc, env vars, or explicit args)
client = ZPoolsClient(
    username="your-username",
    password="your-password"  # Or use PAT instead
)

# Alternatively, use a PAT for non-interactive auth
client = ZPoolsClient(pat="your-personal-access-token")

# List your zpools
zpools = client.list_zpools()
for zpool in zpools:
    print(f"Pool: {zpool.name}, Size: {zpool.size_gib}GiB")

# Create a new zpool
job = client.create_zpool(size_gib=125, volume_type="gp3")
print(f"Job ID: {job.job_id}")

# Check job status
status = client.get_job(job.job_id)
print(f"Status: {status.state}")
```

## Authentication

The SDK supports multiple authentication methods (in priority order):

1. **Explicit arguments** to `ZPoolsClient()`
2. **Environment variables**:
   - `ZPOOL_USER` — Username
   - `ZPOOL_PASSWORD` — Password (for JWT auth)
   - `ZPOOLPAT` — Personal Access Token
   - `ZPOOL_API_URL` — API endpoint (default: `https://api.zpools.io/v1`)
3. **RC file** (`~/.config/zpools.io/zpoolrc`):
   ```bash
   ZPOOL_USER="your-username"
   ZPOOLPAT="your-pat-token"
   ZPOOL_API_URL="https://api.zpools.io/v1"
   ```

**Note:** Passwords are never stored in the RC file. The SDK caches JWT tokens in `/dev/shm` for security.

### Using Personal Access Tokens (PATs)

PATs are recommended for automation and CI/CD:

```python
# Create a PAT (requires JWT auth first)
client = ZPoolsClient(username="user", password="pass")
pat = client.create_pat(
    label="CI/CD Token",
    scopes=["zpool", "job"],
    expiry="2025-12-31T23:59:59Z"
)
print(f"PAT: {pat.key}")

# Use the PAT for subsequent requests
client = ZPoolsClient(pat=pat.key)
```

## Storage Units

All storage sizes in the zpools.io API use **GiB (gibibytes, 1024³ bytes)**. This is the binary unit, distinct from decimal GB (1000³ bytes).

- A 125 GiB volume = 134,217,728,000 bytes
- API parameters: `size_gib`, `new_size_in_gib`
- Response fields: `Size` (in GiB)

## API Reference

### ZPool Operations

```python
# List all zpools
zpools = client.list_zpools()

# Create a zpool
job = client.create_zpool(size_gib=125, volume_type="gp3")

# Delete a zpool
result = client.delete_zpool(zpool_id="zpool-123")

# Modify zpool size
job = client.modify_zpool(zpool_id="zpool-123", new_size_gib=250)

# Scrub a zpool
job = client.scrub_zpool(zpool_id="zpool-123")
```

### Job Management

```python
# Get job status
job = client.get_job(job_id="job-123")
print(f"State: {job.state}")

# List all jobs
jobs = client.list_jobs()
```

### SSH Key Management

```python
# List SSH keys
keys = client.list_sshkeys()

# Add SSH key
with open("~/.ssh/id_ed25519.pub") as f:
    pubkey = f.read()
result = client.add_sshkey(public_key=pubkey)

# Delete SSH key
client.delete_sshkey(pubkey_id="fingerprint-or-id")
```

### Personal Access Tokens

```python
# List PATs
pats = client.list_pats()

# Create PAT
pat = client.create_pat(
    label="My Token",
    scopes=["zpool", "sshkey", "job"],
    expiry="2026-01-01T00:00:00Z"
)

# Revoke PAT
client.revoke_pat(key_id="pat-123")
```

### Billing

```python
# Get billing information
billing = client.get_billing()
print(f"Current charges: ${billing.current_month_estimate}")
```

## Advanced Usage

### Custom API Endpoint

```python
# Use a different API endpoint (e.g., dev environment)
client = ZPoolsClient(
    api_url="https://api-dev.zpools.io/v1",
    username="testuser",
    password="testpass"
)
```

### Direct Access to Generated Client

The wrapped client exposes the raw auto-generated client for advanced use cases:

```python
raw_client = client.get_authenticated_client()
# Use raw_client for operations not wrapped by ZPoolsClient
```

## Configuration File

The SDK reads from `~/.config/zpools.io/zpoolrc`:

```bash
# Required for username/password auth
ZPOOL_USER="your-username"

# API endpoint (optional, defaults to production)
ZPOOL_API_URL="https://api.zpools.io/v1"

# PAT for non-interactive auth (optional)
ZPOOLPAT="your-pat-token"

# SSH configuration (for ZFS over SSH operations)
SSH_HOST="ssh.zpools.io"
SSH_PRIVKEY_FILE="/path/to/your/ssh/key"
```

**Security Notes:**
- Never store passwords in the RC file
- PATs are scoped and can be revoked at any time
- JWT tokens are cached in `/dev/shm` (memory-backed, cleared on reboot)

## Error Handling

```python
from zpools import ZPoolsClient
from zpools._generated.errors import UnexpectedStatus

try:
    client = ZPoolsClient(username="user", password="wrong")
    zpools = client.list_zpools()
except UnexpectedStatus as e:
    print(f"API Error: {e.status_code} - {e.content}")
except Exception as e:
    print(f"Error: {e}")
```

## Development

This SDK uses a clean, modular architecture with separation of concerns.

### Structure

```
src/zpools/
├── __init__.py              # Package exports (ZPoolsClient)
├── client.py                # Main client coordinator (~60 lines)
├── auth.py                  # Authentication & token management
├── helpers.py               # Polling utilities (JobPoller, ModifyPoller)
├── api/                     # API operation modules
│   ├── pats.py              # Personal Access Token operations
│   ├── sshkeys.py           # SSH key management operations
│   ├── zpools.py            # ZPool management operations
│   ├── jobs.py              # Job management operations
│   ├── billing.py           # Billing operations
│   └── zfs_operations.py    # SSH/ZFS operations
└── _generated/              # Auto-generated API client (do not edit)
```

### Architecture

The SDK uses a **mixin-based architecture** for clean separation:

- **`client.py`**: Thin coordinator that inherits from all operation mixins
- **`auth.py`**: Encapsulates all authentication logic (JWT/PAT, token caching)
- **`api/*`**: Each resource type (zpools, jobs, pats, etc.) in its own focused module
- **Mixins**: Each API module provides a mixin class that `ZPoolsClient` inherits from

**Benefits**:
- Each resource type isolated in ~50-100 line files
- Easy to find and modify specific operations
- Clean separation of concerns
- Highly testable components
- No leaky abstractions

### Token Caching

JWT tokens are automatically cached in `/dev/shm` (or temp directory) for performance:
- Tokens are valid for 1 hour
- Cached tokens are reused until expiration
- Login only occurs when needed
- File permissions are set to 600 (user read/write only)

For long-running operations that span multiple hours, the CLI implements periodic token refresh to keep credentials valid.

## Links

- **Service:** https://zpools.io
- **Documentation:** https://docs.zpools.io
- **Discord:** https://discord.gg/q8C6zJYQ
- **CLI Tool:** [zpools-cli](https://github.com/boblaublaw/zpools.io-client)

## License

See the main repository for license information.
