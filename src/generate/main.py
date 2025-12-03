"""Main entry point for model generation."""

import argparse
import logging

from .connector_spec import get_config_spec_for_connector, get_declarative_manifest
from .metadata_generation import (
    generate_consolidated_metadata_model,
    generate_consolidated_registry_model,
    generate_metadata_models,
)
from .model_generation import (
    generate_config_model,
    generate_record_models,
    save_config_schema_artifact,
    save_schema_artifact,
)
from .schema_extraction import extract_inline_schemas
from .utils import get_repo_root

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

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

    repo_root = get_repo_root()
    base_path = repo_root / "models" / "connectors"
    connector_path = base_path / connector_id / connector_type
    config_path = connector_path / "configuration.py"

    spec = get_config_spec_for_connector(connector_name)
    if spec:
        generate_config_model(connector_name, spec, config_path)
        save_config_schema_artifact(connector_id, connector_type, spec)
    else:
        logger.warning(
            f"No config spec found for {connector_name}, skipping config model generation"
        )

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
    parser.add_argument(
        "--metadata",
        action="store_true",
        help="Generate metadata models",
    )
    parser.add_argument(
        "--consolidated",
        action="store_true",
        help="Generate consolidated metadata model from bundled JSON "
        "(requires npm run bundle-schemas first)",
    )
    parser.add_argument(
        "--registry",
        action="store_true",
        help="Generate consolidated registry model from bundled JSON "
        "(requires npm run bundle-schemas first)",
    )

    args = parser.parse_args()

    if args.registry:
        logger.info("Generating consolidated registry model only")
        generate_consolidated_registry_model()
        return

    if args.consolidated:
        logger.info("Generating consolidated metadata model only")
        generate_consolidated_metadata_model()
        return

    if args.metadata:
        logger.info("Generating metadata models only")
        generate_metadata_models()
        return

    if args.connector:
        generate_models_for_connector(args.connector)
    elif args.all:
        for connector in CONNECTORS:
            try:
                generate_models_for_connector(connector)
            except Exception:
                logger.exception(f"Failed to generate models for {connector}")
        try:
            generate_metadata_models()
        except Exception:
            logger.exception("Failed to generate metadata models")
    else:
        for connector in CONNECTORS:
            try:
                generate_models_for_connector(connector)
            except Exception:
                logger.exception(f"Failed to generate models for {connector}")
        try:
            generate_metadata_models()
        except Exception:
            logger.exception("Failed to generate metadata models")


if __name__ == "__main__":
    main()
