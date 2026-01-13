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


class ConnectorRegistryV0(BaseModel):
    """
    describes the collection of connectors retrieved from a registry
    """

    destinations: list[ConnectorRegistryV0ConnectorRegistryDestinationDefinition]
    sources: list[ConnectorRegistryV0ConnectorRegistrySourceDefinition]


class ConnectorRegistryV0ActorDefinitionResourceRequirements(BaseModel):
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


class ConnectorRegistryV0AirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorRegistryV0AirbyteInternalSl | None = None
    ql: ConnectorRegistryV0AirbyteInternalQl | None = None
    isEnterprise: bool | None = False
    requireVersionIncrementsInPullRequests: Annotated[
        bool | None,
        Field(
            description="When false, version increment checks will be skipped for this connector"
        ),
    ] = True


class ConnectorRegistryV0AirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorRegistryV0AirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorRegistryV0ConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None


class ConnectorRegistryV0ConnectorRegistryDestinationDefinition(BaseModel):
    """
    describes a destination
    """

    model_config = ConfigDict(
        extra="allow",
    )
    destinationDefinitionId: UUID
    name: str
    dockerRepository: str
    dockerImageTag: str
    documentationUrl: str
    icon: str | None = None
    iconUrl: str | None = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    releaseStage: ReleaseStage | None = None
    supportLevel: SupportLevel | None = None
    releaseDate: Annotated[
        date | None,
        Field(description="The date when this connector was first released, in yyyy-mm-dd format."),
    ] = None
    tags: Annotated[
        list[str] | None,
        Field(
            description="An array of tags that describe the connector. E.g: language:python, keyword:rds, etc."
        ),
    ] = None
    resourceRequirements: ConnectorRegistryV0ActorDefinitionResourceRequirements | None = None
    protocolVersion: Annotated[
        str | None,
        Field(description="the Airbyte Protocol version supported by the connector"),
    ] = None
    normalizationConfig: Annotated[
        ConnectorRegistryV0ConnectorRegistryDestinationDefinitionNormalizationDestinationDefinitionConfig
        | None,
        Field(
            description="describes a normalization config for destination definition",
            title="NormalizationDestinationDefinitionConfig",
        ),
    ] = None
    supportsDbt: Annotated[
        bool | None,
        Field(
            description="an optional flag indicating whether DBT is used in the normalization. If the flag value is NULL - DBT is not used."
        ),
    ] = None
    allowedHosts: AllowedHosts | None = None
    releases: ConnectorRegistryV0ConnectorRegistryReleases | None = None
    ab_internal: ConnectorRegistryV0AirbyteInternal | None = None
    supportsRefreshes: bool | None = False
    supportsFileTransfer: bool | None = False
    supportsDataActivation: bool | None = False
    generated: ConnectorRegistryV0GeneratedFields | None = None
    packageInfo: ConnectorRegistryV0ConnectorPackageInfo | None = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None


class ConnectorRegistryV0ConnectorRegistryDestinationDefinition1(BaseModel):
    """
    describes a destination
    """

    model_config = ConfigDict(
        extra="allow",
    )
    destinationDefinitionId: UUID
    name: str
    dockerRepository: str
    dockerImageTag: str
    documentationUrl: str
    icon: str | None = None
    iconUrl: str | None = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    releaseStage: ReleaseStage | None = None
    supportLevel: SupportLevel | None = None
    releaseDate: Annotated[
        date | None,
        Field(description="The date when this connector was first released, in yyyy-mm-dd format."),
    ] = None
    tags: Annotated[
        list[str] | None,
        Field(
            description="An array of tags that describe the connector. E.g: language:python, keyword:rds, etc."
        ),
    ] = None
    resourceRequirements: ConnectorRegistryV0ActorDefinitionResourceRequirements | None = None
    protocolVersion: Annotated[
        str | None,
        Field(description="the Airbyte Protocol version supported by the connector"),
    ] = None
    normalizationConfig: Annotated[
        ConnectorRegistryV0ConnectorRegistryDestinationDefinition1NormalizationDestinationDefinitionConfig
        | None,
        Field(
            description="describes a normalization config for destination definition",
            title="NormalizationDestinationDefinitionConfig",
        ),
    ] = None
    supportsDbt: Annotated[
        bool | None,
        Field(
            description="an optional flag indicating whether DBT is used in the normalization. If the flag value is NULL - DBT is not used."
        ),
    ] = None
    allowedHosts: AllowedHosts | None = None
    releases: ConnectorRegistryV0ConnectorRegistryReleases | None = None
    ab_internal: ConnectorRegistryV0AirbyteInternal | None = None
    supportsRefreshes: bool | None = False
    supportsFileTransfer: bool | None = False
    supportsDataActivation: bool | None = False
    generated: ConnectorRegistryV0GeneratedFields | None = None
    packageInfo: ConnectorRegistryV0ConnectorPackageInfo | None = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None


