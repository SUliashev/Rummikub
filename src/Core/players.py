class Player:
    def __init__(self, name, tray_grid):
        self.name = name
        self.tray_grid = tray_grid
        self.first_turn_completed = False
        self.has_drawn_chip = False
        self.chips_placed_this_turn = None
        self.turn = 0
    
    def reset_current_move(self):
        self.has_drawn_chip = False
        self.chips_placed_this_turn = None