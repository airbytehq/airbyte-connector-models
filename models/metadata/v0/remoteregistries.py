# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class PyPi(BaseModel):
    """
    describes the PyPi publishing options
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: bool
    packageName: Annotated[str, Field(description="The name of the package on PyPi.")]


class RemoteRegistries(BaseModel):
    """
    describes how the connector is published to remote registries
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    pypi: PyPi | None = None
