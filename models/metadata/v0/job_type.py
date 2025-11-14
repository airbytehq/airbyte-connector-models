# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum


class JobType(Enum):
    """
    enum that describes the different types of jobs that the platform runs.
    """

    get_spec = "get_spec"
    check_connection = "check_connection"
    discover_schema = "discover_schema"
    sync = "sync"
    reset_connection = "reset_connection"
    connection_updater = "connection_updater"
    replicate = "replicate"
