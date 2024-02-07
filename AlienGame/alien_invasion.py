import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior
    """

    def __init__(self):
        """Initialize the game, and create game resources.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the "Play" and "Pause", and "Level Cleared!" buttons
        self.play_button = Button(ai_game=self, msg="Play", width=200, height=50, 
                                  button_color=(0, 255, 0),      # bright green
                                  text_color=(255, 255, 255),   # white
                                  font=pygame.font.SysFont(None, 48)
                                  )
        self.resume_button = Button(ai_game=self, msg="Resume", width=200, height=50, 
                                  button_color=(255, 0, 0),      # bright red
                                  text_color=(255, 255, 255),   # white
                                  font=pygame.font.SysFont(None, 48)
                                  )
        self.level_cleared_button = Button(ai_game=self, msg="Level Cleared!", width=300, height=50, 
                                  button_color=(0, 0, 255),      # bright blue
                                  text_color=(255, 255, 255),   # white
                                  font=pygame.font.SysFont(None, 48)
                                  )

        # Set the background color (light grey).
        self.bg_color = (230, 230, 230)
    
    def run_game(self) -> None:
        """Starts the main loop for the game.
        """
        while True:
            self._check_events()

            if self.stats.game_active and not self.stats.game_paused and not self.stats.level_break:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            # Update the UI
            self._update_screen()            
    
    def _check_events(self) -> None:
        """PRIVATE: Respond to keypresses and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_resume_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """PRIVATE: Start a new game when the player clicks the "Play" button.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse. Must be over the "Play" button to start the game.
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
    
    def _start_game(self) -> None:
        """Contains the logic to actually start the game.
        Callable fron both clicking the button and pressing the Enter key.
        """
        # Reset game settings.
        self.settings.initialize_dynamic_settings()

        # Reset game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_resume_button(self, mouse_pos: tuple[int, int]) -> None:
        """PRIVATE: Continue the game when the player clicks the "Resume" button.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse. Must be over the "Resume" button to resume the game.
        """
        button_clicked = self.resume_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_paused:
            self._resume_game()
    
    def _resume_game(self) -> None:
        """Contains logic to actually resume the game.
        Callable fron both clicking the button and pressing the Enter key.
        """
        # Reset game statistics.
        self.stats.game_paused = False
        self.stats.level_break = False

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Give the player a second to get set.
        sleep(1.0)

    def _check_level_cleared_button(self, mouse_pos: tuple[int, int]) -> None:
        button_clicked = self.level_cleared_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_paused:
            self._resume_game()
    
    def _update_screen(self) -> None:
        """PRIVATE: Update images on the screen, and flip to the new screen.
        """
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Draw the resume button if the game is paused.
        if self.stats.game_paused:
            self.resume_button.draw_button()

        # Draw the level cleared button once the player cleared a level.
        if self.stats.level_break:
            self.level_cleared_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
    
    def _fire_bullet(self) -> None:
        """PRIVATE: Create a new bullet and add it to the bullets group.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self) -> None:
        """Update position of bullets and get rid of old bullets.
        """
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self) -> None:
        """Respond to bullet-alien collisions.
        """
        # Remove bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()  # game gets tougher with each wave

            # Increase level.
            self.stats.level += 1
            self.stats.level_break = True
            self.sb.prep_level()

    def _create_fleet(self) -> None:
        """Create the fleet of aliens.
        """
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number: int, row_number: int) -> None:
        """Create an alien and place in a row.

        Args:
            alien_number (int): The index of the alien in this row.
            row_number (int): The row that the alien goes in.
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
        self.aliens.add(alien)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens 
        in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self) -> None:
        """Respond appropriately if any aliens have reached an edge.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self) -> None:
        """Drop the entire fleet and change the fleet's direction.
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self) -> None:
        """Respond to the ship being hit by an alien.
        """
        if self.stats.ships_left > 0:
            # Decrement ships remaining and updates scoreboard graphic.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self) -> None:
        """Check if any aliens have reached the bottom of the screen.
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """PRIVATE: Respond to key presses.

        Args:
            event (pygame.event.Event): the key release PyGame event
        """
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key in [pygame.K_ESCAPE, pygame.K_q]:
            sys.exit()
        elif event.key == pygame.K_p:
            self._pause_game()
        elif event.key in [pygame.K_KP_ENTER, pygame.K_RETURN]:
            if not self.stats.game_active:
                self._start_game()
            elif self.stats.game_paused or self.stats.level_break:
                self._resume_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """PRIVATE: Respond to key releases.

        Args:
            event (pygame.event.Event): the key release PyGame event
        """
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _pause_game(self) -> None:
        """PRIVATE: Handles pause game logic.
        """
        self.stats.game_paused = True

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
