# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class AirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: AirbyteInternalSl | None = None
    ql: AirbyteInternalQl | None = None
    isEnterprise: bool | None = False
    requireVersionIncrementsInPullRequests: Annotated[
        bool | None,
        Field(
            description="When false, version increment checks will be skipped for this connector"
        ),
    ] = True


class AirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class AirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
