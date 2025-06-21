class ChipValidator:
    def __init__(self, chip_tracker):    
        self.chip_tracker = chip_tracker
        self.slots = {}
        self.slots_on_board = {}
        self.slot_next_to_chip = {}
        self.validate_current_state()

    def validate_current_state(self):
        self.slots_on_board = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            if item_in_slot is None:
                self.slots_on_board[(row, col)] = True
            else:
                if len(self.get_validation_chips(row, col)) == 1 or len(self.get_validation_chips(row, col)) < 3:
                    self.slots_on_board[(row, col)] = False
                    continue
                self.slots_on_board[(row, col)] = self.validate_combination(self.get_validation_chips(row, col))


    def validate_dragging_chip(self):
        self.slots = {}
        self.slot_next_to_chip = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():

            if item_in_slot is not None:
                self.slots[(row, col)] = False
                continue

            self.slot_next_to_chip[(row, col)] = False
            valid = True

            chip_to_right = self.chip_tracker.board_grid.slots.get((row, col + 1))
            if chip_to_right:
                self.slot_next_to_chip[(row, col)] = True
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False

            chip_to_left = self.chip_tracker.board_grid.slots.get((row, col - 1))
            if chip_to_left:
                self.slot_next_to_chip[(row, col)] = True
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False

            self.slots[(row, col)] = valid
 

    def validate_combination(self, chips):
        jokers = [chip for chip in chips if getattr(chip, 'is_joker', False)]
        non_jokers = [chip for chip in chips if not getattr(chip, 'is_joker', False)]

        # Check for same color, increasing numbers
        if all(chip.color == non_jokers[0].color for chip in non_jokers):
            joker_count = len(jokers)

            prev = None
            for chip in chips:
                if getattr(chip, 'is_joker', False):
                    if prev is not None:
                        prev += 1  
                    continue
                if prev is not None:
                    gap = chip.number - prev - 1
                    if gap < 0:
                        return False  
                    if gap > joker_count:
                        return False  
                    joker_count -= gap
                prev = chip.number
            return True

        # Check for same number, different colors
        if all(chip.number == non_jokers[0].number for chip in non_jokers):
            colors = {chip.color for chip in non_jokers}
            return len(colors) + len(jokers) == len(chips)
     
        return False
        

    def get_validation_chips(self, row, col):
        chips = []
        
        i = 1
        while self.chip_tracker.board_grid.slots.get((row, col - i)) is not None:
            chips.append(self.chip_tracker.board_grid.slots[(row, col - i)])
            i += 1
        chips = chips[::-1]
        if self.chip_tracker.dragging_chip.chip:
            chips.append(self.chip_tracker.dragging_chip.chip)
        else:
            chips.append(self.chip_tracker.board_grid.slots[(row, col)])
        i = 1
        while self.chip_tracker.board_grid.slots.get((row, col + i)) is not None:
            chips.append(self.chip_tracker.board_grid.slots[(row, col + i)])
            i += 1

        return chips

    

    

    
