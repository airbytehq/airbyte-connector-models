# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict


class ConnectorIPCOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    dataChannel: ConnectorIPCOptionsDataChannel


class ConnectorIPCOptionsDataChannel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    version: str
    supportedSerialization: list[ConnectorIPCOptionsDataChannelSupportedSerializationEnum]
    supportedTransport: list[ConnectorIPCOptionsDataChannelSupportedTransportEnum]


class ConnectorIPCOptionsDataChannelSupportedSerializationEnum(Enum):
    JSONL = "JSONL"
    PROTOBUF = "PROTOBUF"
    FLATBUFFERS = "FLATBUFFERS"


class ConnectorIPCOptionsDataChannelSupportedTransportEnum(Enum):
    STDIO = "STDIO"
    SOCKET = "SOCKET"
