class GameLogic:
    def __init__(self, chip_tracker):
        self.chip_tracker = chip_tracker  # Use ChipTracker for chip management

    def place_chip(self, chip, slot_id):
        """
        Place a chip in a slot and validate the move.
        """
        if slot_id in self.board_slots:
            raise ValueError("Slot is already occupied!")
        self.board_slots[slot_id] = chip

    def validate_combination(self, row, col):
        """
        Validate if the chips in the same row or group form a valid combination.
        """
        # Retrieve chips in the same row or group
        chips = self.get_chips_in_combination(row, col)

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

    def get_chips_in_combination(self, row, col) -> list:   # returns a list of chips that are in the same combination 
        chips = []
        i = 1
        while self.chip_tracker.get_chip(row, col - i) is not None:
            chips.append(self.chip_tracker.get_chip(row, col - i))
            i += 1
        chips.append(self.chip_tracker.get_chip(row, col))
        i = 1
        while self.chip_tracker.get_chip(row, col + i) is not None:
            chips.append(self.chip_tracker.get_chip(row, col + i))
            i += 1

        return chips

    def handle_invalid_move(self, chip):
        """
        Handle invalid moves by returning the chip to its original position.
        """
        # Implement logic to return the chip to the bottom row or its original position
        pass