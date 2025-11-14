# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class SecretStore(BaseModel):
    """
    An object describing a secret store metadata
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    alias: Annotated[
        str | None,
        Field(
            description="The alias of the secret store which can map to its actual secret address"
        ),
    ] = None
    type: Annotated[SecretStoreType | None, Field(description="The type of the secret store")] = (
        None
    )


class SecretStoreType(Enum):
    """
    The type of the secret store
    """

    GSM = "GSM"
