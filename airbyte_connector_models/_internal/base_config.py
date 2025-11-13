"""Base class for all generated connector config models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    """Base class for all connector configuration models.

    This base class provides common configuration for all connector config models:
    - Allows population by field name (for alias support)
    - Allows extra fields (for forward compatibility and IDE support without runtime constraints)
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
