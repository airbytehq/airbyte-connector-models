# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, RootModel

from airbyte_connector_models._internal.base_record import BaseRecordModel


class Model(RootModel[Any]):
    root: Any


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
