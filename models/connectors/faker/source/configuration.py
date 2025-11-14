# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class SourceFakerConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    count: Annotated[
        int | None,
        Field(
            description="How many users should be generated in total. The purchases table will be scaled to match, with 10 purchases created per 10 users. This setting does not apply to the products stream.",
            ge=1,
            title="Count",
        ),
    ] = 1000
    seed: Annotated[
        int | None,
        Field(
            description="Manually control the faker random seed to return the same values on subsequent runs (leave -1 for random)",
            title="Seed",
        ),
    ] = -1
    records_per_slice: Annotated[
        int | None,
        Field(
            description="How many fake records will be in each page (stream slice), before a state message is emitted?",
            ge=1,
            title="Records Per Stream Slice",
        ),
    ] = 1000
    always_updated: Annotated[
        bool | None,
        Field(
            description="Should the updated_at values for every record be new each sync?  Setting this to false will case the source to stop emitting records after COUNT records have been emitted.",
            title="Always Updated",
        ),
    ] = True
    parallelism: Annotated[
        int | None,
        Field(
            description="How many parallel workers should we use to generate fake data?  Choose a value equal to the number of CPUs you will allocate to this source.",
            ge=1,
            title="Parallelism",
        ),
    ] = 4
