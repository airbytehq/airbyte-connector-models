# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from datetime import date
from enum import Enum
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


# Defined above BreakingChangeScope which depends on it.
class StreamBreakingChangeScope(BaseModel):
    """
    A scope that can be used to limit the impact of a breaking change to specific streams.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    scopeType: Literal["stream"]
    impactedScopes: Annotated[
        list[str],
        Field(
            description="List of streams that are impacted by the breaking change.",
            min_length=1,
        ),
    ]


class BreakingChangeScope(RootModel[StreamBreakingChangeScope]):
    root: Annotated[
        StreamBreakingChangeScope,
        Field(description="A scope that can be used to limit the impact of a breaking change."),
    ]


class ConnectorMetadataDefinitionV0(BaseModel):
    """
    describes the metadata of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    metadataSpecVersion: str
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
    jobSpecific: list[JobTypeResourceLimit] | None = None


class ConnectorMetadataDefinitionV0Data(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: str
    icon: str | None = None
    definitionId: UUID
    connectorBuildOptions: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorBuildOptions | None,
        Field(
            description="metadata specific to the build process.",
            title="ConnectorBuildOptions",
        ),
    ] = None
    connectorTestSuitesOptions: (
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptions] | None
    ) = None
    connectorType: ConnectorMetadataDefinitionV0DataConnectorType
    dockerRepository: str
    dockerImageTag: str
    supportsDbt: bool | None = None
    supportsNormalization: bool | None = None
    license: str
    documentationUrl: AnyUrl
    externalDocumentationUrls: Annotated[
        list[ConnectorMetadataDefinitionV0DataExternalDocumentationUrl] | None,
        Field(
            description="An array of external vendor documentation URLs (changelogs, API references, deprecation notices, etc.)"
        ),
    ] = None
    githubIssueLabel: str
    maxSecondsBetweenMessages: Annotated[
        int | None,
        Field(
            description="Maximum delay between 2 airbyte protocol messages, in second. The source will timeout if this delay is reached"
        ),
    ] = None
    releaseDate: Annotated[
        date | None,
        Field(description="The date when this connector was first released, in yyyy-mm-dd format."),
    ] = None
    protocolVersion: Annotated[
        str | None,
        Field(description="the Airbyte Protocol version supported by the connector"),
    ] = None
    erdUrl: Annotated[str | None, Field(description="The URL where you can visualize the ERD")] = (
        None
    )
    connectorSubtype: ConnectorMetadataDefinitionV0DataConnectorSubtype
    releaseStage: Annotated[
        ConnectorMetadataDefinitionV0DataReleaseStage,
        Field(
            description="enum that describes a connector's release stage",
            title="ReleaseStage",
        ),
    ]
    supportLevel: Annotated[
        ConnectorMetadataDefinitionV0DataSupportLevel | None,
        Field(
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
    registryOverrides: ConnectorMetadataDefinitionV0DataRegistryOverrides | None = None
    allowedHosts: Annotated[
        ConnectorMetadataDefinitionV0DataAllowedHosts | None,
        Field(
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
    normalizationConfig: Annotated[
        ConnectorMetadataDefinitionV0DataNormalizationDestinationDefinitionConfig | None,
        Field(
            description="describes a normalization config for destination definition",
            title="NormalizationDestinationDefinitionConfig",
        ),
    ] = None
    suggestedStreams: Annotated[
        ConnectorMetadataDefinitionV0DataSuggestedStreams | None,
        Field(
            description="A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.",
            title="SuggestedStreams",
        ),
    ] = None
    resourceRequirements: Annotated[
        ConnectorMetadataDefinitionV0DataActorDefinitionResourceRequirements | None,
        Field(
            description="actor definition specific resource requirements",
            title="ActorDefinitionResourceRequirements",
        ),
    ] = None
    ab_internal: Annotated[
        ConnectorMetadataDefinitionV0DataAirbyteInternal | None,
        Field(description="Fields for internal use only", title="AirbyteInternal"),
    ] = None
    remoteRegistries: Annotated[
        ConnectorMetadataDefinitionV0DataRemoteRegistries | None,
        Field(
            description="describes how the connector is published to remote registries",
            title="RemoteRegistries",
        ),
    ] = None
    supportsRefreshes: bool | None = False
    generated: Annotated[
        ConnectorMetadataDefinitionV0DataGeneratedFields | None,
        Field(
            description="Optional schema for fields generated at metadata upload time",
            title="GeneratedFields",
        ),
    ] = None
    supportsFileTransfer: bool | None = False
    supportsDataActivation: bool | None = False
    connectorIPCOptions: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorIPCOptions | None,
        Field(title="ConnectorIPCOptions"),
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
    jobSpecific: list[JobTypeResourceLimit] | None = None


class ConnectorMetadataDefinitionV0DataAirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorMetadataDefinitionV0DataAirbyteInternalSl | None = None
    ql: ConnectorMetadataDefinitionV0DataAirbyteInternalQl | None = None
    isEnterprise: bool | None = False
    requireVersionIncrementsInPullRequests: Annotated[
        bool | None,
        Field(
            description="When false, version increment checks will be skipped for this connector"
        ),
    ] = True


class ConnectorMetadataDefinitionV0DataAirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorMetadataDefinitionV0DataAirbyteInternalSl(Enum):
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
    baseImage: str | None = None


class ConnectorMetadataDefinitionV0DataConnectorIPCOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dataChannel: ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannel


class ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    version: str
    supportedSerialization: list[
        ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedSerializationEnum
    ]
    supportedTransport: list[
        ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedTransportEnum
    ]


class ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedSerializationEnum(
    Enum
):
    JSONL = "JSONL"
    PROTOBUF = "PROTOBUF"
    FLATBUFFERS = "FLATBUFFERS"


class ConnectorMetadataDefinitionV0DataConnectorIPCOptionsDataChannelSupportedTransportEnum(Enum):
    STDIO = "STDIO"
    SOCKET = "SOCKET"


class ConnectorMetadataDefinitionV0DataConnectorReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    rolloutConfiguration: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorReleasesRolloutConfiguration | None,
        Field(
            description="configuration for the rollout of a connector",
            title="RolloutConfiguration",
        ),
    ] = None
    breakingChanges: Annotated[
        dict[str, VersionBreakingChange] | None,
        Field(
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ] = None
    migrationDocumentationUrl: Annotated[
        AnyUrl | None,
        Field(
            description="URL to documentation on how to migrate from the previous version to the current version. Defaults to ${documentationUrl}-migrations"
        ),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorReleasesRolloutConfiguration(BaseModel):
    """
    configuration for the rollout of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enableProgressiveRollout: Annotated[
        bool | None,
        Field(description="Whether to enable progressive rollout for the connector."),
    ] = False
    initialPercentage: Annotated[
        int | None,
        Field(
            description="The percentage of users that should receive the new version initially.",
            ge=0,
            le=100,
        ),
    ] = 0
    maxPercentage: Annotated[
        int | None,
        Field(
            description="The percentage of users who should receive the release candidate during the test phase before full rollout.",
            ge=0,
            le=100,
        ),
    ] = 50
    advanceDelayMinutes: Annotated[
        int | None,
        Field(
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
    testSecrets: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecret] | None,
        Field(description="List of secrets required to run the test suite"),
    ] = None
    testConnections: Annotated[
        list[ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsTestConnections] | None,
        Field(description="List of sandbox cloud connections that tests can be run against"),
    ] = None


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecret(BaseModel):
    """
    An object describing a secret's metadata
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[str, Field(description="The secret name in the secret store")]
    fileName: Annotated[
        str | None,
        Field(description="The name of the file to which the secret value would be persisted"),
    ] = None
    secretStore: Annotated[
        ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSecretSecretStore,
        Field(
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

    GSM = "GSM"


class ConnectorMetadataDefinitionV0DataConnectorTestSuiteOptionsSuite(Enum):
    """
    Name of the configured test suite
    """

    unitTests = "unitTests"
    integrationTests = "integrationTests"
    acceptanceTests = "acceptanceTests"
    liveTests = "liveTests"


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
        Field(
            description="Category of documentation (api_release_history, api_reference, api_deprecations, or other)"
        ),
    ] = None
    requiresLogin: Annotated[
        bool | None,
        Field(description="Whether the URL requires authentication to access"),
    ] = False


class ConnectorMetadataDefinitionV0DataExternalDocumentationUrlType(Enum):
    """
    Category of documentation (api_release_history, api_reference, api_deprecations, or other)
    """

    api_release_history = "api_release_history"
    api_reference = "api_reference"
    api_deprecations = "api_deprecations"
    other = "other"


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
    sbomUrl: Annotated[str | None, Field(description="URL to the SBOM file")] = None


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
    normalizationRepository: Annotated[
        str,
        Field(
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used."
        ),
    ]
    normalizationTag: Annotated[
        str,
        Field(
            description="a field indicating the tag of the docker repository to be used for normalization."
        ),
    ]
    normalizationIntegrationType: Annotated[
        str,
        Field(
            description="a field indicating the type of integration dialect to use for normalization."
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
    dockerRepository: str | None = None
    dockerImageTag: str | None = None
    supportsDbt: bool | None = None
    supportsNormalization: bool | None = None
    license: str | None = None
    documentationUrl: AnyUrl | None = None
    connectorSubtype: str | None = None
    allowedHosts: AllowedHosts | None = None
    normalizationConfig: (
        ConnectorMetadataDefinitionV0NormalizationDestinationDefinitionConfig | None
    ) = None
    suggestedStreams: SuggestedStreams | None = None
    resourceRequirements: (
        ConnectorMetadataDefinitionV0ActorDefinitionResourceRequirements | None
    ) = None


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
    normalizationRepository: Annotated[
        str,
        Field(
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used."
        ),
    ]
    normalizationTag: Annotated[
        str,
        Field(
            description="a field indicating the tag of the docker repository to be used for normalization."
        ),
    ]
    normalizationIntegrationType: Annotated[
        str,
        Field(
            description="a field indicating the type of integration dialect to use for normalization."
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
    dockerRepository: str | None = None
    dockerImageTag: str | None = None
    supportsDbt: bool | None = None
    supportsNormalization: bool | None = None
    license: str | None = None
    documentationUrl: AnyUrl | None = None
    connectorSubtype: str | None = None
    allowedHosts: AllowedHosts | None = None
    normalizationConfig: (
        ConnectorMetadataDefinitionV0NormalizationDestinationDefinitionConfig | None
    ) = None
    suggestedStreams: SuggestedStreams | None = None
    resourceRequirements: (
        ConnectorMetadataDefinitionV0ActorDefinitionResourceRequirements | None
    ) = None


class JobTypeResourceLimit(BaseModel):
    """
    sets resource requirements for a specific job type for an actor definition. these values override the default, if both are set.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    jobType: Annotated[
        JobTypeResourceLimitJobType,
        Field(
            description="enum that describes the different types of jobs that the platform runs.",
            title="JobType",
        ),
    ]
    resourceRequirements: Annotated[
        JobTypeResourceLimitResourceRequirements,
        Field(
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
    packageName: Annotated[str, Field(description="The name of the package on PyPi.")]


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
    upgradeDeadline: Annotated[
        date,
        Field(
            description="The deadline by which to upgrade before the breaking change takes effect."
        ),
    ]
    message: Annotated[str, Field(description="Descriptive message detailing the breaking change.")]
    deadlineAction: Annotated[
        VersionBreakingChangeDeadlineAction | None,
        Field(description="Action to do when the deadline is reached."),
    ] = None
    migrationDocumentationUrl: Annotated[
        AnyUrl | None,
        Field(
            description="URL to documentation on how to migrate to the current version. Defaults to ${documentationUrl}-migrations#${version}"
        ),
    ] = None
    scopedImpact: Annotated[
        list[BreakingChangeScope] | None,
        Field(
            description="List of scopes that are impacted by the breaking change. If not specified, the breaking change cannot be scoped to reduce impact via the supported scope types.",
            min_length=1,
        ),
    ] = None


class VersionBreakingChangeDeadlineAction(Enum):
    """
    Action to do when the deadline is reached.
    """

    auto_upgrade = "auto_upgrade"
    disable = "disable"
