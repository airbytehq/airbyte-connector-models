# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class SourceXkcdConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    comic_number: Annotated[
        str | None,
        Field(
            description="Specifies the comic number in which details are to be extracted, pagination will begin with that number to end of available comics",
            title="comic_number",
        ),
    ] = "2960"
