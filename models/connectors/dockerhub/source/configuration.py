# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class SourceDockerhubConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    docker_username: Annotated[
        str,
        Field(
            description="Username of DockerHub person or organization (for https://hub.docker.com/v2/repositories/USERNAME/ API call)",
            examples=["airbyte"],
            pattern="^[a-z0-9_\\-]+$",
            title="Docker Username",
        ),
    ]
