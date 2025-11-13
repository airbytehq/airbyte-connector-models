# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, RootModel

from airbyte_connector_models._internal.base_record import BaseRecordModel


class Ability(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    ability: Ability1 | None = None
    is_hidden: bool | None = None
    slot: int | None = None


class Ability1(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class Form(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class GameIndice(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    version: Version | None = None
    game_index: int | None = None


class Generation(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class HeldItem(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    item: Item | None = None
    version_details: list[VersionDetail | None] | None = None


class Item(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class Model(RootModel[Any]):
    root: Any


class Move(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    move: Move1 | None = None
    version_group_details: list[VersionGroupDetail | None] | None = None


class Move1(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class MoveLearnMethod(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PastType(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    generation: Generation | None = None
    types: list[Type | None] | None = None


class PokeapiPokemonRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    abilities: list[Ability | None] | None = None
    base_experience: int | None = None
    forms: list[Form | None] | None = None
    game_indices: list[GameIndice | None] | None = None
    height: int | None = None
    held_items: list[HeldItem | None] | None = None
    id: int | None = None
    is_default: bool | None = None
    location_area_encounters: str | None = None
    moves: list[Move | None] | None = None
    name: str | None = None
    order: int | None = None
    past_types: list[PastType | None] | None = None
    species: Species | None = None
    sprites: Sprites | None = None
    stats: list[Stat | None] | None = None
    types: list[Type2 | None] | None = None
    weight: int | None = None


class Species(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class Sprites(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    back_default: str | None = None
    back_female: str | None = None
    back_shiny: str | None = None
    back_shiny_female: str | None = None
    front_default: str | None = None
    front_female: str | None = None
    front_shiny: str | None = None
    front_shiny_female: str | None = None


class Stat(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    base_stat: int | None = None
    effort: int | None = None
    stat: Stat1 | None = None


class Stat1(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class Type(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: Type1 | None = None
    slot: int | None = None


class Type1(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class Type2(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: Type3 | None = None
    slot: int | None = None


class Type3(BaseRecordModel):
    name: str | None = None
    url: str | None = None


class Version(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class VersionDetail(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    version: Version | None = None
    rarity: int | None = None


class VersionGroup(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class VersionGroupDetail(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    level_learned_at: int | None = None
    move_learn_method: MoveLearnMethod | None = None
    version_group: VersionGroup | None = None
