# OpenAPI Specifications

This directory contains OpenAPI specification files for the zpools.io API.

## Files

- **`stage-definition.yaml`** - Production API specification

## Usage

These OpenAPI specs are used to:
1. Generate the Python SDK (`python/packages/sdk/src/zpools/_generated/`)
2. Ensure client-server API contract compatibility
3. Provide reference documentation for API endpoints

## Version Environments

- **Production (`stage-definition.yaml`)**: Stable API for production use

## Note

These specifications are maintained by the zpools.io team. The Python SDK is automatically generated from these specs to ensure compatibility with the API.
