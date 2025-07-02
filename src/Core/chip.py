import pygame

class Chip:
    sprite: pygame.Surface
    color: str
    number: int
    is_joker: bool
    copy: int
    
    def __init__(self, image: pygame.Surface, color: str = None, number: int = None, is_joker: bool = False, copy: int = None):
        self.sprite = image # Load the chip image
        self.color = color
        self.number = number 
        self.is_joker = is_joker
        self.copy = copy

    def __str__(self) -> str:
        return f"({self.color} {self.number})"
    
    def __repr__(self) -> str:
        return f"Chip({self.color} {self.number})"
    



