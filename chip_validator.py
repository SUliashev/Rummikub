class ChipValidator:
    def __init__(self, chip_tracker):    
        self.chip_tracker = chip_tracker
        self.slots = {}
      


    # def validate_current_state(self):
    #     self.slots = {}
    #     for (row, col), item in self.chip_tracker.board_grid.slots.items():
    #         chip_to_right = self.chip_tracker.board_grid.slots.get((row, col + 1))
    #         chip_to_left = self.chip_tracker.board_grid.slots.get((row, col - 1))
    #         if chip_to_right:
    #             if not self.validate_combination(self.get_validation_chips(row, col)):
    #                 self.slots[(row, col)] = False
                    
    #         if chip_to_left:
    #             if not self.validate_combination(self.get_validation_chips(row, col)):
    #                 self.slots[(row, col)] = False
                    
    #         self.slots[(row, col)] = True
    #     # for value in self.slots.values():
    #     #     print(value)
    def validate_current_state(self):
  
        self.slots = {}

        for (row, col), item_in_slot in self.chip_tracker.board_grid.slots.items():
            # Only validate if there is a chip in this slot
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
        
        # Debug: Print the chips in the combination
        # print(f"Combination for chip at ({row}, {col}): {[str(chip) for chip in chips]}")
       
        # Check if the combination is valid
        if len(chips) > 1:
            # Check for a run (same color, consecutive numbers)
            if all(chip.color == chips[0].color for chip in chips):
                numbers = list(chip.number for chip in chips)
                return all(numbers[i] + 1 == numbers[i + 1] for i in range(len(numbers) - 1))

            # Check for a group (same number, different colors)
            if all(chip.number == chips[0].number for chip in chips):
                colors = {chip.color for chip in chips}
                return len(colors) == len(chips)

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

    

    

    
