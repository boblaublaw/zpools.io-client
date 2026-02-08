# CLI Installation

Install the official zpools.io CLI (`zpcli`) to manage zpools, jobs, SSH keys, and billing from the terminal.

**Note:** The CLI is not yet published to PyPI. Install from the repo for now; PyPI publication is planned.

## Prerequisites

- **Python 3.9+**
- **uv** (recommended) or pip

To install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ensure `~/.local/bin` is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

## Install with uv (recommended)

From the **zpools-io-client** repo root:

```bash
cd python
uv tool install --editable packages/cli
```

This installs `zpcli` in editable mode:

- Available from any directory (for current user)
- Code changes reflected immediately (no reinstall needed)
- Only reinstall if dependencies change in `pyproject.toml`

Verify:

```bash
which zpcli
zpcli --help
```

## Install with pip

From the repo (editable):

```bash
cd python
pip install -e packages/cli
```

## First-time setup

1. **Tab completion (optional):**  
   `zpcli completion --install` then restart your shell.

2. **Configuration:** Create `~/.config/zpools.io/zpoolrc` with at least `ZPOOL_USER` and `ZPOOL_API_URL`. For ZFS commands add `SSH_HOST` and `SSH_PRIVKEY_FILE`. See [Configuration](../../../../docs/configuration.md#required-parameters) and [Authentication](../../../../docs/authentication.md).

## See also

- [Quickstart](../../../../docs/quickstart.md)
- [Command reference](commands.md)
- [Troubleshooting](troubleshooting.md)
