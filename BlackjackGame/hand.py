from typing import Optional
from card import Card

class Hand:
    def __init__(self, cards: Optional[list[Card]]=[]) -> None:
        self.cards = list(cards)    # otherwise the hands end up sharing a list of cards

    def __repr__(self) -> str:
        return ", ".join([repr(card) for card in self.cards])

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_card(self, i: int) -> Card:
        """Retrieves the card at index i.

        Args:
            i (int): the index of a card in the hand.

        Returns:
            Card: The card at the specified index.
        """
        return self.cards[i]

    def get_value(self) -> int:
        value = 0
        aces = 0
        for card in self.cards:
            if card.face_value != "ace":
                value += card.value
            else:
                aces += 1
        while aces:
            if value <= 10:
                value += 11
                aces -= 1
            else:
                value += 1
                aces -= 1
        return value

    def get_size(self) -> int:
        return len(self.cards)
        