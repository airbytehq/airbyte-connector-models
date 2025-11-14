"""Functions for generating Pydantic models from metadata schemas."""

import json
import logging
import subprocess
import tempfile
from pathlib import Path

import yaml

from .utils import get_repo_root, to_snake_case_module

logger = logging.getLogger(__name__)


def generate_metadata_models() -> None:
    """Generate Pydantic models from metadata schemas.

    Reads all YAML schemas from src/metadata/v0/ and generates
    corresponding Pydantic models in models/metadata/v0/.
    """
    logger.info("Generating metadata models")

    repo_root = get_repo_root()
    schema_dir = repo_root / "src" / "metadata" / "v0"
    output_dir = repo_root / "models" / "metadata" / "v0"
    output_dir.mkdir(parents=True, exist_ok=True)

    header_path = repo_root / ".header.txt"

    schema_files = sorted(schema_dir.glob("*.yaml"))

    if not schema_files:
        logger.warning(f"No schema files found in {schema_dir}")
        return

    logger.info(f"Found {len(schema_files)} metadata schema files")

    for schema_file in schema_files:
        model_name = schema_file.stem  # e.g., "ConnectorMetadataDefinitionV0"
        module_name = to_snake_case_module(schema_file.stem)
        output_file = output_dir / f"{module_name}.py"

        logger.info(f"Generating model for {schema_file.name} -> {module_name}.py")

        try:
            with schema_file.open() as f:
                schema_data = yaml.safe_load(f)

            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
                json.dump(schema_data, temp_file)
                temp_schema_path = temp_file.name

            try:
                subprocess.run(
                    [
                        "datamodel-codegen",
                        "--input",
                        temp_schema_path,
                        "--output",
                        str(output_file),
                        "--input-file-type",
                        "jsonschema",
                        "--output-model-type",
                        "pydantic_v2.BaseModel",
                        "--class-name",
                        model_name,
                        "--use-standard-collections",
                        "--use-union-operator",
                        "--field-constraints",
                        "--use-annotated",
                        "--keyword-only",
                        "--disable-timestamp",
                        "--use-exact-imports",
                        "--use-double-quotes",
                        "--keep-model-order",
                        "--use-schema-description",
                        "--parent-scoped-naming",
                        "--use-title-as-name",
                        "--target-python-version",
                        "3.10",
                        "--custom-file-header-path",
                        str(header_path),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                logger.info(f"Generated {output_file}")

            finally:
                Path(temp_schema_path).unlink(missing_ok=True)

        except Exception:
            logger.exception(f"Failed to generate model for {schema_file.name}")

    init_file = output_dir / "__init__.py"
    init_content = (
        "# Copyright (c) 2025 Airbyte, Inc., all rights reserved.\n\n"
        '"""Metadata models for Airbyte connectors."""\n'
    )
    init_file.write_text(init_content)

    logger.info(f"Generated {len(schema_files)} metadata models in {output_dir}")
