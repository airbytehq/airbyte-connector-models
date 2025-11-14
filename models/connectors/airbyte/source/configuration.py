# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import AwareDatetime, ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class SourceAirbyteConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    client_id: Annotated[str, Field(title="Client ID")]
    client_secret: Annotated[str, Field(title="Client Secret")]
    start_date: Annotated[
        AwareDatetime,
        Field(
            pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$",
            title="Start date",
        ),
    ]
    host: Annotated[
        str | None,
        Field(
            description="The Host URL of your Self-Managed Deployment (e.x. airbtye.mydomain.com)",
            title="Self-Managed Host",
        ),
    ] = None
