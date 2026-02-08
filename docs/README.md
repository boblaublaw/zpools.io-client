# zpools.io Client Documentation

Documentation for the **zpools.io** client: CLI (`zpcli`) and Python SDK. Use these docs to get started, configure your environment, and integrate with zpools.io.

## Quick links

- **Service:** https://zpools.io
- **Discord:** https://zpools.io/discord

## Documentation index

### Getting started

- [Quickstart](quickstart.md) — End-to-end "first zpool" flow: sign up, install a client, configure, create a zpool (and optionally snapshot/send). Language-agnostic; links to package-specific install and usage. *(Beta: includes beta code claim step.)*

### Configuration and authentication

- [Configuration](configuration.md) — rcfile path, keys, environment overrides. Same for CLI and SDK.
- [Authentication](authentication.md) — JWT vs PAT, token caching, rcfile and env. Concepts only; package docs add code/CLI usage.

### Reference

- [Resource IDs](reference/ids.md) — How IDs are structured (four words, hyphen-separated); job IDs, zpool IDs, SSH key IDs, PAT key IDs.
- [Storage units](reference/storage-units.md) — GiB (1024³) vs GB; size params and field names in API/CLI/SDK.
- [Async jobs](reference/async-jobs.md) — Operations that return job IDs; polling; job states; timeouts.

### Troubleshooting

- [Troubleshooting](troubleshooting.md) — Conceptual: auth failures, missing rcfile/env, SSH issues, job timeouts, ZFS errors, non-interactive PAT. Links to package docs for tool-specific errors.

## Package documentation

- **CLI (`zpcli`):** [python/packages/cli/README.md](../python/packages/cli/README.md) — Installation, command reference, CLI-specific troubleshooting.
- **Python SDK:** [python/packages/sdk/README.md](../python/packages/sdk/README.md) — Installation, quickstart, API reference, SDK-specific troubleshooting.

All package docs link back here for configuration, authentication, and reference.
