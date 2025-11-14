# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class AllowedHosts(BaseModel):
    """
    A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    hosts: Annotated[
        list[str] | None,
        Field(
            description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted."
        ),
    ] = None
