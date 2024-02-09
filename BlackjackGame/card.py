import pygame

class Card:
    def __init__(self, suit: str, face_value: str) -> None:
        self.suit = suit
        self.face_value = face_value 
        self.value = self.get_value(face_value)
        self.image = pygame.image.load(f"images/cards/{face_value}_of_{suit}.png")
    
    def get_value(self, face_value: str) -> int:
        if face_value in ["ace", "jack", "queen", "king"]:
            return 11
        else:
            return int(face_value)
