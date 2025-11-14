# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class DestinationMysqlConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    host: Annotated[str, Field(description="Hostname of the database.", title="Host")]
    port: Annotated[
        int,
        Field(
            description="Port of the database.",
            examples=["3306"],
            ge=0,
            le=65536,
            title="Port",
        ),
    ]
    database: Annotated[str, Field(description="Name of the database.", title="DB Name")]
    username: Annotated[
        str, Field(description="Username to use to access the database.", title="User")
    ]
    password: Annotated[
        str | None,
        Field(description="Password associated with the username.", title="Password"),
    ] = None
    ssl: Annotated[
        bool | None,
        Field(description="Encrypt data using SSL.", title="SSL Connection"),
    ] = True
    jdbc_url_params: Annotated[
        str | None,
        Field(
            description="Additional properties to pass to the JDBC URL string when connecting to the database formatted as 'key=value' pairs separated by the symbol '&'. (example: key1=value1&key2=value2&key3=value3).",
            title="JDBC URL Params",
        ),
    ] = None
    raw_data_schema: Annotated[
        str | None,
        Field(
            description="The database to write raw tables into",
            title="Raw table database (defaults to airbyte_internal)",
        ),
    ] = None
    disable_type_dedupe: Annotated[
        bool | None,
        Field(
            description="Disable Writing Final Tables. WARNING! The data format in _airbyte_data is likely stable but there are no guarantees that other metadata columns will remain the same in future versions",
            title="Disable Final Tables. (WARNING! Unstable option; Columns in raw table schema might change between versions)",
        ),
    ] = False
