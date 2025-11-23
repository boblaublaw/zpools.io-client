# zpools.io Python Workspace

This directory contains the Python SDK and CLI (`zpcli`) for zpools.io.

## Prerequisites

*   **Python 3.9+**
*   **uv** (Fast Python package manager)

To install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, ensure `~/.local/bin` is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

## Installation (Recommended)

Install `zpcli` as a global command using UV tools:

```bash
cd python
uv tool install --editable packages/cli
```

This installs `zpcli` in editable mode:
- ✅ Available from any directory
- ✅ Code changes reflected immediately (no reinstall needed)
- ✅ Tab completion works
- ✅ Only reinstall if you change dependencies

After installation:
```bash
# Enable tab completion
zpcli --install-completion

# Restart your shell, then use zpcli from anywhere
zpcli --help
zpcli pat list
zpcli billing balance
```

## Development Setup (Alternative)

If you prefer using `uv run` instead of installing globally:

```bash
cd python
uv sync

# Run commands with uv run
uv run zpcli --help
uv run zpcli pat list
```

**Note**: Tab completion doesn't work with `uv run zpcli`. Use the installation method above for tab completion.

## Development

*   **SDK Source:** `packages/sdk/src/zpools`
*   **CLI Source:** `packages/cli/src/zpools_cli`
