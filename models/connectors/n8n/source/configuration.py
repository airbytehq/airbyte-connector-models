# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class SourceN8nConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    host: Annotated[str, Field(description="Hostname of the n8n instance")]
    api_key: Annotated[
        str,
        Field(
            description='Your API KEY. See <a href="https://docs.n8n.io/api/authentication">here</a>'
        ),
    ]
