from __future__ import annotations

import pygame.font

class Button:
    """A class to manage buttons (Pygame doesn't have a built-in button method).
    """
    
    def __init__(self, ai_game: "AlienInvasion", msg: str) -> None:
        """Initialize button attributes.
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)     # bright green
        self.text_color = (255, 255, 255)   # white
        self.font = pygame.font.SysFont(None, 48)

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