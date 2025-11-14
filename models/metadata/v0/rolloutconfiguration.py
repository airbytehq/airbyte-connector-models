# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class RolloutConfiguration(BaseModel):
    """
    configuration for the rollout of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enableProgressiveRollout: Annotated[
        bool | None,
        Field(description="Whether to enable progressive rollout for the connector."),
    ] = False
    initialPercentage: Annotated[
        int | None,
        Field(
            description="The percentage of users that should receive the new version initially.",
            ge=0,
            le=100,
        ),
    ] = 0
    maxPercentage: Annotated[
        int | None,
        Field(
            description="The percentage of users who should receive the release candidate during the test phase before full rollout.",
            ge=0,
            le=100,
        ),
    ] = 50
    advanceDelayMinutes: Annotated[
        int | None,
        Field(
            description="The number of minutes to wait before advancing the rollout percentage.",
            ge=10,
        ),
    ] = 10
