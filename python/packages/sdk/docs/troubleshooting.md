# SDK troubleshooting

SDK-specific errors and fixes. For conceptual causes (auth, SSH, jobs, etc.), see the top-level [Troubleshooting](../../../../docs/troubleshooting.md).

## UnexpectedStatus

The generated client raises `zpools._generated.errors.UnexpectedStatus` when the API returns a non-2xx status. The exception carries status code and response content.

```python
from zpools import ZPoolsClient
from zpools._generated.errors import UnexpectedStatus

try:
    client = ZPoolsClient(username="user", password="wrong")
    client.list_zpools()
except UnexpectedStatus as e:
    print(f"API error: {e.status_code} - {e.content}")
```

- **401** — Authentication failed. Check username/password or PAT. Use PAT for non-interactive use. See [Authentication](../../../../docs/authentication.md).
- **403** — Forbidden; check PAT scopes or account permissions.
- **4xx/5xx** — Inspect `e.content` for the API error message.

## Auth errors

- **No credentials:** Pass `username`/`password` or `pat` to `ZPoolsClient()`, or set `ZPOOL_USER`/`ZPOOL_PASSWORD`/`ZPOOLPAT` in the environment. The SDK does not read the rcfile by default; the CLI does. If you use the SDK standalone, pass credentials explicitly or load from env.
- **PAT scopes:** Ensure your PAT has the scopes required for the operation (e.g. zpool, job, sshkey).
- **Token expired:** JWT tokens are short-lived. Re-initialize the client or use a PAT for long-running scripts.

## Timeouts

- HTTP timeouts are controlled by the underlying client. For long-running operations (e.g. job polling), implement your own timeout in a loop or use a helper (e.g. `JobPoller` in `zpools.helpers`).
- See [Async jobs](../../../../docs/reference/async-jobs.md).

## Custom API URL

Pass `api_url` when constructing the client:

```python
client = ZPoolsClient(
    api_url="https://api.zpools.io/v1",
    username="user",
    password="pass"
)
```

Ensure the URL is correct and reachable.

## See also

- [Top-level troubleshooting](../../../../docs/troubleshooting.md) — Auth failures, missing rcfile/env, SSH, job timeouts, ZFS, non-interactive PAT.
- [Installation](installation.md) | [API reference](api-reference.md)
