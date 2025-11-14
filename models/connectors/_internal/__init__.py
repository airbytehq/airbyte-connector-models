"""Internal utilities for airbyte-connector-models."""

from models.connectors._internal.base_config import BaseConfig
from models.connectors._internal.base_record import BaseRecordModel
from models.connectors._internal.normalizer import (
    needs_normalization,
    normalize_field_name,
)

__all__ = [
    "BaseConfig",
    "BaseRecordModel",
    "needs_normalization",
    "normalize_field_name",
]
