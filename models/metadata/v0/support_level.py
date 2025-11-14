# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum


class SupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"
