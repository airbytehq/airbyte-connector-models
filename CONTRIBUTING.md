# Contributing

## Rebuilding Models

To regenerate all connector and metadata models:

```bash
# Install dependencies
npm install
uv sync

# Generate all models
poe generate-all-consolidated
```

This will:
1. Bundle metadata schemas into consolidated JSON files
2. Generate Python models for all connectors
3. Generate consolidated metadata and registry models

For more granular control:

```bash
# Generate specific connector
poe generate-connector --connector source-postgres

# Generate only metadata models
poe generate-metadata-full

# Generate only registry models
poe generate-registry-full
```

See `poe_tasks.toml` for all available tasks.
