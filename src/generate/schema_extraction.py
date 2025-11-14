"""Functions for extracting schemas from declarative manifests."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


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
