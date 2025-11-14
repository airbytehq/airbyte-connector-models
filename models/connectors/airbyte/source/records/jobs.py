# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import ConfigDict

from models.connectors._internal.base_record import BaseRecordModel


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
