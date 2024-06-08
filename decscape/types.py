import uuid
from enum import IntEnum, StrEnum
from datetime import datetime
from dataclasses import dataclass


class TournamentClass(IntEnum):
    PROFESSIONAL = 3  # big star
    MAJOR = 2  # 3 stars
    COMPETITIVE = 1  # 2 stars
    OPEN = 0  # 1 star


class Format(StrEnum):
    """
    Keys from mtgtop8 format keys
    """
    STANDARD = "ST"
    PIONEER = "PI"
    MODERN = "MO"
    LEGACY = "LE"


@dataclass()
class Deck:
    name: str = ""
    uri: str = ""
    player_name: str = ""
    player_uri: str = ""
    tournament_name: str = ""
    tournament_uri: str = ""
    date: datetime = datetime.now()
    tclass: TournamentClass = TournamentClass.OPEN
    id: str = uuid.uuid4().hex


@dataclass()
class Archetype:
    archetype_name: str = ""
    archetype_uri: str = ""
    meta_share: float = 0.0
    id: str = uuid.uuid4().hex


@dataclass()
class Metagame:
    format: Format
    deck_samples: int
    archetypes: list[Archetype]
    sample_date: datetime = datetime.now()
    id: str = uuid.uuid4().hex
