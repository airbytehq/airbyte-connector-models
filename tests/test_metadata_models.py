# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for metadata models.

Note: The generated metadata models have forward reference issues that prevent
direct import. These tests verify the JSON schema files exist and are valid JSON.
"""

import json
from pathlib import Path

import pytest

MODELS_DIR = Path(__file__).parent.parent / "models"


@pytest.mark.parametrize(
    "schema_file",
    [
        pytest.param(
            "metadata/v0/ConnectorMetadataDefinitionV0.json",
            id="connector-metadata-definition-v0",
        ),
        pytest.param(
            "metadata/v0/ConnectorRegistryV0.json",
            id="connector-registry-v0",
        ),
    ],
)
def test_metadata_json_schema_is_valid(schema_file: str) -> None:
    """Test that metadata JSON schema files exist and are valid JSON."""
    schema_path = MODELS_DIR / schema_file
    assert schema_path.exists(), f"Schema file not found: {schema_path}"

    content = schema_path.read_text()
    schema = json.loads(content)

    assert isinstance(schema, dict), "Schema should be a JSON object"
    assert "$schema" in schema or "type" in schema, "Schema should have $schema or type"


def test_metadata_models_directory_structure() -> None:
    """Test that the metadata models directory has the expected structure."""
    metadata_dir = MODELS_DIR / "metadata" / "v0"
    assert metadata_dir.exists(), "metadata/v0 directory should exist"

    expected_files = [
        "__init__.py",
        "py.typed",
        "connector_metadata_definition_v0.py",
        "connector_registry_v0.py",
        "ConnectorMetadataDefinitionV0.json",
        "ConnectorRegistryV0.json",
    ]

    for filename in expected_files:
        file_path = metadata_dir / filename
        assert file_path.exists(), f"Expected file not found: {file_path}"
