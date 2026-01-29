# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

from __future__ import annotations

from datetime import date
from enum import Enum, IntEnum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AnyUrl, AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class AllowedHosts(BaseModel):
    """
    A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    hosts: Annotated[
        list[str] | None,
        Field(
            description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted."
        ),
    ] = None


class ConnectorMetadataDefinitionV0(BaseModel):
    """
    describes the metadata of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    metadata_spec_version: Annotated[str, Field(alias="metadataSpecVersion")]
    data: ConnectorMetadataDefinitionV0Data


class ConnectorMetadataDefinitionV0ActorDefinitionResourceRequirements(BaseModel):
    """
    actor definition specific resource requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    default: Annotated[
        ResourceRequirements | None,
        Field(
            description="if set, these are the requirements that should be set for ALL jobs run for this actor definition."
        ),
    ] = None
    job_specific: Annotated[list[JobTypeResourceLimit] | None, Field(alias="jobSpecific")] = None


class ConnectorMetadataDefinitionV0Data(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: str
    icon: str | None = None
    definition_id: Annotated[UUID, Field(alias="definitionId")]
    connector_build_options: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorBuildOptions | None,
        Field(
            alias="connectorBuildOptions",
            description="metadata specific to the build process.",
            title="ConnectorBuildOptions",
        ),
    ] = None
    connector_test_suites_options: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptions] | None,
        Field(alias="connectorTestSuitesOptions"),
    ] = None
    connector_type: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorType, Field(alias="connectorType")
    ]
    docker_repository: Annotated[str, Field(alias="dockerRepository")]
    docker_image_tag: Annotated[str, Field(alias="dockerImageTag")]
    supports_dbt: Annotated[bool | None, Field(alias="supportsDbt")] = None
    supports_normalization: Annotated[bool | None, Field(alias="supportsNormalization")] = None
    license: str
    documentation_url: Annotated[AnyUrl, Field(alias="documentationUrl")]
    external_documentation_urls: Annotated[
        list[ConnectorMetadataDefinitionV0DataExternalDocumentationUrl] | None,
        Field(
            alias="externalDocumentationUrls",
            description="An array of external vendor documentation URLs (changelogs, API references, deprecation notices, etc.)",
        ),
    ] = None
    github_issue_label: Annotated[str, Field(alias="githubIssueLabel")]
    max_seconds_between_messages: Annotated[
        int | None,
        Field(
            alias="maxSecondsBetweenMessages",
            description="Maximum delay between 2 airbyte protocol messages, in second. The source will timeout if this delay is reached",
        ),
    ] = None
    release_date: Annotated[
        date | None,
        Field(
            alias="releaseDate",
            description="The date when this connector was first released, in yyyy-mm-dd format.",
        ),
    ] = None
    protocol_version: Annotated[
        str | None,
        Field(
            alias="protocolVersion",
            description="the Airbyte Protocol version supported by the connector",
        ),
    ] = None
    erd_url: Annotated[
        str | None,
        Field(alias="erdUrl", description="The URL where you can visualize the ERD"),
    ] = None
    connector_subtype: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorSubtype,
        Field(alias="connectorSubtype"),
    ]
    release_stage: Annotated[
        ConnectorMetadataDefinitionV0DataReleaseStage,
        Field(
            alias="releaseStage",
            description="enum that describes a connector's release stage",
            title="ReleaseStage",
        ),
    ]
    support_level: Annotated[
        ConnectorMetadataDefinitionV0DataSupportLevel | None,
        Field(
            alias="supportLevel",
            description="enum that describes a connector's release stage",
            title="SupportLevel",
        ),
    ] = None
    tags: Annotated[
        list[str] | None,
        Field(
            description="An array of tags that describe the connector. E.g: language:python, keyword:rds, etc."
        ),
    ] = []
    registry_overrides: Annotated[
        ConnectorMetadataDefinitionV0DataRegistryOverrides | None,
        Field(alias="registryOverrides"),
    ] = None
    allowed_hosts: Annotated[
        ConnectorMetadataDefinitionV0DataAllowedHosts | None,
        Field(
            alias="allowedHosts",
            description="A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.",
            title="AllowedHosts",
        ),
    ] = None
    releases: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorReleases | None,
        Field(
            description="Contains information about different types of releases for a connector.",
            title="ConnectorReleases",
        ),
    ] = None
    normalization_config: Annotated[
        ConnectorMetadataDefinitionV0DataNormalizationDestinationDefinitionConfig | None,
        Field(
            alias="normalizationConfig",
            description="describes a normalization config for destination definition",
            title="NormalizationDestinationDefinitionConfig",
        ),
    ] = None
    suggested_streams: Annotated[
        ConnectorMetadataDefinitionV0DataSuggestedStreams | None,
        Field(
            alias="suggestedStreams",
            description="A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.",
            title="SuggestedStreams",
        ),
    ] = None
    resource_requirements: Annotated[
        ConnectorMetadataDefinitionV0DataActorDefinitionResourceRequirements | None,
        Field(
            alias="resourceRequirements",
            description="actor definition specific resource requirements",
            title="ActorDefinitionResourceRequirements",
        ),
    ] = None
    ab_internal: Annotated[
        ConnectorMetadataDefinitionV0DataAirbyteInternal | None,
        Field(description="Fields for internal use only", title="AirbyteInternal"),
    ] = None
    remote_registries: Annotated[
        ConnectorMetadataDefinitionV0DataRemoteRegistries | None,
        Field(
            alias="remoteRegistries",
            description="describes how the connector is published to remote registries",
            title="RemoteRegistries",
        ),
    ] = None
    supports_refreshes: Annotated[bool | None, Field(alias="supportsRefreshes")] = False
    generated: Annotated[
        ConnectorMetadataDefinitionV0DataGeneratedFields | None,
        Field(
            description="Optional schema for fields generated at metadata upload time",
            title="GeneratedFields",
        ),
    ] = None
    supports_file_transfer: Annotated[bool | None, Field(alias="supportsFileTransfer")] = False
    supports_data_activation: Annotated[bool | None, Field(alias="supportsDataActivation")] = False
    connector_ipc_options: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorIPCOptions | None,
        Field(alias="connectorIPCOptions", title="ConnectorIPCOptions"),
    ] = None


class ConnectorMetadataDefinitionV0DataActorDefinitionResourceRequirements(BaseModel):
    """
    actor definition specific resource requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    default: Annotated[
        ResourceRequirements | None,
        Field(
            description="if set, these are the requirements that should be set for ALL jobs run for this actor definition."
        ),
    ] = None
    job_specific: Annotated[list[JobTypeResourceLimit] | None, Field(alias="jobSpecific")] = None


