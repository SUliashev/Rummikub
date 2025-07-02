from src.Grids.tray_grid import TrayGrid
class Player:
    name: str
    tray_grid: TrayGrid
    first_turn_completed: bool
    has_drawn_chip: bool
    turn: int

    def __init__(self, name: str, tray_grid: TrayGrid):
        self.name = name
        self.tray_grid = tray_grid
        self.first_turn_completed = False
        self.has_drawn_chip = False
        self.turn = 0
    
    def end_turn(self) -> None:
        self.has_drawn_chip = False
        self.chips_placed_this_turn = None
        self.turn += 1
