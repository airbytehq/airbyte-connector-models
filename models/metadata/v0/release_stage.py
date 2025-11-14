# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum


class ReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"
