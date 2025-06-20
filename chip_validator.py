class ChipValidator:
    def __init__(self, chip_tracker):    
        self.chip_tracker = chip_tracker
        self.slots = {}
      

    def validate_current_state(self):
  
        self.slots = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():

            if item_in_slot is not None:
                self.slots[(row, col)] = False
                continue

            valid = True
            # Check right neighbor
            chip_to_right = self.chip_tracker.board_grid.slots.get((row, col + 1))
            if chip_to_right:
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False
            # Check left neighbor
            chip_to_left = self.chip_tracker.board_grid.slots.get((row, col - 1))
            if chip_to_left:
                if not self.validate_combination(self.get_validation_chips(row, col)):
                    valid = False
            self.slots[(row, col)] = valid
 

    def validate_combination(self, chips):
        if len(chips) == 1:
            return True

        jokers = [chip for chip in chips if getattr(chip, 'is_joker', False)]
        non_jokers = [chip for chip in chips if not getattr(chip, 'is_joker', False)]

        if all(chip.color == non_jokers[0].color for chip in non_jokers):
            numbers = [chip.number for chip in chips if not getattr(chip, 'is_joker', False)]
            joker_count = len(jokers)
            # Validate consecutive numbers with jokers filling gaps
            prev = None
            for chip in chips:
                if getattr(chip, 'is_joker', False):
                    if prev is not None:
                        prev += 1  # Joker acts as the next needed number
                    continue
                if prev is not None:
                    gap = chip.number - prev - 1
                    if gap < 0:
                        return False  # Not strictly increasing
                    if gap > joker_count:
                        return False  # Not enough jokers to fill the gap
                    joker_count -= gap
                prev = chip.number
            return True

        # Check for a group (same number, different colors)
        if all(chip.number == non_jokers[0].number for chip in non_jokers):
            colors = {chip.color for chip in non_jokers}
            # No duplicate colors allowed, jokers can fill missing colors
            return len(colors) + len(jokers) == len(chips)

        return False
    def get_validation_chips(self, row, col):
        chips = []
        i = 1
        while self.chip_tracker.board_grid.slots.get((row, col - i)) is not None:
            chips.append(self.chip_tracker.board_grid.slots[(row, col - i)])
            i += 1
        chips = chips[::-1]
        chips.append(self.chip_tracker.dragging_chip.chip)
        i = 1
        while self.chip_tracker.board_grid.slots.get((row, col + i)) is not None:
            chips.append(self.chip_tracker.board_grid.slots[(row, col + i)])
            i += 1

        return chips

    

    

    
