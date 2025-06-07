import pygame

class Tray:
    def __init__(self, window, width=1200, height=220, chip_capacity=26):
        self.window = window
        self.width = width
        self.height = height
        self.chip_capacity = chip_capacity
        self.chips = []
        self.bg_color = (40, 40, 40)  # Dark gray

        # Centered at the bottom
        win_width, win_height = window.get_size()
        self.x = (win_width - self.width) // 2
        self.y = win_height - self.height - 30  # 30px margin from bottom

    def get_height(self):
        return self.height
    
    def add_chip(self, chip):
        if len(self.chips) < self.chip_capacity:
            self.chips.append(chip)

    def draw(self):
        # Draw tray background
        pygame.draw.rect(self.window, self.bg_color, (self.x, self.y, self.width, self.height), border_radius=20)
        

