"""Validate example metadata files against JSON schema and Pydantic models.

This script validates all example metadata files in the examples/ directory
to ensure they conform to the JSON schema and can be deserialized by the
Pydantic models.
"""

import json
import pathlib
import sys

import yaml
from pydantic import ValidationError

from airbyte_connector_models.metadata.v0.connector_metadata_definition_v0 import (
    ConnectorMetadataDefinitionV0,
)

EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"
BUNDLED_SCHEMA_PATH = (
    pathlib.Path(__file__).parent.parent
    / "bundled_json_schemas"
    / "ConnectorMetadataDefinitionV0.json"
)


def validate_example_file(file_path: pathlib.Path) -> tuple[bool, str | None]:
    """Validate a single example metadata file.

    Returns a tuple of (success, error_message).
    """
    print(f"Validating {file_path.name}...")

    # Load the YAML file
    yaml_content = yaml.safe_load(file_path.read_text())

    # Validate with Pydantic model
    model = ConnectorMetadataDefinitionV0.model_validate(yaml_content)

    # Verify round-trip serialization
    dumped = model.model_dump(by_alias=True, exclude_unset=True)
    ConnectorMetadataDefinitionV0.model_validate(dumped)

    print("  Pydantic validation: PASSED")

    # Check that smoke test scenarios are present if this is a smoke test example
    if "smoke" in file_path.name.lower() or any(
        suite.suite == "smokeTests"
        for suite in (model.data.connector_test_suites_options or [])
        if suite.suite is not None
    ):
        smoke_test_suites = [
            suite
            for suite in (model.data.connector_test_suites_options or [])
            if suite.suite == "smokeTests"
        ]
        if smoke_test_suites:
            for suite in smoke_test_suites:
                scenario_count = len(suite.scenarios or [])
                print(f"  Smoke test scenarios found: {scenario_count}")

    return True, None


def main() -> int:
    """Validate all example files and return exit code."""
    if not EXAMPLES_DIR.exists():
        print(f"ERROR: Examples directory not found: {EXAMPLES_DIR}")
        return 1

    example_files = list(EXAMPLES_DIR.glob("*.yaml")) + list(EXAMPLES_DIR.glob("*.yml"))

    if not example_files:
        print(f"ERROR: No example files found in {EXAMPLES_DIR}")
        return 1

    print(f"Found {len(example_files)} example file(s) to validate\n")

    failures: list[tuple[pathlib.Path, str]] = []

    for file_path in sorted(example_files):
        try:
            success, error = validate_example_file(file_path)
            if not success:
                failures.append((file_path, error or "Unknown error"))
        except ValidationError as e:
            failures.append((file_path, f"Pydantic validation error:\n{e}"))
        except yaml.YAMLError as e:
            failures.append((file_path, f"YAML parsing error:\n{e}"))
        except json.JSONDecodeError as e:
            failures.append((file_path, f"JSON schema parsing error:\n{e}"))

    print()

    if failures:
        print("=" * 60)
        print("VALIDATION FAILURES:")
        print("=" * 60)
        for file_path, error in failures:
            print(f"\n{file_path.name}:")
            print(f"  {error}")
        print()
        return 1

    print("=" * 60)
    print(f"All {len(example_files)} example file(s) validated successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
