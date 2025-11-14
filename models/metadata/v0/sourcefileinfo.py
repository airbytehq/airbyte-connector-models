# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import BaseModel


class SourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None
