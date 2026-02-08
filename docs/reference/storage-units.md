# Storage units

All storage sizes in zpools.io use **GiB (gibibytes)**: 1 GiB = 1024³ bytes. This is the binary unit, distinct from decimal **GB** (1 GB = 1000³ bytes).

## In the API

- **Parameters:** e.g. `size_gib`, `new_size_in_gib` (create zpool, modify zpool).
- **Response fields:** Sizes are reported in GiB (e.g. `Size` or `size_gib` in API responses).

## In the CLI

- Size arguments use GiB. Example: `zpcli zpool create --size 125 --volume-type gp3` creates a 125 GiB volume.
- All size-related flags and output are in GiB.

## In the SDK

- Method parameters use GiB (e.g. `size_gib=125`, `new_size_in_gib=250`).
- Returned objects expose sizes in GiB (e.g. `size_gib`).

## Conversion

- 1 GiB = 1,073,741,824 bytes.
- Example: 125 GiB = 134,217,728,000 bytes.

When integrating with systems that use decimal GB, convert as needed (multiply GiB by 1024³ for bytes, or use your target unit).
