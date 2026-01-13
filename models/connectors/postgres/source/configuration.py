# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import ConfigDict, Field

from models.connectors._internal.base_config import BaseConfig


class SourcePostgresConfigSpec(BaseConfig):
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
    database: Annotated[str, Field(description="Name of the database.", title="Database Name")]
    schemas: Annotated[
        list[str] | None,
        Field(
            description="The list of schemas (case sensitive) to sync from. Defaults to public.",
            min_length=0,
            title="Schemas",
        ),
    ] = ["public"]
    username: Annotated[
        str, Field(description="Username to access the database.", title="Username")
    ]
    password: Annotated[
        str | None,
        Field(description="Password associated with the username.", title="Password"),
    ] = None
    jdbc_url_params: Annotated[
        str | None,
        Field(
            description="Additional properties to pass to the JDBC URL string when connecting to the database formatted as 'key=value' pairs separated by the symbol '&'. (Eg. key1=value1&key2=value2&key3=value3). For more information read about <a href=\"https://jdbc.postgresql.org/documentation/head/connect.html\">JDBC URL parameters</a>.",
            title="JDBC URL Parameters (Advanced)",
        ),
    ] = None
    ssl_mode: Annotated[
        SourcePostgresConfigSpecDisable
        | SourcePostgresConfigSpecAllow
        | SourcePostgresConfigSpecPrefer
        | SourcePostgresConfigSpecRequire
        | SourcePostgresConfigSpecVerifyCa
        | SourcePostgresConfigSpecVerifyFull
        | None,
        Field(
            description='SSL connection modes. \n  Read more <a href="https://jdbc.postgresql.org/documentation/head/ssl-client.html"> in the docs</a>.',
            title="SSL Modes",
        ),
    ] = None
    replication_method: Annotated[
        SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDC
        | SourcePostgresConfigSpecDetectChangesWithXminSystemColumn
        | SourcePostgresConfigSpecScanChangesWithUserDefinedCursor
        | None,
        Field(
            description="Configures how data is extracted from the database.",
            title="Update Method",
        ),
        # pyrefly: ignore [bad-assignment]
    ] = "CDC"
    entra_service_principal_auth: Annotated[
        bool | None,
        Field(
            description="Interpret password as a client secret for a Microsft Entra service principal",
            title="Entra service principal authentication",
        ),
    ] = False
    entra_tenant_id: Annotated[
        str | None,
        Field(
            description="If using Entra service principal, the ID of the tenant",
            title="Entra tenant id",
        ),
    ] = None
    entra_client_id: Annotated[
        str | None,
        Field(
            description="If using Entra service principal, the application ID of the service principal",
            title="Entra client id",
        ),
    ] = None


class SourcePostgresConfigSpecAllow(BaseConfig):
    """
    Enables encryption only when required by the source database.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    mode: Literal["allow"]


class SourcePostgresConfigSpecDetectChangesWithXminSystemColumn(BaseConfig):
    """
    <i>Recommended</i> - Incrementally reads new inserts and updates via Postgres <a href="https://docs.airbyte.com/integrations/sources/postgres/#xmin">Xmin system column</a>. Suitable for databases that have low transaction pressure.
    """

    method: Literal["Xmin"]


class SourcePostgresConfigSpecDisable(BaseConfig):
    """
    Disables encryption of communication between Airbyte and source database.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    mode: Literal["disable"]


