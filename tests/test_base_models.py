# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for base models."""

from pydantic import BaseModel

from models import BaseRecordModel


def test_base_record_model_import() -> None:
    """Test that BaseRecordModel can be imported from the models package."""
    assert BaseRecordModel is not None


def test_base_record_model_is_pydantic_model() -> None:
    """Test that BaseRecordModel is a Pydantic model."""
    assert issubclass(BaseRecordModel, BaseModel)
