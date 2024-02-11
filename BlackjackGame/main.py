import sys
import pygame
from player import PlayerAction
from engine import BlackjackEngine
from definitions import Definitions
from card import Card

class Blackjack:
    def __init__(self) -> None:
        pygame.init()
        self.definitions = Definitions()
        self.size = self.definitions.window_size
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Blackjack")

        self.engine = BlackjackEngine()
        self.card_back = self.load_back_of_card()
    
    def load_back_of_card(self) -> pygame.surface.Surface:
        image = pygame.image.load('images/cards/card_back.png')
        image = pygame.transform.scale(image, self.definitions.card_size)
        return image
        
    def run_game(self) -> None:
        while True:
            action = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    action = self.key_to_action(event)
            self.engine.play(action)
            self.render_game(self.window)
            pygame.display.flip()

    def key_to_action(self, event: pygame.event.Event) -> PlayerAction:
        if event.key in [pygame.K_ESCAPE, pygame.K_q]:
            sys.exit()
        if event.key == pygame.K_h:
            return PlayerAction.HIT
        elif event.key == pygame.K_s:
            return PlayerAction.STAY
        
    def center_surface_on_point(self, surface: pygame.surface.Surface, dest: tuple[int, int]) -> tuple[int, int]:
        """Calculates the correct spot to place a surface given an intended destination.
        
        Pygame uses the upper left corner of a surface as a surface's coordinates.
        This method takes the size of the surface and the intended center of that surface
        to find where we should actually place the object if we want it's center in the 
        specified destination.

        Args:
            surface (pygame.surface.Surface): The surface we are trying to center on a point.
            dest (tuple[int, int]): The point we want to be the center of the surface. 

        Returns:
            tuple[int, int]: Where the upper left corner of the surface should go to get the intended center.
        """
        dest_x, dest_y = dest
        return (dest_x - surface.get_rect().centerx, dest_y - surface.get_rect().centery)
        
    def render_game(self, window: pygame.surface.Surface) -> None:
        self.render_static_elements(window)        

    def render_static_elements(self, window: pygame.surface.Surface) -> None:
        window.fill(self.definitions.window_bg_color)

        # The "deck" (just a single card back) shows off to the side
        window.blit(self.card_back, (100, 300))

        # The dealer's hand and player's hand are labeled
        text = self.definitions.md_font.render("Dealer", True, (255,255,255))
        coords = self.center_surface_on_point(text, self.definitions.dealer_hand_label_placement)
        window.blit(text, coords)

        text = self.definitions.md_font.render("Player", True, (255,255,255))
        coords = self.center_surface_on_point(text, self.definitions.player_hand_label_placement)
        window.blit(text, coords)

    def render_player_hands(self, window: pygame.surface.Surface) -> None:
        pass

    def render_dealer_hand(self, window: pygame.surface.Surface) -> None:
        """The dealer's hand goes in the top of the screen.

        Args:
            window (pygame.surface.Surface): The current pygame window.
        """
        

if __name__ == "__main__":
    game = Blackjack()
    game.run_game() 