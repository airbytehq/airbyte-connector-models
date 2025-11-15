# Airbyte Connector Models

Typed Pydantic models for Airbyte connectors, providing type-safe configuration and record handling.

## Overview

This package provides automatically generated Pydantic models for:
- **Config Models**: Type-safe configuration for all Airbyte connectors
- **Record Models**: Typed records for all source connector streams
- **Metadata Models**: Models used in `metadata.yaml` files
- **Registry Models**: Modules used by the Airbyte Connector Registry

Models are generated nightly from the latest connector specifications and schemas.

## Installation

```bash
pip install airbyte-connector-models
```

## Usage

### Config Models

```python
from airbyte_connector_models.connectors.postgres.source.config import SourcePostgresConfigSpec
import airbyte as ab  # Optional import if using with PyAirbyte

# Type-safe config
config = SourcePostgresConfigSpec(
    host="localhost",
    port=5432,
    database="mydb",
    username="user",
    password="pass"
)

# Use with PyAirbyte (optional)
source = ab.get_source("source-postgres", config=config)
```

### Record Models

Note: Below is planned functionality (not yet available).

```python
from airbyte_connector_models.connectors.postgres.source.records import PostgresUsersRecord
import airbyte as ab

source = ab.get_source("source-postgres", config=config)
source.select_streams(["users"])

# Get typed records
for record in source.get_records("users", as_model=PostgresUsersRecord):
    print(f"User: {record.name}, Email: {record.email}")
    # Access extra properties ergonomically
    if hasattr(record, "custom_field"):
        print(f"Custom: {record.custom_field}")
```

## Features

- **Type Safety**: Full type hints for IDE autocomplete and type checking
- **Additional Properties**: Ergonomic access to extra fields not in the schema
- **Minimal Normalization**: Field names preserve original casing, only illegal characters are replaced
- **Validation**: Automatic validation of configs and records using Pydantic
- **Nightly Updates**: Models are regenerated nightly to stay in sync with connector changes

## Structure

```
airbyte_connector_models/
├── connectors/
│   ├── github/
│   │   ├── source/
│   │   │   ├── configuration.py      # SourceGitHubConficSpec
│   │   │   ├── configuration.json    # JSON Schema Spec
│   │   │   └── records/              # Module containing record model specifications
│   │   └── destination/
│   │   │   ├── configuration.py      # DestinationGitHubConficSpec
│   │   │   ├── configuration.json    # JSON Schema Spec
│   └── ...
```

## Contributing

See the [Contributing Guide](CONTRIBUTING.md)

