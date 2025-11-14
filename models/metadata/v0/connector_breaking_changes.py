# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated, Literal

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, RootModel


class BreakingChangeScope(RootModel[StreamBreakingChangeScope]):
    root: Annotated[
        StreamBreakingChangeScope,
        Field(description="A scope that can be used to limit the impact of a breaking change."),
    ]


class ConnectorBreakingChanges(RootModel[dict[str, VersionBreakingChange]]):
    root: Annotated[
        dict[str, VersionBreakingChange],
        Field(
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ]


class StreamBreakingChangeScope(BaseModel):
    """
    A scope that can be used to limit the impact of a breaking change to specific streams.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    scopeType: Literal["stream"]
    impactedScopes: Annotated[
        list[str],
        Field(
            description="List of streams that are impacted by the breaking change.",
            min_length=1,
        ),
    ]


class VersionBreakingChange(BaseModel):
    """
    Contains information about a breaking change, including the deadline to upgrade and a message detailing the change.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    upgradeDeadline: Annotated[
        date,
        Field(
            description="The deadline by which to upgrade before the breaking change takes effect."
        ),
    ]
    message: Annotated[str, Field(description="Descriptive message detailing the breaking change.")]
    deadlineAction: Annotated[
        VersionBreakingChangeDeadlineAction | None,
        Field(description="Action to do when the deadline is reached."),
    ] = None
    migrationDocumentationUrl: Annotated[
        AnyUrl | None,
        Field(
            description="URL to documentation on how to migrate to the current version. Defaults to ${documentationUrl}-migrations#${version}"
        ),
    ] = None
    scopedImpact: Annotated[
        list[BreakingChangeScope] | None,
        Field(
            description="List of scopes that are impacted by the breaking change. If not specified, the breaking change cannot be scoped to reduce impact via the supported scope types.",
            min_length=1,
        ),
    ] = None


class VersionBreakingChangeDeadlineAction(Enum):
    """
    Action to do when the deadline is reached.
    """

    auto_upgrade = "auto_upgrade"
    disable = "disable"
