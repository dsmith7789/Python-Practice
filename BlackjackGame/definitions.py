import pygame

class Definitions:
    def __init__(self) -> None:
        # game play elements
        self.suits = ["spades", "clubs", "diamonds", "hearts"]
        self.face_values = ["ace", "2", "3", "4" , "5", "6", "7",
                            "8", "9", "10", "jack", "queen", "king"]
        self.max_score = 21

        # colors
        self.window_bg_color = (20, 75, 35)             # the color of felt at a cards table
        self.hit_button_color = (0, 0, 255)             # blue
        self.stay_button_color = (200, 150, 20)         # gold-yellow (sort of a neutral color)
        self.win_button_color = (0, 255, 20)            # green (for victory)
        self.lose_button_color = (255, 0, 0)            # red (for loss)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # sizes (width, height)
        self.window_size = (1300, 800) 
        self.card_size = (int(238*0.6), int(332*0.6))   # (142, 199)
        self.button_size = (325, 50)
        self.end_button_size = (500, 50)

        # fonts
        self.xl_font = pygame.font.SysFont('helvetica', 60)
        self.lg_font = pygame.font.SysFont('helvetica', 48)
        self.md_font = pygame.font.SysFont('helvetica', 36)
        self.sm_font = pygame.font.SysFont('helvetica', 24)
        self.xs_font = pygame.font.SysFont('helvetica', 12)

        # placements
        self.dealer_hand_label_placement = (self.window_size[0] // 2, 25)
        self.player_hand_label_placement = (self.window_size[0] // 2, self.window_size[1] - 25)

        self.dealer_hand_placement = (self.window_size[0] // 2, 200)
        self.player_hand_placement = (self.window_size[0] // 2, 650)

        self.hit_button_center = (self.window_size[0] - self.button_size[0] // 2 - 20, self.window_size[1] // 2 - 30)
        self.stay_button_center = (self.window_size[0] - self.button_size[0] // 2 - 20, self.window_size[1] // 2 + 30)

        self.dealer_wins_placement = (self.window_size[0] - self.button_size[0] // 2 - 20, 25)
        self.player_wins_placement = (self.window_size[0] - self.button_size[0] // 2 - 20, self.window_size[1] - 25)

        self.card_margin = 20

        self.deck_placement = (100, self.window_size[1] // 2 - self.card_size[1] // 2)