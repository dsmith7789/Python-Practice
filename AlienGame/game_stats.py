from __future__ import annotations
import json

class GameStats:
    """Track statistics for Alien Invasion.
    """

    def __init__(self, ai_game: "AlienInvasion") -> None:
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state.
        self.game_active = False
        self.game_paused = False
        self.level_break = False

        # Handle high scores
        self.load_high_scores()
        self.high_score = max(self.high_score_list.values()) if self.high_score_list else 0

    def reset_stats(self) -> None:
        """Initialize statistics that can change during the game.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_scores(self) -> None:
        """Read in the top 10 high scores from file.
        """
        try:
            with open("high_scores.json") as f:
                self.high_score_list = json.load(f)
        except json.decoder.JSONDecodeError:
            self.high_score_list = {}
