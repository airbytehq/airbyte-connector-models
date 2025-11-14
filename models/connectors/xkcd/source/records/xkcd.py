# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import ConfigDict

from models.connectors._internal.base_record import BaseRecordModel


class XkcdXkcdRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    alt: str | None = None
    day: str | None = None
    img: str | None = None
    link: str | None = None
    month: str | None = None
    news: str | None = None
    num: int | None = None
    safe_title: str | None = None
    title: str | None = None
    transcript: str | None = None
    year: str | None = None
