import pygame

class Chip:
    def __init__(self, x, y, image_path):
        self.sprite = pygame.image.load(image_path)  # Load the chip image
        self.x = x
        self.y = y
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.update_boundaries()

    def update_boundaries(self):
        self.x_line = (self.x, self.x + self.width)
        self.y_line = (self.y, self.y + self.height)

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))