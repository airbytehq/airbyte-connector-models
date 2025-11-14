"""Functions for fetching connector specifications."""

import json
import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

AIRBYTE_MONOREPO_PATH = Path(os.getenv("AIRBYTE_MONOREPO_PATH", "/home/ubuntu/repos/airbyte"))


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


def get_config_spec_for_connector(connector_name: str) -> dict[str, Any] | None:
    """Get config spec from either spec files or declarative manifest.

    Args:
        connector_name: The connector name (e.g., "source-postgres")

    Returns:
        A dict with connectionSpecification key, or None if no spec found
    """
    try:
        spec = get_connector_spec(connector_name)
        logger.info(f"Found spec file for {connector_name}")
        return spec
    except RuntimeError:
        logger.info(f"No spec file found for {connector_name}, checking manifest")

    try:
        manifest = get_declarative_manifest(connector_name)
        if manifest and "spec" in manifest:
            spec_section = manifest["spec"]

            connection_spec = spec_section.get("connection_specification") or spec_section.get(
                "connectionSpecification"
            )

            if connection_spec:
                logger.info(f"Found declarative spec in manifest for {connector_name}")
                return {"connectionSpecification": connection_spec}
            logger.info(
                f"Manifest spec section exists but no connection_specification "
                f"found for {connector_name}"
            )
    except Exception as e:
        logger.debug(f"Could not extract spec from manifest for {connector_name}: {e}")

    logger.info(f"No config spec found for {connector_name} (neither spec file nor manifest)")
    return None
