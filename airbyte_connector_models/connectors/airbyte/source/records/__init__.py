# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from .connections import AirbyteConnectionsRecord
from .jobs import AirbyteJobsRecord
from .workspaces import AirbyteWorkspacesRecord

__all__ = [
    "AirbyteConnectionsRecord",
    "AirbyteJobsRecord",
    "AirbyteWorkspacesRecord",
]
