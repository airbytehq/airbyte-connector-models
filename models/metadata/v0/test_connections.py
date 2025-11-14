# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TestConnections(BaseModel):
    """
    List of sandbox cloud connections that tests can be run against
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[str, Field(description="The connection name")]
    id: Annotated[str, Field(description="The connection ID")]
