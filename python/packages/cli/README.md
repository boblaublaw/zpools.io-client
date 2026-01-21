# zpools-cli

The official command line interface for zpools.io.

## Installation

Install `zpcli` for the current user using UV tools:

```bash
cd python
uv tool install --editable packages/cli
```

This installs `zpcli` in editable mode, which means:
- ✅ Available from any directory (for current user)
- ✅ Code changes reflected immediately (no reinstall needed)
- ✅ Updates to the Python package are instantly available
- ✅ Only reinstall if dependencies change in `pyproject.toml`

After installation, ensure `~/.local/bin` is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

**Verify installation:**
```bash
which zpcli
# Should output: /home/youruser/.local/bin/zpcli

zpcli --help
```

Once installed and your PATH is updated, `zpcli` will be available from any directory in your terminal sessions.

## First-time Setup

Enable tab completion (optional but recommended):
```bash
zpcli --install-completion
# Restart your shell
```

Create configuration file at `~/.config/zpools.io/zpoolrc`:
```bash
ZPOOL_USER="your zpools.io username"
ZPOOL_API_URL="https://api.zpools.io/v1"
SSH_HOST="ssh.zpools.io"  # Required for ZFS commands
SSH_PRIVKEY_FILE="/path/to/private/key"  # Required for ZFS commands
```

**See:** `../README.md` for full configuration details and optional settings.

## Usage

```bash
# List jobs with filtering
zpcli job list --limit 10 --sort desc

# Manage zpools
zpcli zpool list
zpcli zpool create --size 125 --volume-type gp3  # Returns job ID (async)
zpcli zpool create --size 125 --volume-type gp3 --wait  # Wait for completion
zpcli zpool modify <zpool_id> --volume-type sc1  # Switch to cold tier (async)
zpcli zpool modify <zpool_id> --volume-type sc1 --wait  # Wait for completion
zpcli zpool scrub <zpool_id>  # Returns job ID (async)
zpcli zpool scrub <zpool_id> --wait  # Wait for completion
```

**Storage Units:** All size values (e.g., `--size 125`) use GiB (1024³ bytes).

```bash
# Manage SSH keys
zpcli sshkey list
zpcli sshkey add ~/.ssh/id_ed25519.pub

# Check billing
zpcli billing balance

# ZFS operations (over SSH)
zpcli zfs list <dataset> [-r|--recursive]
zpcli zfs snapshot <dataset@snapname>
zpcli zfs destroy <dataset> [-r|--recursive]
zpcli zfs recv <dataset> [-F|--force]  # Receives stream from stdin
zpcli zfs ssh [command...]  # Interactive SSH or run command
```

**Note:** ZFS commands require SSH configuration in `~/.config/zpools.io/zpoolrc`:
- `SSH_HOST` - SSH endpoint (e.g., `ssh.zpools.io`)
- `SSH_PRIVKEY_FILE` - Path to private key
- `ZPOOL_USER` - Username for SSH access

**Async Operations:** Commands like `zpool create`, `zpool modify`, and `zpool scrub` are asynchronous by default and return a job ID. Use the `--wait` flag to poll until completion (with timeout).

## Development

If you're developing the CLI and want to see changes immediately, the editable installation handles this automatically. Just edit the code and run `zpcli` - your changes will be live.

For using `uv run` instead (without user installation):
```bash
cd python
uv sync
uv run zpcli --help
```

**Note**: Tab completion doesn't work with `uv run zpcli`. Use the editable installation method above for the best experience.
