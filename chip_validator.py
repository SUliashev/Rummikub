class ChipValidator:
    def __init__(self, rows=5, cols=29):
        self.slots = {}  # Map (row, col) to chips for validation

        # Initialize empty slots
        for row in range(rows):
            for col in range(cols):
                self.slots[(row, col)] = None  # None means the slot is empty


    def validate_chip(self, chip, row, col):
        if self.slots[(row, col)] is not None:
            raise ValueError(f"Slot ({row}, {col}) is already occupied! (validation)")
        self.slots[(row, col)] = chip  # Mark the slot as valid
        
    def get_validation_chip(self, row, col):
        return self.slots.get((row, col))
    
    def validate_combination(self, row, col):
        """
        Validate if the chips in the same row or group form a valid combination.
        """
        # Retrieve chips in the same row or group
        chips = self.get_validation_chips(row, col)

        # Debug: Print the chips in the combination
        print(f"Combination for chip at ({row}, {col}): {[str(chip) for chip in chips]}")

        # Check if the combination is valid
        if len(chips) < 3:
            return False

        # Check for a run (same color, consecutive numbers)
        if all(chip.color == chips[0].color for chip in chips):
            numbers = sorted(chip.number for chip in chips)
            return all(numbers[i] + 1 == numbers[i + 1] for i in range(len(numbers) - 1))

        # Check for a group (same number, different colors)
        if all(chip.number == chips[0].number for chip in chips):
            colors = {chip.color for chip in chips}
            return len(colors) == len(chips)

        return False

    def get_validation_chips(self, row, col):
        chips = []
        i = 1
        while self.chip_tracker.get_validation_chip(row, col - i) is not None:
            chips.append(self.chip_tracker.get_validation_chip(row, col - i))
            i += 1
        chips.append(self.chip_tracker.get_validation_chip(row, col))
        i = 1
        while self.chip_tracker.get_validation_chip(row, col + i) is not None:
            chips.append(self.chip_tracker.get_validation_chip(row, col + i))
            i += 1

        return chips
    

    def handle_invalid_move(self, chip):
        """
        Handle invalid moves by returning the chip to its original position.
        """
        # Implement logic to return the chip to the bottom row or its original position
        pass