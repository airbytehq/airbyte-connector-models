"""Generate Pydantic models from Airbyte connector specifications and schemas."""

import argparse
import json
import keyword
import logging
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

AIRBYTE_MONOREPO_PATH = Path(os.getenv("AIRBYTE_MONOREPO_PATH", "/home/ubuntu/repos/airbyte"))
REPO_ROOT = Path(__file__).parent.parent
JSON_SCHEMA_DIR = REPO_ROOT / "json-schema"

CONNECTORS = [
    "source-faker",
    "source-postgres",
    "destination-duckdb",
    "destination-postgres",
    "source-mysql",
    "destination-mysql",
    "destination-dev-null",
    "source-github",
    "source-xkcd",
    "source-n8n",
    "source-dockerhub",
    "source-pokeapi",
    "source-airbyte",
]


def get_connector_spec(connector_name: str) -> dict[str, Any]:
    """Fetch the connector specification from the Airbyte monorepo.

    Args:
        connector_name: The connector name (e.g., "source-postgres")

    Returns:
        The connector specification as a dictionary

    Raises:
        RuntimeError: If the spec cannot be found
    """
    connector_path = AIRBYTE_MONOREPO_PATH / "airbyte-integrations" / "connectors" / connector_name

    if not connector_path.exists():
        logger.error(f"Connector directory not found: {connector_path}")
        raise RuntimeError(f"Connector directory not found for {connector_name}")

    spec_candidates = [
        connector_path / "resources" / "spec.json",
        connector_path / "resources" / "spec.yaml",
        connector_path / "src" / "main" / "resources" / "spec.json",
        connector_path / "spec.json",
        connector_path / "spec.yaml",
    ]

    for spec_file in spec_candidates:
        if spec_file.exists():
            logger.info(f"Found spec file: {spec_file}")
            try:
                with spec_file.open() as f:
                    spec = json.load(f) if spec_file.suffix == ".json" else yaml.safe_load(f)

                if "connectionSpecification" in spec:
                    return spec

            except Exception as e:
                logger.warning(f"Failed to parse {spec_file}: {e}")
                continue

    logger.info(f"Searching recursively for spec files in {connector_path}")
    for spec_file in connector_path.rglob("spec.json"):
        try:
            with spec_file.open() as f:
                spec = json.load(f)
            if "connectionSpecification" in spec:
                logger.info(f"Found spec file: {spec_file}")
                return spec
        except Exception:
            continue

    for spec_file in connector_path.rglob("spec.yaml"):
        try:
            with spec_file.open() as f:
                spec = yaml.safe_load(f)
            if "connectionSpecification" in spec:
                logger.info(f"Found spec file: {spec_file}")
                return spec
        except Exception:
            continue

    logger.error(f"No spec file found for {connector_name}")
    raise RuntimeError(f"No spec file found for {connector_name}")


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

        header_path = REPO_ROOT / ".header.txt"

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
                "airbyte_connector_models._internal.base_config.BaseConfig",
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


def get_declarative_manifest(connector_name: str) -> dict[str, Any] | None:
    """Fetch the declarative manifest from the Airbyte monorepo.

    Args:
        connector_name: The connector name (e.g., "source-xkcd")

    Returns:
        The manifest as a dictionary, or None if not found
    """
    connector_path = AIRBYTE_MONOREPO_PATH / "airbyte-integrations" / "connectors" / connector_name
    manifest_file = connector_path / "manifest.yaml"

    if not manifest_file.exists():
        logger.debug(f"No manifest.yaml found for {connector_name}")
        return None

    try:
        with manifest_file.open() as f:
            manifest = yaml.safe_load(f)
        logger.info(f"Found manifest file: {manifest_file}")
        return manifest
    except Exception as e:
        logger.warning(f"Failed to parse {manifest_file}: {e}")
        return None


