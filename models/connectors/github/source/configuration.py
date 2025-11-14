# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AwareDatetime, ConfigDict, Field, RootModel

from models.connectors._internal.base_config import BaseConfig


class SourceGithubConfigSpec(BaseConfig):
    model_config = ConfigDict(
        extra="allow",
        regex_engine="python-re",
    )
    credentials: Annotated[
        SourceGithubConfigSpecOAuth | SourceGithubConfigSpecPersonalAccessToken,
        Field(description="Choose how to authenticate to GitHub", title="Authentication"),
    ]
    repository: Annotated[
        str | None,
        Field(
            description="(DEPRCATED) Space-delimited list of GitHub organizations/repositories, e.g. `airbytehq/airbyte` for single repository, `airbytehq/*` for get all repositories from organization and `airbytehq/airbyte airbytehq/another-repo` for multiple repositories.",
            examples=[
                "airbytehq/airbyte airbytehq/another-repo",
                "airbytehq/*",
                "airbytehq/airbyte",
            ],
            pattern="^([\\w.-]+/(\\*|[\\w.-]+(?<!\\.git))\\s+)*[\\w.-]+/(\\*|[\\w.-]+(?<!\\.git))$",
            title="GitHub Repositories",
        ),
    ] = None
    repositories: Annotated[
        list[SourceGithubConfigSpecGitHubRepository],
        Field(
            description="List of GitHub organizations/repositories, e.g. `airbytehq/airbyte` for single repository, `airbytehq/*` for get all repositories from organization and `airbytehq/a* for matching multiple repositories by pattern.",
            examples=[
                "airbytehq/airbyte",
                "airbytehq/another-repo",
                "airbytehq/*",
                "airbytehq/a*",
            ],
            min_length=1,
            title="GitHub Repositories",
        ),
    ]
    start_date: Annotated[
        AwareDatetime | None,
        Field(
            description="The date from which you'd like to replicate data from GitHub in the format YYYY-MM-DDT00:00:00Z. If the date is not set, all data will be replicated.  For the streams which support this configuration, only data generated on or after the start date will be replicated. This field doesn't apply to all streams, see the <a href=\"https://docs.airbyte.com/integrations/sources/github\">docs</a> for more info",
            examples=["2021-03-01T00:00:00Z"],
            pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$",
            title="Start date",
        ),
    ] = None
    api_url: Annotated[
        str | None,
        Field(
            description="Please enter your basic URL from self-hosted GitHub instance or leave it empty to use GitHub.",
            examples=["https://github.com", "https://github.company.org"],
            title="API URL",
        ),
    ] = "https://api.github.com/"
    branch: Annotated[
        str | None,
        Field(
            description="(DEPRCATED) Space-delimited list of GitHub repository branches to pull commits for, e.g. `airbytehq/airbyte/master`. If no branches are specified for a repository, the default branch will be pulled.",
            examples=["airbytehq/airbyte/master airbytehq/airbyte/my-branch"],
            title="Branch",
        ),
    ] = None
    branches: Annotated[
        list[str] | None,
        Field(
            description="List of GitHub repository branches to pull commits for, e.g. `airbytehq/airbyte/master`. If no branches are specified for a repository, the default branch will be pulled.",
            examples=["airbytehq/airbyte/master", "airbytehq/airbyte/my-branch"],
            title="Branches",
        ),
    ] = None
    max_waiting_time: Annotated[
        int | None,
        Field(
            description="Max Waiting Time for rate limit. Set higher value to wait till rate limits will be resetted to continue sync",
            examples=[10, 30, 60],
            ge=1,
            le=60,
            title="Max Waiting Time (in minutes)",
        ),
    ] = 10


class SourceGithubConfigSpecGitHubRepository(RootModel[str]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: Annotated[str, Field(pattern="^[\\w.-]+/(([\\w.-]*\\*)|[\\w.-]+(?<!\\.git))$")]


class SourceGithubConfigSpecOAuth(BaseConfig):
    """
    Choose how to authenticate to GitHub
    """

    option_title: Literal["OAuth Credentials"] = "OAuth Credentials"
    access_token: Annotated[str, Field(description="OAuth access token", title="Access Token")]
    client_id: Annotated[str | None, Field(description="OAuth Client Id", title="Client Id")] = None
    client_secret: Annotated[
        str | None, Field(description="OAuth Client secret", title="Client secret")
    ] = None


class SourceGithubConfigSpecPersonalAccessToken(BaseConfig):
    """
    Choose how to authenticate to GitHub
    """

    option_title: Literal["PAT Credentials"] = "PAT Credentials"
    personal_access_token: Annotated[
        str,
        Field(
            description='Log into GitHub and then generate a <a href="https://github.com/settings/tokens">personal access token</a>. To load balance your API quota consumption across multiple API tokens, input multiple tokens separated with ","',
            title="Personal Access Tokens",
        ),
    ]
