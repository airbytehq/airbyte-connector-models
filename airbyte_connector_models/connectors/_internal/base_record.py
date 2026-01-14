"""Base record model for all generated record models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseRecordModel(BaseModel):
    """Base class for all generated record models.

    This class provides:
    - Support for additional properties via extra='allow'
    - Ergonomic attribute access to extra properties
    - Dict-like interface for compatibility with existing code
    - Support for both raw and normalized field names via populate_by_name
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )

    def __getattr__(self, name: str) -> Any:
        """Access extra properties ergonomically.

        This allows accessing additional properties that aren't defined in the schema
        using attribute syntax: record.custom_field

        Args:
            name: The attribute name to access

        Returns:
            The value of the extra property

        Raises:
            AttributeError: If the attribute doesn't exist in fields or extras
        """
        extra = object.__getattribute__(self, "__pydantic_extra__")
        if extra and name in extra:
            return extra[name]
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        """Dict-like access to fields and extras.

        This allows accessing fields using dict syntax: record["field_name"]

        Args:
            key: The field or extra property name

        Returns:
            The value of the field or extra property

        Raises:
            KeyError: If the key doesn't exist in fields or extras
        """
        if key in type(self).model_fields:
            return getattr(self, key)

        extra = self.__pydantic_extra__
        if extra and key in extra:
            return extra[key]

        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a field or extra property with a default value.

        Args:
            key: The field or extra property name
            default: The default value to return if key doesn't exist

        Returns:
            The value of the field/extra or the default value
        """
        try:
            return self[key]
        except (KeyError, AttributeError):
            return default

    def __contains__(self, key: object) -> bool:
        """Check if a field or extra property exists.

        Args:
            key: The field or extra property name to check

        Returns:
            True if the key exists in fields or extras, False otherwise
        """
        if not isinstance(key, str):
            return False

        if key in type(self).model_fields:
            return True

        extra = self.__pydantic_extra__
        return bool(extra and key in extra)

    def keys(self) -> list[str]:
        """Get all field and extra property names.

        Returns:
            List of all field and extra property names
        """
        base = list(type(self).model_fields.keys())
        extra = list((self.__pydantic_extra__ or {}).keys())
        return base + extra

    def items(self) -> list[tuple[str, Any]]:
        """Get all field and extra property items as (key, value) tuples.

        Returns:
            List of (key, value) tuples for all fields and extras
        """
        result = [(k, getattr(self, k)) for k in type(self).model_fields]
        extra = self.__pydantic_extra__
        if extra:
            result.extend(extra.items())
        return result

    def values(self) -> list[Any]:
        """Get all field and extra property values.

        Returns:
            List of all field and extra property values
        """
        result = [getattr(self, k) for k in type(self).model_fields]
        extra = self.__pydantic_extra__
        if extra:
            result.extend(extra.values())
        return result

    def to_dict(self) -> dict[str, Any]:
        """Convert the model to a dictionary.

        Returns:
            Dictionary representation of the model including extra fields
        """
        return self.model_dump(mode="python", by_alias=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BaseRecordModel:
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
    def from_json(cls, json_str: str) -> BaseRecordModel:
        """Create a model instance from a JSON string.

        Args:
            json_str: JSON string containing model data

        Returns:
            New instance of the model
        """
        return cls.model_validate_json(json_str)
