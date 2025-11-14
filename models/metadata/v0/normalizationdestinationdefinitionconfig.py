# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class NormalizationDestinationDefinitionConfig(BaseModel):
    """
    describes a normalization config for destination definition
    """

    model_config = ConfigDict(
        extra="allow",
    )
    normalizationRepository: Annotated[
        str,
        Field(
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used."
        ),
    ]
    normalizationTag: Annotated[
        str,
        Field(
            description="a field indicating the tag of the docker repository to be used for normalization."
        ),
    ]
    normalizationIntegrationType: Annotated[
        str,
        Field(
            description="a field indicating the type of integration dialect to use for normalization."
        ),
    ]
