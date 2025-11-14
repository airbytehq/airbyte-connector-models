# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class DestinationPostgresConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
    )
    host: Annotated[str, Field(description="Hostname of the database.", title="Host")]
    port: Annotated[
        int,
        Field(
            description="Port of the database.",
            examples=["5432"],
            ge=0,
            le=65536,
            title="Port",
        ),
    ]
    database: Annotated[str, Field(description="Name of the database.", title="DB Name")]
    schema_: Annotated[
        str,
        Field(
            alias="schema",
            description='The default schema tables are written to if the source does not specify a namespace. The usual value for this field is "public".',
            examples=["public"],
            title="Default Schema",
        ),
    ]
    username: Annotated[
        str, Field(description="Username to use to access the database.", title="User")
    ]
    password: Annotated[
        str | None,
        Field(description="Password associated with the username.", title="Password"),
    ] = None
    ssl: Annotated[
        bool | None,
        Field(
            description="Encrypt data using SSL. When activating SSL, please select one of the connection modes.",
            title="SSL Connection",
        ),
    ] = False
    ssl_mode: Annotated[
        DestinationPostgresConfigSpecDisable
        | DestinationPostgresConfigSpecAllow
        | DestinationPostgresConfigSpecPrefer
        | DestinationPostgresConfigSpecRequire
        | DestinationPostgresConfigSpecVerifyCa
        | DestinationPostgresConfigSpecVerifyFull
        | None,
        Field(
            description='SSL connection modes. \n <b>disable</b> - Chose this mode to disable encryption of communication between Airbyte and destination database\n <b>allow</b> - Chose this mode to enable encryption only when required by the source database\n <b>prefer</b> - Chose this mode to allow unencrypted connection only if the source database does not support encryption\n <b>require</b> - Chose this mode to always require encryption. If the source database server does not support encryption, connection will fail\n  <b>verify-ca</b> - Chose this mode to always require encryption and to verify that the source database server has a valid SSL certificate\n  <b>verify-full</b> - This is the most secure mode. Chose this mode to always require encryption and to verify the identity of the source database server\n See more information - <a href="https://jdbc.postgresql.org/documentation/head/ssl-client.html"> in the docs</a>.',
            title="SSL modes",
        ),
    ] = None
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
            description="The schema to write raw tables into",
            title="Raw table schema (defaults to airbyte_internal)",
        ),
    ] = None
    disable_type_dedupe: Annotated[
        bool | None,
        Field(
            description="Disable Writing Final Tables. WARNING! The data format in _airbyte_data is likely stable but there are no guarantees that other metadata columns will remain the same in future versions",
            title="Disable Final Tables. (WARNING! Unstable option; Columns in raw table schema might change between versions)",
        ),
    ] = False
    drop_cascade: Annotated[
        bool | None,
        Field(
            description="Drop tables with CASCADE. WARNING! This will delete all data in all dependent objects (views, etc.). Use with caution. This option is intended for usecases which can easily rebuild the dependent objects.",
            title="Drop tables with CASCADE. (WARNING! Risk of unrecoverable data loss)",
        ),
    ] = False
    unconstrained_number: Annotated[
        bool | None,
        Field(
            description="Create numeric columns as unconstrained DECIMAL instead of NUMBER(38, 9). This will allow increased precision in numeric values. (this is disabled by default for backwards compatibility, but is recommended to enable)",
            title="Unconstrained numeric columns",
        ),
    ] = False


class DestinationPostgresConfigSpecAllow(BaseConfig):
    """
    Allow SSL mode.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Literal["allow"]


class DestinationPostgresConfigSpecAllowMode(Enum):
    allow = "allow"


class DestinationPostgresConfigSpecDisable(BaseConfig):
    """
    Disable SSL.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Literal["disable"]


class DestinationPostgresConfigSpecDisableMode(Enum):
    disable = "disable"


class DestinationPostgresConfigSpecPrefer(BaseConfig):
    """
    Prefer SSL mode.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Literal["prefer"]


class DestinationPostgresConfigSpecPreferMode(Enum):
    prefer = "prefer"


class DestinationPostgresConfigSpecRequire(BaseConfig):
    """
    Require SSL mode.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Literal["require"]


class DestinationPostgresConfigSpecRequireMode(Enum):
    require = "require"


class DestinationPostgresConfigSpecVerifyCa(BaseConfig):
    """
    Verify-ca SSL mode.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Literal["verify-ca"]
    ca_certificate: Annotated[str, Field(description="CA certificate", title="CA certificate")]
    client_key_password: Annotated[
        str | None,
        Field(
            description="Password for keystorage. This field is optional. If you do not add it - the password will be generated automatically.",
            title="Client key password",
        ),
    ] = None


class DestinationPostgresConfigSpecVerifyCaMode(Enum):
    verify_ca = "verify-ca"


class DestinationPostgresConfigSpecVerifyFull(BaseConfig):
    """
    Verify-full SSL mode.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    mode: Literal["verify-full"]
    ca_certificate: Annotated[str, Field(description="CA certificate", title="CA certificate")]
    client_certificate: Annotated[
        str, Field(description="Client certificate", title="Client certificate")
    ]
    client_key: Annotated[str, Field(description="Client key", title="Client key")]
    client_key_password: Annotated[
        str | None,
        Field(
            description="Password for keystorage. This field is optional. If you do not add it - the password will be generated automatically.",
            title="Client key password",
        ),
    ] = None


class DestinationPostgresConfigSpecVerifyFullMode(Enum):
    verify_full = "verify-full"
