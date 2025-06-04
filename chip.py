import pygame

class Chip:
    tray = 'Chip currently in tray'
    board = 'Chip currently on the board'
    hidden = 'Chip currently hidden'
    def __init__(self, x: int, y: int, image_path: str, color: str = None, number: int = None):
        self.sprite = pygame.image.load(image_path)  # Load the chip image
        self.x = x
        self.y = y
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.row = None
        self.col = None
        self.tray_row = None
        self.tray_col = None
        self.color = color
        self.number = number 
        self.state = Chip.hidden
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
        self.state = Chip.board
    
    def remove_chip_from_slot(self):
        """
        Remove the chip from its current slot.
        """
        self.row = None
        self.col = None


    def put_chip_in_tray(self, row, col):
        self.tray_row = row
        self.tray_col = col
        self.state = Chip.tray
    
    def remove_chip_from_tray(self):
        self.tray_row = None
        self.tray_col = None