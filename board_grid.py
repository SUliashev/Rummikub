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
        start_x = Config.board_horizontal_edge + Config.slot_horizontal_spacing // 2
        for row in range(Config.board_rows):
            for col in range(Config.board_cols):
                x = start_x + (Config.chip_width + Config.slot_horizontal_spacing) * col
                y = Config.board_vertical_edge +  (Config.chip_height + Config.slot_vertical_spacing) * row
                self.slot_coordinates[(row, col)] = (x, y)
                self.slots[(row, col)] = None
                