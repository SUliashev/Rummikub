class ChipValidator:
    def __init__(self ):    
        self.validation_chip = None
        self.validation_pos = None


    def validate_chip(self, chip, row, col):
        self.validation_chip = chip
        self.validation_pos = (row, col)
        
    
    def validate_combination(self, chip_tracker, chip, row, col):
        """
        Validate if the chips in the same row or group form a valid combination.
        """
        # Retrieve chips in the same row or group
        chips = self.get_validation_chips(chip_tracker, chip, row, col)

        if len(chips) == 1:
            return True
        
        # Debug: Print the chips in the combination
        print(f"Combination for chip at ({row}, {col}): {[str(chip) for chip in chips]}")
       
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
    
        

    def get_validation_chips(self, chip_tracker, chip, row, col):
        chips = []
        i = 1
        while chip_tracker.get_chip(row, col - i) is not None:
            chips.append(chip_tracker.get_chip(row, col - i))
            i += 1
        chips = chips[::-1]
        chips.append(chip)
        i = 1
        while chip_tracker.get_chip(row, col + i) is not None:
            chips.append(chip_tracker.get_chip(row, col + i))
            i += 1

        return chips
    

    def handle_invalid_move(self, chip):
        """
        Handle invalid moves by returning the chip to its original position.
        """
        # Implement logic to return the chip to the bottom row or its original position
        pass