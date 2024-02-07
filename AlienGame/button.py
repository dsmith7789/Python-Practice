from __future__ import annotations
from typing import Optional

import pygame.font

class Button:
    """A class to manage buttons (Pygame doesn't have a built-in button method).
    """
    
    def __init__(self, ai_game: "AlienInvasion", 
                 msg: str, 
                 width: int,
                 height: int,
                 button_color: tuple[int, int, int], 
                 text_color: tuple[int, int, int],
                 font: pygame.font.SysFont
                 ) -> None:
        """Initialize button attributes

        Args:
            ai_game (AlienInvasion): the current Alien Invasion game.
            msg (str): The text we want to display on the button.
            width (int): How wide the button should be.
            height (int): How tall the button should be.
            button_color (Optional[tuple[int, int, int]], optional): Background color of the button. Defaults to (0, 255, 0).
            text_color (Optional[tuple[int, int, int]], optional): Text color of the button. Defaults to (255, 255, 255).
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = width, height
        self.button_color = button_color     # bright green
        self.text_color = text_color   # white
        self.font = font

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message only needs to be prepped once.
        self._prep_msg(msg)
    
    def _prep_msg(self, msg: str) -> None:
        """Turns a message into a rendered image and centered text on the button.

        Args:
            msg (str): The message to put on the button.
        """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        """Draw blank button and then draw message.
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)