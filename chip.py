import pygame

class Chip:
    def __init__(self, x: int, y: int, image: pygame.Surface, color: str = None, number: int = None):
        self.sprite = image # Load the chip image
        self.color = color
        self.number = number 
       
    def __str__(self):
        return f"({self.color} {self.number})"
    
    def __repr__(self):
        return f"Chip({self.color} {self.number})"
    



