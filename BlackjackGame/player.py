from enum import Enum
from hand import Hand
from definitions import Definitions

class PlayerAction(Enum):
    HIT = 0
    STAY = 1
    RESET = 2

class Player:
    def __init__(self) -> None:
        self.defs = Definitions()
        self.hand = Hand()
    
    def get_score(self) -> int:
        return self.hand.get_value()
    
    def busted(self) -> bool:
        return self.get_score() > self.defs.max_score
