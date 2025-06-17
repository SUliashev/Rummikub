import pygame
from chip import Chip
from config import Config

class TrayGrid:
    def __init__(self):
        self.slot_coordinates = {}
        self.slots = {}
        self.create_coordinates()

    def create_coordinates(self):
        spacing = 1
        for row in range(Config.tray_rows):
            for col in range(Config.tray_cols):
                x = Config.tray_grid_x + col * (Config.chip_width + Config.slot_spacing)
                y = Config.tray_grid_y + row * (Config.chip_height + spacing) 
                self.slot_coordinates[(row, col)] = (x, y)
                self.slots[(row, col)] = None
                print(f'tray {x}, {y} created')

    # def create_tray_location(self):
    #     rows = 2
    #     cols = 13
    #     spacing = 8  # Same spacing as your tray grid, adjust if needed

    #     tray_width = cols * Chip.chip_width + (cols - 1) * spacing
    #     tray_height = rows * Chip.chip_height + (rows - 1) * spacing

    #     win_width, win_height = self.window.get_size()
    #     x = (win_width - tray_width) // 2
    #     margin_bottom = 30
    #     y = win_height - tray_height - margin_bottom
    #     self.x = x
    #     self.y = y


        

