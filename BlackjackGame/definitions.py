import pygame

class Definitions:
    def __init__(self) -> None:
        # game play elements
        self.suits = ["spades", "clubs", "diamonds", "hearts"]
        self.face_values = ["ace", "2", "3", "4" , "5", "6", "7",
                            "8", "9", "10", "jack", "queen", "king"]
        self.max_score = 21

        # colors
        self.window_bg_color = (20, 75, 35)     # the color of felt at a cards table

        # sizes (width, height)
        self.window_size = (1200, 800) 
        self.card_size = (int(238*0.6), int(332*0.6))

        # fonts
        self.xl_font = pygame.font.SysFont('helvetica', 60)
        self.lg_font = pygame.font.SysFont('helvetica', 48)
        self.md_font = pygame.font.SysFont('helvetica', 36)
        self.sm_font = pygame.font.SysFont('helvetica', 24)
        self.xs_font = pygame.font.SysFont('helvetica', 12)

        # placements
        self.dealer_hand_label_placement = (self.window_size[0] // 2, 25)
        self.player_hand_label_placement = (self.window_size[0] // 2, self.window_size[1] - 25)

        self.dealer_hand_placement = (self.window_size[0] // 2, 150)
        self.player_hand_placement = (self.window_size[0] // 2, 650)