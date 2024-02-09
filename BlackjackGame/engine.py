from deck import Deck
from hand import Hand
from card import Card
from enum import Enum
from definitions import Definitions

from player import Player, PlayerAction

class GameState(Enum):
    PLAYING = 0
    ENDED = 1

class BlackjackEngine:
    def __init__(self) -> None:
        self.deck = Deck()
        self.deck.shuffle_cards()
        self.human_turn = True
        self.human_player, self.dealer_player = Player(), Player()
        self.definitions = Definitions()
        self.state = GameState.PLAYING
        self.result = None

    def hit(self, player: Player):
        card = self.deck.deal()
        player.hand.add_card(card)

    def stay(self):
        self.human_turn = False

    def is_hand_valid(self, player: Player) -> bool:
        if player.hand.get_value() > self.definitions.max_score:
            return False
        else:
            return True
    
    def dealer_process(self):
        # Per https://bicyclecards.com/how-to-play/blackjack/
        # Dealer must hit if they have a hand with value 16 or less
        while self.dealer_player.hand.get_value() < 17:
            self.hit(self.dealer_player)
    
    def winner(self) -> bool:
        if not self.is_hand_valid(self.human_player):
            # we don't have a valid hand so we always lose in this scenario
            return False
        elif not self.is_hand_valid(self.dealer_player):
            # we have a valid hand and the dealer doesn't, so they lose
            return True
        else:
            # we both have valid hands, so we need to outright beat the dealer in order to win
            return self.human_player.hand.get_value() > self.dealer_player.hand.get_value()
    
    def play(self, action: PlayerAction):
        if self.state == GameState.PLAYING:
            if self.human_turn:
                if action == PlayerAction.HIT:
                    self.hit(self.human_player)
                elif action == PlayerAction.STAY:
                    self.stay()
            else:
                self.dealer_process()
        elif self.state == GameState.ENDED:
            self.result = self.winner()