# zpools.io-client

Open-source client repository for **zpools.io** — home-use ZFS storage with durable offsite replication. For service details, pricing, and sign-up, visit https://zpools.io.

## Status

- **Service:** private beta — early features and limited access.
- **Community:** Discord for updates, questions, and beta access: https://zpools.io/discord

## Documentation

**Start here:** [docs/](docs/README.md) — language-independent documentation.

- [Quickstart](docs/quickstart.md) — End-to-end "first zpool" flow.
- [Configuration](docs/configuration.md) — rcfile path, keys, environment overrides.
- [Authentication](docs/authentication.md) — JWT vs PAT, token caching.
- [Reference: Storage units](docs/reference/storage-units.md) and [Async jobs](docs/reference/async-jobs.md).
- [Troubleshooting](docs/troubleshooting.md) — Auth, SSH, jobs, ZFS.

**Package docs:**

- **Python CLI (`zpcli`):** [python/packages/cli/README.md](python/packages/cli/README.md) — Installation, command reference, CLI troubleshooting.
- **Python SDK:** [python/packages/sdk/README.md](python/packages/sdk/README.md) — Installation, quickstart, API reference, SDK troubleshooting.

## Bash CLI — deprecated

The **Bash CLI** (`bash/zpoolcli.sh`) is **deprecated**. It was an early proof-of-concept; it is not the sustained way to support these operations. Documentation and support focus on the **Python CLI** (`zpcli`) and the **Python SDK**. The Bash prototype may remain in the repo for reference but is not a first-class documentation target. Use `zpcli` and the SDK with the [docs/](docs/README.md) above.

## Layout

- **`docs/`** — Language-independent docs (quickstart, configuration, authentication, reference, troubleshooting).
- **`python/`** — Python workspace: `packages/cli` (CLI `zpcli`), `packages/sdk` (SDK).
- **`bash/`** — Deprecated Bash prototype CLI.
- **`spec/`** — OpenAPI specification.

## Support

- **Discord:** https://zpools.io/discord

## Contributing

PRs and issues are welcome. Use Discord to coordinate changes. Do not put internal/SaaS-only notes in this repo (it is public).
