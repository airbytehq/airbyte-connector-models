# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from airbyte_connector_models._internal.base_record import BaseRecordModel


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


class AirbyteWorkspacesRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    dataResidency: str | None = None
    name: str | None = None
    notifications: AirbyteWorkspacesRecordNotifications | None = None
    workspaceId: str


class AirbyteWorkspacesRecordNotifications(BaseRecordModel):
    connectionUpdate: AirbyteWorkspacesRecordNotificationsConnectionUpdate | None = None
    connectionUpdateActionRequired: (
        AirbyteWorkspacesRecordNotificationsConnectionUpdateActionRequired | None
    ) = None
    failure: AirbyteWorkspacesRecordNotificationsFailure | None = None
    success: AirbyteWorkspacesRecordNotificationsSuccess | None = None
    syncDisabled: AirbyteWorkspacesRecordNotificationsSyncDisabled | None = None
    syncDisabledWarning: AirbyteWorkspacesRecordNotificationsSyncDisabledWarning | None = None


class AirbyteWorkspacesRecordNotificationsConnectionUpdate(BaseRecordModel):
    email: AirbyteWorkspacesRecordNotificationsConnectionUpdateEmail | None = None
    webhook: AirbyteWorkspacesRecordNotificationsConnectionUpdateWebhook | None = None


class AirbyteWorkspacesRecordNotificationsConnectionUpdateActionRequired(BaseRecordModel):
    email: AirbyteWorkspacesRecordNotificationsConnectionUpdateActionRequiredEmail | None = None
    webhook: AirbyteWorkspacesRecordNotificationsConnectionUpdateActionRequiredWebhook | None = None


class AirbyteWorkspacesRecordNotificationsConnectionUpdateActionRequiredEmail(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsConnectionUpdateActionRequiredWebhook(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsConnectionUpdateEmail(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsConnectionUpdateWebhook(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsFailure(BaseRecordModel):
    email: AirbyteWorkspacesRecordNotificationsFailureEmail | None = None
    webhook: AirbyteWorkspacesRecordNotificationsFailureWebhook | None = None


class AirbyteWorkspacesRecordNotificationsFailureEmail(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsFailureWebhook(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsSuccess(BaseRecordModel):
    email: AirbyteWorkspacesRecordNotificationsSuccessEmail | None = None
    webhook: AirbyteWorkspacesRecordNotificationsSuccessWebhook | None = None


class AirbyteWorkspacesRecordNotificationsSuccessEmail(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsSuccessWebhook(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsSyncDisabled(BaseRecordModel):
    email: AirbyteWorkspacesRecordNotificationsSyncDisabledEmail | None = None
    webhook: AirbyteWorkspacesRecordNotificationsSyncDisabledWebhook | None = None


class AirbyteWorkspacesRecordNotificationsSyncDisabledEmail(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsSyncDisabledWarning(BaseRecordModel):
    email: AirbyteWorkspacesRecordNotificationsSyncDisabledWarningEmail | None = None
    webhook: AirbyteWorkspacesRecordNotificationsSyncDisabledWarningWebhook | None = None


class AirbyteWorkspacesRecordNotificationsSyncDisabledWarningEmail(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsSyncDisabledWarningWebhook(BaseRecordModel):
    enabled: bool | None = None


class AirbyteWorkspacesRecordNotificationsSyncDisabledWebhook(BaseRecordModel):
    enabled: bool | None = None
