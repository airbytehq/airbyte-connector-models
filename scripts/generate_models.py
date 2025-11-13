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

    try:
        spec = get_connector_spec(connector_name)
    except RuntimeError:
        logger.exception(f"Skipping {connector_name} due to spec fetch failure")
        return

    base_path = Path(__file__).parent.parent / "airbyte_connector_models" / "connectors"
    connector_path = base_path / connector_id / connector_type
    config_path = connector_path / "config.py"

    generate_config_model(connector_name, spec, config_path)

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
        ]
        for connector in poc_connectors:
            try:
                generate_models_for_connector(connector)
            except Exception:
                logger.exception(f"Failed to generate models for {connector}")


if __name__ == "__main__":
    main()
