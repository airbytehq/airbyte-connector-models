# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, RootModel

from airbyte_connector_models._internal.base_record import BaseRecordModel


class AirbyteConnectionsRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    configurations: Configurations | None = None
    connectionId: str
    createdAt: float | None = None
    dataResidency: str | None = None
    destinationId: str | None = None
    name: str | None = None
    namespaceDefinition: str | None = None
    namespaceFormat: str | None = None
    nonBreakingSchemaUpdatesBehavior: str | None = None
    prefix: str | None = None
    schedule: Schedule | None = None
    sourceId: str | None = None
    status: str | None = None
    tags: list[Any] | None = None
    workspaceId: str | None = None


class AirbyteJobsRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    bytesSynced: float | None = None
    connectionId: str | None = None
    duration: str | None = None
    jobId: float
    jobType: str | None = None
    lastUpdatedAt: str
    rowsSynced: float | None = None
    startTime: str | None = None
    status: str | None = None


class AirbyteWorkspacesRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    dataResidency: str | None = None
    name: str | None = None
    notifications: Notifications | None = None
    workspaceId: str


class Configurations(BaseRecordModel):
    streams: list[Stream | None] | None = None


class ConnectionUpdate(BaseRecordModel):
    email: Email | None = None
    webhook: Webhook | None = None


class ConnectionUpdateActionRequired(BaseRecordModel):
    email: Email | None = None
    webhook: Webhook | None = None


class Email(BaseRecordModel):
    enabled: bool | None = None


class Failure(BaseRecordModel):
    email: Email | None = None
    webhook: Webhook | None = None


class Model(RootModel[Any]):
    root: Any


class Notifications(BaseRecordModel):
    connectionUpdate: ConnectionUpdate | None = None
    connectionUpdateActionRequired: ConnectionUpdateActionRequired | None = None
    failure: Failure | None = None
    success: Success | None = None
    syncDisabled: SyncDisabled | None = None
    syncDisabledWarning: SyncDisabledWarning | None = None


class Schedule(BaseRecordModel):
    basicTiming: str | None = None
    cronExpression: str | None = None
    scheduleType: str | None = None


class Stream(BaseRecordModel):
    cursorField: list[str | None] | None = None
    mappers: list[Any] | None = None
    name: str | None = None
    primaryKey: list[list[str | None]] | None = None
    selectedFields: list[Any] | None = None
    syncMode: str | None = None


class Success(BaseRecordModel):
    email: Email | None = None
    webhook: Webhook | None = None


class SyncDisabled(BaseRecordModel):
    email: Email | None = None
    webhook: Webhook | None = None


class SyncDisabledWarning(BaseRecordModel):
    email: Email | None = None
    webhook: Webhook | None = None


class Webhook(BaseRecordModel):
    enabled: bool | None = None
