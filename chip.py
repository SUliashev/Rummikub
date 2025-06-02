import pygame

class Chip:
    def __init__(self, x: int, y: int, image_path: str, color: str = None, number: int = None):
        self.sprite = pygame.image.load(image_path)  # Load the chip image
        self.x = x
        self.y = y
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.row = None
        self.col = None
        self.color = color
        self.number = number 
        self.update_boundaries()

    def __str__(self):
        return f"({self.color} {self.number})"
    
    def __repr__(self):
        return f"({self.color} {self.number})"
    
    def update_boundaries(self):
        self.x_line = (self.x, self.x + self.width)
        self.y_line = (self.y, self.y + self.height)

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

    def put_chip_in_slot(self, row, col):
        """
        Place the chip in a specific slot.
        """
        self.row = row
        self.col = col
    
    def remove_chip_from_slot(self):
        """
        Remove the chip from its current slot.
        """
        self.row = None
        self.col = None