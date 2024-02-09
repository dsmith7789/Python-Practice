from typing import Optional
from card import Card

class Hand:
    def __init__(self, cards: Optional[list[Card]]) -> None:
        self.cards = cards

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_value(self) -> int:
        value = 0
        for card in self.cards:
            value += card.value
        return value
        