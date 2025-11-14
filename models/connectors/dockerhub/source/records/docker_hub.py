# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import Field

from models.connectors._internal.base_record import BaseRecordModel


class DockerhubDockerHubRecord(BaseRecordModel):
    user: Annotated[str | None, Field(description="The user associated with the repository.")] = (
        None
    )
    name: Annotated[str | None, Field(description="The name of the repository.")] = None
    namespace: Annotated[
        str | None, Field(description="The namespace associated with the repository.")
    ] = None
    repository_type: Annotated[str | None, Field(description="The type of the repository.")] = None
    status: Annotated[int | None, Field(description="The status of the repository.")] = None
    description: Annotated[str | None, Field(description="The description of the repository.")] = (
        None
    )
    is_private: Annotated[
        bool | None, Field(description="Indicates whether the repository is private.")
    ] = None
    is_automated: Annotated[
        bool | None, Field(description="Indicates whether the repository is automated.")
    ] = None
    can_edit: Annotated[
        bool | None,
        Field(description="Indicates whether the user has edit permissions for the repository."),
    ] = None
    star_count: Annotated[
        int | None, Field(description="The count of stars or likes for the repository.")
    ] = None
    pull_count: Annotated[
        int | None,
        Field(description="The count of pulls or downloads for the repository."),
    ] = None
    date_registered: Annotated[
        str | None,
        Field(description="The date when the repository was registered on Docker Hub."),
    ] = None
    status_description: Annotated[
        str | None,
        Field(description="The description of the status of the repository."),
    ] = None
    content_types: Annotated[
        list[str | None] | None,
        Field(description="The content types supported by the repository."),
    ] = None
    media_types: Annotated[
        list[str | None] | None,
        Field(description="The media types supported by the repository."),
    ] = None
    last_updated: Annotated[
        str | None, Field(description="The date when the repository was last updated.")
    ] = None
    is_migrated: Annotated[
        bool | None,
        Field(description="Indicates whether the repository has been migrated."),
    ] = None
    collaborator_count: Annotated[
        int | None,
        Field(description="The count of collaborators associated with the repository."),
    ] = None
    affiliation: Annotated[
        str | None,
        Field(description="The affiliation of the user or organization that owns the repository."),
    ] = None
    hub_user: Annotated[
        str | None,
        Field(description="The user associated with the repository on Docker Hub."),
    ] = None
