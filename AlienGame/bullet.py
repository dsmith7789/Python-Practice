from __future__ import annotations

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship.
    """

    def __init__(self, ai_game: "AlienInvasion"):
        """Create a bullet object at the ship's current position.

        Args:
            ai_game (AlienInvasion): The current alien invasion game.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        # Not based on image so we need to make our own rect.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet up the screen.
        """
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen.
        """
        pygame.draw.rect(surface=self.screen, 
                         color=self.color, 
                         rect=self.rect)