# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from pydantic import ConfigDict

from models.connectors._internal.base_record import BaseRecordModel


class PokeapiPokemonRecord(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    abilities: list[PokeapiPokemonRecordAbility | None] | None = None
    base_experience: int | None = None
    forms: list[PokeapiPokemonRecordForm | None] | None = None
    game_indices: list[PokeapiPokemonRecordGameIndice | None] | None = None
    height: int | None = None
    held_items: list[PokeapiPokemonRecordHeldItem | None] | None = None
    id: int | None = None
    is_default: bool | None = None
    location_area_encounters: str | None = None
    moves: list[PokeapiPokemonRecordMove | None] | None = None
    name: str | None = None
    order: int | None = None
    past_types: list[PokeapiPokemonRecordPastType | None] | None = None
    species: PokeapiPokemonRecordSpecies | None = None
    sprites: PokeapiPokemonRecordSprites | None = None
    stats: list[PokeapiPokemonRecordStat | None] | None = None
    types: list[PokeapiPokemonRecordType | None] | None = None
    weight: int | None = None


class PokeapiPokemonRecordAbility(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    ability: PokeapiPokemonRecordAbilityAbility | None = None
    is_hidden: bool | None = None
    slot: int | None = None


class PokeapiPokemonRecordAbilityAbility(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordForm(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordGameIndice(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    version: PokeapiPokemonRecordGameIndiceVersion | None = None
    game_index: int | None = None


class PokeapiPokemonRecordGameIndiceVersion(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordHeldItem(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    item: PokeapiPokemonRecordHeldItemItem | None = None
    version_details: list[PokeapiPokemonRecordHeldItemVersionDetail | None] | None = None


class PokeapiPokemonRecordHeldItemItem(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordHeldItemVersionDetail(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    version: PokeapiPokemonRecordHeldItemVersionDetailVersion | None = None
    rarity: int | None = None


class PokeapiPokemonRecordHeldItemVersionDetailVersion(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordMove(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    move: PokeapiPokemonRecordMoveMove | None = None
    version_group_details: list[PokeapiPokemonRecordMoveVersionGroupDetail | None] | None = None


class PokeapiPokemonRecordMoveMove(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordMoveVersionGroupDetail(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    level_learned_at: int | None = None
    move_learn_method: PokeapiPokemonRecordMoveVersionGroupDetailMoveLearnMethod | None = None
    version_group: PokeapiPokemonRecordMoveVersionGroupDetailVersionGroup | None = None


class PokeapiPokemonRecordMoveVersionGroupDetailMoveLearnMethod(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordMoveVersionGroupDetailVersionGroup(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordPastType(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    generation: PokeapiPokemonRecordPastTypeGeneration | None = None
    types: list[PokeapiPokemonRecordPastTypeType | None] | None = None


class PokeapiPokemonRecordPastTypeGeneration(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordPastTypeType(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: PokeapiPokemonRecordPastTypeTypeType | None = None
    slot: int | None = None


class PokeapiPokemonRecordPastTypeTypeType(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordSpecies(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordSprites(BaseRecordModel):
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


class PokeapiPokemonRecordStat(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    base_stat: int | None = None
    effort: int | None = None
    stat: PokeapiPokemonRecordStatStat | None = None


class PokeapiPokemonRecordStatStat(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    url: str | None = None


class PokeapiPokemonRecordType(BaseRecordModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: PokeapiPokemonRecordTypeType | None = None
    slot: int | None = None


class PokeapiPokemonRecordTypeType(BaseRecordModel):
    name: str | None = None
    url: str | None = None
