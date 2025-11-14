# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from models.connectors._internal.base_record import BaseRecordModel


class AirbyteConnectionsRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    configurations: AirbyteConnectionsRecordConfigurations | None = None
    connectionId: str
    createdAt: float | None = None
    dataResidency: str | None = None
    destinationId: str | None = None
    name: str | None = None
    namespaceDefinition: str | None = None
    namespaceFormat: str | None = None
    nonBreakingSchemaUpdatesBehavior: str | None = None
    prefix: str | None = None
    schedule: AirbyteConnectionsRecordSchedule | None = None
    sourceId: str | None = None
    status: str | None = None
    tags: list[Any] | None = None
    workspaceId: str | None = None


class AirbyteConnectionsRecordConfigurations(BaseRecordModel):
    streams: list[AirbyteConnectionsRecordConfigurationsStream | None] | None = None


class AirbyteConnectionsRecordConfigurationsStream(BaseRecordModel):
    cursorField: list[str | None] | None = None
    mappers: list[Any] | None = None
    name: str | None = None
    primaryKey: list[list[str | None]] | None = None
    selectedFields: list[Any] | None = None
    syncMode: str | None = None


class AirbyteConnectionsRecordSchedule(BaseRecordModel):
    basicTiming: str | None = None
    cronExpression: str | None = None
    scheduleType: str | None = None
