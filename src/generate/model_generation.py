"""Functions for generating Pydantic models from JSON schemas."""

import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .utils import get_repo_root, normalize_stream_name_to_module

logger = logging.getLogger(__name__)


def save_schema_artifact(
    connector_id: str,
    connector_type: str,
    stream_name: str,
    schema: dict[str, Any],
) -> Path:
    """Save a JSON schema artifact for a stream adjacent to the Python model.

    Args:
        connector_id: The connector ID (e.g., "xkcd")
        connector_type: The connector type ("source" or "destination")
        stream_name: The stream name
        schema: The JSON schema

    Returns:
        Path to the saved schema file
    """
    repo_root = get_repo_root()
    schema_dir = repo_root / "models" / "connectors" / connector_id / connector_type / "records"
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_file = schema_dir / f"{stream_name}.json"
    schema_file.write_text(json.dumps(schema, indent=2))

    logger.info(f"Saved schema artifact: {schema_file}")
    return schema_file


def save_config_schema_artifact(
    connector_id: str,
    connector_type: str,
    spec: dict[str, Any],
) -> Path:
    """Save a JSON schema artifact for connector configuration adjacent to the Python model.

    Args:
        connector_id: The connector ID (e.g., "xkcd")
        connector_type: The connector type ("source" or "destination")
        spec: The connector spec containing connectionSpecification

    Returns:
        Path to the saved schema file
    """
    repo_root = get_repo_root()
    schema_dir = repo_root / "models" / "connectors" / connector_id / connector_type
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_file = schema_dir / "configuration.json"
    config_schema = spec.get("connectionSpecification", {})
    schema_file.write_text(json.dumps(config_schema, indent=2))

    logger.info(f"Saved config schema artifact: {schema_file}")
    return schema_file


def generate_config_model(
    connector_name: str,
    spec: dict[str, Any],
    output_path: Path,
) -> None:
    """Generate a Pydantic config model from a connector spec.

    Args:
        connector_name: The connector name (e.g., "source-postgres")
        spec: The connector specification
        output_path: Path to write the generated model
    """
    logger.info(f"Generating config model for {connector_name}")

    connection_spec = spec.get("connectionSpecification", {})
    if not connection_spec:
        logger.warning(f"No connection specification found for {connector_name}")
        return

    parts = connector_name.split("-")
    connector_type = parts[0].capitalize()
    connector_id = "".join(p.capitalize() for p in parts[1:])
    model_name = f"{connector_type}{connector_id}ConfigSpec"

    schema_for_codegen = connection_spec.copy()
    schema_for_codegen.pop("title", None)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
        json.dump(schema_for_codegen, temp_file)
        temp_schema_path = temp_file.name

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        repo_root = get_repo_root()
        header_path = repo_root / ".header.txt"

        subprocess.run(
            [
                "datamodel-codegen",
                "--input",
                temp_schema_path,
                "--output",
                str(output_path),
                "--input-file-type",
                "jsonschema",
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--class-name",
                model_name,
                "--base-class",
                "models.connectors._internal.base_config.BaseConfig",
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

        logger.info(f"Generated config model at {output_path}")

    finally:
        Path(temp_schema_path).unlink(missing_ok=True)


def generate_record_models(
    connector_name: str,
    connector_id: str,
    schemas: dict[str, dict[str, Any]],
    output_dir: Path,
) -> None:
    """Generate Pydantic record models from schemas.

    Generates each stream into a separate file in the records/ directory.
    Creates records/__init__.py with re-exports for backward compatibility.

    Args:
        connector_name: The connector name (e.g., "source-xkcd")
        connector_id: The connector ID (e.g., "xkcd")
        schemas: Dictionary mapping stream names to their schemas
        output_dir: Path to the records/ directory
    """
    logger.info(f"Generating record models for {connector_name}")

    if not schemas:
        logger.warning(f"No schemas found for {connector_name}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    repo_root = get_repo_root()
    header_path = repo_root / ".header.txt"

    module_names_seen: dict[str, list[str]] = {}

    for stream_name, schema in schemas.items():
        module_name = normalize_stream_name_to_module(stream_name)

        if module_name not in module_names_seen:
            module_names_seen[module_name] = []
        module_names_seen[module_name].append(stream_name)

        if len(module_names_seen[module_name]) > 1:
            suffix_num = len(module_names_seen[module_name]) - 1
            module_name = f"{module_name}_{suffix_num}"
            logger.warning(
                f"Module name collision for streams {module_names_seen[module_name]}, "
                f"using {module_name} for {stream_name}"
            )

        class_name = "".join(word.capitalize() for word in stream_name.replace("-", "_").split("_"))
        model_name = f"{connector_id.capitalize()}{class_name}Record"

        # Create temp schema file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            json.dump(schema, temp_file)
            temp_schema_path = temp_file.name

        try:
            output_file = output_dir / f"{module_name}.py"

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
                    "--base-class",
                    "models.connectors._internal.base_record.BaseRecordModel",
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

    init_file = output_dir / "__init__.py"
    init_file.write_text("")

    logger.info(f"Generated {len(schemas)} record model files in {output_dir}")
