from chip import Chip
from config import Config

class BoardGrid:
    def __init__(self, rows: int=5, cols: int=29):
        self.slot_coordinates = {}
        self.slots = {}
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(Config.board_cols)] for _ in range(Config.board_rows)]
        self.hovering_slot = None 
        self.create_coordinates()

    def create_coordinates(self):
        spacing = 1
        for row in range(5):
            for col in range(Config.board_cols):
                x = 3 + col * (Config.chip_width + Config.slot_spacing)
                y = row * (Config.chip_height + spacing) * 1.9
                self.slot_coordinates[(row, col)] = (x, y)
                self.slots[(row, col)] = None
                