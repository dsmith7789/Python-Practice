import pygame
from definitions import Definitions

class Button:
    def __init__(self, 
                 text: str, 
                 width: int, 
                 height: int, 
                 center: tuple[int, int],
                 button_color: tuple[int, int, int], 
                 text_color: tuple[int, int, int]) -> None:
        self.defs = Definitions()
        self.text = text
        self.width = width
        self.height = height
        self.button_color = button_color
        self.text_color = text_color

        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
        self.rect.center = center
        self.prep_text(text)
    
    def prep_text(self, text: str):
        self.text_image = self.defs.sm_font.render(text, True, self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self, window: pygame.surface.Surface):
        window.fill(self.button_color, self.rect)
        window.blit(self.text_image, self.text_image_rect)