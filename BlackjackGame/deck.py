from card import Card
from definitions import Definitions
import random

class Deck:
    def __init__(self) -> None:
        self.cards = self._generate_cards()
        self.definitions = Definitions()
    
    def _generate_cards(self) -> list[Card]:
        cards = []
        for suit in self.definitions.suits:
            for face_value in self.definitions.face_values:
                cards.append(Card(suit, face_value))
        return cards
    
    def shuffle_cards(self) -> None:
        """Uses Fisher-Yates random shuffle of array.
        """
        for i in range(len(self.cards)):
            swap_idx = random.randrange(i, len(self.cards))
            self.cards[i], self.cards[swap_idx] = self.array[swap_idx], self.array[i]
    
    def deal(self) -> Card:
        return self.cards.pop()