def extract_inline_schemas(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Extract inline schemas from a declarative manifest.

    Args:
        manifest: The declarative manifest

    Returns:
        Dictionary mapping stream names to their schemas
    """
    schemas = {}

    if "schemas" in manifest:
        for stream_name, schema in manifest["schemas"].items():
            schemas[stream_name] = schema
            logger.info(f"Found schema for stream: {stream_name}")

    if "definitions" in manifest and "streams" in manifest["definitions"]:
        for stream_name, stream_def in manifest["definitions"]["streams"].items():
            if "schema_loader" in stream_def:
                schema_loader = stream_def["schema_loader"]
                if schema_loader.get("type") == "InlineSchemaLoader":
                    if "schema" in schema_loader:
                        schema = schema_loader["schema"]
                        if isinstance(schema, dict) and "$ref" in schema:
                            ref_path = schema["$ref"]
                            if ref_path.startswith("#/schemas/"):
                                schema_name = ref_path.replace("#/schemas/", "")
                                if "schemas" in manifest and schema_name in manifest["schemas"]:
                                    schemas[stream_name] = manifest["schemas"][schema_name]
                                    msg = f"Resolved schema reference for stream: {stream_name}"
                                    logger.info(msg)
                        else:
                            schemas[stream_name] = schema
                            logger.info(f"Found inline schema for stream: {stream_name}")

    if "streams" in manifest:
        for stream in manifest["streams"]:
            if isinstance(stream, dict):
                stream_name = stream.get("name")
                if stream_name and "schema_loader" in stream:
                    schema_loader = stream["schema_loader"]
                    if schema_loader.get("type") == "InlineSchemaLoader":
                        if "schema" in schema_loader:
                            schemas[stream_name] = schema_loader["schema"]
                            logger.info(f"Found inline schema for stream: {stream_name}")

    return schemas


def normalize_stream_name_to_module(stream_name: str) -> str:
    """Normalize a stream name to a valid Python module name.

    Args:
        stream_name: The stream name (e.g., "Jobs", "docker-hub", "Checkout Sessions")

    Returns:
        A valid Python module name (e.g., "jobs", "docker_hub", "checkout_sessions")
    """
    normalized = stream_name.lower()

    normalized = re.sub(r"[\s-]+", "_", normalized)

    normalized = re.sub(r"[^a-z0-9_]", "", normalized)

    normalized = normalized.strip("_")

    if normalized and (normalized[0].isdigit() or keyword.iskeyword(normalized)):
        normalized = f"stream_{normalized}"

    if not normalized:
        normalized = "stream"

    return normalized


def save_schema_artifact(
    connector_id: str,
    connector_type: str,
    stream_name: str,
    schema: dict[str, Any],
) -> Path:
    """Save a JSON schema artifact for a stream.

    Args:
        connector_id: The connector ID (e.g., "xkcd")
        connector_type: The connector type ("source" or "destination")
        stream_name: The stream name
        schema: The JSON schema

    Returns:
        Path to the saved schema file
    """
    schema_dir = JSON_SCHEMA_DIR / connector_id / connector_type / "records"
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
    """Save a JSON schema artifact for connector configuration.

    Args:
        connector_id: The connector ID (e.g., "xkcd")
        connector_type: The connector type ("source" or "destination")
        spec: The connector spec containing connectionSpecification

    Returns:
        Path to the saved schema file
    """
    schema_dir = JSON_SCHEMA_DIR / connector_id / connector_type
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_file = schema_dir / "configuration.json"
    config_schema = spec.get("connectionSpecification", {})
    schema_file.write_text(json.dumps(config_schema, indent=2))

    logger.info(f"Saved config schema artifact: {schema_file}")
    return schema_file


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
    header_path = REPO_ROOT / ".header.txt"

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
                    "airbyte_connector_models._internal.base_record.BaseRecordModel",
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


def generate_models_for_connector(connector_name: str) -> None:
    """Generate models for a specific connector.

    Args:
        connector_name: The connector name (e.g., "source-postgres")
    """
    logger.info(f"Generating models for {connector_name}")

    if connector_name.startswith("source-"):
        connector_type = "source"
        connector_id = connector_name.replace("source-", "")
    elif connector_name.startswith("destination-"):
        connector_type = "destination"
        connector_id = connector_name.replace("destination-", "")
    else:
        logger.error(f"Invalid connector name: {connector_name}")
        return

    base_path = Path(__file__).parent.parent / "airbyte_connector_models" / "connectors"
    connector_path = base_path / connector_id / connector_type
    config_path = connector_path / "config.py"

    try:
        spec = get_connector_spec(connector_name)
        generate_config_model(connector_name, spec, config_path)
        save_config_schema_artifact(connector_id, connector_type, spec)
    except RuntimeError:
        logger.warning(f"No spec file found for {connector_name}, skipping config model generation")

    # Try to generate record models from declarative manifest
    manifest = get_declarative_manifest(connector_name)
    if manifest:
        schemas = extract_inline_schemas(manifest)
        if schemas:
            for stream_name, schema in schemas.items():
                save_schema_artifact(connector_id, connector_type, stream_name, schema)

            old_records_file = connector_path / "records.py"
            if old_records_file.exists():
                old_records_file.unlink()
                logger.info(f"Removed old records.py file: {old_records_file}")

            records_dir = connector_path / "records"
            generate_record_models(connector_name, connector_id, schemas, records_dir)
        else:
            logger.warning(f"No inline schemas found in manifest for {connector_name}")
    else:
        logger.warning(f"No declarative manifest found for {connector_name}")

    records_dir = connector_path / "records"
    if config_path.exists() or records_dir.exists():
        (base_path / connector_id / "__init__.py").write_text(
            f'"""Models for {connector_id} connector."""\n'
        )
        (connector_path / "__init__.py").write_text(f'"""Models for {connector_name}."""\n')


def main() -> None:
    """Main entry point for model generation."""
    parser = argparse.ArgumentParser(description="Generate Airbyte connector models")
    parser.add_argument(
        "--connector",
        type=str,
        help="Generate models for a specific connector (e.g., source-postgres)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate models for all connectors",
    )

    args = parser.parse_args()

    if args.connector:
        generate_models_for_connector(args.connector)
    elif args.all:
        for connector in CONNECTORS:
            try:
                generate_models_for_connector(connector)
            except Exception:
                logger.exception(f"Failed to generate models for {connector}")
    else:
        for connector in CONNECTORS:
            try:
                generate_models_for_connector(connector)
            except Exception:
                logger.exception(f"Failed to generate models for {connector}")


if __name__ == "__main__":
    main()
