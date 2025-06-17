import pygame

class Chip:
    chip_width = None
    chip_height = None


    def __init__(self, x: int, y: int, image: pygame.Surface, color: str = None, number: int = None):
        self.sprite = image # Load the chip image
        self.color = color
        self.number = number 
        if Chip.chip_height is None or Chip.chip_width is None:
            Chip.set_chip_size(Chip, image.get_width(), image.get_height())
  

    def __str__(self):
        return f"({self.color} {self.number})"
    
    def __repr__(self):
        return f"({self.color} {self.number})"
    
    def set_chip_size(cls, width: int, height: int):
        cls.chip_width = width
        cls.chip_height = height
    
    def update_boundaries(self):
        self.x_line = (self.x, self.x + Chip.chip_width)
        self.y_line = (self.y, self.y + Chip.chip_height)

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

    def put_chip_in_slot(self):
        
        self.state = Chip.board
        self.update_boundaries()


    def put_chip_in_tray(self):
        self.state = Chip.tray
        self.update_boundaries()

