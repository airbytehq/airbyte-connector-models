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


def get_repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).parent.parent.parent
