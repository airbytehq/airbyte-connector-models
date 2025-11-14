# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ConnectorBuildOptions(BaseModel):
    """
    metadata specific to the build process.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    baseImage: str | None = None