class SourcePostgresConfigSpecPrefer(BaseConfig):
    """
    Allows unencrypted connection only if the source database does not support encryption.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    mode: Literal["prefer"]


class SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDC(BaseConfig):
    """
    <i>Recommended</i> - Incrementally reads new inserts, updates, and deletes using the Postgres <a href="https://docs.airbyte.com/integrations/sources/postgres/#cdc">write-ahead log (WAL)</a>. This needs to be configured on the source database itself. Recommended for tables of any size.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    method: Literal["CDC"]
    plugin: Annotated[
        SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDCPlugin | None,
        Field(
            description="A logical decoding plugin installed on the PostgreSQL server.",
            title="Plugin",
        ),
        # pyrefly: ignore [bad-assignment]
    ] = "pgoutput"
    replication_slot: Annotated[
        str,
        Field(
            description='A plugin logical replication slot. Read about <a href="https://docs.airbyte.com/integrations/sources/postgres#step-3-create-replication-slot">replication slots</a>.',
            title="Replication Slot",
        ),
    ]
    publication: Annotated[
        str,
        Field(
            description='A Postgres publication used for consuming changes. Read about <a href="https://docs.airbyte.com/integrations/sources/postgres#step-4-create-publications-and-replication-identities-for-tables">publications and replication identities</a>.',
            title="Publication",
        ),
    ]
    initial_waiting_seconds: Annotated[
        int | None,
        Field(
            description='The amount of time the connector will wait when it launches to determine if there is new data to sync or not. Defaults to 1200 seconds. Valid range: 120 seconds to 2400 seconds. Read about <a href="https://docs.airbyte.com/integrations/sources/postgres/postgres-troubleshooting#advanced-setting-up-initial-cdc-waiting-time">initial waiting time</a>.',
            title="Initial Waiting Time in Seconds (Advanced)",
        ),
    ] = 1200
    queue_size: Annotated[
        int | None,
        Field(
            description="The size of the internal queue. This may interfere with memory consumption and efficiency of the connector, please be careful.",
            title="Size of the queue (Advanced)",
        ),
    ] = 10000
    lsn_commit_behaviour: Annotated[
        SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDCLSNCommitBehaviour | None,
        Field(
            description="Determines when Airbyte should flush the LSN of processed WAL logs in the source database. `After loading Data in the destination` is default. If `While reading Data` is selected, in case of a downstream failure (while loading data into the destination), next sync would result in a full sync.",
            title="LSN commit behaviour",
        ),
        # pyrefly: ignore [bad-assignment]
    ] = "After loading Data in the destination"
    heartbeat_action_query: Annotated[
        str | None,
        Field(
            description='Specifies a query that the connector executes on the source database when the connector sends a heartbeat message. Please see the <a href="https://docs.airbyte.com/integrations/sources/postgres/postgres-troubleshooting#advanced-wal-disk-consumption-and-heartbeat-action-query">setup guide</a> for how and when to configure this setting.',
            title="Debezium heartbeat query (Advanced)",
        ),
    ] = ""
    invalid_cdc_cursor_position_behavior: Annotated[
        SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDCInvalidCDCPositionBehaviorAdvanced
        | None,
        Field(
            description="Determines whether Airbyte should fail or re-sync data in case of an stale/invalid cursor value into the WAL. If 'Fail sync' is chosen, a user will have to manually reset the connection before being able to continue syncing data. If 'Re-sync data' is chosen, Airbyte will automatically trigger a refresh but could lead to higher cloud costs and data loss.",
            title="Invalid CDC position behavior (Advanced)",
        ),
        # pyrefly: ignore [bad-assignment]
    ] = "Fail sync"
    initial_load_timeout_hours: Annotated[
        int | None,
        Field(
            description="The amount of time an initial load is allowed to continue for before catching up on CDC logs.",
            title="Initial Load Timeout in Hours (Advanced)",
        ),
    ] = 8


class SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDCInvalidCDCPositionBehaviorAdvanced(
    Enum
):
    """
    Determines whether Airbyte should fail or re-sync data in case of an stale/invalid cursor value into the WAL. If 'Fail sync' is chosen, a user will have to manually reset the connection before being able to continue syncing data. If 'Re-sync data' is chosen, Airbyte will automatically trigger a refresh but could lead to higher cloud costs and data loss.
    """

    Fail_sync = "Fail sync"
    Re_sync_data = "Re-sync data"


class SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDCLSNCommitBehaviour(Enum):
    """
    Determines when Airbyte should flush the LSN of processed WAL logs in the source database. `After loading Data in the destination` is default. If `While reading Data` is selected, in case of a downstream failure (while loading data into the destination), next sync would result in a full sync.
    """

    While_reading_Data = "While reading Data"
    After_loading_Data_in_the_destination = "After loading Data in the destination"


class SourcePostgresConfigSpecReadChangesUsingWriteAheadLogCDCPlugin(Enum):
    """
    A logical decoding plugin installed on the PostgreSQL server.
    """

    pgoutput = "pgoutput"


class SourcePostgresConfigSpecRequire(BaseConfig):
    """
    Always require encryption. If the source database server does not support encryption, connection will fail.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    mode: Literal["require"]


class SourcePostgresConfigSpecScanChangesWithUserDefinedCursor(BaseConfig):
    """
    Incrementally detects new inserts and updates using the <a href="https://docs.airbyte.com/understanding-airbyte/connections/incremental-append/#user-defined-cursor">cursor column</a> chosen when configuring a connection (e.g. created_at, updated_at).
    """

    method: Literal["Standard"]


class SourcePostgresConfigSpecVerifyCa(BaseConfig):
    """
    Always require encryption and verifies that the source database server has a valid SSL certificate.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    mode: Literal["verify-ca"]
    ca_certificate: Annotated[str, Field(description="CA certificate", title="CA Certificate")]
    client_certificate: Annotated[
        str | None, Field(description="Client certificate", title="Client Certificate")
    ] = None
    client_key: Annotated[str | None, Field(description="Client key", title="Client Key")] = None
    client_key_password: Annotated[
        str | None,
        Field(
            description="Password for keystorage. If you do not add it - the password will be generated automatically.",
            title="Client key password",
        ),
    ] = None


class SourcePostgresConfigSpecVerifyFull(BaseConfig):
    """
    This is the most secure mode. Always require encryption and verifies the identity of the source database server.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    mode: Literal["verify-full"]
    ca_certificate: Annotated[str, Field(description="CA certificate", title="CA Certificate")]
    client_certificate: Annotated[
        str | None, Field(description="Client certificate", title="Client Certificate")
    ] = None
    client_key: Annotated[str | None, Field(description="Client key", title="Client Key")] = None
    client_key_password: Annotated[
        str | None,
        Field(
            description="Password for keystorage. If you do not add it - the password will be generated automatically.",
            title="Client key password",
        ),
    ] = None
