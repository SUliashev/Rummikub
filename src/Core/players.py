class Player:
    def __init__(self, name, tray_grid):
        self.name = name
        self.tray_grid = tray_grid
        self.first_turn_completed = False
        self.has_drawn_chip = False
        self.chips_placed_this_turn = []
        self.turn = 0
    
    def end_turn(self):
        self.has_drawn_chip = False
        self.chips_placed_this_turn = None
        self.chips_placed_this_turn = []
        self.turn += 1
