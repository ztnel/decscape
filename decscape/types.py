from enum import IntEnum
from datetime import datetime
from dataclasses import dataclass

class TournamentClass(IntEnum):
    PROFESSIONAL = 3 # big star
    MAJOR = 2 # 3 stars
    COMPETITIVE = 1 # 2 stars
    OPEN = 0 # 1 star

@dataclass()
class Entry:
    deck_name:str = ""
    deck_uri:str = ""
    player_uri:str = ""
    tournament_uri:str = ""
    date: datetime = datetime.now()
    tclass:TournamentClass = TournamentClass.OPEN
