# zpools.io Python Workspace

This directory contains the Python SDK and CLI for zpools.io.

## Prerequisites

*   **Python 3.9+**
*   **uv** (Fast Python package manager)

To install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

1.  **Sync the workspace:**
    This creates the virtual environment and installs dependencies.
    ```bash
    cd python
    uv sync
    ```

2.  **Install packages in editable mode:**
    This links the local source code to the environment.
    ```bash
    uv pip install -e packages/sdk -e packages/cli
    ```

## Running the CLI

You can run the CLI using `uv run`:

```bash
# Run the 'hello' command
uv run zpools hello

# View help
uv run zpools --help
```

## Development

*   **SDK Source:** `packages/sdk/src/zpools`
*   **CLI Source:** `packages/cli/src/zpools_cli`
*   **OpenAPI Spec:** `../spec/stage-definition.yaml`

### Regenerating the SDK
If the OpenAPI spec changes, regenerate the client code:

```bash
# From the repo root
uvx openapi-python-client generate \
  --path spec/stage-definition.yaml \
  --output-path temp_gen \
  --overwrite

# Move the generated code (adjust paths as needed)
rm -rf python/packages/sdk/src/zpools/_generated
mv temp_gen/zpools_api_prod_client python/packages/sdk/src/zpools/_generated
rm -rf temp_gen
```
