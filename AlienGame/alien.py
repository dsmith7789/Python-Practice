from __future__ import annotations

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Represents a single alien in the fleet."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        """Initialize the alien and sets its starting position

        Args:
            ai_game (AlienInvasion): The current alien invasion game.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self) -> bool:
        """Return True if alien is at edge of screen.
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self) -> None:
        """Move the alien left or right.
        """
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
