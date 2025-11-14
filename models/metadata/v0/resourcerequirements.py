# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ResourceRequirements(BaseModel):
    """
    generic configuration for pod source requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    cpu_request: str | None = None
    cpu_limit: str | None = None
    memory_request: str | None = None
    memory_limit: str | None = None