class ConnectorMetadataDefinitionV0DataAirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorMetadataDefinitionV0DataAirbyteInternalSl | None = None
    ql: ConnectorMetadataDefinitionV0DataAirbyteInternalQl | None = None
    is_enterprise: Annotated[bool | None, Field(alias="isEnterprise")] = False
    require_version_increments_in_pull_requests: Annotated[
        bool | None,
        Field(
            alias="requireVersionIncrementsInPullRequests",
            description="When false, version increment checks will be skipped for this connector",
        ),
    ] = True


class ConnectorMetadataDefinitionV0DataAirbyteInternalQl(IntEnum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorMetadataDefinitionV0DataAirbyteInternalSl(IntEnum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorMetadataDefinitionV0DataAllowedHosts(BaseModel):
    """
    A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    hosts: Annotated[
        list[str] | None,
        Field(
            description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted."
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorBuildOptions(BaseModel):
    """
    metadata specific to the build process.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    base_image: Annotated[str | None, Field(alias="baseImage")] = None


class ConnectorMetadataDefinitionV0DataConnectorIPCOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    data_channel: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannel,
        Field(alias="dataChannel"),
    ]


class ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    version: str
    supported_serialization: Annotated[
        list[
            ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedSerializationEnum
        ],
        Field(alias="supportedSerialization"),
    ]
    supported_transport: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedTransportEnum],
        Field(alias="supportedTransport"),
    ]


class ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedSerializationEnum(
    Enum
):
    jsonl = "JSONL"
    protobuf = "PROTOBUF"
    flatbuffers = "FLATBUFFERS"


class ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedTransportEnum(Enum):
    stdio = "STDIO"
    socket = "SOCKET"


class ConnectorMetadataDefinitionV0DataConnectorReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    rollout_configuration: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorReleasesRolloutConfiguration | None,
        Field(
            alias="rolloutConfiguration",
            description="configuration for the rollout of a connector",
            title="RolloutConfiguration",
        ),
    ] = None
    breaking_changes: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorReleasesConnectorBreakingChanges | None,
        Field(
            alias="breakingChanges",
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ] = None
    migration_documentation_url: Annotated[
        AnyUrl | None,
        Field(
            alias="migrationDocumentationUrl",
            description="URL to documentation on how to migrate from the previous version to the current version. Defaults to ${documentationUrl}-migrations",
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorReleasesRolloutConfiguration(BaseModel):
    """
    configuration for the rollout of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enable_progressive_rollout: Annotated[
        bool | None,
        Field(
            alias="enableProgressiveRollout",
            description="Whether to enable progressive rollout for the connector.",
        ),
    ] = False
    initial_percentage: Annotated[
        int | None,
        Field(
            alias="initialPercentage",
            description="The percentage of users that should receive the new version initially.",
            ge=0,
            le=100,
        ),
    ] = 0
    max_percentage: Annotated[
        int | None,
        Field(
            alias="maxPercentage",
            description="The percentage of users who should receive the release candidate during the test phase before full rollout.",
            ge=0,
            le=100,
        ),
    ] = 50
    advance_delay_minutes: Annotated[
        int | None,
        Field(
            alias="advanceDelayMinutes",
            description="The number of minutes to wait before advancing the rollout percentage.",
            ge=10,
        ),
    ] = 10


class ConnectorMetadataDefinitionV0DataConnectorSubtype(Enum):
    api = "api"
    database = "database"
    datalake = "datalake"
    file = "file"
    custom = "custom"
    message_queue = "message_queue"
    unknown = "unknown"
    vectorstore = "vectorstore"


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptions(BaseModel):
    """
    Options for a specific connector test suite.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    suite: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSuite,
        Field(description="Name of the configured test suite"),
    ]
    test_secrets: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecret] | None,
        Field(
            alias="testSecrets",
            description="List of secrets required to run the test suite",
        ),
    ] = None
    test_connections: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsTestConnections] | None,
        Field(
            alias="testConnections",
            description="List of sandbox cloud connections that tests can be run against",
        ),
    ] = None
    scenarios: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSmokeTestScenario] | None,
        Field(
            description="List of smoke test scenarios (only applicable when suite is 'smokeTests')"
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecret(BaseModel):
    """
    An object describing a secret's metadata
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[str, Field(description="The secret name in the secret store")]
    file_name: Annotated[
        str | None,
        Field(
            alias="fileName",
            description="The name of the file to which the secret value would be persisted",
        ),
    ] = None
    secret_store: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecretSecretStore,
        Field(
            alias="secretStore",
            description="An object describing a secret store metadata",
            title="SecretStore",
        ),
    ]


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecretSecretStore(BaseModel):
    """
    An object describing a secret store metadata
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    alias: Annotated[
        str | None,
        Field(
            description="The alias of the secret store which can map to its actual secret address"
        ),
    ] = None
    type: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecretSecretStoreType | None,
        Field(description="The type of the secret store"),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecretSecretStoreType(Enum):
    """
    The type of the secret store
    """

    gsm = "GSM"


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSmokeTestScenario(BaseModel):
    """
    A single smoke test scenario configuration for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[
        str,
        Field(
            description="Name of the test scenario (e.g., 'default', 'invalid_config', 'oauth_config')"
        ),
    ]
    config_file: Annotated[
        str | None,
        Field(
            alias="configFile",
            description="Relative path to the config file to use for this scenario",
        ),
    ] = None
    config_settings: Annotated[
        dict[str, Any] | None,
        Field(
            alias="configSettings",
            description="Optional dictionary of config settings to override or supplement configFile settings",
        ),
    ] = None
    expect_failure: Annotated[
        bool | None,
        Field(
            alias="expectFailure",
            description="Whether the scenario is expected to fail",
        ),
    ] = False
    only_streams: Annotated[
        list[str] | None,
        Field(
            alias="onlyStreams",
            description="List of stream names to include in the scenario (if specified, only these streams will be tested)",
        ),
    ] = None
    exclude_streams: Annotated[
        list[str] | None,
        Field(
            alias="excludeStreams",
            description="List of stream names to exclude from the scenario",
        ),
    ] = None
    suggested_streams_only: Annotated[
        bool | None,
        Field(
            alias="suggestedStreamsOnly",
            description="Whether to limit testing to the connector's suggested streams list (from data.suggestedStreams)",
        ),
    ] = False
    configured_catalog_path: Annotated[
        str | None,
        Field(
            alias="configuredCatalogPath",
            description="Path to a pre-configured catalog file for the scenario",
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSuite(Enum):
    """
    Name of the configured test suite
    """

    unit_tests = "unitTests"
    integration_tests = "integrationTests"
    acceptance_tests = "acceptanceTests"
    live_tests = "liveTests"
    smoke_tests = "smokeTests"


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsTestConnections(BaseModel):
    """
    List of sandbox cloud connections that tests can be run against
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[str, Field(description="The connection name")]
    id: Annotated[str, Field(description="The connection ID")]


class ConnectorMetadataDefinitionV0DataConnectorType(Enum):
    destination = "destination"
    source = "source"


class ConnectorMetadataDefinitionV0DataExternalDocumentationUrl(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    title: Annotated[str, Field(description="Display title for the documentation link")]
    url: Annotated[AnyUrl, Field(description="URL to the external documentation")]
    type: Annotated[
        ConnectorMetadataDefinitionV0DataExternalDocumentationUrlType | None,
        Field(description="Category of documentation"),
    ] = None
    requires_login: Annotated[
        bool | None,
        Field(
            alias="requiresLogin",
            description="Whether the URL requires authentication to access",
        ),
    ] = False


class ConnectorMetadataDefinitionV0DataExternalDocumentationUrlType(Enum):
    """
    Category of documentation
    """

    api_deprecations = "api_deprecations"
    api_reference = "api_reference"
    api_release_history = "api_release_history"
    authentication_guide = "authentication_guide"
    data_model_reference = "data_model_reference"
    developer_community = "developer_community"
    migration_guide = "migration_guide"
    openapi_spec = "openapi_spec"
    other = "other"
    permissions_scopes = "permissions_scopes"
    rate_limits = "rate_limits"
    sql_reference = "sql_reference"
    status_page = "status_page"


class ConnectorMetadataDefinitionV0DataGeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorMetadataDefinitionV0DataGeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorMetadataDefinitionV0DataGeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorMetadataDefinitionV0DataGeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbom_url: Annotated[str | None, Field(alias="sbomUrl", description="URL to the SBOM file")] = (
        None
    )


class ConnectorMetadataDefinitionV0DataGeneratedFieldsConnectorMetrics(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorMetadataDefinitionV0DataGeneratedFieldsGitInfo(BaseModel):
    """
    Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    commit_sha: Annotated[
        str | None,
        Field(description="The git commit sha of the last commit that modified this file."),
    ] = None
    commit_timestamp: Annotated[
        AwareDatetime | None,
        Field(description="The git commit timestamp of the last commit that modified this file."),
    ] = None
    commit_author: Annotated[
        str | None,
        Field(description="The git commit author of the last commit that modified this file."),
    ] = None
    commit_author_email: Annotated[
        str | None,
        Field(
            description="The git commit author email of the last commit that modified this file."
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataGeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class ConnectorMetadataDefinitionV0DataNormalizationDestinationDefinitionConfig(BaseModel):
    """
    describes a normalization config for destination definition
    """

    model_config = ConfigDict(
        extra="allow",
    )
    normalization_repository: Annotated[
        str,
        Field(
            alias="normalizationRepository",
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used.",
        ),
    ]
    normalization_tag: Annotated[
        str,
        Field(
            alias="normalizationTag",
            description="a field indicating the tag of the docker repository to be used for normalization.",
        ),
    ]
    normalization_integration_type: Annotated[
        str,
        Field(
            alias="normalizationIntegrationType",
            description="a field indicating the type of integration dialect to use for normalization.",
        ),
    ]


class ConnectorMetadataDefinitionV0DataRegistryOverrides(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    oss: ConnectorMetadataDefinitionV0DataRegistryOverridesRegistryOverrides | None = None
    cloud: ConnectorMetadataDefinitionV0RegistryOverrides | None = None


class ConnectorMetadataDefinitionV0DataRegistryOverridesRegistryOverrides(BaseModel):
    """
    describes the overrides per registry of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: bool
    name: str | None = None
    docker_repository: Annotated[str | None, Field(alias="dockerRepository")] = None
    docker_image_tag: Annotated[str | None, Field(alias="dockerImageTag")] = None
    supports_dbt: Annotated[bool | None, Field(alias="supportsDbt")] = None
    supports_normalization: Annotated[bool | None, Field(alias="supportsNormalization")] = None
    license: str | None = None
    documentation_url: Annotated[AnyUrl | None, Field(alias="documentationUrl")] = None
    connector_subtype: Annotated[str | None, Field(alias="connectorSubtype")] = None
    allowed_hosts: Annotated[AllowedHosts | None, Field(alias="allowedHosts")] = None
    normalization_config: Annotated[
        ConnectorMetadataDefinitionV0NormalizationDestinationDefinitionConfig | None,
        Field(alias="normalizationConfig"),
    ] = None
    suggested_streams: Annotated[SuggestedStreams | None, Field(alias="suggestedStreams")] = None
    resource_requirements: Annotated[
        ConnectorMetadataDefinitionV0ActorDefinitionResourceRequirements | None,
        Field(alias="resourceRequirements"),
    ] = None


class ConnectorMetadataDefinitionV0DataReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


class ConnectorMetadataDefinitionV0DataRemoteRegistries(BaseModel):
    """
    describes how the connector is published to remote registries
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    pypi: PyPi | None = None


class ConnectorMetadataDefinitionV0DataSuggestedStreams(BaseModel):
    """
    A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    streams: Annotated[
        list[str] | None,
        Field(
            description="An array of streams that this connector suggests the average user will want.  SuggestedStreams not being present for the source means that all streams are suggested.  An empty list here means that no streams are suggested."
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataSupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


class ConnectorMetadataDefinitionV0NormalizationDestinationDefinitionConfig(BaseModel):
    """
    describes a normalization config for destination definition
    """

    model_config = ConfigDict(
        extra="allow",
    )
    normalization_repository: Annotated[
        str,
        Field(
            alias="normalizationRepository",
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used.",
        ),
    ]
    normalization_tag: Annotated[
        str,
        Field(
            alias="normalizationTag",
            description="a field indicating the tag of the docker repository to be used for normalization.",
        ),
    ]
    normalization_integration_type: Annotated[
        str,
        Field(
            alias="normalizationIntegrationType",
            description="a field indicating the type of integration dialect to use for normalization.",
        ),
    ]


class ConnectorMetadataDefinitionV0RegistryOverrides(BaseModel):
    """
    describes the overrides per registry of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: bool
    name: str | None = None
    docker_repository: Annotated[str | None, Field(alias="dockerRepository")] = None
    docker_image_tag: Annotated[str | None, Field(alias="dockerImageTag")] = None
    supports_dbt: Annotated[bool | None, Field(alias="supportsDbt")] = None
    supports_normalization: Annotated[bool | None, Field(alias="supportsNormalization")] = None
    license: str | None = None
    documentation_url: Annotated[AnyUrl | None, Field(alias="documentationUrl")] = None
    connector_subtype: Annotated[str | None, Field(alias="connectorSubtype")] = None
    allowed_hosts: Annotated[AllowedHosts | None, Field(alias="allowedHosts")] = None
    normalization_config: Annotated[
        ConnectorMetadataDefinitionV0NormalizationDestinationDefinitionConfig | None,
        Field(alias="normalizationConfig"),
    ] = None
    suggested_streams: Annotated[SuggestedStreams | None, Field(alias="suggestedStreams")] = None
    resource_requirements: Annotated[
        ConnectorMetadataDefinitionV0ActorDefinitionResourceRequirements | None,
        Field(alias="resourceRequirements"),
    ] = None


class JobTypeResourceLimit(BaseModel):
    """
    sets resource requirements for a specific job type for an actor definition. these values override the default, if both are set.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    job_type: Annotated[
        JobTypeResourceLimitJobType,
        Field(
            alias="jobType",
            description="enum that describes the different types of jobs that the platform runs.",
            title="JobType",
        ),
    ]
    resource_requirements: Annotated[
        JobTypeResourceLimitResourceRequirements,
        Field(
            alias="resourceRequirements",
            description="generic configuration for pod source requirements",
            title="ResourceRequirements",
        ),
    ]


class JobTypeResourceLimitJobType(Enum):
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


class JobTypeResourceLimitResourceRequirements(BaseModel):
    """
    generic configuration for pod source requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    cpu_request: str | None = None
    cpu_limit: str | None = None
    memory_request: str | None = None
    memory_limit: str | None = None


class PyPi(BaseModel):
    """
    describes the PyPi publishing options
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: bool
    package_name: Annotated[
        str, Field(alias="packageName", description="The name of the package on PyPi.")
    ]


class ResourceRequirements(BaseModel):
    """
    generic configuration for pod source requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    cpu_request: str | None = None
    cpu_limit: str | None = None
    memory_request: str | None = None
    memory_limit: str | None = None


class StreamBreakingChangeScope(BaseModel):
    """
    A scope that can be used to limit the impact of a breaking change to specific streams.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    scope_type: Annotated[Literal["stream"], Field(alias="scopeType")]
    impacted_scopes: Annotated[
        list[str],
        Field(
            alias="impactedScopes",
            description="List of streams that are impacted by the breaking change.",
            min_length=1,
        ),
    ]


class BreakingChangeScope(RootModel[StreamBreakingChangeScope]):
    root: Annotated[
        StreamBreakingChangeScope,
        Field(description="A scope that can be used to limit the impact of a breaking change."),
    ]


class SuggestedStreams(BaseModel):
    """
    A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    streams: Annotated[
        list[str] | None,
        Field(
            description="An array of streams that this connector suggests the average user will want.  SuggestedStreams not being present for the source means that all streams are suggested.  An empty list here means that no streams are suggested."
        ),
    ] = None


class VersionBreakingChange(BaseModel):
    """
    Contains information about a breaking change, including the deadline to upgrade and a message detailing the change.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    upgrade_deadline: Annotated[
        date,
        Field(
            alias="upgradeDeadline",
            description="The deadline by which to upgrade before the breaking change takes effect.",
        ),
    ]
    message: Annotated[str, Field(description="Descriptive message detailing the breaking change.")]
    deadline_action: Annotated[
        VersionBreakingChangeDeadlineAction | None,
        Field(
            alias="deadlineAction",
            description="Action to do when the deadline is reached.",
        ),
    ] = None
    migration_documentation_url: Annotated[
        AnyUrl | None,
        Field(
            alias="migrationDocumentationUrl",
            description="URL to documentation on how to migrate to the current version. Defaults to ${documentationUrl}-migrations#${version}",
        ),
    ] = None
    scoped_impact: Annotated[
        list[BreakingChangeScope] | None,
        Field(
            alias="scopedImpact",
            description="List of scopes that are impacted by the breaking change. If not specified, the breaking change cannot be scoped to reduce impact via the supported scope types.",
            min_length=1,
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorReleasesConnectorBreakingChanges(
    RootModel[dict[str, VersionBreakingChange]]
):
    root: Annotated[
        dict[str, VersionBreakingChange],
        Field(
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ]


class VersionBreakingChangeDeadlineAction(Enum):
    """
    Action to do when the deadline is reached.
    """

    auto_upgrade = "auto_upgrade"
    disable = "disable"
