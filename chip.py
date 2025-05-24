import pygame

class Chip:
    def __init__(self, x: int, y: int, image_path: str, color: str = None, number: int = None):
        self.sprite = pygame.image.load(image_path)  # Load the chip image
        self.x = x
        self.y = y
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.color = None
        self.number = None 
        self.update_boundaries()

    def __str__(self):
        return f"{self.color} {self.number} at ({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Chip({self.x}, {self.y}, {self.sprite})"
    
    def update_boundaries(self):
        self.x_line = (self.x, self.x + self.width)
        self.y_line = (self.y, self.y + self.height)

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))