"""Utility functions for model generation."""

import keyword
import re
from pathlib import Path


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


def to_snake_case_module(name: str) -> str:
    """Convert a PascalCase or CamelCase name to snake_case for module names.

    Args:
        name: The name to convert (e.g., "ConnectorBreakingChanges", "IPCOptions")

    Returns:
        A snake_case module name (e.g., "connector_breaking_changes", "ipc_options")

    Examples:
        >>> to_snake_case_module("ConnectorBreakingChanges")
        'connector_breaking_changes'
        >>> to_snake_case_module("IPCOptions")
        'ipc_options'
        >>> to_snake_case_module("ConnectorMetadataDefinitionV0")
        'connector_metadata_definition_v0'
    """
    s = re.sub(r"[\s-]+", "_", name)

    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s)

    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)

    s = s.lower()

    s = re.sub(r"[^a-z0-9_]", "", s)

    s = re.sub(r"_+", "_", s).strip("_")

    if s and (s[0].isdigit() or keyword.iskeyword(s)):
        s = f"model_{s}"

    if not s:
        s = "model"

    return s


def get_repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).parent.parent.parent