class ConnectorRegistryV0ConnectorRegistryDestinationDefinition1NormalizationDestinationDefinitionConfig(
    BaseModel
):
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


class ConnectorRegistryV0ConnectorRegistryDestinationDefinitionNormalizationDestinationDefinitionConfig(
    BaseModel
):
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


class ConnectorRegistryV0ConnectorRegistryReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    releaseCandidates: ConnectorReleaseCandidates | None = None
    rolloutConfiguration: Annotated[
        ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfiguration | None,
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


class ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfiguration(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition(BaseModel):
    """
    describes a source
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sourceDefinitionId: UUID
    name: str
    dockerRepository: str
    dockerImageTag: str
    documentationUrl: str
    icon: str | None = None
    iconUrl: str | None = None
    sourceType: ConnectorRegistryV0ConnectorRegistrySourceDefinitionSourceType | None = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    releaseStage: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionReleaseStage | None,
        Field(
            description="enum that describes a connector's release stage",
            title="ReleaseStage",
        ),
    ] = None
    supportLevel: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionSupportLevel | None,
        Field(
            description="enum that describes a connector's release stage",
            title="SupportLevel",
        ),
    ] = None
    releaseDate: Annotated[
        date | None,
        Field(description="The date when this connector was first released, in yyyy-mm-dd format."),
    ] = None
    resourceRequirements: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionActorDefinitionResourceRequirements
        | None,
        Field(
            description="actor definition specific resource requirements",
            title="ActorDefinitionResourceRequirements",
        ),
    ] = None
    protocolVersion: Annotated[
        str | None,
        Field(description="the Airbyte Protocol version supported by the connector"),
    ] = None
    allowedHosts: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionAllowedHosts | None,
        Field(
            description="A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.",
            title="AllowedHosts",
        ),
    ] = None
    suggestedStreams: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionSuggestedStreams | None,
        Field(
            description="A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.",
            title="SuggestedStreams",
        ),
    ] = None
    maxSecondsBetweenMessages: Annotated[
        int | None,
        Field(
            description="Number of seconds allowed between 2 airbyte protocol messages. The source will timeout if this delay is reach"
        ),
    ] = None
    erdUrl: Annotated[str | None, Field(description="The URL where you can visualize the ERD")] = (
        None
    )
    releases: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleases | None,
        Field(
            description="Contains information about different types of releases for a connector.",
            title="ConnectorRegistryReleases",
        ),
    ] = None
    ab_internal: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternal | None,
        Field(description="Fields for internal use only", title="AirbyteInternal"),
    ] = None
    generated: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFields | None,
        Field(
            description="Optional schema for fields generated at metadata upload time",
            title="GeneratedFields",
        ),
    ] = None
    packageInfo: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorPackageInfo | None,
        Field(
            description="Information about the contents of the connector image",
            title="ConnectorPackageInfo",
        ),
    ] = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None
    supportsFileTransfer: bool | None = False
    supportsDataActivation: bool | None = False


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1(BaseModel):
    """
    describes a source
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sourceDefinitionId: UUID
    name: str
    dockerRepository: str
    dockerImageTag: str
    documentationUrl: str
    icon: str | None = None
    iconUrl: str | None = None
    sourceType: ConnectorRegistryV0ConnectorRegistrySourceDefinition1SourceType | None = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    releaseStage: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ReleaseStage | None,
        Field(
            description="enum that describes a connector's release stage",
            title="ReleaseStage",
        ),
    ] = None
    supportLevel: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1SupportLevel | None,
        Field(
            description="enum that describes a connector's release stage",
            title="SupportLevel",
        ),
    ] = None
    releaseDate: Annotated[
        date | None,
        Field(description="The date when this connector was first released, in yyyy-mm-dd format."),
    ] = None
    resourceRequirements: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ActorDefinitionResourceRequirements
        | None,
        Field(
            description="actor definition specific resource requirements",
            title="ActorDefinitionResourceRequirements",
        ),
    ] = None
    protocolVersion: Annotated[
        str | None,
        Field(description="the Airbyte Protocol version supported by the connector"),
    ] = None
    allowedHosts: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1AllowedHosts | None,
        Field(
            description="A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.",
            title="AllowedHosts",
        ),
    ] = None
    suggestedStreams: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1SuggestedStreams | None,
        Field(
            description="A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.",
            title="SuggestedStreams",
        ),
    ] = None
    maxSecondsBetweenMessages: Annotated[
        int | None,
        Field(
            description="Number of seconds allowed between 2 airbyte protocol messages. The source will timeout if this delay is reach"
        ),
    ] = None
    erdUrl: Annotated[str | None, Field(description="The URL where you can visualize the ERD")] = (
        None
    )
    releases: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleases | None,
        Field(
            description="Contains information about different types of releases for a connector.",
            title="ConnectorRegistryReleases",
        ),
    ] = None
    ab_internal: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternal | None,
        Field(description="Fields for internal use only", title="AirbyteInternal"),
    ] = None
    generated: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFields | None,
        Field(
            description="Optional schema for fields generated at metadata upload time",
            title="GeneratedFields",
        ),
    ] = None
    packageInfo: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorPackageInfo | None,
        Field(
            description="Information about the contents of the connector image",
            title="ConnectorPackageInfo",
        ),
    ] = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None
    supportsFileTransfer: bool | None = False
    supportsDataActivation: bool | None = False


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ActorDefinitionResourceRequirements(
    BaseModel
):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalSl | None = None
    ql: ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalQl | None = None
    isEnterprise: bool | None = False
    requireVersionIncrementsInPullRequests: Annotated[
        bool | None,
        Field(
            description="When false, version increment checks will be skipped for this connector"
        ),
    ] = True


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AllowedHosts(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    releaseCandidates: ConnectorReleaseCandidates | None = None
    rolloutConfiguration: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfiguration
        | None,
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfiguration(
    BaseModel
):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbomUrl: Annotated[str | None, Field(description="URL to the SBOM file")] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsConnectorMetrics(
    BaseModel
):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsGitInfo(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1SourceType(Enum):
    api = "api"
    file = "file"
    database = "database"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1SuggestedStreams(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1SupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionActorDefinitionResourceRequirements(
    BaseModel
):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalSl | None = None
    ql: ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalQl | None = None
    isEnterprise: bool | None = False
    requireVersionIncrementsInPullRequests: Annotated[
        bool | None,
        Field(
            description="When false, version increment checks will be skipped for this connector"
        ),
    ] = True


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAllowedHosts(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    releaseCandidates: ConnectorReleaseCandidates | None = None
    rolloutConfiguration: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfiguration
        | None,
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfiguration(
    BaseModel
):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbomUrl: Annotated[str | None, Field(description="URL to the SBOM file")] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsConnectorMetrics(
    BaseModel
):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsGitInfo(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionSourceType(Enum):
    api = "api"
    file = "file"
    database = "database"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionSuggestedStreams(BaseModel):
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


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionSupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


class ConnectorRegistryV0GeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorRegistryV0GeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorRegistryV0GeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorRegistryV0GeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbomUrl: Annotated[str | None, Field(description="URL to the SBOM file")] = None


class ConnectorRegistryV0GeneratedFieldsConnectorMetrics(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorRegistryV0GeneratedFieldsGitInfo(BaseModel):
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


class ConnectorRegistryV0GeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class ConnectorReleaseCandidates(RootModel[dict[str, VersionReleaseCandidate]]):
    root: Annotated[
        dict[str, VersionReleaseCandidate],
        Field(description="Each entry denotes a release candidate version of a connector."),
    ]


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


class ReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


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


class SupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


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


class VersionReleaseCandidate(
    RootModel[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1
        | ConnectorRegistryV0ConnectorRegistryDestinationDefinition1
    ]
):
    root: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1
        | ConnectorRegistryV0ConnectorRegistryDestinationDefinition1,
        Field(description="Contains information about a release candidate version of a connector."),
    ]


ConnectorRegistryV0ConnectorRegistryDestinationDefinition.model_rebuild()
ConnectorRegistryV0ConnectorRegistryReleases.model_rebuild()
ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleases.model_rebuild()
ConnectorReleaseCandidates.model_rebuild()
VersionReleaseCandidate.model_rebuild()
