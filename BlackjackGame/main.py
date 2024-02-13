import sys
import pygame
from player import PlayerAction
from engine import BlackjackEngine
from definitions import Definitions
from card import Card
from hand import Hand

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
    
    def get_upper_left_coords(self, center: tuple[int, int], width: int, height: int) -> tuple[int, int]:
        """ Translates a center coordinate to its corresponding upper left coordinate.

        Given the center of a rectangular object (defined by its width and height), find the coordinate of its upper left corner.

        Args:
            center (tuple[int, int]): The center of the object (X, Y)
            width (int): How wide the object is.
            height (int): How tall the object is.

        Returns:
            tuple[int, int]: The coordinates of the upper left corner of the object (X, Y).
        """
        center_x, center_y = center
        return center_x - (width // 2), center_y - (height // 2)
        
    def render_game(self, window: pygame.surface.Surface) -> None:
        self.render_static_elements(window)  
        self.render_dynamic_elements(window)      

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

    def render_dynamic_elements(self, window: pygame.surface.Surface) -> None:
        # render dealer hand
        #print(f"Dealer Hand: {self.engine.dealer_player.hand}")
        self.render_hand(window, self.engine.dealer_player.hand, self.definitions.dealer_hand_placement)

        # render player hand
        #print(f"Player Hand: {self.engine.human_player.hand}")
        self.render_hand(window, self.engine.human_player.hand, self.definitions.player_hand_placement)


    def render_hand(self, window: pygame.surface.Surface, hand: Hand, dest: tuple[int, int]) -> None:
        card_width, card_height = self.definitions.card_size
        hand_width = (hand.get_size() * card_width) + (hand.get_size() * self.definitions.card_margin)
        hand_height = card_height + (2 * self.definitions.card_margin)
        position = self.get_upper_left_coords(dest, hand_width, hand_height)
        for i in range(hand.get_size()):
            card = hand.get_card(i)
            self.render_card(window, card, position)
            x, y = position
            x += card_width + self.definitions.card_margin
            position = (x, y)

    def render_dealer_hand(self, window: pygame.surface.Surface) -> None:
        """The dealer's hand goes in the top of the screen.

        Args:
            window (pygame.surface.Surface): The current pygame window.
        """
        pass
        
    def render_card(self, window: pygame.surface.Surface, card: Card, dest: tuple[int, int]) -> None:
        window.blit(card.fetch_image(), dest)
        pass

if __name__ == "__main__":
    game = Blackjack()
    game.run_game() 