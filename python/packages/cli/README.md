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

## Usage

```bash
# List jobs with filtering
zpcli job list --limit 10 --sort desc

# Manage zpools
zpcli zpool list
zpcli zpool create --size 125 --volume-type gp3
zpcli zpool modify <zpool_id> --volume-type sc1  # Switch to cold tier
zpcli zpool modify <zpool_id> --volume-type gp3  # Switch to hot tier

# Manage SSH keys
zpcli sshkey list
zpcli sshkey add ~/.ssh/id_ed25519.pub

# Check billing
zpcli billing balance
```

## Development

If you're developing the CLI and want to see changes immediately, the editable installation handles this automatically. Just edit the code and run `zpcli` - your changes will be live.

For using `uv run` instead (without user installation):
```bash
cd python
uv sync
uv run zpcli --help
```

**Note**: Tab completion doesn't work with `uv run zpcli`. Use the editable installation method above for the best experience.
