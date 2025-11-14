# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import ConfigDict

from models.connectors._internal.base_record import BaseRecordModel


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
