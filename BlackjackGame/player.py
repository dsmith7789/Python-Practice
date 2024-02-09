from enum import Enum
from hand import Hand

class PlayerAction(Enum):
    HIT = 0
    STAY = 1

class Player:
    def __init__(self) -> None:
        self.hand = Hand()
