# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import BaseModel


class ConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None
