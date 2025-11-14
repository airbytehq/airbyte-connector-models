# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ConnectorMetrics(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorMetricsConnectorMetric(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    usage: str | ConnectorMetricsConnectorMetricUsage | None = None
    sync_success_rate: str | ConnectorMetricsConnectorMetricSyncSuccessRate | None = None
    connector_version: str | None = None


class ConnectorMetricsConnectorMetricSyncSuccessRate(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ConnectorMetricsConnectorMetricUsage(Enum):
    low = "low"
    medium = "medium"
    high = "high"
