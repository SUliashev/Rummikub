import pygame

class Chip:
    def __init__(self, image: pygame.Surface, color: str = None, number: int = None, is_joker: bool = False):
        self.sprite = image # Load the chip image
        self.color = color
        self.number = number 
        self.is_joker = is_joker

    def __str__(self):
        return f"({self.color} {self.number})"
    
    def __repr__(self):
        return f"Chip({self.color} {self.number})"
    



