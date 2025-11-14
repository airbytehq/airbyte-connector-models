# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class DestinationDuckdbConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    motherduck_api_key: Annotated[
        str | None,
        Field(
            description="API key to use for authentication to a MotherDuck database.",
            title="MotherDuck API Key",
        ),
    ] = None
    destination_path: Annotated[
        str,
        Field(
            description="Path to the .duckdb file, or the text 'md:' to connect to MotherDuck. The file will be placed inside that local mount. For more information check out our <a href=\"https://docs.airbyte.io/integrations/destinations/duckdb\">docs</a>",
            examples=["/local/destination.duckdb", "md:", "motherduck:"],
            title="Destination DB",
        ),
    ]
    schema_: Annotated[
        str | None,
        Field(
            alias="schema",
            description="Database schema name, default for duckdb is 'main'.",
            examples=["main"],
            title="Destination Schema",
        ),
    ] = None
