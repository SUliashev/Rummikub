class ChipTracker:
    def __init__(self, board_grid, tray_grid, dragging_chip):
        self.chips_on_board_and_tray = []
        self.dragging_chip = dragging_chip
        self.board_grid = board_grid
        self.tray_grid = tray_grid
        self.origin_pos = None
        self.hidden_chips = [] 
        self.hovering_slot = None
     

    def return_chip_to_origin_pos(self):
        chip = self.dragging_chip.chip
        if self.origin_pos[0] == 'tray':
            self.chip_from_dragging_to_tray(self.origin_pos[1])
            
        elif self.origin_pos[0] == 'board':
            self.chip_from_dragging_to_board(self.origin_pos[1])
        self.origin_pos = None
        self.dragging_chip.chip == None


    def chip_from_tray_to_dragging(self, coordinates):
        chip = self.tray_grid.slots.get(coordinates)
        if chip:
            self.tray_grid.slots[coordinates] = None
            self.dragging_chip.chip = chip
            self.origin_pos = ('tray', coordinates)
            return chip
        

    def chip_from_board_to_dragging(self, coordinates):
        chip = self.board_grid.slots.get(coordinates)
        if chip:
            self.board_grid.slots[coordinates] = None
            self.dragging_chip.chip = chip
            self.origin_pos = ('board', coordinates)
            self.hovering_slot = None
            return chip
        

    def chip_from_dragging_to_board(self, coordinates: tuple ):# update later with validation
        chip = self.dragging_chip.chip
        if self.board_grid.slots[coordinates] is None:
            self.dragging_chip.chip = None
            self.origin_pos = None
            self.board_grid.slots[coordinates] = chip
            self.hovering_slot = None
        else:
            self.return_chip_to_origin_pos()


    def chip_from_dragging_to_tray(self, coordinates): #update later with chips moving to the side while hovering
        chip = self.dragging_chip.chip
        if self.tray_grid.slots[coordinates] is None:
            self.dragging_chip.chip = None
            self.origin_pos = None
            self.tray_grid.slots[coordinates] = chip
            self.hovering_slot = None
        else:
            self.return_chip_to_origin_pos()


    def place_chip_in_tray_from_hidden(self):
        if not self.hidden_chips:
            print("No hidden chips left!")
            return

        chip = self.hidden_chips.pop()
        self.tray_grid.put_chip_in_tray_from_hidden(chip)





