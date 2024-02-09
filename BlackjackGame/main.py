import sys
import pygame
from player import PlayerAction
from engine import BlackjackEngine

class Blackjack:
    def __init__(self) -> None:
        pygame.init()
        self.size = (1200, 800) # width, height
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Blackjack")

        self.engine = BlackjackEngine()

    def run_game(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    action = self.key_to_action(event)
                    self.engine.play(action)
            pygame.display.flip()

    def key_to_action(self, event: pygame.event.Event) -> PlayerAction:
        if event.key == pygame.K_h:
            return PlayerAction.HIT
        elif event.key == pygame.K_s:
            return PlayerAction.STAY

if __name__ == "__main__":
    game = Blackjack()
    game.run_game() 