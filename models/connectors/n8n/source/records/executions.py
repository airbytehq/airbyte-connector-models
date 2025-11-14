# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import ConfigDict

from models.connectors._internal.base_record import BaseRecordModel


class N8nExecutionsRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    id: int | None = None
    finished: bool | None = None
    mode: str | None = None
    retryOf: str | None = None
    retrySuccessId: int | None = None
    startedAt: str | None = None
    stoppedAt: str | None = None
    workflowId: str | None = None
    waitTill: str | None = None
