import sys
import pygame
import logging
import queue
import time
from player import PlayerAction
from engine import BlackjackEngine, GameState
from definitions import Definitions
from card import Card
from hand import Hand
from button import Button
from loggerThread import LoggerThread
from queueHandler import QueueHandler

class Blackjack:
    def __init__(self) -> None:
        pygame.init()
        self.session_id = int(time.time())
        self.start = time.time()
        self.logger = logging.getLogger('asyncLogger')
        self.logger.debug(f"Session: {self.session_id}; Event: Game Start")
        self.definitions = Definitions()
        self.size = self.definitions.window_size
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Blackjack")

        self.engine = BlackjackEngine()
        self.card_back = self.load_back_of_card()
        self.create_buttons()

    def create_buttons(self) -> None:
        self.hit_button = Button(text="Click to Hit (or press H key)", width=self.definitions.button_size[0], 
                                 height=self.definitions.button_size[1], center=self.definitions.hit_button_center,
                                 button_color=self.definitions.hit_button_color, text_color=self.definitions.white)
        self.stay_button = Button(text="Click to Stay (or press S key)", width=self.definitions.button_size[0], 
                                  height=self.definitions.button_size[1], center=self.definitions.stay_button_center,
                                  button_color=self.definitions.stay_button_color, text_color=self.definitions.white)
        self.win_button = Button(text="You won! Click to play again (or press Enter)", width=self.definitions.end_button_size[0],
                                 height=self.definitions.end_button_size[1], center=self.window.get_rect().center,
                                 button_color=self.definitions.win_button_color, text_color=self.definitions.white)
        self.lose_button = Button(text="You lost. Click to play again (or press Enter)", width=self.definitions.end_button_size[0],
                                  height=self.definitions.end_button_size[1], center=self.window.get_rect().center,
                                  button_color=self.definitions.lose_button_color, text_color=self.definitions.white)
    
    def load_back_of_card(self) -> pygame.surface.Surface:
        image = pygame.image.load('images/cards/card_back.png')
        image = pygame.transform.scale(image, self.definitions.card_size)
        return image
        
    def run_game(self) -> None:
        while True:
            action = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.info(f"Session: {self.session_id}; Event: Game End; Method: Click Exit")
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.logger.info(f"Session: {self.session_id}; Event: Key Press; Key: {pygame.key.name(event.key)}")
                    action = self.key_to_action(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.logger.info(f"Session: {self.session_id}; Event: Click; Click Position: {mouse_pos}")
                    action = self.click_to_action(mouse_pos)
            self.engine.play(action)
            self.render_game(self.window)
            pygame.display.flip()

    def key_to_action(self, event: pygame.event.Event) -> PlayerAction:
        if event.key in [pygame.K_ESCAPE, pygame.K_q]:
            self.logger.info(f"Session: {self.session_id}; Event: Game End; Method: Key Press {pygame.key.name(event.key)}")
            sys.exit()
        if event.key == pygame.K_h and self.engine.state == GameState.PLAYING:
            self.logger.info(f"Session: {self.session_id}; Event: Player Hit (Key Press); Hand Value: {self.engine.human_player.get_score()}")
            return PlayerAction.HIT
        elif event.key == pygame.K_s and self.engine.state == GameState.PLAYING:
            self.logger.info(f"Session: {self.session_id}; Event: Player Stay (Key Press); Hand Value: {self.engine.human_player.get_score()}")
            return PlayerAction.STAY
        elif event.key in [pygame.K_KP_ENTER, pygame.K_RETURN] and self.engine.state == GameState.ENDED:
            if self.engine.winner():
                self.logger.info(f"Session: {self.session_id}; Event: Player Victory; Player Score: {self.engine.human_player.get_score()}")
            else:
                self.logger.info(f"Session: {self.session_id}; Event: Player Defeat; Player Score: {self.engine.human_player.get_score()}")
            self.logger.info(f"Session: {self.session_id}; Event: Reset Game (Key Press): Duration: {time.time() - self.start}")
            self.start = time.time()
            return PlayerAction.RESET
        else:
            return None
        
    def click_to_action(self, mouse_pos: tuple[int, int]) -> PlayerAction:
        hb_clicked = self.hit_button.rect.collidepoint(mouse_pos)
        sb_clicked = self.stay_button.rect.collidepoint(mouse_pos)
        wb_clicked = self.win_button.rect.collidepoint(mouse_pos)
        lb_clicked = self.lose_button.rect.collidepoint(mouse_pos)

        if hb_clicked and self.engine.state == GameState.PLAYING:
            self.logger.info(f"Session: {self.session_id}; Event: Player Hit (Button Click); Hand Value: {self.engine.human_player.get_score()}")
            return PlayerAction.HIT
        elif sb_clicked and self.engine.state == GameState.PLAYING:
            self.logger.info(f"Session: {self.session_id}; Event: Player Stay (Button Click); Hand Value: {self.engine.human_player.get_score()}")
            return PlayerAction.STAY
        elif (wb_clicked or lb_clicked) and self.engine.state == GameState.ENDED:
            if self.engine.winner():
                self.logger.info(f"Session: {self.session_id}; Event: Player Victory; Player Score: {self.engine.human_player.get_score()}")
            else:
                self.logger.info(f"Session: {self.session_id}; Event: Player Defeat; Player Score: {self.engine.human_player.get_score()}")
            self.logger.info(f"Session: {self.session_id}; Event: Reset Game (Button Click); Duration: {time.time() - self.start}")
            self.start = time.time()
            return PlayerAction.RESET
        else:
            return None
        
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
        window.blit(self.card_back, self.definitions.deck_placement)

        self.hit_button.draw_button(window)
        self.stay_button.draw_button(window)

    def render_dynamic_elements(self, window: pygame.surface.Surface) -> None:
        # The dealer's hand and player's hand are labeled
        dealer_text = f"Dealer: Score = {self.engine.dealer_player.get_score()}" if not self.engine.human_turn else f"Dealer: Score = ???"
        dealer_text += ("" if not self.engine.dealer_player.busted() else " [BUSTED]")
        text = self.definitions.md_font.render(dealer_text, True, (255,255,255))
        coords = self.center_surface_on_point(text, self.definitions.dealer_hand_label_placement)
        window.blit(text, coords)

        player_text = f"Player: Score = {self.engine.human_player.get_score()}"
        player_text += ("" if not self.engine.human_player.busted() else " [BUSTED]")
        text = self.definitions.md_font.render(player_text, True, (255,255,255))
        coords = self.center_surface_on_point(text, self.definitions.player_hand_label_placement)
        window.blit(text, coords)

        dealer_wins = f"Dealer victories: {self.engine.dealer_wins}"
        text = self.definitions.sm_font.render(dealer_wins, True, (255,255,255))
        coords = self.center_surface_on_point(text, self.definitions.dealer_wins_placement)
        window.blit(text, coords)

        player_wins = f"Your victories: {self.engine.player_wins}"
        text = self.definitions.sm_font.render(player_wins, True, (255,255,255))
        coords = self.center_surface_on_point(text, self.definitions.player_wins_placement)
        window.blit(text, coords)

        # render dealer hand
        #print(f"Dealer Hand: {self.engine.dealer_player.hand}")
        dealer_hand = self.get_dealer_hand()
        self.render_hand(window, dealer_hand, self.definitions.dealer_hand_placement)

        # render player hand
        #print(f"Player Hand: {self.engine.human_player.hand}")
        self.render_hand(window, self.engine.human_player.hand, self.definitions.player_hand_placement)

        if self.engine.state == GameState.ENDED:
            if self.engine.winner():
                self.win_button.draw_button(window)
            else:
                self.lose_button.draw_button(window)


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

    def get_dealer_hand(self) -> Hand:
        """The dealer's hand goes in the top of the screen.

        Args:
            window (pygame.surface.Surface): The current pygame window.
        """
        if self.engine.human_turn:
            hidden_hand = Hand()
            dummy_card = Card("", "", True)
            hidden_hand.add_card(dummy_card)
            dealer_cards = self.engine.dealer_player.hand.cards
            for i in range(1, len(dealer_cards)):
                hidden_hand.add_card(dealer_cards[i])
            return hidden_hand
        else:
            return self.engine.dealer_player.hand
        
    def render_card(self, window: pygame.surface.Surface, card: Card, dest: tuple[int, int]) -> None:
        window.blit(card.fetch_image(), dest)

def setup_logging() -> logging.Logger:
    logger = logging.getLogger('asyncLogger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    return logger, formatter

if __name__ == "__main__":
    log_queue = queue.Queue()
    logger, formatter = setup_logging()

    # Setup and start the logger thread
    logger_thread = LoggerThread(log_queue, formatter)
    logger_thread.start()

    # Replace the logger's default handler with the queue-based handler
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    game = Blackjack()
    game.run_game() 