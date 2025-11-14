# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class GitInfo(BaseModel):
    """
    Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    commit_sha: Annotated[
        str | None,
        Field(description="The git commit sha of the last commit that modified this file."),
    ] = None
    commit_timestamp: Annotated[
        AwareDatetime | None,
        Field(description="The git commit timestamp of the last commit that modified this file."),
    ] = None
    commit_author: Annotated[
        str | None,
        Field(description="The git commit author of the last commit that modified this file."),
    ] = None
    commit_author_email: Annotated[
        str | None,
        Field(
            description="The git commit author email of the last commit that modified this file."
        ),
    ] = None
