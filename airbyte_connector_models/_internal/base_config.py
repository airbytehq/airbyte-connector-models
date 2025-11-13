"""Base class for all generated connector config models."""

from __future__ import annotations

from typing import Any

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

    def to_dict(self) -> dict[str, Any]:
        """Convert the model to a dictionary.

        Returns:
            Dictionary representation of the model including extra fields
        """
        return self.model_dump(mode="python", by_alias=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BaseConfig:
        """Create a model instance from a dictionary.

        Args:
            data: Dictionary containing model data

        Returns:
            New instance of the model
        """
        return cls.model_validate(data)

    def to_json(self) -> str:
        """Convert the model to a JSON string.

        Returns:
            JSON string representation of the model
        """
        return self.model_dump_json(by_alias=False)

    @classmethod
    def from_json(cls, json_str: str) -> BaseConfig:
        """Create a model instance from a JSON string.

        Args:
            json_str: JSON string containing model data

        Returns:
            New instance of the model
        """
        return cls.model_validate_json(json_str)
