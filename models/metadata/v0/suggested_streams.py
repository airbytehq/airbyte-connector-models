# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class SuggestedStreams(BaseModel):
    """
    A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    streams: Annotated[
        list[str] | None,
        Field(
            description="An array of streams that this connector suggests the average user will want.  SuggestedStreams not being present for the source means that all streams are suggested.  An empty list here means that no streams are suggested."
        ),
    ] = None
