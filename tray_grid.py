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
                x = Config.tray_grid_x + col * (Config.chip_width + Config.slot_horizontal_spacing)
                y = Config.tray_grid_y + row * (Config.chip_height + spacing) 
                self.slot_coordinates[(row, col)] = (x, y)
                self.slots[(row, col)] = None
          




        

