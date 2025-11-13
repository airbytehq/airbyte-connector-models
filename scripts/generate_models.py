"""Generate Pydantic models from Airbyte connector specifications and schemas."""

import argparse
import json
import logging
import os
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
SCHEMAS_DIR = REPO_ROOT / "schemas"


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
    model_name = f"{connector_type}{connector_id}Config"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
        json.dump(connection_spec, temp_file)
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


def save_schema_artifact(
    connector_id: str,
    connector_type: str,
    stream_name: str,
    schema: dict[str, Any],
) -> Path:
    """Save a JSON schema artifact.

    Args:
        connector_id: The connector ID (e.g., "xkcd")
        connector_type: The connector type ("source" or "destination")
        stream_name: The stream name
        schema: The JSON schema

    Returns:
        Path to the saved schema file
    """
    schema_dir = SCHEMAS_DIR / connector_id / connector_type
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_file = schema_dir / f"{stream_name}.json"
    with schema_file.open("w") as f:
        json.dump(schema, f, indent=2)

    logger.info(f"Saved schema artifact: {schema_file}")
    return schema_file


def generate_record_models(
    connector_name: str,
    connector_id: str,
    schemas: dict[str, dict[str, Any]],
    output_path: Path,
) -> None:
    """Generate Pydantic record models from schemas.

    Generates each stream separately and combines them into a single records.py file.
    This approach allows --parent-scoped-naming to work properly without "Model" prefixes.

    Args:
        connector_name: The connector name (e.g., "source-xkcd")
        connector_id: The connector ID (e.g., "xkcd")
        schemas: Dictionary mapping stream names to their schemas
        output_path: Path to write the generated models
    """
    logger.info(f"Generating record models for {connector_name}")

    if not schemas:
        logger.warning(f"No schemas found for {connector_name}")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    header_path = REPO_ROOT / ".header.txt"

    all_generated_code = []
    imports_seen = set()

    for stream_name, schema in schemas.items():
        class_name = "".join(word.capitalize() for word in stream_name.replace("-", "_").split("_"))
        model_name = f"{connector_id.capitalize()}{class_name}Record"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            json.dump(schema, temp_file)
            temp_schema_path = temp_file.name

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_output:
                temp_output_path = temp_output.name

            subprocess.run(
                [
                    "datamodel-codegen",
                    "--input",
                    temp_schema_path,
                    "--output",
                    temp_output_path,
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
                    "--target-python-version",
                    "3.10",
                    "--custom-file-header-path",
                    str(header_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            with Path(temp_output_path).open() as f:
                generated_code = f.read()

            lines = generated_code.split("\n")
            code_lines = []
            in_header = True

            for line in lines:
                if in_header:
                    if line.startswith("#") or line.strip() == "":
                        continue
                    in_header = False

                if line.startswith(("from ", "import ")):
                    imports_seen.add(line)
                elif line.strip() or code_lines:  # Non-empty, non-import line
                    code_lines.append(line)

            all_generated_code.append("\n".join(code_lines))

            Path(temp_output_path).unlink(missing_ok=True)

        finally:
            Path(temp_schema_path).unlink(missing_ok=True)

    with Path(header_path).open() as f:
        header = f.read()

    sorted_imports = sorted(imports_seen)

    final_code = (
        header
        + "\n\n"
        + "\n".join(sorted_imports)
        + "\n\n\n"
        + "\n\n\n".join(all_generated_code)
        + "\n"
    )

    with Path(output_path).open("w") as f:
        f.write(final_code)

    logger.info(f"Generated record models at {output_path}")


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
    except RuntimeError:
        logger.warning(f"No spec file found for {connector_name}, skipping config model generation")

    # Try to generate record models from declarative manifest
    manifest = get_declarative_manifest(connector_name)
    if manifest:
        schemas = extract_inline_schemas(manifest)
        if schemas:
            for stream_name, schema in schemas.items():
                save_schema_artifact(connector_id, connector_type, stream_name, schema)

            records_path = connector_path / "records.py"
            generate_record_models(connector_name, connector_id, schemas, records_path)
        else:
            logger.warning(f"No inline schemas found in manifest for {connector_name}")
    else:
        logger.warning(f"No declarative manifest found for {connector_name}")

    if config_path.exists() or (connector_path / "records.py").exists():
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
        logger.error("--all flag not yet implemented")
    else:
        poc_connectors = [
            "source-faker",
            "source-postgres",
            "destination-duckdb",
            "destination-postgres",
            "source-mysql",
            "destination-mysql",
            "destination-dev-null",
            "source-stripe",
            "source-github",
            "source-xkcd",
            "source-n8n",
            "source-dockerhub",
            "source-pokeapi",
            "source-airbyte",
        ]
        for connector in poc_connectors:
            try:
                generate_models_for_connector(connector)
            except Exception:
                logger.exception(f"Failed to generate models for {connector}")


if __name__ == "__main__":
    main()
